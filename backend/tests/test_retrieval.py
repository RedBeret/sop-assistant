from pathlib import Path

from app.chunking import load_corpus
from app.embeddings import LocalHashEmbeddings
from app.store import SQLiteVectorStore


def build_store(tmp_path: Path) -> SQLiteVectorStore:
    root = Path(__file__).resolve().parents[2]
    store = SQLiteVectorStore(tmp_path / "test.db", LocalHashEmbeddings())
    store.rebuild(load_corpus(root / "data" / "sops"))
    return store


def test_hybrid_retrieval_finds_expected_router_sop(tmp_path: Path) -> None:
    store = build_store(tmp_path)
    try:
        hits = store.search("rollback failed edge router firmware upgrade", top_k=3)
        assert hits[0].chunk.doc_id == "NET-SOP-104"
        assert any("checksum" in hit.chunk.content.lower() for hit in hits)
    finally:
        store.close()


def test_hybrid_retrieval_finds_credential_response(tmp_path: Path) -> None:
    store = build_store(tmp_path)
    try:
        hits = store.search("immediate actions exposed API key", top_k=3)
        assert hits[0].chunk.doc_id == "SEC-SOP-402"
    finally:
        store.close()
