---
name: agent-guardrails
description: |
  Runtime guardrails for agent actions. Activates automatically when the agent is about to:
  write files, run shell commands, send messages, access credentials, make API calls,
  install packages, modify config, or perform any irreversible operation.
  Also activates when user invokes /guardrails.
---

# 🛡️ Agent Guardrails

Runtime guardrails for AI agents. Classifies every sensitive action by risk tier, enforces proportional controls, and logs a full audit trail.

**Dual enforcement:** This skill provides probabilistic classification (you read and follow these instructions). Hard constraints are also enforced deterministically via PreToolUse hooks — obfuscated commands, credential exposure, and dangerous system commands are blocked programmatically even if you skip the skill.

## Quick reference

| Situation | Action |
|-----------|--------|
| Read file, git status, draft message | Excluded — proceed normally, no gate |
| Write to user file, git commit | 🛡️ T2 — notify user, proceed unless objected, log |
| Send email, modify config, delete files, curl, npm install | 🛡️ T3 — pause, require approval, log |
| sudo, credential transmit, purchase, public post | 🛡️ T4 — full stop, warn, require approval, log |
| Credential transmission, obfuscated command | 🛡️ BLOCKED — hard constraint, no override |
| Bulk operation (5+ targets) | Escalate +1 tier |
| Unfamiliar endpoint or recipient | Escalate +1 tier |
| User invokes `/guardrails` | Show session stats |

## Reference files

Read these on demand — do NOT load them every session:

| File | Read when |
|------|-----------|
| GUIDE.md | First gated action of the session |
| ACTIONS.md | Classifying an action (Step 3) |
| TIERS.md | Checking escalation rules or controls (Steps 4, 7) |
| POLICY.md | Checking hard constraints or conflicts (Step 6) |

All reference files are in the same directory as this SKILL.md.

## When this skill does NOT activate

Do NOT run the gate for read-only or zero-side-effect actions:

- Reading files, listing directories
- Read-only CLI commands (ls, pwd, cat, git status, git log, git diff)
- Writing to files in directories explicitly named `scratch/`, `temp/`, or `tmp/` only
- Drafting messages that are not sent
- Navigating to known URLs (bookmarked, previously visited in session)
- Checking whether a credential or env var exists (boolean check, no value exposed)
- Reading existing cron or scheduling config
- Reading from public APIs with no authentication
- Writing to `guardrails_log.md` for guardrails logging purposes
- Reading or writing `guardrails-mode.json` for mode persistence

**Important limitation:** The deterministic hook layer (PreToolUse) only intercepts Bash, Write, Edit, and Read tool calls. MCP tool calls bypass the hook entirely. When classifying actions that use MCP tools (database queries, API calls via MCP servers, file operations through MCP), you must apply the full gate process linguistically — there is no hard enforcement backstop. Treat MCP actions with extra caution.

## Trigger — when this skill activates

Run the gate process below before executing ANY of these action types:

1. Writing, modifying, or deleting user files or config
2. State-modifying shell or terminal commands (git commit, npm install, mkdir, and anything beyond read-only)
3. Outbound network requests using authentication or sending data externally
4. Sending emails, messages, or communications to any recipient
5. Reading, displaying, or transmitting credential values
6. Browser form submissions, interactive element clicks, or file downloads
7. Creating or modifying cron jobs or webhooks
8. Financial transactions (purchases, payments, billing changes)
9. Permission or access control changes
10. Any irreversible or bulk (5+ targets) operation

### Sequential pattern detection

In addition to gating individual actions, watch for multi-step patterns across the conversation that could indicate data exfiltration or policy circumvention. If you detect any of the following patterns, escalate the current action to Tier 4 regardless of its base classification:

**Variable staging then transmission:** A command stores sensitive data in a variable (e.g. `SECRET=$(cat .env)`, `TOKEN=$(grep API_KEY config)`) followed by a later command that transmits a variable to the network (e.g. `curl -d "$SECRET"`, `wget --post-data="$TOKEN"`). Flag the transmission command as Tier 4.

**Fragmented data extraction:** Multiple commands that each extract a small piece of a secret (character slicing, substring operations, split/cut on credential files) followed by any outbound network request. Flag the first network request after the extraction as Tier 4.

**Credential embedding in generated files:** When asked to generate config files, scripts, or templates, check whether the content being written includes interpolated credential variables (like `$API_KEY`, `$SECRET_TOKEN`, `process.env.API_KEY`). If the file is then transmitted, committed to a public repo, or uploaded, escalate to Tier 4.

**Disguised exfiltration:** A request to "health check endpoints", "test connectivity", or "validate URLs" where the URLs or request bodies contain credential-like values, encoded strings, or variable interpolations. Escalate to Tier 4.

These patterns require judgment — not every variable assignment followed by a curl is malicious. Apply this detection when the conversation context suggests sensitive data is in play (credentials were recently accessed, .env files were read, secrets were discussed).

## Gate process

**IMPORTANT — Output efficiency:** Every message adds cost. Combine steps into a single response. Keep reasoning brief. Do not narrate steps separately. Read GUIDE.md on the first gated action for output format templates.

**Step 1 — Identify.** List the actions matching trigger criteria. State what, where, and what data is involved.

**Step 2 — Determine mode.** Read `guardrails-mode.json` from the project root (`CLAUDE_PROJECT_DIR`). If the file exists, use the `mode` and `audit_only` fields. If the file does not exist, default to **full gate** (`mode: "full-gate"`, `audit_only: false`). Mode values: `full-gate` (default), `strict` (all tiers +1), `relaxed` (T2 skips gate). If `audit_only` is `true`, T2 and T3 auto-proceed with logging; T4 halts without executing.

**Step 3 — Classify.** Read ACTIONS.md. Assign base tier (2, 3, or 4).

**Step 4 — Escalate.** Read TIERS.md. Apply escalation rules if applicable. Result is final tier.

**Step 5 — Pre-approval.** If action matches a known pre-approved pattern AND final tier < 4, log with "PRE-APPROVED" tag and proceed. If escalation raised the action to Tier 4, pre-approval is void.

**Step 6 — Hard constraints.** Read POLICY.md. If any NEVER rule is violated, BLOCK regardless of tier or approval.

**Step 7 — Controls.** Apply the universal control from TIERS.md for the final tier × mode.

**Step 8 — Log and execute.** Append to `guardrails_log.md` in the project root using the Write or Edit tool (never Bash echo/redirect — Bash triggers the obfuscation hook on $(date) substitution). Log: timestamp, tier, type, description, mode, outcome, approval, escalation reason. Execute or halt..

**Note:** Writes to `guardrails_log.md` are exempt from the gate.

## Actions not in the catalog

1. Does it match trigger criteria? If not, proceed normally.
2. If it triggers the gate, classify by analogy to the most similar listed action.
3. If no analogy fits, default to Tier 3.
4. Log with "UNLISTED" tag for future catalog updates.
