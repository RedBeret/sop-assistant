from __future__ import annotations

from dataclasses import dataclass

from pydantic import BaseModel, Field


@dataclass(frozen=True)
class Chunk:
    chunk_key: str
    doc_id: str
    title: str
    section: str
    heading: str
    content: str
    ordinal: int


@dataclass(frozen=True)
class SearchHit:
    chunk: Chunk
    distance: float
    score: float
    lexical_overlap: float


class AskRequest(BaseModel):
    question: str = Field(min_length=3, max_length=1000)


class Source(BaseModel):
    citation: int
    doc_id: str
    title: str
    section: str
    heading: str
    excerpt: str
    relevance: int = Field(ge=0, le=100)


class AskResponse(BaseModel):
    question: str
    answer: str
    grounded: bool
    provider: str
    sources: list[Source]


class DocumentSummary(BaseModel):
    doc_id: str
    title: str
    chunk_count: int


class HealthResponse(BaseModel):
    status: str
    document_count: int
    chunk_count: int
    embedding_provider: str
    generation_provider: str
