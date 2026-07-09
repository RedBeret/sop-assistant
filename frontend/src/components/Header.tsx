import { AskIcon, BookIcon, EvalIcon } from "./Icons";
import type { ViewName } from "../types";

interface HeaderProps {
  view: ViewName;
  onViewChange: (view: ViewName) => void;
}

const NAV_ITEMS = [
  { id: "ask" as const, label: "Ask", icon: AskIcon },
  { id: "library" as const, label: "Library", icon: BookIcon },
  { id: "evaluation" as const, label: "Evaluation", icon: EvalIcon },
];

export function Header({ view, onViewChange }: HeaderProps) {
  return (
    <header className="topbar">
      <button className="brand" onClick={() => onViewChange("ask")} aria-label="Watchline home">
        Watchline
      </button>
      <nav className="primary-nav" aria-label="Primary navigation">
        {NAV_ITEMS.map((item) => {
          const Icon = item.icon;
          return (
            <button
              key={item.id}
              className={`nav-item ${view === item.id ? "is-active" : ""}`}
              onClick={() => onViewChange(item.id)}
              aria-current={view === item.id ? "page" : undefined}
            >
              <Icon />
              {item.label}
            </button>
          );
        })}
      </nav>
      <div className="brand-end" aria-hidden="true">W</div>
    </header>
  );
}
