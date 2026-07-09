export type ViewName = "ask" | "library" | "evaluation";

export interface Source {
  citation: number;
  doc_id: string;
  title: string;
  section: string;
  heading: string;
  excerpt: string;
  relevance: number;
}

export interface AskResponse {
  question: string;
  answer: string;
  grounded: boolean;
  provider: string;
  sources: Source[];
}

export interface HealthResponse {
  status: string;
  document_count: number;
  chunk_count: number;
  embedding_provider: string;
  generation_provider: string;
}

export interface DocumentSummary {
  doc_id: string;
  title: string;
  chunk_count: number;
}
