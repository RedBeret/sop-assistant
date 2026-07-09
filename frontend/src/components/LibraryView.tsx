import type { DocumentSummary } from "../types";

export function LibraryView({ documents }: { documents: DocumentSummary[] }) {
  return (
    <main className="secondary-view">
      <div className="secondary-heading">
        <h1>Procedure library</h1>
        <p>Twelve synthetic, unclassified procedures built for repeatable retrieval evaluation.</p>
      </div>
      <div className="library-table" role="table" aria-label="Indexed SOPs">
        <div className="library-row library-header" role="row">
          <span role="columnheader">Document</span>
          <span role="columnheader">Procedure</span>
          <span role="columnheader">Sections indexed</span>
        </div>
        {documents.map((document) => (
          <div className="library-row" role="row" key={document.doc_id}>
            <code role="cell">{document.doc_id}</code>
            <strong role="cell">{document.title}</strong>
            <span role="cell">{document.chunk_count}</span>
          </div>
        ))}
      </div>
    </main>
  );
}
