# Agent Guardrails — Risk Tiers and Controls

## Universal control table

Controls depend only on the final tier and the guardrails mode. They are the same for every action at that tier.

### Tier 1 — Routine (Green)

Not applicable. Tier 1 actions are excluded from the gate and do not trigger the gate process.

### Tier 2 — Standard (Amber)

Modifies persistent local state or involves authenticated external reads.

**Full gate:** Notify the user (briefly state the action and its tier classification). Proceed unless the user objects. Log.

**Audit-only:** Auto-proceed. Log with action detail.

### Tier 3 — Elevated (Red)

Involves outbound data transmission, communication on behalf of the user, credential handling, or modifications to systems outside the local workspace.

**Full gate:** Pause. Present the action, its scope, and what data is involved. Wait for explicit user approval. If denied, log denial and stop.

**Audit-only:** Auto-proceed. Alert the user with full details of the action taken. Log.

### Tier 4 — Critical (Black)

Irreversible actions with significant consequences. Financial impact, bulk destruction, permission changes, public-facing effects, or attack surface modifications.

**Full gate:** Full stop. Warn the user concisely: state the action, what is at risk, and whether it is reversible. Ask for approval. If the user requests details, provide a full impact assessment (what will happen, what cannot be undone, blast radius). If the user gives explicit approval, execute and log. If denied or ambiguous, log denial and stop.

**Audit-only:** HALT. Do NOT execute. Alert the user immediately with full details of the attempted action. Log with "HALTED" status.

## Escalation rules

Escalate an action by one tier (e.g. Tier 2 becomes Tier 3) when ANY of these conditions apply:

- **Unfamiliar target:** Any system, endpoint, file path, domain, or recipient not previously accessed or referenced in this session. Use this decision tree:

  1. **Email/messaging recipient** — seen this session? If no → unfamiliar. If yes → familiar.
  2. **Domain** (e.g. `api.example.com`) — seen this session in any command? If no → unfamiliar. If yes → go to step 3.
  3. **Endpoint path** (e.g. `/users` vs `/orders`) — exact path called this session? If no → unfamiliar. If yes → familiar. Note: same domain with a new path = unfamiliar endpoint.
  4. **API versioning** (e.g. `v1` vs `v2` of same domain) — treat different versions as different endpoints → unfamiliar unless that exact version was called this session.
  5. **File path** — within the current working directory tree and read/written this session? If no → unfamiliar.
  6. **Subdomains** — `api.example.com` and `admin.example.com` are different targets → treat each subdomain independently.

  If in doubt after applying the decision tree, treat as unfamiliar and escalate.
- **Third-party data:** the action involves data belonging to someone other than the current user.
- **Scope expansion:** the agent plans to do more than the user explicitly requested (e.g. user asked to edit one file, agent plans to edit three).
- **Bulk operation:** the action affects 5 or more files, records, or targets.
- **Chained actions (3+ sequential):** If you have already committed to executing 2 or more gated actions (Tier 2+) in the current response — all fulfilling a single user request — escalate the next gated action by +1 tier. "Committed to executing" means the action has been classified, approved (or auto-proceeded at T2), and is queued or already executed in this turn. A new user message resets the chain count. To track this: before classifying the current action, count the gated actions you have already decided to execute in this turn. If that count is 2 or more, escalate. Denied actions do not count toward the chain.
- **Destination change:** the action targets a different recipient, endpoint, folder, or publication surface than what the user explicitly indicated or from prior session context.

Tier 4 is the maximum — no further escalation. Apply the Tier 4 control.

## De-escalation

- **Relaxed mode** (`/guardrails relaxed`): Tier 2 actions skip the gate entirely (treated as Tier 1). Tier 3 and 4 are never de-escalated.
- **Pre-approved patterns**: matching actions skip approval and alerting, but still undergo classification, escalation, and hard-constraint checks. Log with the tier and a "PRE-APPROVED" tag. If escalation raises the action to Tier 4, pre-approval is void.
- De-escalation never applies to Tier 4 actions. Tier 4 controls are absolute.

## Audit-only mode (CI / unattended runs)

Set via `/guardrails audit` or by writing `"audit_only": true` to `guardrails-mode.json`.

**Why this exists:** In full-gate mode, Tier 2 uses "proceed unless objected" — this is safe when a human is watching but becomes unconditional auto-approval in a CI pipeline or unattended session where no one can object. Audit-only mode makes this explicit and consistent across all tiers below T4.

| Tier | Audit-only behaviour |
|------|----------------------|
| T1 | Excluded as normal |
| T2 | Auto-proceed. Log with full action detail. |
| T3 | Auto-proceed. Alert the user with full details of the action taken. Log. |
| T4 | **HALT.** Do NOT execute. Log with "HALTED" status. Alert immediately. |

Hard constraints (POLICY.md NEVER rules) still apply in audit-only mode. The hook layer is unaffected.
