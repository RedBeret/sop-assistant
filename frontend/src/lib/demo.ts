import type { AskResponse } from "../types";

export const DEFAULT_QUESTION =
  "What is the rollback procedure for a failed edge router firmware upgrade?";

export const DEFAULT_RESPONSE: AskResponse = {
  question: DEFAULT_QUESTION,
  grounded: true,
  provider: "local-extractive",
  answer: [
    "1. Isolate the affected node from production forwarding. [1]",
    "2. Reboot into the previous signed firmware image and verify its signature and SHA-256 checksum before activation. [1]",
    "3. Restore interfaces one at a time, then confirm routing adjacencies, critical route reachability, and management telemetry. [1]",
    "4. Record the rollback decision, actual commands, validation results, and anomalies in the change record. [2]",
  ].join("\n"),
  sources: [
    {
      citation: 1,
      doc_id: "NET-SOP-104",
      title: "Edge Router Firmware Rollback",
      section: "5",
      heading: "Firmware rollback procedure",
      relevance: 96,
      excerpt:
        "Isolate the affected node from production forwarding. Reboot into the previous signed firmware image stored in the approved local image slot. Verify the image signature and SHA-256 checksum before activation. Confirm routing adjacencies, critical route reachability, and management telemetry.",
    },
    {
      citation: 2,
      doc_id: "OPS-SOP-301",
      title: "Network Change Control and Maintenance Windows",
      section: "5",
      heading: "Rollback and closeout",
      relevance: 83,
      excerpt:
        "Begin rollback early enough to finish before the window closes. After restoration, repeat the original validation plan. Close the record with actual outcomes, evidence links, deviations, incidents, and follow-up work.",
    },
  ],
};
