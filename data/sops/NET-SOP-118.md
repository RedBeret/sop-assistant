# NET-SOP-118 — DNS Service Restoration

**Owner:** Infrastructure Services  
**Revision:** 4.0  
**Classification:** Synthetic training material — unclassified

## 1. Purpose

Restore recursive and authoritative DNS service while preventing stale or poisoned data from spreading.

## 2. Triage

Test one known-good internal record, one external record, and one authoritative zone directly against each resolver. Check service health, disk space, time synchronization, upstream reachability, replication status, and recent zone changes.

## 3. Resolver recovery

1. Remove the unhealthy resolver from the service pool.
2. Preserve logs and a copy of the active configuration.
3. Validate configuration syntax and zone-file serials.
4. Restart the DNS service once. Do not loop restarts.
5. Flush only the affected cache entry or zone when the fault is scoped; flush the full cache only with supervisor approval.
6. Query the resolver directly for known-good internal, external, and negative responses.
7. Return the resolver to the pool at reduced weight for five minutes before restoring full weight.

## 4. Authoritative zone rollback

If a zone change is faulty, restore the last signed zone bundle, increment the serial number, reload the zone, and verify transfer to secondaries. Never reduce a zone serial to perform a rollback.

## 5. Validation

Confirm response codes, answer content, TTL values, DNSSEC validation, and latency from two network segments. Monitor SERVFAIL and timeout rates for fifteen minutes.
