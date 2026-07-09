from __future__ import annotations

import hashlib
import math
import os
import re
from collections.abc import Sequence
from typing import Protocol

from .config import Settings

TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9-]+")


class EmbeddingProvider(Protocol):
    name: str
    dimensions: int

    def embed(self, texts: Sequence[str]) -> list[list[float]]: ...


class LocalHashEmbeddings:
    """Deterministic, dependency-free embeddings for local development and CI.

    Production mode uses OpenAI embeddings when a key is available. This local
    provider makes the full retrieval/eval loop reproducible without network calls.
    """

    name = "local-hash-v1"

    def __init__(self, dimensions: int = 384):
        self.dimensions = dimensions

    def _embed_one(self, text: str) -> list[float]:
        tokens = TOKEN_RE.findall(text.lower())
        features = tokens + [f"{a}_{b}" for a, b in zip(tokens, tokens[1:], strict=False)]
        vector = [0.0] * self.dimensions
        for feature in features:
            digest = hashlib.blake2b(feature.encode("utf-8"), digest_size=8).digest()
            value = int.from_bytes(digest, "little")
            index = value % self.dimensions
            sign = 1.0 if value & 1 else -1.0
            vector[index] += sign
        norm = math.sqrt(sum(value * value for value in vector)) or 1.0
        return [value / norm for value in vector]

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        return [self._embed_one(text) for text in texts]


class OpenAIEmbeddings:
    name = "openai"

    def __init__(self, model: str, dimensions: int):
        from openai import OpenAI

        self.client = OpenAI()
        self.model = model
        self.dimensions = dimensions
        self.name = f"openai:{model}:{dimensions}"

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        response = self.client.embeddings.create(
            model=self.model,
            input=list(texts),
            dimensions=self.dimensions,
            encoding_format="float",
        )
        return [item.embedding for item in sorted(response.data, key=lambda item: item.index)]


def create_embedding_provider(settings: Settings) -> EmbeddingProvider:
    mode = settings.embedding_mode
    if mode not in {"auto", "local", "openai"}:
        raise ValueError("WATCHLINE_EMBEDDINGS must be auto, local, or openai")
    if mode == "openai" and not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("WATCHLINE_EMBEDDINGS=openai requires OPENAI_API_KEY")
    if mode == "openai" or (mode == "auto" and settings.has_openai_key):
        return OpenAIEmbeddings(settings.embedding_model, settings.embedding_dimensions)
    return LocalHashEmbeddings(settings.embedding_dimensions)
