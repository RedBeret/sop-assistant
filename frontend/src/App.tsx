import { useEffect, useState } from "react";
import { AskWorkspace } from "./components/AskWorkspace";
import { EvaluationView } from "./components/EvaluationView";
import { Header } from "./components/Header";
import { LibraryView } from "./components/LibraryView";
import { StatusBar } from "./components/StatusBar";
import { getDocuments, getHealth, askQuestion } from "./lib/api";
import { DEFAULT_QUESTION, DEFAULT_RESPONSE } from "./lib/demo";
import type { AskResponse, DocumentSummary, HealthResponse, ViewName } from "./types";

export default function App() {
  const [view, setView] = useState<ViewName>("ask");
  const [question, setQuestion] = useState(DEFAULT_QUESTION);
  const [response, setResponse] = useState<AskResponse>(DEFAULT_RESPONSE);
  const [selectedCitation, setSelectedCitation] = useState<number | null>(1);
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [documents, setDocuments] = useState<DocumentSummary[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    void Promise.all([getHealth(), getDocuments()])
      .then(([nextHealth, nextDocuments]) => {
        setHealth(nextHealth);
        setDocuments(nextDocuments);
      })
      .catch(() => setError("The API is offline. The example answer remains available."));
  }, []);

  async function submitQuestion() {
    const cleanQuestion = question.trim();
    if (cleanQuestion.length < 3 || loading) return;
    setLoading(true);
    setError(null);
    try {
      const nextResponse = await askQuestion(cleanQuestion);
      setResponse(nextResponse);
      setSelectedCitation(nextResponse.sources[0]?.citation ?? null);
    } catch {
      setError("The search request failed. Check that the FastAPI service is running.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app-shell">
      <Header view={view} onViewChange={setView} />
      {view === "ask" ? (
        <AskWorkspace
          question={question}
          onQuestionChange={setQuestion}
          onSubmit={submitQuestion}
          response={response}
          selectedCitation={selectedCitation}
          onCitationSelect={setSelectedCitation}
          loading={loading}
          error={error}
        />
      ) : view === "library" ? (
        <LibraryView documents={documents} />
      ) : (
        <EvaluationView />
      )}
      <StatusBar health={health} />
    </div>
  );
}
