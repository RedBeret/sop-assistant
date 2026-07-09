# NET-SOP-126 — Site-to-Site VPN Tunnel Recovery

**Owner:** Network Security Operations  
**Revision:** 1.9  
**Classification:** Synthetic training material — unclassified

## 1. Purpose

Restore a site-to-site IPsec tunnel without weakening encryption or bypassing approved policy.

## 2. Diagnosis

Confirm which tunnel, peer, and protected subnets are affected. Check internet reachability to the peer, IKE phase-one state, IPsec phase-two security associations, certificate validity, system time, and recent policy changes.

## 3. Recovery procedure

1. Verify peer reachability and that UDP 500 and 4500 traffic is not blocked.
2. Compare proposals, lifetimes, traffic selectors, and certificate references with the approved baseline.
3. Check for clock drift greater than two minutes before investigating certificates.
4. Clear only the affected child security association and allow it to renegotiate.
5. Clear the IKE association only if child-SA renegotiation fails and the watch supervisor approves.
6. Never disable certificate validation, reduce encryption strength, or add an any-any rule to restore service.

## 4. Validation

Generate traffic between approved protected subnets. Confirm encapsulation and decapsulation counters increase, no replay or authentication errors occur, and application probes succeed in both directions. Observe two successful rekey events when practical.

## 5. Escalation

Escalate certificate-chain failures, repeated rekey failures, selector disagreements that require policy changes, and peer-side outages.
