from pathlib import Path

from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app


def test_api_returns_grounded_answer_and_citations(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parents[2]
    settings = Settings(
        project_root=root,
        sop_dir=root / "data" / "sops",
        database_path=tmp_path / "api.db",
        embedding_mode="local",
        generation_mode="local",
    )
    with TestClient(create_app(settings)) as client:
        health = client.get("/api/health")
        assert health.status_code == 200
        assert health.json()["document_count"] == 12

        response = client.post(
            "/api/ask",
            json={
                "question": (
                    "What is the rollback procedure for a failed edge router firmware upgrade?"
                )
            },
        )
        assert response.status_code == 200
        payload = response.json()
        assert payload["grounded"] is True
        assert payload["sources"][0]["doc_id"] == "NET-SOP-104"
        assert "[1]" in payload["answer"]


def test_api_refuses_question_without_evidence(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parents[2]
    settings = Settings(
        project_root=root,
        sop_dir=root / "data" / "sops",
        database_path=tmp_path / "unknown.db",
        embedding_mode="local",
        generation_mode="local",
    )
    with TestClient(create_app(settings)) as client:
        response = client.post(
            "/api/ask", json={"question": "What is today's cafeteria lunch menu?"}
        )
        assert response.status_code == 200
        assert response.json()["grounded"] is False
        assert response.json()["sources"] == []
