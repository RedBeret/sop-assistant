# COM-SOP-510 — Primary Time Source Recovery

**Owner:** Communications Systems  
**Revision:** 2.0  
**Classification:** Synthetic training material — unclassified

## 1. Purpose

Restore reliable network time when the primary time source is unreachable, unstable, or reporting excessive offset.

## 2. Detection and triage

Confirm the alert from two independent clients. Check source reachability, stratum, offset, jitter, leap status, authentication state, and recent antenna or upstream changes. A single client with drift is not proof that the primary source failed.

## 3. Recovery procedure

1. Remove an unstable source from the preferred set when offset exceeds the approved threshold.
2. Promote the designated secondary source; do not point clients at an unapproved public server.
3. Verify NTP authentication and source access controls.
4. Allow clients to slew time gradually. Step the clock only during an approved outage because abrupt time changes can break logs, certificates, and distributed systems.
5. Repair or restart the primary source, then observe it for thirty minutes before making it preferred again.

## 4. Validation

Confirm at least two reachable sources, acceptable offset and jitter, consistent time across authentication, logging, and database systems, and no certificate-validity alarms. Verify security logs maintain chronological order.

## 5. Escalation

Escalate suspected antenna failure, upstream reference loss, repeated leap alarms, or time divergence that affects authentication or evidence integrity.
