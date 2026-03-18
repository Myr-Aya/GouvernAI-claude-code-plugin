# 🛡️ GouvernAI — Claude Code Plugin

Runtime guardrails for AI agents. Classifies every sensitive action by risk tier, enforces proportional controls, and logs a full audit trail. For teams using Claude Code with higher-risk workflows, CI pipelines, or approval requirements.

GouvernAI is an **operational safety and governance layer** — designed to catch mistakes, enforce consistent approval workflows, and create accountability through audit logging. It is one layer in a [defense-in-depth](https://internationalaisafetyreport.org/publication/2026-report-extended-summary-policymakers) approach to AI agent risk management, as recommended by the 2026 International AI Safety Report: multiple layers of safeguards compensating for weaknesses in any single control.

**Dual enforcement:** Linguistic skill (probabilistic risk classification by Claude) + deterministic hooks (pattern-based blocking via PreToolUse scripts). The hooks block common obfuscated commands, credential transmission patterns, and catastrophic system commands — even if Claude skips the skill. Some bypass patterns exist (see Threat Model). > 

**Note:** The hook layer covers common patterns, not all possible bypass techniques. See the Threat Model section for documented gaps.

## Install

```bash
# Add the marketplace first
claude plugin marketplace add Myr-Aya/GouvernAI-claude-code-plugin

# Then install the plugin
claude plugin install gouvernai@mindxo
```

After install, guardrails activate automatically on the next session. No configuration required.

## Usage

**Claude Code Terminal:** Guardrails activate automatically. No action needed.

**Claude Desktop / Cowork:** Run `/gouvernai:guardrails` at the start of your session to activate the gate. The skill may not auto-trigger reliably in these environments.

## Quick test

Try these after installing to see the guardrails in action:

1. **Allowed:** `git status` — Tier 1, excluded from gate, no overhead
2. **Gated:** Ask Claude to write a file — Tier 2 notification appears
3. **Blocked:** Ask Claude to run `echo aGVsbG8= | base64 -d | bash` — hook blocks with exit code 2

## What you'll see

- **Tier 1** (reads, drafts, known URLs) — invisible, zero overhead
- **Tier 2** (file writes, git commit) — 🛡️ notification, proceeds automatically
- **Tier 3** (email, config changes, npm install, curl) — 🛡️ pauses for your approval
- **Tier 4** (sudo, credential transmit, purchases) — 🛡️ full stop with risk assessment
- **BLOCKED** (obfuscated commands, credential exfiltration) — hard block, no override

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

## License

MIT — see [LICENSE](LICENSE)

## Built by Myr-Aya, MindXO

[mind-xo.com](https://mind-xo.com)
