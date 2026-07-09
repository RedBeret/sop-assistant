# SYS-SOP-205 — Identity Provider Failover

**Owner:** Platform Operations  
**Revision:** 2.7  
**Classification:** Synthetic training material — unclassified

## 1. Purpose

Fail authentication services to the standby identity provider while preserving auditability and avoiding split-brain writes.

## 2. Failover criteria

Fail over when the active provider is unreachable from two application zones, token issuance fails for five consecutive minutes, or the platform owner confirms unrecoverable database or certificate failure.

## 3. Failover procedure

1. Place the active provider in read-only or fenced state.
2. Verify replication lag on the standby is less than sixty seconds.
3. Promote the standby using the approved orchestration command.
4. Update the service discovery record and lower the old endpoint weight to zero.
5. Invalidate only sessions issued after the last confirmed replication checkpoint when required.
6. Do not run both providers as writable primaries.

## 4. Validation

Test interactive login, service-account token issuance, multi-factor authentication, token refresh, and logout from two application zones. Confirm audit events arrive at the security log service with correct timestamps.

## 5. Return to normal

Rebuild the former active node as a standby, complete a replication consistency check, and schedule a controlled failback rather than reversing roles during the incident.
