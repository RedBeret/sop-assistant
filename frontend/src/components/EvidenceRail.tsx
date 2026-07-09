import { useState } from "react";
import type { Source } from "../types";
import { CopyIcon } from "./Icons";

interface EvidenceRailProps {
  sources: Source[];
  selectedCitation: number | null;
  onSelect: (citation: number) => void;
}

export function EvidenceRail({ sources, selectedCitation, onSelect }: EvidenceRailProps) {
  const [copied, setCopied] = useState(false);
  const selected = sources.find((source) => source.citation === selectedCitation) ?? sources[0];

  async function copyExcerpt() {
    if (!selected) return;
    await navigator.clipboard.writeText(selected.excerpt);
    setCopied(true);
    window.setTimeout(() => setCopied(false), 1200);
  }

  return (
    <aside className="evidence-rail" aria-label="Answer evidence">
      <div className="evidence-intro">
        <div className="rail-title-row">
          <h2>Evidence</h2>
          <span />
        </div>
        <p>Select a source to inspect the excerpt supporting the answer.</p>
      </div>
      {sources.length ? (
        <>
          <div className="source-list">
            {sources.map((source) => (
              <button
                className={`source-row ${selected?.citation === source.citation ? "is-selected" : ""}`}
                key={`${source.doc_id}-${source.section}-${source.citation}`}
                onClick={() => onSelect(source.citation)}
              >
                <span className="citation-number">{source.citation}</span>
                <span className="source-summary">
                  <strong>{source.title}</strong>
                  <span className="source-meta">
                    {source.doc_id} <i /> Section {source.section}
                  </span>
                  <span className="source-relevance">Relevance: {source.relevance}%</span>
                </span>
                <span className="source-chevron" aria-hidden="true">›</span>
              </button>
            ))}
          </div>
          {selected ? (
            <article className="source-excerpt">
              <div className="excerpt-toolbar">
                <span>Excerpt from</span>
                <code>{selected.doc_id}</code>
                <span>· Section {selected.section}</span>
                <button onClick={copyExcerpt} aria-label="Copy source excerpt" title="Copy excerpt">
                  {copied ? "Copied" : <CopyIcon />}
                </button>
              </div>
              <h3>{selected.heading}</h3>
              <p>{selected.excerpt}</p>
            </article>
          ) : null}
        </>
      ) : (
        <div className="empty-evidence">
          No source met the evidence threshold. Refine the question with a system or failure mode.
        </div>
      )}
    </aside>
  );
}
