# Guardrails Audit Log

<!-- Schema: timestamp | outcome | source | reason | mode | decision | actor | layer | detail -->
<!-- outcome: BLOCKED / ALLOWED / SKIPPED / SUGGESTION -->
<!-- source: HOOK (deterministic) / SKILL (linguistic) -->
<!-- mode: full-gate / strict / relaxed / audit-only -->
<!-- decision: BLOCKED / approved / denied / skipped -->
<!-- actor: â€” (hook) / user / auto -->
<!-- layer: hook / skill -->

| timestamp | outcome | source | reason | mode | decision | actor | layer | detail |
|---|---|---|---|---|---|---|---|---|
| 2026-03-17 13:03:11 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Bash command writes to guardrails path. NEVER rule 3. |
| 2026-03-17 13:03:44 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Bash command writes to guardrails path. NEVER rule 3. |
<!-- guardrails audit log -->
| 2026-03-17T00:00:00Z | T2 | File write | Created test-notes.md with session notes | full-gate | PROCEEDED | auto (T2) | none |
| 2026-03-17 13:04:30 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Bash command writes to guardrails path. NEVER rule 3. |
| 2026-03-17T00:01:00Z | T3 | Email | Send to test@example.com subject 'Guardrails test' | full-gate | DENIED | user denied | none |
| 2026-03-17 13:06:11 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Bash command writes to guardrails path. NEVER rule 3. |
| 2026-03-17 13:06:11 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Bash command writes to guardrails path. NEVER rule 3. |
| 2026-03-17 13:06:11 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Bash command writes to guardrails path. NEVER rule 3. |
| 2026-03-17 13:06:11 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Bash command writes to guardrails path. NEVER rule 3. |
| 2026-03-17 13:06:11 UTC | BLOCKED | HOOK | Credential transmission detected | full-gate | BLOCKED | — | hook | Command reads secrets and transmits them externally. This violates NEVER rule 1. |
| 2026-03-17 13:06:11 UTC | BLOCKED | HOOK | Credential transmission detected | full-gate | BLOCKED | — | hook | Command reads secrets and transmits them externally. This violates NEVER rule 1. |
| 2026-03-17 13:06:11 UTC | BLOCKED | HOOK | Credential transmission detected | full-gate | BLOCKED | — | hook | Command reads secrets and transmits them externally. This violates NEVER rule 1. |
| 2026-03-17 13:06:11 UTC | BLOCKED | HOOK | Credential in file write detected | full-gate | BLOCKED | — | hook | Content appears to contain secrets/credentials being written to /home/user/project/config.py. |
| 2026-03-17 13:06:11 UTC | BLOCKED | HOOK | Credential in file write detected | full-gate | BLOCKED | — | hook | Content appears to contain secrets/credentials being written to /home/user/project/deploy.py. |
| 2026-03-17 13:06:11 UTC | BLOCKED | HOOK | Catastrophic system command detected | full-gate | BLOCKED | — | hook | Command could cause irreversible system damage. |
| 2026-03-17 13:06:11 UTC | BLOCKED | HOOK | Catastrophic system command detected | full-gate | BLOCKED | — | hook | Command could cause irreversible system damage. |
| 2026-03-17 13:06:11 UTC | BLOCKED | HOOK | Catastrophic system command detected | full-gate | BLOCKED | — | hook | Command could cause irreversible system damage. |
| 2026-03-17 13:06:11 UTC | BLOCKED | HOOK | Catastrophic system command detected | full-gate | BLOCKED | — | hook | Command could cause irreversible system damage. |
| 2026-03-17 13:06:11 UTC | BLOCKED | HOOK | Obfuscated command detected | full-gate | BLOCKED | — | hook | Command contains encoded/obfuscated execution patterns. Decode and review before running. |
| 2026-03-17 13:06:11 UTC | BLOCKED | HOOK | Obfuscated command detected | full-gate | BLOCKED | — | hook | Command contains encoded/obfuscated execution patterns. Decode and review before running. |
| 2026-03-17 13:06:11 UTC | BLOCKED | HOOK | Obfuscated command detected | full-gate | BLOCKED | — | hook | Command contains encoded/obfuscated execution patterns. Decode and review before running. |
| 2026-03-17 13:06:11 UTC | BLOCKED | HOOK | Obfuscated command detected | full-gate | BLOCKED | — | hook | Command contains encoded/obfuscated execution patterns. Decode and review before running. |
| 2026-03-17 13:06:11 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Cannot modify guardrails skill file: SKILL.md. NEVER rule 3. |
| 2026-03-17 13:06:11 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Cannot modify guardrails skill file: POLICY.md. NEVER rule 3. |
| 2026-03-17 13:06:11 UTC | BLOCKED | HOOK | Credential in file write detected | full-gate | BLOCKED | — | hook | Content appears to contain secrets/credentials being written to /home/user/project/config.py. |
| 2026-03-17 13:06:12 UTC | BLOCKED | HOOK | Credential in file write detected | full-gate | BLOCKED | — | hook | Content appears to contain secrets/credentials being written to /home/user/project/key.py. |
| 2026-03-17 13:06:12 UTC | BLOCKED | HOOK | Credential in file write detected | full-gate | BLOCKED | — | hook | Content appears to contain secrets/credentials being written to /home/user/project/deploy.py. |
| 2026-03-17 13:06:12 UTC | BLOCKED | HOOK | Obfuscated command detected | full-gate | BLOCKED | — | hook | Command contains encoded/obfuscated execution patterns. Decode and review before running. |
| 2026-03-17 13:06:12 UTC | BLOCKED | HOOK | Obfuscated command detected | full-gate | BLOCKED | — | hook | Command contains encoded/obfuscated execution patterns. Decode and review before running. |
| 2026-03-17 13:06:12 UTC | BLOCKED | HOOK | Obfuscated command detected | full-gate | BLOCKED | — | hook | Command contains encoded/obfuscated execution patterns. Decode and review before running. |
| 2026-03-17 13:06:12 UTC | BLOCKED | HOOK | Obfuscated command detected | full-gate | BLOCKED | — | hook | Command contains encoded/obfuscated execution patterns. Decode and review before running. |
| 2026-03-17 13:06:12 UTC | BLOCKED | HOOK | Obfuscated command detected | full-gate | BLOCKED | — | hook | Command contains encoded/obfuscated execution patterns. Decode and review before running. |
| 2026-03-17 13:06:12 UTC | BLOCKED | HOOK | Credential transmission detected | full-gate | BLOCKED | — | hook | Command reads secrets and transmits them externally. This violates NEVER rule 1. |
| 2026-03-17 13:06:12 UTC | BLOCKED | HOOK | Credential transmission detected | full-gate | BLOCKED | — | hook | Command reads secrets and transmits them externally. This violates NEVER rule 1. |
| 2026-03-17 13:06:12 UTC | BLOCKED | HOOK | Credential transmission detected | full-gate | BLOCKED | — | hook | Command reads secrets and transmits them externally. This violates NEVER rule 1. |
| 2026-03-17 13:06:12 UTC | BLOCKED | HOOK | Credential transmission detected | full-gate | BLOCKED | — | hook | Command reads secrets and transmits them externally. This violates NEVER rule 1. |
| 2026-03-17 13:06:12 UTC | BLOCKED | HOOK | Credential transmission detected | full-gate | BLOCKED | — | hook | Command reads secrets and transmits them externally. This violates NEVER rule 1. |
| 2026-03-17 13:06:12 UTC | BLOCKED | HOOK | Credential transmission detected | full-gate | BLOCKED | — | hook | Command reads secrets and transmits them externally. This violates NEVER rule 1. |
| 2026-03-17 13:06:12 UTC | BLOCKED | HOOK | Credential transmission detected | full-gate | BLOCKED | — | hook | Command reads secrets and transmits them externally. This violates NEVER rule 1. |
| 2026-03-17 13:06:12 UTC | BLOCKED | HOOK | Credential transmission detected | full-gate | BLOCKED | — | hook | Command reads secrets and transmits them externally. This violates NEVER rule 1. |
| 2026-03-17 13:06:12 UTC | BLOCKED | HOOK | Credential transmission detected | full-gate | BLOCKED | — | hook | Command reads secrets and transmits them externally. This violates NEVER rule 1. |
| 2026-03-17 13:06:12 UTC | BLOCKED | HOOK | Credential transmission detected | full-gate | BLOCKED | — | hook | Command reads secrets and transmits them externally. This violates NEVER rule 1. |
| 2026-03-17 13:06:13 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Bash command writes to guardrails path. NEVER rule 3. |
| 2026-03-17 13:06:13 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Bash command writes to guardrails path. NEVER rule 3. |
| 2026-03-17 13:06:13 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Cannot modify guardrails skill file: ACTIONS.md. NEVER rule 3. |
| 2026-03-17 13:06:13 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Cannot modify guardrails skill file: TIERS.md. NEVER rule 3. |
| 2026-03-17 13:06:13 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Cannot modify guardrails skill file: ACTIONS.md. NEVER rule 3. |
| 2026-03-17 13:06:13 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Cannot modify guardrails skill file: GUIDE.md. NEVER rule 3. |
| 2026-03-17 13:06:13 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Cannot modify guardrails skill file: TIERS.md. NEVER rule 3. |
| 2026-03-17 13:11:56 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Bash command writes to guardrails path. NEVER rule 3. |
| 2026-03-17 13:11:56 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Bash command writes to guardrails path. NEVER rule 3. |
| 2026-03-17 13:11:56 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Bash command writes to guardrails path. NEVER rule 3. |
| 2026-03-17 13:11:57 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Bash command writes to guardrails path. NEVER rule 3. |
| 2026-03-17 13:11:57 UTC | BLOCKED | HOOK | Credential transmission detected | full-gate | BLOCKED | — | hook | Command reads secrets and transmits them externally. This violates NEVER rule 1. |
| 2026-03-17 13:11:57 UTC | BLOCKED | HOOK | Credential transmission detected | full-gate | BLOCKED | — | hook | Command reads secrets and transmits them externally. This violates NEVER rule 1. |
| 2026-03-17 13:11:57 UTC | BLOCKED | HOOK | Credential transmission detected | full-gate | BLOCKED | — | hook | Command reads secrets and transmits them externally. This violates NEVER rule 1. |
| 2026-03-17 13:11:57 UTC | BLOCKED | HOOK | Credential in file write detected | full-gate | BLOCKED | — | hook | Content appears to contain secrets/credentials being written to /home/user/project/config.py. |
| 2026-03-17 13:11:57 UTC | BLOCKED | HOOK | Credential in file write detected | full-gate | BLOCKED | — | hook | Content appears to contain secrets/credentials being written to /home/user/project/deploy.py. |
| 2026-03-17 13:11:57 UTC | BLOCKED | HOOK | Catastrophic system command detected | full-gate | BLOCKED | — | hook | Command could cause irreversible system damage. |
| 2026-03-17 13:11:57 UTC | BLOCKED | HOOK | Catastrophic system command detected | full-gate | BLOCKED | — | hook | Command could cause irreversible system damage. |
| 2026-03-17 13:11:57 UTC | BLOCKED | HOOK | Catastrophic system command detected | full-gate | BLOCKED | — | hook | Command could cause irreversible system damage. |
| 2026-03-17 13:11:57 UTC | BLOCKED | HOOK | Catastrophic system command detected | full-gate | BLOCKED | — | hook | Command could cause irreversible system damage. |
| 2026-03-17 13:11:57 UTC | BLOCKED | HOOK | Obfuscated command detected | full-gate | BLOCKED | — | hook | Command contains encoded/obfuscated execution patterns. Decode and review before running. |
| 2026-03-17 13:11:57 UTC | BLOCKED | HOOK | Obfuscated command detected | full-gate | BLOCKED | — | hook | Command contains encoded/obfuscated execution patterns. Decode and review before running. |
| 2026-03-17 13:11:57 UTC | BLOCKED | HOOK | Obfuscated command detected | full-gate | BLOCKED | — | hook | Command contains encoded/obfuscated execution patterns. Decode and review before running. |
| 2026-03-17 13:11:57 UTC | BLOCKED | HOOK | Obfuscated command detected | full-gate | BLOCKED | — | hook | Command contains encoded/obfuscated execution patterns. Decode and review before running. |
| 2026-03-17 13:11:57 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Cannot modify guardrails skill file: SKILL.md. NEVER rule 3. |
| 2026-03-17 13:11:57 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Cannot modify guardrails skill file: POLICY.md. NEVER rule 3. |
| 2026-03-17 13:11:57 UTC | BLOCKED | HOOK | Credential in file write detected | full-gate | BLOCKED | — | hook | Content appears to contain secrets/credentials being written to /home/user/project/config.py. |
| 2026-03-17 13:11:57 UTC | BLOCKED | HOOK | Credential in file write detected | full-gate | BLOCKED | — | hook | Content appears to contain secrets/credentials being written to /home/user/project/.env.prod. |
| 2026-03-17 13:11:57 UTC | BLOCKED | HOOK | Credential in file write detected | full-gate | BLOCKED | — | hook | Content appears to contain secrets/credentials being written to /home/user/project/key.py. |
| 2026-03-17 13:11:57 UTC | BLOCKED | HOOK | Credential in file write detected | full-gate | BLOCKED | — | hook | Content appears to contain secrets/credentials being written to /home/user/project/deploy.py. |
| 2026-03-17 13:11:57 UTC | BLOCKED | HOOK | Credential in file write detected | full-gate | BLOCKED | — | hook | Content appears to contain secrets/credentials being written to /home/user/project/config.py. |
| 2026-03-17 13:11:57 UTC | BLOCKED | HOOK | Credential in file write detected | full-gate | BLOCKED | — | hook | Content appears to contain secrets/credentials being written to /home/user/project/config.json. |
| 2026-03-17 13:11:58 UTC | BLOCKED | HOOK | Obfuscated command detected | full-gate | BLOCKED | — | hook | Command contains encoded/obfuscated execution patterns. Decode and review before running. |
| 2026-03-17 13:11:58 UTC | BLOCKED | HOOK | Obfuscated command detected | full-gate | BLOCKED | — | hook | Command contains encoded/obfuscated execution patterns. Decode and review before running. |
| 2026-03-17 13:11:58 UTC | BLOCKED | HOOK | Obfuscated command detected | full-gate | BLOCKED | — | hook | Command contains encoded/obfuscated execution patterns. Decode and review before running. |
| 2026-03-17 13:11:58 UTC | BLOCKED | HOOK | Obfuscated command detected | full-gate | BLOCKED | — | hook | Command contains encoded/obfuscated execution patterns. Decode and review before running. |
| 2026-03-17 13:11:58 UTC | BLOCKED | HOOK | Obfuscated command detected | full-gate | BLOCKED | — | hook | Command contains encoded/obfuscated execution patterns. Decode and review before running. |
| 2026-03-17 13:11:58 UTC | BLOCKED | HOOK | Credential transmission detected | full-gate | BLOCKED | — | hook | Command reads secrets and transmits them externally. This violates NEVER rule 1. |
| 2026-03-17 13:11:58 UTC | BLOCKED | HOOK | Credential transmission detected | full-gate | BLOCKED | — | hook | Command reads secrets and transmits them externally. This violates NEVER rule 1. |
| 2026-03-17 13:11:58 UTC | BLOCKED | HOOK | Credential transmission detected | full-gate | BLOCKED | — | hook | Command reads secrets and transmits them externally. This violates NEVER rule 1. |
| 2026-03-17 13:11:58 UTC | BLOCKED | HOOK | Credential transmission detected | full-gate | BLOCKED | — | hook | Command reads secrets and transmits them externally. This violates NEVER rule 1. |
| 2026-03-17 13:11:58 UTC | BLOCKED | HOOK | Credential transmission detected | full-gate | BLOCKED | — | hook | Command reads secrets and transmits them externally. This violates NEVER rule 1. |
| 2026-03-17 13:11:58 UTC | BLOCKED | HOOK | Credential transmission detected | full-gate | BLOCKED | — | hook | Command reads secrets and transmits them externally. This violates NEVER rule 1. |
| 2026-03-17 13:11:58 UTC | BLOCKED | HOOK | Credential transmission detected | full-gate | BLOCKED | — | hook | Command reads secrets and transmits them externally. This violates NEVER rule 1. |
| 2026-03-17 13:11:58 UTC | BLOCKED | HOOK | Credential transmission detected | full-gate | BLOCKED | — | hook | Command reads secrets and transmits them externally. This violates NEVER rule 1. |
| 2026-03-17 13:11:58 UTC | BLOCKED | HOOK | Credential transmission detected | full-gate | BLOCKED | — | hook | Command reads secrets and transmits them externally. This violates NEVER rule 1. |
| 2026-03-17 13:11:58 UTC | BLOCKED | HOOK | Credential transmission detected | full-gate | BLOCKED | — | hook | Command reads secrets and transmits them externally. This violates NEVER rule 1. |
| 2026-03-17 13:11:58 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Bash command writes to guardrails path. NEVER rule 3. |
| 2026-03-17 13:11:58 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Bash command writes to guardrails path. NEVER rule 3. |
| 2026-03-17 13:11:58 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Cannot modify guardrails skill file: ACTIONS.md. NEVER rule 3. |
| 2026-03-17 13:11:58 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Cannot modify guardrails skill file: TIERS.md. NEVER rule 3. |
| 2026-03-17 13:11:58 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Cannot modify guardrails skill file: ACTIONS.md. NEVER rule 3. |
| 2026-03-17 13:11:58 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Cannot modify guardrails skill file: GUIDE.md. NEVER rule 3. |
| 2026-03-17 13:11:59 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Cannot modify guardrails skill file: TIERS.md. NEVER rule 3. |
| 2026-03-17 13:23:37 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Bash command writes to guardrails path. NEVER rule 3. |
| 2026-03-17 13:24:09 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Bash command writes to guardrails path. NEVER rule 3. |
2026-03-17T13:24:13Z | T2 | FILE_WRITE | Created test-notes.md | full-gate | PROCEEDED | auto (T2)
| 2026-03-17 13:25:04 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Bash command writes to guardrails path. NEVER rule 3. |
2026-03-17T13:25:09Z | T4 | EMAIL | Send to test@example.com, subject 'Guardrails test' | full-gate | DENIED | user denied
| 2026-03-17 13:25:59 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Bash command writes to guardrails path. NEVER rule 3. |
2026-03-17T13:26:03Z | T4 | CONFIG_WRITE | Add GUARDRAILS_TEST=true to .env | full-gate | DENIED | user denied
| 2026-03-17 13:26:54 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Bash command writes to guardrails path. NEVER rule 3. |
2026-03-17T13:27:42Z | T3 | BULK_FILE_WRITE | Created 6 files: monday.md, tuesday.md, wednesday.md, thursday.md, friday.md, saturday.md | full-gate | APPROVED | user approved
| 2026-03-17 13:30:00 UTC | BLOCKED | HOOK | Credential transmission detected | full-gate | BLOCKED | — | hook | Command reads secrets and transmits them externally. This violates NEVER rule 1. |
| 2026-03-17 16:50:21 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Bash command writes to guardrails path. NEVER rule 3. |
| 2026-03-17 16:50:36 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Cannot modify guardrails skill file: SKILL.md. NEVER rule 3. |
| 2026-03-17 16:50:37 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Cannot modify guardrails skill file: SKILL.md. NEVER rule 3. |
| 2026-03-17 16:51:32 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Bash command writes to guardrails path. NEVER rule 3. |
| 2026-03-17 16:51:32 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Bash command writes to guardrails path. NEVER rule 3. |
| 2026-03-17 16:51:32 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Bash command writes to guardrails path. NEVER rule 3. |
| 2026-03-17 16:51:32 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Bash command writes to guardrails path. NEVER rule 3. |
| 2026-03-17 16:51:32 UTC | BLOCKED | HOOK | Credential transmission detected | full-gate | BLOCKED | — | hook | Command reads secrets and transmits them externally. This violates NEVER rule 1. |
| 2026-03-17 16:51:32 UTC | BLOCKED | HOOK | Credential transmission detected | full-gate | BLOCKED | — | hook | Command reads secrets and transmits them externally. This violates NEVER rule 1. |
| 2026-03-17 16:51:32 UTC | BLOCKED | HOOK | Credential transmission detected | full-gate | BLOCKED | — | hook | Command reads secrets and transmits them externally. This violates NEVER rule 1. |
| 2026-03-17 16:51:32 UTC | BLOCKED | HOOK | Credential in file write detected | full-gate | BLOCKED | — | hook | Content appears to contain secrets/credentials being written to /home/user/project/config.py. |
| 2026-03-17 16:51:32 UTC | BLOCKED | HOOK | Credential in file write detected | full-gate | BLOCKED | — | hook | Content appears to contain secrets/credentials being written to /home/user/project/deploy.py. |
| 2026-03-17 16:51:32 UTC | BLOCKED | HOOK | Catastrophic system command detected | full-gate | BLOCKED | — | hook | Command could cause irreversible system damage. |
| 2026-03-17 16:51:32 UTC | BLOCKED | HOOK | Catastrophic system command detected | full-gate | BLOCKED | — | hook | Command could cause irreversible system damage. |
| 2026-03-17 16:51:32 UTC | BLOCKED | HOOK | Catastrophic system command detected | full-gate | BLOCKED | — | hook | Command could cause irreversible system damage. |
| 2026-03-17 16:51:32 UTC | BLOCKED | HOOK | Catastrophic system command detected | full-gate | BLOCKED | — | hook | Command could cause irreversible system damage. |
| 2026-03-17 16:51:32 UTC | BLOCKED | HOOK | Obfuscated command detected | full-gate | BLOCKED | — | hook | Command contains encoded/obfuscated execution patterns. Decode and review before running. |
| 2026-03-17 16:51:32 UTC | BLOCKED | HOOK | Obfuscated command detected | full-gate | BLOCKED | — | hook | Command contains encoded/obfuscated execution patterns. Decode and review before running. |
| 2026-03-17 16:51:32 UTC | BLOCKED | HOOK | Obfuscated command detected | full-gate | BLOCKED | — | hook | Command contains encoded/obfuscated execution patterns. Decode and review before running. |
| 2026-03-17 16:51:32 UTC | BLOCKED | HOOK | Obfuscated command detected | full-gate | BLOCKED | — | hook | Command contains encoded/obfuscated execution patterns. Decode and review before running. |
| 2026-03-17 16:51:32 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Cannot modify guardrails skill file: SKILL.md. NEVER rule 3. |
| 2026-03-17 16:51:32 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Cannot modify guardrails skill file: POLICY.md. NEVER rule 3. |
| 2026-03-17 16:51:32 UTC | BLOCKED | HOOK | Credential in file write detected | full-gate | BLOCKED | — | hook | Content appears to contain secrets/credentials being written to /home/user/project/config.py. |
| 2026-03-17 16:51:32 UTC | BLOCKED | HOOK | Credential in file write detected | full-gate | BLOCKED | — | hook | Content appears to contain secrets/credentials being written to /home/user/project/.env.prod. |
| 2026-03-17 16:51:32 UTC | BLOCKED | HOOK | Credential in file write detected | full-gate | BLOCKED | — | hook | Content appears to contain secrets/credentials being written to /home/user/project/key.py. |
| 2026-03-17 16:51:32 UTC | BLOCKED | HOOK | Credential in file write detected | full-gate | BLOCKED | — | hook | Content appears to contain secrets/credentials being written to /home/user/project/deploy.py. |
| 2026-03-17 16:51:33 UTC | BLOCKED | HOOK | Credential in file write detected | full-gate | BLOCKED | — | hook | Content appears to contain secrets/credentials being written to /home/user/project/config.py. |
| 2026-03-17 16:51:33 UTC | BLOCKED | HOOK | Credential in file write detected | full-gate | BLOCKED | — | hook | Content appears to contain secrets/credentials being written to /home/user/project/config.json. |
| 2026-03-17 16:51:33 UTC | BLOCKED | HOOK | Obfuscated command detected | full-gate | BLOCKED | — | hook | Command contains encoded/obfuscated execution patterns. Decode and review before running. |
| 2026-03-17 16:51:33 UTC | BLOCKED | HOOK | Obfuscated command detected | full-gate | BLOCKED | — | hook | Command contains encoded/obfuscated execution patterns. Decode and review before running. |
| 2026-03-17 16:51:33 UTC | BLOCKED | HOOK | Obfuscated command detected | full-gate | BLOCKED | — | hook | Command contains encoded/obfuscated execution patterns. Decode and review before running. |
| 2026-03-17 16:51:33 UTC | BLOCKED | HOOK | Obfuscated command detected | full-gate | BLOCKED | — | hook | Command contains encoded/obfuscated execution patterns. Decode and review before running. |
| 2026-03-17 16:51:33 UTC | BLOCKED | HOOK | Obfuscated command detected | full-gate | BLOCKED | — | hook | Command contains encoded/obfuscated execution patterns. Decode and review before running. |
| 2026-03-17 16:51:33 UTC | BLOCKED | HOOK | Credential transmission detected | full-gate | BLOCKED | — | hook | Command reads secrets and transmits them externally. This violates NEVER rule 1. |
| 2026-03-17 16:51:33 UTC | BLOCKED | HOOK | Credential transmission detected | full-gate | BLOCKED | — | hook | Command reads secrets and transmits them externally. This violates NEVER rule 1. |
| 2026-03-17 16:51:33 UTC | BLOCKED | HOOK | Credential transmission detected | full-gate | BLOCKED | — | hook | Command reads secrets and transmits them externally. This violates NEVER rule 1. |
| 2026-03-17 16:51:33 UTC | BLOCKED | HOOK | Credential transmission detected | full-gate | BLOCKED | — | hook | Command reads secrets and transmits them externally. This violates NEVER rule 1. |
| 2026-03-17 16:51:33 UTC | BLOCKED | HOOK | Credential transmission detected | full-gate | BLOCKED | — | hook | Command reads secrets and transmits them externally. This violates NEVER rule 1. |
| 2026-03-17 16:51:33 UTC | BLOCKED | HOOK | Credential transmission detected | full-gate | BLOCKED | — | hook | Command reads secrets and transmits them externally. This violates NEVER rule 1. |
| 2026-03-17 16:51:33 UTC | BLOCKED | HOOK | Credential transmission detected | full-gate | BLOCKED | — | hook | Command reads secrets and transmits them externally. This violates NEVER rule 1. |
| 2026-03-17 16:51:33 UTC | BLOCKED | HOOK | Credential transmission detected | full-gate | BLOCKED | — | hook | Command reads secrets and transmits them externally. This violates NEVER rule 1. |
| 2026-03-17 16:51:33 UTC | BLOCKED | HOOK | Credential transmission detected | full-gate | BLOCKED | — | hook | Command reads secrets and transmits them externally. This violates NEVER rule 1. |
| 2026-03-17 16:51:33 UTC | BLOCKED | HOOK | Credential transmission detected | full-gate | BLOCKED | — | hook | Command reads secrets and transmits them externally. This violates NEVER rule 1. |
| 2026-03-17 16:51:33 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Bash command writes to guardrails path. NEVER rule 3. |
| 2026-03-17 16:51:33 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Bash command writes to guardrails path. NEVER rule 3. |
| 2026-03-17 16:51:33 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Cannot modify guardrails skill file: ACTIONS.md. NEVER rule 3. |
| 2026-03-17 16:51:33 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Cannot modify guardrails skill file: TIERS.md. NEVER rule 3. |
| 2026-03-17 16:51:33 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Cannot modify guardrails skill file: ACTIONS.md. NEVER rule 3. |
| 2026-03-17 16:51:33 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Cannot modify guardrails skill file: GUIDE.md. NEVER rule 3. |
| 2026-03-17 16:51:34 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Cannot modify guardrails skill file: TIERS.md. NEVER rule 3. |
| 2026-03-17 17:22:05 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Bash command writes to guardrails path. NEVER rule 3. |
| 2026-03-17 17:22:05 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Bash command writes to guardrails path. NEVER rule 3. |
| 2026-03-17 17:22:05 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Bash command writes to guardrails path. NEVER rule 3. |
| 2026-03-17 17:22:05 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Bash command writes to guardrails path. NEVER rule 3. |
| 2026-03-17 17:22:05 UTC | BLOCKED | HOOK | Credential transmission detected | full-gate | BLOCKED | — | hook | Command reads secrets and transmits them externally. This violates NEVER rule 1. |
| 2026-03-17 17:22:05 UTC | BLOCKED | HOOK | Credential transmission detected | full-gate | BLOCKED | — | hook | Command reads secrets and transmits them externally. This violates NEVER rule 1. |
| 2026-03-17 17:22:05 UTC | BLOCKED | HOOK | Credential transmission detected | full-gate | BLOCKED | — | hook | Command reads secrets and transmits them externally. This violates NEVER rule 1. |
| 2026-03-17 17:22:05 UTC | BLOCKED | HOOK | Credential in file write detected | full-gate | BLOCKED | — | hook | Content appears to contain secrets/credentials being written to /home/user/project/config.py. |
| 2026-03-17 17:22:05 UTC | BLOCKED | HOOK | Credential in file write detected | full-gate | BLOCKED | — | hook | Content appears to contain secrets/credentials being written to /home/user/project/deploy.py. |
| 2026-03-17 17:22:05 UTC | BLOCKED | HOOK | Catastrophic system command detected | full-gate | BLOCKED | — | hook | Command could cause irreversible system damage. |
| 2026-03-17 17:22:05 UTC | BLOCKED | HOOK | Catastrophic system command detected | full-gate | BLOCKED | — | hook | Command could cause irreversible system damage. |
| 2026-03-17 17:22:05 UTC | BLOCKED | HOOK | Catastrophic system command detected | full-gate | BLOCKED | — | hook | Command could cause irreversible system damage. |
| 2026-03-17 17:22:05 UTC | BLOCKED | HOOK | Catastrophic system command detected | full-gate | BLOCKED | — | hook | Command could cause irreversible system damage. |
| 2026-03-17 17:22:05 UTC | BLOCKED | HOOK | Obfuscated command detected | full-gate | BLOCKED | — | hook | Command contains encoded/obfuscated execution patterns. Decode and review before running. |
| 2026-03-17 17:22:05 UTC | BLOCKED | HOOK | Obfuscated command detected | full-gate | BLOCKED | — | hook | Command contains encoded/obfuscated execution patterns. Decode and review before running. |
| 2026-03-17 17:22:05 UTC | BLOCKED | HOOK | Obfuscated command detected | full-gate | BLOCKED | — | hook | Command contains encoded/obfuscated execution patterns. Decode and review before running. |
| 2026-03-17 17:22:05 UTC | BLOCKED | HOOK | Obfuscated command detected | full-gate | BLOCKED | — | hook | Command contains encoded/obfuscated execution patterns. Decode and review before running. |
| 2026-03-17 17:22:05 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Cannot modify guardrails skill file: SKILL.md. NEVER rule 3. |
| 2026-03-17 17:22:05 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Cannot modify guardrails skill file: POLICY.md. NEVER rule 3. |
| 2026-03-17 17:22:05 UTC | BLOCKED | HOOK | Credential in file write detected | full-gate | BLOCKED | — | hook | Content appears to contain secrets/credentials being written to /home/user/project/config.py. |
| 2026-03-17 17:22:06 UTC | BLOCKED | HOOK | Credential in file write detected | full-gate | BLOCKED | — | hook | Content appears to contain secrets/credentials being written to /home/user/project/.env.prod. |
| 2026-03-17 17:22:06 UTC | BLOCKED | HOOK | Credential in file write detected | full-gate | BLOCKED | — | hook | Content appears to contain secrets/credentials being written to /home/user/project/key.py. |
| 2026-03-17 17:22:06 UTC | BLOCKED | HOOK | Credential in file write detected | full-gate | BLOCKED | — | hook | Content appears to contain secrets/credentials being written to /home/user/project/deploy.py. |
| 2026-03-17 17:22:06 UTC | BLOCKED | HOOK | Credential in file write detected | full-gate | BLOCKED | — | hook | Content appears to contain secrets/credentials being written to /home/user/project/config.py. |
| 2026-03-17 17:22:06 UTC | BLOCKED | HOOK | Credential in file write detected | full-gate | BLOCKED | — | hook | Content appears to contain secrets/credentials being written to /home/user/project/config.json. |
| 2026-03-17 17:22:06 UTC | BLOCKED | HOOK | Obfuscated command detected | full-gate | BLOCKED | — | hook | Command contains encoded/obfuscated execution patterns. Decode and review before running. |
| 2026-03-17 17:22:06 UTC | BLOCKED | HOOK | Obfuscated command detected | full-gate | BLOCKED | — | hook | Command contains encoded/obfuscated execution patterns. Decode and review before running. |
| 2026-03-17 17:22:06 UTC | BLOCKED | HOOK | Obfuscated command detected | full-gate | BLOCKED | — | hook | Command contains encoded/obfuscated execution patterns. Decode and review before running. |
| 2026-03-17 17:22:06 UTC | BLOCKED | HOOK | Obfuscated command detected | full-gate | BLOCKED | — | hook | Command contains encoded/obfuscated execution patterns. Decode and review before running. |
| 2026-03-17 17:22:06 UTC | BLOCKED | HOOK | Obfuscated command detected | full-gate | BLOCKED | — | hook | Command contains encoded/obfuscated execution patterns. Decode and review before running. |
| 2026-03-17 17:22:06 UTC | BLOCKED | HOOK | Credential transmission detected | full-gate | BLOCKED | — | hook | Command reads secrets and transmits them externally. This violates NEVER rule 1. |
| 2026-03-17 17:22:06 UTC | BLOCKED | HOOK | Credential transmission detected | full-gate | BLOCKED | — | hook | Command reads secrets and transmits them externally. This violates NEVER rule 1. |
| 2026-03-17 17:22:06 UTC | BLOCKED | HOOK | Credential transmission detected | full-gate | BLOCKED | — | hook | Command reads secrets and transmits them externally. This violates NEVER rule 1. |
| 2026-03-17 17:22:06 UTC | BLOCKED | HOOK | Credential transmission detected | full-gate | BLOCKED | — | hook | Command reads secrets and transmits them externally. This violates NEVER rule 1. |
| 2026-03-17 17:22:06 UTC | BLOCKED | HOOK | Credential transmission detected | full-gate | BLOCKED | — | hook | Command reads secrets and transmits them externally. This violates NEVER rule 1. |
| 2026-03-17 17:22:06 UTC | BLOCKED | HOOK | Credential transmission detected | full-gate | BLOCKED | — | hook | Command reads secrets and transmits them externally. This violates NEVER rule 1. |
| 2026-03-17 17:22:06 UTC | BLOCKED | HOOK | Credential transmission detected | full-gate | BLOCKED | — | hook | Command reads secrets and transmits them externally. This violates NEVER rule 1. |
| 2026-03-17 17:22:06 UTC | BLOCKED | HOOK | Credential transmission detected | full-gate | BLOCKED | — | hook | Command reads secrets and transmits them externally. This violates NEVER rule 1. |
| 2026-03-17 17:22:07 UTC | BLOCKED | HOOK | Credential transmission detected | full-gate | BLOCKED | — | hook | Command reads secrets and transmits them externally. This violates NEVER rule 1. |
| 2026-03-17 17:22:07 UTC | BLOCKED | HOOK | Credential transmission detected | full-gate | BLOCKED | — | hook | Command reads secrets and transmits them externally. This violates NEVER rule 1. |
| 2026-03-17 17:22:07 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Bash command writes to guardrails path. NEVER rule 3. |
| 2026-03-17 17:22:07 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Bash command writes to guardrails path. NEVER rule 3. |
| 2026-03-17 17:22:07 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Cannot modify guardrails skill file: ACTIONS.md. NEVER rule 3. |
| 2026-03-17 17:22:07 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Cannot modify guardrails skill file: TIERS.md. NEVER rule 3. |
| 2026-03-17 17:22:07 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Cannot modify guardrails skill file: ACTIONS.md. NEVER rule 3. |
| 2026-03-17 17:22:07 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Cannot modify guardrails skill file: GUIDE.md. NEVER rule 3. |
| 2026-03-17 17:22:07 UTC | BLOCKED | HOOK | Guardrails self-modification blocked | full-gate | BLOCKED | — | hook | Cannot modify guardrails skill file: TIERS.md. NEVER rule 3. |
