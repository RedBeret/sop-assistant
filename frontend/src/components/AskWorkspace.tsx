import { useRef } from "react";
import type { FormEvent, KeyboardEvent } from "react";
import type { AskResponse } from "../types";
import { AnswerPanel } from "./AnswerPanel";
import { EvidenceRail } from "./EvidenceRail";
import { SearchIcon } from "./Icons";

interface AskWorkspaceProps {
  question: string;
  onQuestionChange: (value: string) => void;
  onSubmit: () => void;
  response: AskResponse;
  selectedCitation: number | null;
  onCitationSelect: (citation: number) => void;
  loading: boolean;
  error: string | null;
}

export function AskWorkspace(props: AskWorkspaceProps) {
  const formRef = useRef<HTMLFormElement>(null);

  function submit(event: FormEvent) {
    event.preventDefault();
    props.onSubmit();
  }

  function onKeyDown(event: KeyboardEvent<HTMLTextAreaElement>) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      formRef.current?.requestSubmit();
    }
  }

  return (
    <main className="ask-layout">
      <div className="ask-main">
        <section className="query-section">
          <h1>Ask the watch</h1>
          <p className="page-subtitle">Ground every answer in the procedure.</p>
          <form ref={formRef} onSubmit={submit}>
            <label className="sr-only" htmlFor="question">Operational question</label>
            <textarea
              id="question"
              value={props.question}
              onChange={(event) => props.onQuestionChange(event.target.value)}
              onKeyDown={onKeyDown}
              maxLength={1000}
              rows={4}
            />
            <div className="query-actions">
              <div>
                <p>Ask a precise operational question. Answers are grounded in indexed SOPs.</p>
                <span className="char-count">{props.question.length} / 1000</span>
              </div>
              <button className="submit-button" disabled={props.loading || props.question.trim().length < 3}>
                <SearchIcon />
                {props.loading ? "Searching…" : "Find answer"}
              </button>
            </div>
            {props.error ? <p className="request-error" role="alert">{props.error}</p> : null}
          </form>
        </section>
        <AnswerPanel response={props.response} onCitationSelect={props.onCitationSelect} />
      </div>
      <EvidenceRail
        sources={props.response.sources}
        selectedCitation={props.selectedCitation}
        onSelect={props.onCitationSelect}
      />
    </main>
  );
}
