from __future__ import annotations

import argparse
import json
import os
import re
from datetime import UTC, datetime
from pathlib import Path

from app.config import PROJECT_ROOT, Settings
from app.runtime import Runtime


def run_evaluation(cases_path: Path, report_path: Path) -> dict:
    os.environ.setdefault("WATCHLINE_EMBEDDINGS", "local")
    os.environ.setdefault("WATCHLINE_GENERATION", "local")
    cases = json.loads(cases_path.read_text(encoding="utf-8"))
    runtime = Runtime.build(Settings.from_env())
    results = []
    try:
        for case in cases:
            response = runtime.answers.ask(case["question"])
            source_ids = [source.doc_id for source in response.sources]
            expected_source = case.get("expected_source")
            should_answer = case.get("should_answer", True)
            if should_answer:
                source_hit = expected_source in source_ids
                expected_keywords = case.get("expected_keywords", [])
                normalized_answer = re.sub(r"\s+", " ", response.answer.lower())
                matched = [word for word in expected_keywords if word.lower() in normalized_answer]
                keyword_recall = len(matched) / max(1, len(expected_keywords))
                passed = source_hit and keyword_recall >= 0.5 and response.grounded
            else:
                source_hit = not source_ids
                matched = []
                keyword_recall = 1.0 if not response.grounded else 0.0
                passed = source_hit and not response.grounded
            results.append(
                {
                    "id": case["id"],
                    "question": case["question"],
                    "passed": passed,
                    "source_hit": source_hit,
                    "keyword_recall": round(keyword_recall, 3),
                    "matched_keywords": matched,
                    "returned_sources": source_ids,
                    "grounded": response.grounded,
                }
            )
    finally:
        runtime.close()

    total = len(results)
    passed_count = sum(item["passed"] for item in results)
    source_hits = sum(item["source_hit"] for item in results)
    avg_recall = sum(item["keyword_recall"] for item in results) / total
    report = {
        "generated_at": datetime.now(UTC).isoformat(),
        "embedding_provider": "local-hash-v1",
        "generation_provider": "local-extractive",
        "case_count": total,
        "passed": passed_count,
        "pass_rate": round(passed_count / total, 3),
        "source_hit_rate": round(source_hits / total, 3),
        "average_keyword_recall": round(avg_recall, 3),
        "results": results,
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Watchline's reproducible RAG evaluation")
    parser.add_argument(
        "--cases", type=Path, default=PROJECT_ROOT / "backend" / "evals" / "questions.json"
    )
    parser.add_argument(
        "--report", type=Path, default=PROJECT_ROOT / "backend" / "evals" / "latest-report.json"
    )
    arguments = parser.parse_args()
    report = run_evaluation(arguments.cases, arguments.report)
    print(
        f"{report['passed']}/{report['case_count']} passed "
        f"({report['pass_rate']:.0%}); source hit {report['source_hit_rate']:.0%}; "
        f"keyword recall {report['average_keyword_recall']:.0%}"
    )
    failures = [item["id"] for item in report["results"] if not item["passed"]]
    if failures:
        print("Failed cases: " + ", ".join(failures))
    return 0 if report["pass_rate"] >= 0.85 else 1


if __name__ == "__main__":
    raise SystemExit(main())
