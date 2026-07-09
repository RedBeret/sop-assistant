# NET-SOP-141 — Emergency Firewall Rule Reversion

**Owner:** Network Security Operations  
**Revision:** 3.3  
**Classification:** Synthetic training material — unclassified

## 1. Purpose

Safely revert a firewall rule change that blocks approved traffic, exposes an unintended path, or causes platform instability.

## 2. Preconditions

Identify the exact rule, policy package, change record, and affected services. Obtain watch-supervisor and security-duty-officer approval. Export the active policy and preserve traffic logs covering the incident window.

## 3. Reversion procedure

1. Compare the changed rule with the pre-change policy diff.
2. Disable or restore only the changed rule; do not roll back unrelated policy updates.
3. Validate policy syntax and run the platform's shadowed-rule and conflict checks.
4. Publish to the standby member first when the platform supports staged deployment.
5. Confirm management access and cluster health, then publish to the active member.
6. If the deployment fails, stop and restore the exported pre-change package.

## 4. Validation

Test the specific approved flow, confirm the unintended flow is still denied, review hit counters, and verify cluster synchronization. Monitor deny spikes, CPU, session establishment, and critical application probes for fifteen minutes.

## 5. Guardrails

Never add a temporary any-any permit, disable inspection globally, or bypass approval because the incident is urgent. Emergency change control shortens the path; it does not remove accountability.
