from pathlib import Path

from app.chunking import chunk_document, load_corpus
from app.config import PROJECT_ROOT


def test_corpus_has_twelve_synthetic_sops() -> None:
    chunks = load_corpus(PROJECT_ROOT / "data" / "sops")
    assert len({chunk.doc_id for chunk in chunks}) == 12
    assert all(chunk.section and chunk.heading and chunk.content for chunk in chunks)


def test_chunking_preserves_section_identity(tmp_path: Path) -> None:
    document = tmp_path / "test.md"
    document.write_text(
        "# NET-SOP-999 — Test Procedure\n\n## 1. Purpose\n\nA short purpose.\n\n"
        "## 2. Steps\n\n" + "Verify the system state. " * 120,
        encoding="utf-8",
    )
    chunks = chunk_document(document, max_chars=320, overlap_chars=40)
    assert chunks[0].doc_id == "NET-SOP-999"
    assert chunks[0].section == "1"
    assert len([chunk for chunk in chunks if chunk.section == "2"]) > 1
