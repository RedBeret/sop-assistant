from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

from .config import Settings
from .models import AskRequest, AskResponse, DocumentSummary, HealthResponse
from .runtime import Runtime


def create_app(settings: Settings | None = None) -> FastAPI:
    active_settings = settings or Settings.from_env()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        app.state.runtime = Runtime.build(active_settings)
        yield
        app.state.runtime.close()

    app = FastAPI(
        title="Watchline SOP Assistant",
        version="1.0.0",
        description="Citation-first RAG over synthetic technical SOPs.",
        lifespan=lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
        allow_credentials=False,
        allow_methods=["GET", "POST"],
        allow_headers=["*"],
    )

    def runtime(request: Request) -> Runtime:
        return request.app.state.runtime

    @app.get("/api/health", response_model=HealthResponse)
    def health(request: Request) -> HealthResponse:
        active = runtime(request)
        return HealthResponse(
            status="ok",
            document_count=active.store.document_count(),
            chunk_count=active.store.chunk_count(),
            embedding_provider=active.embeddings.name,
            generation_provider=active.answers.provider_name,
        )

    @app.get("/api/documents", response_model=list[DocumentSummary])
    def documents(request: Request) -> list[DocumentSummary]:
        return runtime(request).store.documents()

    @app.post("/api/ask", response_model=AskResponse)
    def ask(payload: AskRequest, request: Request) -> AskResponse:
        question = payload.question.strip()
        if len(question) < 3:
            raise HTTPException(status_code=422, detail="Question is too short")
        return runtime(request).answers.ask(question)

    @app.post("/api/reindex", response_model=HealthResponse)
    def reindex(request: Request) -> HealthResponse:
        current = runtime(request)
        replacement = Runtime.build(active_settings, force_rebuild=True)
        request.app.state.runtime = replacement
        current.close()
        return HealthResponse(
            status="ok",
            document_count=replacement.store.document_count(),
            chunk_count=replacement.store.chunk_count(),
            embedding_provider=replacement.embeddings.name,
            generation_provider=replacement.answers.provider_name,
        )

    return app


app = create_app()
