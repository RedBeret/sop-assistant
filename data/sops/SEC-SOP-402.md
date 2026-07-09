# SEC-SOP-402 — Exposed Credential Response

**Owner:** Security Operations  
**Revision:** 3.8  
**Classification:** Synthetic training material — unclassified

## 1. Purpose

Contain and investigate an exposed password, API key, certificate private key, or service token.

## 2. Immediate actions

1. Open a security incident and record where and when the credential was found.
2. Revoke or disable the exposed credential immediately; do not wait for proof of misuse.
3. Preserve the source artifact and relevant audit logs without redistributing the secret.
4. Issue a replacement credential through the approved secret-management system.
5. Update dependent services using staged deployment and verify successful authentication.
6. Search audit logs from the earliest possible exposure time for use of the old credential.

## 3. Scope and investigation

Identify permissions, systems, data, and network paths available to the credential. Check source-control history, build logs, chat systems, ticket attachments, shell history, and deployment artifacts. Treat copied or cached versions as exposed too.

## 4. Validation

Confirm the old credential fails, the replacement works only from approved locations, dependent services are healthy, and no unauthorized access persists. Increase monitoring for the old credential identifier for seven days.

## 5. Guardrails

Never paste the exposed value into a ticket or chat. Reference a secure evidence location and redact all but the final four characters when an identifier is necessary.
