# Agent Guardrails — Output Guide

Read this file on the first gated action of the session. Follow these output templates for all subsequent gated actions.

## Output format per tier

Minimize messages. Combine classification, presentation, and action into the fewest messages possible.

**Tier 2 (full gate) — auto-approved with notification:**
> 🛡️ **T2 — [action type]**: [brief description]. Auto-approved — proceeding unless you object.
Then execute immediately in the same response. Log.

**Tier 3 (full gate) — requires approval, then wait:**
> 🛡️ **T3 — [action type]**: [what, where, what data]. Approve? (yes/no)
Wait for response. Then execute or deny in one message. Log.

**Tier 4 (full gate) — requires approval after risk assessment:**
> 🛡️ **T4 — [action type]**: [what action, what's at risk, is it reversible?]. Approve? (yes/no/details)
If user says "details" or asks for more info, then provide full impact assessment. Otherwise wait for yes/no. Then execute or deny in one message. Log.

**Hard constraint violation — one message:**
> 🛡️ **BLOCKED — [constraint name]**: [what was attempted, which rule prevents it].
Log.

Do NOT split classification and presentation into separate messages. Do NOT narrate the gate steps ("Step 1, I will identify... Step 2, I will classify..."). Run the steps internally, then present the result in the format above.

**CRITICAL — After logging:** Do NOT read back, cat, display, or echo the log file after writing to it. Do NOT show the last N entries. Do NOT include log contents in your response. The log write is completely silent — proceed with the action or halt immediately. The user sees log entries ONLY when they run `/guardrails log`. This rule has no exceptions.

**Token cap exceeded — one message, then wait:**
> 🛡️ **T3 — Token cap**: Estimated ~[N] tokens (cap: [cap]). [what action, what will be written/executed]. Approve? (yes/no)
Wait for response. Then execute or deny in one message. Log with "TOKEN-CAP" tag.

## Self-improvement

When you encounter any of the following, append a note to `guardrails_log.md` with a "SUGGESTION" tag:

- An action that triggers the gate but has no good match in the catalog — suggest adding it with a proposed tier.
- An action where the tier classification feels wrong (too high or too low for the actual risk) — suggest a reclassification with reasoning.
- A pattern of repeated user approvals for the same action type — suggest pre-approval.
- A pattern of repeated user denials for an action type — suggest escalating its base tier.
- A gap in the trigger criteria or exclusion list — suggest an update.

These suggestions are logged, not acted on. The user or administrator reviews them and decides whether to update the skill files.
