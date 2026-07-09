from __future__ import annotations

import json
import sqlite3
from collections import defaultdict
from pathlib import Path

import sqlite_vec

from .embeddings import TOKEN_RE, EmbeddingProvider
from .models import Chunk, DocumentSummary, SearchHit

STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "before",
    "do",
    "for",
    "from",
    "how",
    "i",
    "if",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "should",
    "the",
    "to",
    "we",
    "what",
    "when",
    "where",
    "which",
    "with",
}


class SQLiteVectorStore:
    def __init__(self, path: Path, provider: EmbeddingProvider):
        self.path = path
        self.provider = provider
        path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(path, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self.connection.enable_load_extension(True)
        sqlite_vec.load(self.connection)
        self.connection.enable_load_extension(False)
        self._create_schema()

    def close(self) -> None:
        self.connection.close()

    def _create_schema(self) -> None:
        self.connection.executescript(
            f"""
            CREATE TABLE IF NOT EXISTS metadata (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS chunks (
                id INTEGER PRIMARY KEY,
                chunk_key TEXT NOT NULL UNIQUE,
                doc_id TEXT NOT NULL,
                title TEXT NOT NULL,
                section TEXT NOT NULL,
                heading TEXT NOT NULL,
                content TEXT NOT NULL,
                ordinal INTEGER NOT NULL
            );
            CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5(
                title, heading, content, content='chunks', content_rowid='id'
            );
            CREATE VIRTUAL TABLE IF NOT EXISTS vec_chunks USING vec0(
                embedding float[{self.provider.dimensions}] distance_metric=cosine
            );
            """
        )
        self.connection.commit()

    def _metadata(self, key: str) -> str | None:
        row = self.connection.execute("SELECT value FROM metadata WHERE key = ?", (key,)).fetchone()
        return str(row["value"]) if row else None

    def needs_rebuild(self, chunks: list[Chunk]) -> bool:
        corpus_signature = "|".join(chunk.chunk_key for chunk in chunks)
        return (
            self._metadata("provider") != self.provider.name
            or self._metadata("dimensions") != str(self.provider.dimensions)
            or self._metadata("corpus_signature") != corpus_signature
            or self.chunk_count() != len(chunks)
        )

    def rebuild(self, chunks: list[Chunk], batch_size: int = 64) -> None:
        vectors: list[list[float]] = []
        texts = [f"{chunk.title}\n{chunk.heading}\n{chunk.content}" for chunk in chunks]
        for start in range(0, len(texts), batch_size):
            vectors.extend(self.provider.embed(texts[start : start + batch_size]))

        with self.connection:
            self.connection.execute("DELETE FROM chunks_fts")
            self.connection.execute("DELETE FROM vec_chunks")
            self.connection.execute("DELETE FROM chunks")
            for chunk, vector in zip(chunks, vectors, strict=True):
                cursor = self.connection.execute(
                    """
                    INSERT INTO chunks(chunk_key, doc_id, title, section, heading, content, ordinal)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        chunk.chunk_key,
                        chunk.doc_id,
                        chunk.title,
                        chunk.section,
                        chunk.heading,
                        chunk.content,
                        chunk.ordinal,
                    ),
                )
                rowid = int(cursor.lastrowid)
                self.connection.execute(
                    "INSERT INTO chunks_fts(rowid, title, heading, content) VALUES (?, ?, ?, ?)",
                    (rowid, chunk.title, chunk.heading, chunk.content),
                )
                self.connection.execute(
                    "INSERT INTO vec_chunks(rowid, embedding) VALUES (?, ?)",
                    (rowid, json.dumps(vector)),
                )
            metadata = {
                "provider": self.provider.name,
                "dimensions": str(self.provider.dimensions),
                "corpus_signature": "|".join(chunk.chunk_key for chunk in chunks),
            }
            self.connection.executemany(
                "INSERT OR REPLACE INTO metadata(key, value) VALUES (?, ?)", metadata.items()
            )

    def chunk_count(self) -> int:
        return int(self.connection.execute("SELECT COUNT(*) FROM chunks").fetchone()[0])

    def document_count(self) -> int:
        return int(
            self.connection.execute("SELECT COUNT(DISTINCT doc_id) FROM chunks").fetchone()[0]
        )

    def documents(self) -> list[DocumentSummary]:
        rows = self.connection.execute(
            """
            SELECT doc_id, title, COUNT(*) AS chunk_count
            FROM chunks GROUP BY doc_id, title ORDER BY doc_id
            """
        ).fetchall()
        return [DocumentSummary(**dict(row)) for row in rows]

    @staticmethod
    def _query_terms(question: str) -> list[str]:
        return [
            token
            for token in TOKEN_RE.findall(question.lower())
            if token not in STOPWORDS and len(token) > 1
        ]

    @staticmethod
    def _chunk_from_row(row: sqlite3.Row) -> Chunk:
        return Chunk(
            chunk_key=row["chunk_key"],
            doc_id=row["doc_id"],
            title=row["title"],
            section=row["section"],
            heading=row["heading"],
            content=row["content"],
            ordinal=row["ordinal"],
        )

    def search(self, question: str, top_k: int = 5) -> list[SearchHit]:
        if not question.strip() or not self.chunk_count():
            return []
        query_vector = self.provider.embed([question])[0]
        candidate_k = min(max(top_k * 4, 12), self.chunk_count())
        vector_rows = self.connection.execute(
            """
            SELECT c.*, v.distance
            FROM vec_chunks v JOIN chunks c ON c.id = v.rowid
            WHERE v.embedding MATCH ? AND k = ?
            ORDER BY v.distance
            """,
            (json.dumps(query_vector), candidate_k),
        ).fetchall()

        terms = self._query_terms(question)
        lexical_rows: list[sqlite3.Row] = []
        if terms:
            fts_query = " OR ".join(f'"{term.replace(chr(34), "")}"' for term in terms)
            lexical_rows = self.connection.execute(
                """
                SELECT c.*, bm25(chunks_fts, 4.0, 3.0, 1.0) AS fts_score
                FROM chunks_fts JOIN chunks c ON c.id = chunks_fts.rowid
                WHERE chunks_fts MATCH ? ORDER BY fts_score LIMIT ?
                """,
                (fts_query, candidate_k),
            ).fetchall()

        fused: dict[int, float] = defaultdict(float)
        distances: dict[int, float] = {}
        rows_by_id: dict[int, sqlite3.Row] = {}
        for rank, row in enumerate(vector_rows, start=1):
            rowid = int(row["id"])
            rows_by_id[rowid] = row
            distances[rowid] = float(row["distance"])
            fused[rowid] += 1.0 / (60 + rank)
        for rank, row in enumerate(lexical_rows, start=1):
            rowid = int(row["id"])
            rows_by_id[rowid] = row
            fused[rowid] += 1.25 / (60 + rank)

        query_set = set(terms)
        results: list[SearchHit] = []
        for rowid, score in sorted(fused.items(), key=lambda item: item[1], reverse=True):
            row = rows_by_id[rowid]
            searchable = set(
                TOKEN_RE.findall(f"{row['title']} {row['heading']} {row['content']}".lower())
            )
            overlap = len(query_set & searchable) / max(1, len(query_set))
            results.append(
                SearchHit(
                    chunk=self._chunk_from_row(row),
                    distance=distances.get(rowid, 1.0),
                    score=score,
                    lexical_overlap=overlap,
                )
            )
        return results[:top_k]
