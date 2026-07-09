# NET-SOP-132 — Layer 2 Loop Containment

**Owner:** Network Operations  
**Revision:** 2.2  
**Classification:** Synthetic training material — unclassified

## 1. Purpose

Contain a suspected switching loop quickly while preserving management access and minimizing unnecessary disruption.

## 2. Indicators

Common indicators include a broadcast storm, rapidly changing MAC addresses, high switch CPU, spanning-tree topology changes, duplicate-address alarms, and simultaneous packet loss across one broadcast domain.

## 3. Immediate containment

1. Notify the watch supervisor and identify the affected VLAN and access layer.
2. Use interface counters and MAC-move logs to identify the smallest suspected link set.
3. Administratively disable the most likely recently changed access or trunk port.
4. Wait sixty seconds and verify broadcast rate, CPU, and topology-change counters decline.
5. If the storm continues, isolate the affected access switch from both distribution uplinks one at a time while preserving its management path when possible.
6. Do not disable spanning tree globally or clear the entire MAC table as a first response.

## 4. Recovery

Inspect cabling, port-channel membership, native VLAN settings, and spanning-tree guard status. Correct the fault through change control. Re-enable one link at a time and watch the broadcast rate for five minutes.

## 5. Validation

Confirm a stable spanning-tree root, no unexpected blocked uplinks, normal MAC learning, restored endpoint reachability, and no new topology changes for ten minutes.
