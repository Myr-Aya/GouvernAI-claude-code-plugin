---
name: guardrails
description: "Show guardrails status, switch modes, set token cap, or view the audit log. Usage: /guardrails [status|log|strict|relaxed|audit|reset|policy|tokencap]"
---

Show the current guardrails status and provide mode controls.

## Mode config file

Modes are persisted to `guardrails-mode.json` in the project root (`CLAUDE_PROJECT_DIR`). Read this file at the start of any command to determine the current mode. Write to it when mode changes. This file survives context resets and new sessions.

Schema:
```json
{
  "mode": "full-gate",
  "audit_only": false,
  "token_cap": null,
  "set_at": "<ISO 8601 timestamp>",
  "set_by": "user"
}
```

Valid `mode` values: `"full-gate"` (default), `"strict"`, `"relaxed"`.
`audit_only: true` overrides tier controls — T2/T3 auto-proceed with logging, T4 halts without executing.
`token_cap`: integer or null. When set to an integer, actions whose estimated payload exceeds this token count pause for approval (T3 gate). When null or absent, the token cap is inactive.

## Commands

If the user typed `/guardrails` with no argument or `/guardrails status`:
- Read `guardrails-mode.json` (if it exists) to get persisted mode; otherwise assume full-gate
- Show the current guardrails mode (full-gate, strict, relaxed, audit-only)
- Show tier distribution for this session (how many T2, T3, T4 actions gated)
- Show approval/denial counts
- Show whether any pre-approved patterns are active
- Show token cap setting: if token_cap is set in the config, show "Token cap: <N> tokens"; otherwise "Token cap: not set"

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

If the user typed `/guardrails tokencap <number>`:
- Read the existing `guardrails-mode.json` (if it exists) to preserve current mode and audit_only settings
- Add or update the `token_cap` field with the integer value
- Write the updated config to `guardrails-mode.json` in the project root
- Confirm: "🛡️ Token cap set to <number> tokens. Actions exceeding this will pause for approval. Persists across sessions until changed."

If the user typed `/guardrails tokencap off`:
- Read the existing `guardrails-mode.json` (if it exists) to preserve current mode settings
- Set `token_cap` to null
- Write the updated config to `guardrails-mode.json`
- Confirm: "🛡️ Token cap disabled."

If the user typed `/guardrails tokencap` (no argument):
- Read `guardrails-mode.json` and show the current token cap value
- If not set or null: "Token cap: not set (all actions proceed regardless of size)"
- If set: "Token cap: <number> tokens. Actions exceeding this pause for approval."
