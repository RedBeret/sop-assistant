export function EvaluationView() {
  return (
    <main className="secondary-view evaluation-view">
      <div className="secondary-heading">
        <h1>Evaluation</h1>
        <p>A reproducible offline baseline—because a RAG demo without evals is just a confident anecdote.</p>
      </div>
      <div className="score-band">
        <div>
          <strong>20 / 20</strong>
          <span>cases passed</span>
        </div>
        <div>
          <strong>100%</strong>
          <span>source hit rate</span>
        </div>
        <div>
          <strong>93%</strong>
          <span>keyword recall</span>
        </div>
      </div>
      <div className="evaluation-notes">
        <section>
          <h2>What the suite checks</h2>
          <p>Each case names an expected SOP, answer keywords, and whether the system should answer at all. A pass requires the right source, at least half the expected details, and valid citations.</p>
        </section>
        <section>
          <h2>Why the baseline is local</h2>
          <p>The checked-in score uses deterministic hash embeddings and extractive generation, so CI does not need an API key. OpenAI embeddings and generation are available as the production path.</p>
        </section>
        <section>
          <h2>Failure is visible</h2>
          <p>The evaluator exits non-zero below an 85% pass rate and writes per-case source hits and keyword recall to a JSON report.</p>
        </section>
      </div>
    </main>
  );
}
