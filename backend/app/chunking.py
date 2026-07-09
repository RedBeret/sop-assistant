from __future__ import annotations

import hashlib
import re
from pathlib import Path

from .models import Chunk

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
DOC_ID_RE = re.compile(r"\b([A-Z]{3}-SOP-\d{3})\b")
SECTION_RE = re.compile(r"^(\d+(?:\.\d+)*)\.?\s*(.*)$")


def _split_long_section(text: str, max_chars: int, overlap_chars: int) -> list[str]:
    paragraphs: list[str] = []
    for paragraph in (value.strip() for value in text.split("\n\n") if value.strip()):
        if len(paragraph) <= max_chars:
            paragraphs.append(paragraph)
            continue
        remaining = paragraph
        while len(remaining) > max_chars:
            cut = remaining.rfind(" ", 0, max_chars + 1)
            cut = cut if cut > max_chars // 2 else max_chars
            paragraphs.append(remaining[:cut].strip())
            next_start = max(0, cut - overlap_chars)
            remaining = remaining[next_start:].strip()
        if remaining:
            paragraphs.append(remaining)
    if not paragraphs:
        return []

    parts: list[str] = []
    current = ""
    for paragraph in paragraphs:
        candidate = f"{current}\n\n{paragraph}".strip()
        if current and len(candidate) > max_chars:
            parts.append(current)
            tail = current[-overlap_chars:].lstrip() if overlap_chars else ""
            current = f"{tail}\n\n{paragraph}".strip()
        else:
            current = candidate
    if current:
        parts.append(current)
    return parts


def chunk_document(path: Path, max_chars: int = 1500, overlap_chars: int = 180) -> list[Chunk]:
    raw = path.read_text(encoding="utf-8").strip()
    headings = list(HEADING_RE.finditer(raw))
    if not headings:
        raise ValueError(f"No Markdown headings found in {path}")

    title_line = headings[0].group(2)
    doc_match = DOC_ID_RE.search(title_line)
    if not doc_match:
        raise ValueError(f"No SOP document id found in {path}")
    doc_id = doc_match.group(1)
    title = title_line.split("—", 1)[-1].strip()

    chunks: list[Chunk] = []
    ordinal = 0
    for index, match in enumerate(headings[1:], start=1):
        start = match.end()
        end = headings[index + 1].start() if index + 1 < len(headings) else len(raw)
        heading = match.group(2).strip()
        body = raw[start:end].strip()
        if not body:
            continue
        section_match = SECTION_RE.match(heading)
        section = section_match.group(1) if section_match else str(index)
        clean_heading = section_match.group(2).strip() if section_match else heading
        for part_index, part in enumerate(_split_long_section(body, max_chars, overlap_chars)):
            ordinal += 1
            digest = hashlib.sha1(f"{doc_id}:{section}:{part_index}:{part}".encode()).hexdigest()[
                :12
            ]
            chunks.append(
                Chunk(
                    chunk_key=f"{doc_id}:{section}:{digest}",
                    doc_id=doc_id,
                    title=title,
                    section=section,
                    heading=clean_heading,
                    content=part,
                    ordinal=ordinal,
                )
            )
    return chunks


def load_corpus(directory: Path) -> list[Chunk]:
    paths = sorted(directory.glob("*.md"))
    if not paths:
        raise FileNotFoundError(f"No SOP Markdown files found in {directory}")
    return [chunk for path in paths for chunk in chunk_document(path)]
