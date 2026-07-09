from __future__ import annotations

from dataclasses import dataclass

from .answering import AnswerService
from .chunking import load_corpus
from .config import Settings
from .embeddings import EmbeddingProvider, create_embedding_provider
from .store import SQLiteVectorStore


@dataclass
class Runtime:
    settings: Settings
    embeddings: EmbeddingProvider
    store: SQLiteVectorStore
    answers: AnswerService

    @classmethod
    def build(cls, settings: Settings | None = None, force_rebuild: bool = False) -> Runtime:
        settings = settings or Settings.from_env()
        provider = create_embedding_provider(settings)
        store = SQLiteVectorStore(settings.database_path, provider)
        chunks = load_corpus(settings.sop_dir)
        if force_rebuild or store.needs_rebuild(chunks):
            store.rebuild(chunks)
        return cls(settings, provider, store, AnswerService(store, settings))

    def close(self) -> None:
        self.store.close()
