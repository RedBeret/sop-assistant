# NET-SOP-104 — Edge Router Firmware Rollback

**Owner:** Network Operations  
**Revision:** 3.1  
**Classification:** Synthetic training material — unclassified

## 1. Purpose

Restore an edge router to its last approved firmware image when an upgrade fails, the router cannot complete health checks, or post-change behavior is unstable.

## 2. Preconditions

- Confirm an approved change record exists and record the decision to roll back.
- Notify the watch supervisor and service owner.
- Verify console or out-of-band access and the checksum of the prior signed image.
- Capture the running configuration, interface state, routing neighbors, and current alarms.

## 3. Rollback triggers

Initiate rollback when the device fails to boot twice, critical interfaces remain down for more than five minutes, routing adjacencies do not recover within ten minutes, or the watch supervisor determines that service risk exceeds the benefit of continuing.

## 4. Containment

Place the node in maintenance mode or withdraw it from dynamic routing. Administratively downlink external interfaces if traffic is black-holing or flapping. Keep the management and console paths available. Do not erase the current image or configuration.

## 5. Firmware rollback procedure

1. Isolate the affected node from production forwarding.
2. Reboot into the previous signed firmware image stored in the approved local image slot.
3. Verify the image signature and SHA-256 checksum before activation.
4. Load the pre-change startup configuration only if the configuration schema changed.
5. Confirm the router reaches a stable ready state with no critical hardware alarms.
6. Restore one external interface at a time and watch error counters for two minutes.
7. Confirm routing adjacencies, critical route reachability, and management telemetry.

## 6. Validation and return to service

Compare interface state and neighbor counts with the pre-change capture. Run reachability tests to the operations gateway, DNS service, authentication service, and two critical remote prefixes. Observe the node for fifteen minutes. Return it to service only after the watch supervisor accepts the validation results.

## 7. Records and escalation

Record timestamps, image versions, checksum, commands, validation results, and anomalies in the change record. Escalate to vendor support if the prior image also fails, storage validation reports corruption, or the console becomes unavailable.
