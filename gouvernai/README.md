# 🛡️ GouvernAI — Claude Code Plugin

![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Tests](https://img.shields.io/badge/tests-85%20passing-brightgreen)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Claude Code](https://img.shields.io/badge/Claude%20Code-plugin-blueviolet)
![Zero Dependencies](https://img.shields.io/badge/dependencies-zero-brightgreen)

> Permissive where risk is low. Conservative where it matters. Invisible everywhere else.

Runtime guardrails that preserve your flow state — reads, drafts, and routine writes flow through with zero friction. Guardrails only activate when actions carry real risk: credential transmission, bulk deletions, unfamiliar endpoints, scope expansion.

Dual enforcement: Skill layer (proportional risk classification by Claude) + deterministic hooks (hard constraint blocking via PreToolUse scripts). The hooks physically block obfuscated commands, credential transmission, and catastrophic system commands — even if Claude skips the skill. Some bypass patterns exist (see Threat Model). > 

## Install

```bash
# Add the marketplace first
claude plugin marketplace add Myr-Aya/GouvernAI-claude-code-plugin

# Then install the plugin
claude plugin install gouvernai@mindxo
```
## Usage

**Claude Code Terminal:** Guardrails activate automatically. No action needed.

**Claude Code Desktop:** Run `/gouvernai:guardrails` at the start of your session to activate the gate. The skill may not auto-trigger reliably in these environments.

## Quick test

Try these after installing to see the guardrails in action:

1. **Allowed:** `git status` — Tier 1, excluded from gate, no overhead
2. **Gated:** Ask Claude to write a file — Tier 2 notification appears
3. **Blocked:** Ask Claude to run `echo aGVsbG8= | base64 -d | bash` — hook blocks with exit code 2

## What you'll see

Most of the time, you won't notice GouvernAI is running. ~60% of typical agent actions are reads, drafts, and navigation — all excluded from the gate. Zero overhead, zero prompts, zero friction. When risk is real, GouvernAI steps in proportionally:

| Risk | Actions | Your experience |
|------|---------|-----------------|
| **T1** | reads, drafts, git status | Invisible. Flow state preserved. |
| **T2** | file writes, git commit | Brief notification, keeps going. |
| **T3** | npm install, curl, email, config | Pauses for approval — only when consequences are real. |
| **T4** | sudo, credential transmit, bulk delete | Full stop with risk assessment — because it should. |
| **BLOCKED** | obfuscated commands, credential exfil | Hard block. No override. Even if Claude skips the skill. |

## Screenshots

### `/guardrails` — Session status
![Session status](assets/screenshots/guardrails-status.png)

### Tier 2 — Notify and proceed
File write in the workspace. GouvernAI notifies and proceeds unless you object.

![T2 notification](assets/screenshots/t2-notify.png)

### Tier 3 — Pause for approval
Package installation requires explicit approval before executing.

![T3 npm install](assets/screenshots/t3-npm-install.png)

### Tier 4 — Full stop (bulk delete with escalation)
Bulk file deletion: base tier T3 escalated to T4 for 9 targets. Lists every file and asks for confirmation.

![T4 bulk delete](assets/screenshots/t4-bulk-delete.png)

### Tier 4 — Full stop (email with escalation)
Outbound email to unfamiliar recipient: base tier T3 escalated to T4. Shows the escalation chain.

![T4 email halt](assets/screenshots/t4-email-halt.png)

### BLOCKED — Obfuscated command (hard constraint)
Base64-to-bash pipe detected and blocked. No override possible.

![Blocked obfuscated](assets/screenshots/blocked-obfuscated.png)

### BLOCKED — Self-modification attempt (hard constraint)
Attempt to edit SKILL.md to remove the gate. Blocked with explanation and alternatives.

![Blocked self-modification](assets/screenshots/blocked-self-modification.png)

### BLOCKED — Credential hardcoded in file
API key detected in file write. Shows the key, explains the risk, suggests alternatives.

![Blocked credential](assets/screenshots/blocked-credential-in-file.png)

### Relaxed mode — T2 skips the gate
In relaxed mode, T2 actions proceed with no gate. T3 and T4 still require approval.

![Relaxed mode](assets/screenshots/mode-relaxed.png)
![T2 relaxed skip](assets/screenshots/t2-relaxed-skip.png)

### Audit log
Full session audit trail showing every gated action with tier, outcome, and escalation reason.

![Audit log](assets/screenshots/audit-log.png)

## Complements Claude Code's auto mode

PreToolUse hooks run *before* the auto mode classifier — GouvernAI acts as a first pass. What it adds on top:

| Auto mode | GouvernAI |
|-----------|-----------|
| Binary allow/block | 4-tier proportional controls |
| Opaque classifier | Transparent, editable policy files you own |
| No audit trail | Append-only log with tier, escalation, outcome |
| No configurable modes | strict / relaxed / audit-only, persistent across sessions |
| No escalation rules | Unfamiliar targets, bulk ops, scope expansion, chained actions |

## Slash commands

| Command | What it does |
|---------|-------------|
| `/guardrails` | Show current mode, tier distribution, approvals/denials |
| `/guardrails log` | Display recent audit log entries |
| `/guardrails strict` | All tiers +1 — persisted to `guardrails-mode.json` |
| `/guardrails relaxed` | Tier 2 skips gate — persisted to `guardrails-mode.json` |
| `/guardrails audit` | Audit-only mode: T2/T3 auto-proceed, T4 halts (for CI/unattended) |
| `/guardrails reset` | Return to default full-gate mode |
| `/guardrails policy` | Display hard constraints |

Mode changes are written to `guardrails-mode.json` in the project root and **persist across sessions and context resets**. Previously, mode was held only in the model's context window and was silently lost on reset.

## CI and unattended use

In full-gate mode, Tier 2 actions use "proceed unless objected" — which is silent auto-approval when no human is watching. For scheduled tasks, CI pipelines, or any unattended run, set audit-only mode first:

```bash
/guardrails audit
```

In audit-only mode: T2 and T3 auto-proceed with full logging, T4 halts without executing. Hard constraints still block regardless of mode.

## How it works

### Skill layer (probabilistic)

The SKILL.md file teaches Claude the 8-step gate process: identify, determine mode, classify (using ACTIONS.md), escalate (using TIERS.md), check pre-approval, check hard constraints (using POLICY.md), apply controls, log and execute. Claude reads and follows these instructions with judgment.

### Hook layer (deterministic)

The PreToolUse hook (`scripts/guardrails-enforce.py`) runs on every Bash, Write, and Edit tool call. It checks for:

- **Obfuscated commands** — base64 decoding piped to bash, eval with encoded strings, hex-encoded commands
- **Credential transmission** — reading .env/secrets and piping to curl/wget/netcat
- **Catastrophic commands** — rm -rf /, fork bombs, dd to disk devices
- **Credential in file writes** — API keys, private keys, AWS access keys in committed files
- **Self-modification** — any attempt to edit the guardrails skill files

If a violation is detected, the hook exits with code 2 (hard block). Claude cannot override this.

### Why both?

Skills are probabilistic — Claude uses judgment about when to apply them. On complex tasks, it might skip classification. Hooks are deterministic — they run every time, no exceptions. The skill handles the nuanced risk classification (is this a Tier 2 or Tier 3?). The hooks enforce the non-negotiable rules (never transmit credentials, never run obfuscated commands).

## Plugin structure

```
gouvernai/
├── .claude-plugin/
│   └── plugin.json              # Plugin metadata
├── skills/
│   └── gouvernai/
│       ├── SKILL.md             # Gate orchestrator (always loaded)
│       ├── ACTIONS.md           # Action → tier classification lookup
│       ├── TIERS.md             # Universal controls + escalation rules
│       ├── POLICY.md            # Hard constraints (NEVER rules)
│       └── GUIDE.md             # Output format templates
├── commands/
│   └── guardrails.md            # /guardrails slash command
├── hooks/
│   └── hooks.json               # PreToolUse hook configuration
├── scripts/
│   └── guardrails-enforce.py    # Deterministic enforcement script
├── tests/
│   └── test_guardrails_enforce.py  # Hook unit tests
└── README.md                    # This file
```

Runtime files written to the project root during use:
- `guardrails_log.md` — append-only audit log
- `guardrails-mode.json` — persisted mode config (created on first `/guardrails` mode command)

## Environment variables

| Variable | Set by | Purpose |
|----------|--------|---------|
| `CLAUDE_PLUGIN_ROOT` | Claude Code | Absolute path to the installed plugin directory. Used by `hooks.json` to locate `guardrails-enforce.py`. |
| `CLAUDE_PROJECT_DIR` | Claude Code | Absolute path to the current project. Used by the hook and skill to locate `guardrails_log.md` and `guardrails-mode.json`. |

**If `CLAUDE_PLUGIN_ROOT` is not set** (e.g. when running the hook script manually or in tests), the script falls back to its own parent directory (`scripts/../` = plugin root). No action required — the fallback is automatic.

## Security

**Important:** This plugin installs hooks that run on every tool call. Review the source code before installing. The enforcement script (`scripts/guardrails-enforce.py`) is transparent and auditable.

In February 2026, Check Point Research disclosed CVEs allowing RCE through Claude Code hooks in untrusted repos. This plugin should be installed at user scope (default), not project scope, unless you trust all contributors to the project.

```bash
# Add the marketplace first
claude plugin marketplace add Myr-Aya/GouvernAI-claude-code-plugin

# User scope (default, recommended)
claude plugin install gouvernai@mindxo

# Project scope (only if you trust all contributors)
claude plugin install gouvernai@mindxo --scope project
```

## Limitations

- **Hooks cannot intercept MCP tool calls.** If Claude uses MCP servers to execute actions, the PreToolUse hook does not fire. The skill layer still applies (Claude reads SKILL.md and classifies MCP actions), but there is no deterministic enforcement.
- **Skill compliance varies by model.** Tested informally on Claude Sonnet 4.6 (9/10 correct in Scenario A, 1 known low-risk issue accepted). Smaller models (Haiku) may have lower compliance rates.
- **Hooks add ~10ms per tool call.** The Python script is lightweight, but it runs on every Bash/Write/Edit call.
- **Hook patterns target Unix/Bash syntax.** PowerShell equivalents (e.g. `Get-Content`, `Invoke-WebRequest`, `Remove-Item`) are not covered. Claude Code uses Bash on all platforms, so this is low risk for typical usage.

## Threat model and limitations

GouvernAI is an operational safety and governance layer, not a security boundary. In the defense-in-depth model described by the [2026 International AI Safety Report](https://internationalaisafetyreport.org/publication/2026-report-extended-summary-policymakers), it sits at the runtime layer — gating agent actions before execution through a combination of linguistic classification and pattern-based blocking.

Its real value is:
- Catching accidental destructive actions before they happen
- Forcing a consistent approval and logging workflow across sessions
- Providing an auditable policy scaffold for teams
- Reducing variance between "careful" and "careless" agent sessions

It does not protect against sophisticated, determined adversaries. Regex-plus-prompt guardrails are effective at stopping mistakes, not targeted attacks.

**What it catches:**
- Single-command credential exfiltration (cat .env | curl)
- Obfuscated command execution (base64 -d | bash)
- Accidental writes to guardrails files
- Catastrophic commands (rm -rf /, fork bombs)
- Unintentional scope expansion (escalation rules)
- Credential exposure in file writes (API keys in committed files)

**What it does NOT catch:**
- Multi-step exfiltration where credentials are staged in variables across separate commands
- Fragmented data extraction (extracting one character at a time)
- Credential embedding in generated files that are later transmitted
- Exfiltration disguised as legitimate work (health checks, config generation)
- Attacks routed through MCP tools (hook layer bypassed entirely)
- Novel obfuscation techniques not covered by current regex patterns
- Prompt injection that convinces the model to ignore the skill layer

**Defense in depth:** GouvernAI is one layer in a multi-layer safety stack. For production or high-security environments, complement it with:
- **Network egress policies** — restrict which external endpoints the agent can reach
- **Secret vaults** — never expose raw credential values to the agent; use short-lived tokens
- **Sandboxed execution** — run agent actions in isolated environments with limited blast radius
- **DLP monitoring** — detect and alert on sensitive data leaving the environment
- **Audit and incident response** — GouvernAI's log provides the audit trail; pair it with alerting and review processes

No single layer is sufficient. The 2026 International AI Safety Report's Swiss cheese model applies: each layer has holes, but layered together they provide meaningful protection.

## Uninstallation

To uninstall: `claude plugin uninstall gouvernai@mindxo` or go to Browse plugins → Personal → select the plugin → Uninstall.

## License

MIT — see [LICENSE](LICENSE)

**Website:** [gouvernai.ai](https://gouvernai.ai)

## Built by Myr-Aya, MindXO
