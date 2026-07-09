# OPS-SOP-301 — Network Change Control and Maintenance Windows

**Owner:** Operations Governance  
**Revision:** 4.2  
**Classification:** Synthetic training material — unclassified

## 1. Purpose

Define the minimum planning, approval, execution, and closeout controls for production network changes.

## 2. Required change record

Every production change must name the owner, affected assets and services, purpose, risk, implementation steps, validation plan, rollback trigger, rollback procedure, maintenance window, communications plan, and approvers.

## 3. Pre-change review

Peer review is required for commands and policy diffs. The operator must capture a pre-change baseline, confirm out-of-band access, verify backups, identify a clear stop time, and rehearse the rollback when the change is high risk.

## 4. Execution controls

The change lead announces start, executes one bounded step at a time, records actual commands and timestamps, and runs the stated validation after each checkpoint. Pause when observed results differ from the plan. The watch supervisor alone may authorize continuation past a rollback trigger.

## 5. Rollback and closeout

Begin rollback early enough to finish before the window closes. After restoration, repeat the original validation plan. Close the record with actual outcomes, evidence links, deviations, incidents, and follow-up work. A successful technical change with missing evidence is not complete.

## 6. Emergency changes

Emergency changes require a named incident, verbal approval from the watch supervisor and service owner, a minimally safe rollback plan, and retrospective review within one business day.
