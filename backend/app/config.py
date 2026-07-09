from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Settings:
    project_root: Path = PROJECT_ROOT
    sop_dir: Path = PROJECT_ROOT / "data" / "sops"
    database_path: Path = PROJECT_ROOT / "data" / "watchline.db"
    embedding_mode: str = "auto"
    generation_mode: str = "auto"
    embedding_model: str = "text-embedding-3-small"
    generation_model: str = "gpt-5.4-mini"
    embedding_dimensions: int = 384
    top_k: int = 5

    @classmethod
    def from_env(cls) -> Settings:
        root = Path(os.getenv("WATCHLINE_PROJECT_ROOT", PROJECT_ROOT)).resolve()
        return cls(
            project_root=root,
            sop_dir=Path(os.getenv("WATCHLINE_SOP_DIR", root / "data" / "sops")).resolve(),
            database_path=Path(
                os.getenv("WATCHLINE_DATABASE_PATH", root / "data" / "watchline.db")
            ).resolve(),
            embedding_mode=os.getenv("WATCHLINE_EMBEDDINGS", "auto").lower(),
            generation_mode=os.getenv("WATCHLINE_GENERATION", "auto").lower(),
            embedding_model=os.getenv("WATCHLINE_EMBEDDING_MODEL", "text-embedding-3-small"),
            generation_model=os.getenv("WATCHLINE_GENERATION_MODEL", "gpt-5.4-mini"),
            embedding_dimensions=int(os.getenv("WATCHLINE_EMBEDDING_DIMENSIONS", "384")),
            top_k=int(os.getenv("WATCHLINE_TOP_K", "5")),
        )

    @property
    def has_openai_key(self) -> bool:
        return bool(os.getenv("OPENAI_API_KEY"))
