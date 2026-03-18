---
name: guardrails
description: "Show guardrails status, switch modes, or view the audit log. Usage: /guardrails [status|log|strict|relaxed|audit|reset|policy]"
---

Show the current guardrails status and provide mode controls.

## Mode config file

Modes are persisted to `guardrails-mode.json` in the project root (`CLAUDE_PROJECT_DIR`). Read this file at the start of any command to determine the current mode. Write to it when mode changes. This file survives context resets and new sessions.

Schema:
```json
{
  "mode": "full-gate",
  "audit_only": false,
  "set_at": "<ISO 8601 timestamp>",
  "set_by": "user"
}
```

Valid `mode` values: `"full-gate"` (default), `"strict"`, `"relaxed"`.
`audit_only: true` overrides tier controls — T2/T3 auto-proceed with logging, T4 halts without executing.

## Commands

If the user typed `/guardrails` with no argument or `/guardrails status`:
- Read `guardrails-mode.json` (if it exists) to get persisted mode; otherwise assume full-gate
- Show the current guardrails mode (full-gate, strict, relaxed, audit-only)
- Show tier distribution for this session (how many T2, T3, T4 actions gated)
- Show approval/denial counts
- Show whether any pre-approved patterns are active

If the user typed `/guardrails log`:
- Read and display the last 20 entries from `guardrails_log.md` in the project root
- If no log exists, say "No guardrails log found. The log is created on the first gated action."

If the user typed `/guardrails strict`:
- Write `{"mode": "strict", "audit_only": false, "set_at": "<now ISO 8601>", "set_by": "user"}` to `guardrails-mode.json` in the project root
- Confirm: "🛡️ Strict mode saved. All tiers escalated by +1. Persists across sessions until changed."

If the user typed `/guardrails relaxed`:
- Write `{"mode": "relaxed", "audit_only": false, "set_at": "<now ISO 8601>", "set_by": "user"}` to `guardrails-mode.json` in the project root
- Confirm: "🛡️ Relaxed mode saved. Tier 2 actions will skip the gate. Persists across sessions until changed."

If the user typed `/guardrails audit`:
- Write `{"mode": "full-gate", "audit_only": true, "set_at": "<now ISO 8601>", "set_by": "user"}` to `guardrails-mode.json` in the project root
- Confirm: "🛡️ Audit-only mode saved. T2/T3 actions auto-proceed and are logged. T4 actions are halted. Use this for CI or unattended runs."

If the user typed `/guardrails reset`:
- Write `{"mode": "full-gate", "audit_only": false, "set_at": "<now ISO 8601>", "set_by": "user"}` to `guardrails-mode.json` in the project root
- Confirm: "🛡️ Guardrails reset to full-gate mode."

If the user typed `/guardrails policy`:
- Read and display the hard constraints from POLICY.md in the skill directory
