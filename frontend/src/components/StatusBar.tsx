import type { HealthResponse } from "../types";
import { CheckIcon } from "./Icons";

export function StatusBar({ health }: { health: HealthResponse | null }) {
  return (
    <footer className="status-bar">
      <div>
        <span><CheckIcon /> {health?.document_count ?? 12} SOPs indexed</span>
        <i />
        <span><b /> {health ? "Local retrieval ready" : "Connecting to retrieval"}</span>
      </div>
      <div className="keyboard-help">
        <kbd>Enter</kbd> to search <i /> <kbd>↑↓</kbd> to review sources
      </div>
    </footer>
  );
}
