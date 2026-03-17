# Agent Guardrails — Action Catalog

Classification lookup table. Find the category, find the action, read the base tier. Controls are not listed here — they come from TIERS.md based on the final tier and guardrails mode.

---

## §FILE — File system

| Action | Base tier |
|--------|-----------|
| Write to user working files | 2 |
| Overwrite user file without backup or version control | 3 |
| Overwrite or modify config files (.bashrc, openclaw.json, .env) | 3 |
| Write to files that influence execution, deployment, auth, or CI/CD (Dockerfile, .github/workflows/, auth tokens) | 3 |
| Delete files | 3 |
| Bulk file operations (5+ files) | 3 |

## §SHELL — Shell execution

| Action | Base tier |
|--------|-----------|
| Local state-modifying command (git commit, mkdir, mv) | 2 |
| Execute local script or binary not previously reviewed in session | 3 |
| Package install from network registry (npm install, pip install, apt install) | 3 |
| Command with network access (curl, wget, fetch) | 3 |
| System-level command (sudo, chmod, chown, systemctl) | 4 |
| Obfuscated or encoded command (base64 -d \| bash, eval, hex) | 4 |

## §NET — Network and API

| Action | Base tier |
|--------|-----------|
| Read from authenticated API (Gmail read, calendar fetch) | 2 |
| Bulk export, cross-entity fetch, or read admin/secret data via authenticated API | 3 |
| Write to external API (POST to webhook, update CRM) | 3 |
| Transmit user data externally (upload to S3, send to third-party) | 3 |
| Connect to unfamiliar endpoint (URL from skill docs, unknown webhook) | 4 |

## §COMM — Communication

| Action | Base tier |
|--------|-----------|
| Send message to user's own channel (self-notification) | 2 |
| Send message to another person (email, Slack DM) | 3 |
| Send to group or public channel (Slack channel, team email, forum) | 4 |

## §CRED — Credentials and secrets

| Action | Base tier |
|--------|-----------|
| Use credential in authenticated request (API call with stored token) | 2 |
| Display or read credential value (cat .env, show API key) | 3 |
| Transmit credential externally (send key via email, paste in webhook) | 4 |

## §BROWSER — Browser automation

| Action | Base tier |
|--------|-----------|
| Navigate to URL from external source (skill instructions, email link) | 2 |
| Fill form or click interactive elements | 3 |
| Download file from web | 3 |
| Download executable, script, or binary from web | 4 |

## §SCHED — Automation and scheduling

| Action | Base tier |
|--------|-----------|
| Create or modify cron job | 3 |
| Create or modify webhook endpoint | 4 |

## §FIN — Financial and transactional

| Action | Base tier |
|--------|-----------|
| Look up pricing or account info | 2 |
| Initiate purchase or payment | 4 |
| Modify billing or subscription | 4 |
