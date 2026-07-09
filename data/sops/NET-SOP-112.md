# NET-SOP-112 — BGP Neighbor Recovery

**Owner:** Network Operations  
**Revision:** 2.4  
**Classification:** Synthetic training material — unclassified

## 1. Purpose

Recover a failed Border Gateway Protocol neighbor while protecting stable routing and preserving evidence for root-cause analysis.

## 2. Initial checks

Confirm the peer address, autonomous system number, outage start time, and whether one or multiple neighbors are affected. Check interface state, local address reachability, recent configuration changes, authentication failures, and routing-process alarms.

## 3. Recovery procedure

1. Verify the underlying interface is up and has no excessive errors or drops.
2. Ping the peer from the configured source address. If unreachable, troubleshoot the transport path before touching BGP.
3. Compare the active neighbor configuration with the approved baseline, including peer address, remote AS, source interface, address family, and authentication key reference.
4. Review the last fifty routing log entries for hold-timer expiry, rejected capabilities, or authentication mismatch.
5. If transport and configuration are healthy, clear only the affected neighbor using a soft reset.
6. Use a hard reset only with watch-supervisor approval and only after a soft reset fails.

## 4. Validation

The neighbor must remain Established for ten minutes. Confirm expected prefixes are received and advertised, route-policy counters are normal, and no unexpected default route appears. Compare route count with the baseline and test reachability through the restored path.

## 5. Escalation

Escalate when more than one peer fails simultaneously, the peer repeatedly cycles between Active and Established, the advertised prefix set changes unexpectedly, or transport loss is outside the local boundary.
