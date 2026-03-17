# 🛡️ Agent Guardrails — Claude Code Plugin

Runtime guardrails for AI agents. Classifies every sensitive action by risk tier, enforces proportional controls, blocks dangerous actions with hard constraints, and logs a full audit trail.

**Dual enforcement:** Linguistic skill (probabilistic classification by Claude) + deterministic hooks (hard constraint blocking via PreToolUse scripts). The hooks physically block obfuscated commands, credential transmission, and catastrophic system commands — even if Claude skips the skill.

## Install

```bash
# From GitHub
/plugin install github.com/myr-aya/gouvernai-claude-code-plugin

# Or clone and install locally
git clone https://github.com/myr-aya/gouvernai-claude-code-plugin.git
/plugin install ./gouvernai-claude-code-plugin
```

After install, guardrails activate automatically on the next session. No configuration required.

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
agent-guardrails/
├── .claude-plugin/
│   └── plugin.json              # Plugin metadata
├── skills/
│   └── agent-guardrails/
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
# User scope (default, recommended)
/plugin install github.com/mindxo/agent-guardrails

# Project scope (only if you trust all contributors)
/plugin install github.com/mindxo/agent-guardrails --scope project
```

## Limitations

- **Hooks cannot intercept MCP tool calls.** If Claude uses MCP servers to execute actions, the PreToolUse hook does not fire. The skill layer still applies (Claude reads SKILL.md and classifies MCP actions), but there is no deterministic enforcement.
- **Skill compliance varies by model.** Tested on Claude Sonnet 4.6 (10/10 correct). Smaller models (Haiku) may have lower compliance rates.
- **Hooks add ~10ms per tool call.** The Python script is lightweight, but it runs on every Bash/Write/Edit call.

## Threat model and limitations

This plugin is a risk management tool, not a security boundary. It is designed to catch mistakes, obvious misuse, and common attack patterns. It does not protect against sophisticated, determined adversaries.

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

**Defense in depth:** For production or high-security environments, complement this plugin with infrastructure-level controls: network egress policies, secret vaults (never expose raw credential values to the agent), sandboxed execution environments, and DLP (data loss prevention) monitoring.

## License

MIT — see [LICENSE](LICENSE)

## Built by MindXO

[mind-xo.com](https://mind-xo.com)
