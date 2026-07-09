# SYS-SOP-214 — Database Backup Restoration

**Owner:** Data Platform Operations  
**Revision:** 5.1  
**Classification:** Synthetic training material — unclassified

## 1. Purpose

Restore a service database from an approved backup and prove that the restored data is complete before application traffic returns.

## 2. Restore preparation

Declare the target recovery point and recovery time objective. Quarantine the target environment, verify available storage, capture the failed database state, and identify the full backup plus required incremental or transaction-log files.

## 3. Restoration procedure

1. Verify backup signatures, checksums, encryption-key access, and retention metadata.
2. Restore the latest valid full backup into an isolated recovery instance.
3. Apply incremental backups and transaction logs in chronological order up to the approved recovery point.
4. Run database integrity checks before opening the instance to application connections.
5. Reconcile row counts for critical tables and independently verify three known business records.
6. Rotate credentials used during recovery and remove temporary access.

## 4. Cutover

Place the application in maintenance mode, take a final logical export when possible, update the database endpoint, and allow a single application instance to connect first. Expand traffic only after read and write smoke tests pass.

## 5. Validation and records

Record backup identifiers, checksums, recovery point, integrity results, row-count reconciliation, data-loss window, and approvers. Retain the failed instance read-only until the incident commander authorizes disposal.
