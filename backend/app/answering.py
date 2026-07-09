from __future__ import annotations

import os
import re

from .config import Settings
from .embeddings import TOKEN_RE
from .models import AskResponse, SearchHit, Source
from .store import STOPWORDS, SQLiteVectorStore

SENTENCE_RE = re.compile(r"(?<=[.!?])\s+|\n(?=\d+\.)")
CITATION_RE = re.compile(r"\[(\d+)]")
ACTION_WORDS = {
    "confirm",
    "disable",
    "escalate",
    "isolate",
    "notify",
    "record",
    "restore",
    "revoke",
    "test",
    "validate",
    "verify",
}


def _intent_headings(question: str) -> set[str]:
    lowered = question.lower()
    intents: set[str] = set()
    if any(term in lowered for term in ("validate", "validation", "tested", "prove")):
        intents.add("validation")
    if any(term in lowered for term in ("recover", "restore", "steps", "procedure")):
        intents.update({"recovery", "procedure", "restoration"})
    if any(term in lowered for term in ("rollback", "roll back")):
        intents.update({"rollback", "procedure", "trigger"})
    if any(term in lowered for term in ("revert", "reversion")):
        intents.update({"reversion", "procedure"})
    if "failover" in lowered:
        intents.update({"failover", "procedure"})
    if "immediate" in lowered:
        intents.add("immediate")
    if "emergency" in lowered:
        intents.add("emergency")
    if any(term in lowered for term in ("when", "trigger", "criteria")):
        intents.update({"trigger", "criteria"})
    return intents


class AnswerService:
    def __init__(self, store: SQLiteVectorStore, settings: Settings):
        self.store = store
        self.settings = settings
        mode = settings.generation_mode
        if mode not in {"auto", "local", "openai"}:
            raise ValueError("WATCHLINE_GENERATION must be auto, local, or openai")
        if mode == "openai" and not os.getenv("OPENAI_API_KEY"):
            raise RuntimeError("WATCHLINE_GENERATION=openai requires OPENAI_API_KEY")
        self.use_openai = mode == "openai" or (mode == "auto" and settings.has_openai_key)

    @property
    def provider_name(self) -> str:
        return f"openai:{self.settings.generation_model}" if self.use_openai else "local-extractive"

    @staticmethod
    def _sources(hits: list[SearchHit]) -> list[Source]:
        sources: list[Source] = []
        for index, hit in enumerate(hits, start=1):
            similarity = max(0.0, min(1.0, 1.0 - hit.distance))
            relevance = round(100 * max(similarity, hit.lexical_overlap * 0.92))
            excerpt = hit.chunk.content.strip()
            if len(excerpt) > 720:
                excerpt = excerpt[:717].rsplit(" ", 1)[0] + "…"
            sources.append(
                Source(
                    citation=index,
                    doc_id=hit.chunk.doc_id,
                    title=hit.chunk.title,
                    section=hit.chunk.section,
                    heading=hit.chunk.heading,
                    excerpt=excerpt,
                    relevance=relevance,
                )
            )
        return sources

    @staticmethod
    def _enough_evidence(hits: list[SearchHit]) -> bool:
        if not hits:
            return False
        return hits[0].lexical_overlap >= 0.16 or hits[0].distance <= 0.48

    def _extractive_answer(self, question: str, hits: list[SearchHit]) -> str:
        query_terms = {
            token
            for token in TOKEN_RE.findall(question.lower())
            if token not in STOPWORDS and len(token) > 1
        }
        intents = _intent_headings(question)
        candidates: list[tuple[float, int, str]] = []
        for citation, hit in enumerate(hits[:5], start=1):
            heading_tokens = set(TOKEN_RE.findall(hit.chunk.heading.lower()))
            heading_bonus = 2.5 if intents & heading_tokens else 0.0
            for position, sentence in enumerate(SENTENCE_RE.split(hit.chunk.content)):
                sentence = sentence.strip(" \n-*#")
                if len(sentence) < 25:
                    continue
                sentence_tokens = set(TOKEN_RE.findall(sentence.lower()))
                overlap = len(query_terms & sentence_tokens)
                action_bonus = 0.4 if sentence_tokens & ACTION_WORDS else 0.0
                list_bonus = 0.25 if re.match(r"^\d+\.", sentence) else 0.0
                score = (
                    overlap
                    + action_bonus
                    + list_bonus
                    + heading_bonus
                    - (position * 0.015)
                    - (citation * 0.02)
                )
                candidates.append((score, citation, sentence))

        chosen: list[tuple[int, str]] = []
        seen: set[str] = set()
        for _, citation, sentence in sorted(candidates, reverse=True):
            normalized = re.sub(r"\W+", " ", sentence.lower()).strip()
            if normalized in seen:
                continue
            seen.add(normalized)
            chosen.append((citation, sentence))
            if len(chosen) == 7:
                break
        chosen.sort(key=lambda item: (item[0], hit_order(item[1])))
        if not chosen:
            return "The indexed procedures do not contain enough evidence to answer that question."
        return "\n".join(f"- {sentence} [{citation}]" for citation, sentence in chosen)

    def _openai_answer(self, question: str, sources: list[Source]) -> str:
        from openai import OpenAI

        context = "\n\n".join(
            f"[{source.citation}] {source.doc_id} — {source.title}, section {source.section} "
            f"({source.heading})\n{source.excerpt}"
            for source in sources
        )
        client = OpenAI()
        response = client.responses.create(
            model=self.settings.generation_model,
            instructions=(
                "You answer operational questions using only the supplied SOP excerpts. "
                "Give concise, actionable steps. Cite every factual sentence with one or more "
                "source numbers like [1]. Never invent commands, approvals, timing, or policy. "
                "If the excerpts are insufficient, say so plainly."
            ),
            input=f"Question:\n{question}\n\nSOP excerpts:\n{context}",
            max_output_tokens=600,
        )
        answer = response.output_text.strip()
        cited = {int(match) for match in CITATION_RE.findall(answer)}
        if not answer or not cited or any(value > len(sources) for value in cited):
            raise ValueError("Model response did not contain valid grounded citations")
        return answer

    def ask(self, question: str) -> AskResponse:
        hits = self.store.search(question, self.settings.top_k)
        if not self._enough_evidence(hits):
            return AskResponse(
                question=question,
                answer=(
                    "I could not find enough evidence in the indexed SOPs to answer that. "
                    "Try naming the affected system, failure, or procedure."
                ),
                grounded=False,
                provider=self.provider_name,
                sources=[],
            )
        sources = self._sources(hits)
        provider = self.provider_name
        if self.use_openai:
            try:
                answer = self._openai_answer(question, sources)
            except Exception:
                answer = self._extractive_answer(question, hits)
                provider = f"{self.provider_name}->local-extractive-fallback"
        else:
            answer = self._extractive_answer(question, hits)
        return AskResponse(
            question=question,
            answer=answer,
            grounded=bool(sources and CITATION_RE.search(answer)),
            provider=provider,
            sources=sources,
        )


def hit_order(sentence: str) -> int:
    match = re.match(r"^(\d+)\.", sentence)
    return int(match.group(1)) if match else 999
