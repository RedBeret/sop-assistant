import type { AskResponse } from "../types";
import { CheckIcon } from "./Icons";

interface AnswerPanelProps {
  response: AskResponse;
  onCitationSelect: (citation: number) => void;
}

function AnswerLine({ line, onCitationSelect }: { line: string; onCitationSelect: (id: number) => void }) {
  const pieces = line.split(/(\[\d+\])/g);
  return (
    <li>
      {pieces.map((piece, index) => {
        const match = piece.match(/^\[(\d+)\]$/);
        return match ? (
          <button
            className="inline-citation"
            key={`${piece}-${index}`}
            onClick={() => onCitationSelect(Number(match[1]))}
            aria-label={`View source ${match[1]}`}
          >
            {piece}
          </button>
        ) : (
          <span key={`${piece}-${index}`}>
            {piece.replace(/^(?:[-•]|\d+\.)\s*/, "")}
          </span>
        );
      })}
    </li>
  );
}

export function AnswerPanel({ response, onCitationSelect }: AnswerPanelProps) {
  const lines = response.answer.split("\n").filter(Boolean);
  return (
    <section className="answer-section" aria-live="polite">
      <div className="section-heading-row">
        <div className="section-heading-wrap">
          <span className="accent-rule" />
          <h2>Answer</h2>
          <span className="section-qualifier">{response.grounded ? "grounded" : "insufficient evidence"}</span>
        </div>
        {response.grounded ? (
          <span className="grounded-status">
            <CheckIcon /> Grounded in {response.sources.length} sources
          </span>
        ) : null}
      </div>
      {response.grounded ? (
        <ol className="answer-list">
          {lines.map((line, index) => (
            <AnswerLine key={`${line}-${index}`} line={line} onCitationSelect={onCitationSelect} />
          ))}
        </ol>
      ) : (
        <p className="no-evidence">{response.answer}</p>
      )}
      <p className="synthetic-note">
        Sources are synthetic Navy-flavored SOPs. Always follow required approvals and local policy.
      </p>
    </section>
  );
}
