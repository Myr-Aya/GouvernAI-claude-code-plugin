#!/usr/bin/env python3
"""
Agent Guardrails — PreToolUse Hook (Deterministic Enforcement)

Runs before every Bash, Write, and Edit tool call. Checks for hard constraint
violations that must be blocked programmatically, not just linguistically.

Exit codes:
  0 = allow (no violation detected)
  2 = block (hard constraint violated)

This hook enforces POLICY.md NEVER rules 1, 2, 6 deterministically.
Rules 3-8 are linguistic (enforced by the skill, not this hook).
"""

import json
import sys
import re
import os
from datetime import datetime, timezone

# Resolve plugin root: prefer the env var Claude Code sets; fall back to the
# parent of the directory this script lives in so the hook works even when
# CLAUDE_PLUGIN_ROOT is not set (e.g. during local testing).
PLUGIN_ROOT = os.environ.get(
    "CLAUDE_PLUGIN_ROOT",
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

def get_log_path():
    """Find the guardrails log in the project directory."""
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
    return os.path.join(project_dir, "guardrails_log.md")

def log_block(reason, detail):
    """Append a BLOCKED entry to the guardrails log."""
    try:
        log_path = get_log_path()
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        entry = f"| {ts} | BLOCKED | HOOK | {reason} | full-gate | BLOCKED | — | hook | {detail} |\n"
        with open(log_path, "a") as f:
            f.write(entry)
    except Exception:
        pass  # logging failure should not prevent the block

def block(reason, detail=""):
    """Output block message and exit with code 2."""
    log_block(reason, detail)
    output = {
        "hookSpecificOutput": {
            "permissionDecision": "deny"
        },
        "systemMessage": f"🛡️ BLOCKED by guardrails hook — {reason}: {detail}"
    }
    print(json.dumps(output))
    sys.exit(2)

def check_obfuscated_command(command):
    """NEVER rule 2: Never execute obfuscated commands."""
    patterns = [
        r'base64\s+(-d|--decode)',
        r'base64\s+-D',
        r'\|\s*bash',
        r'\|\s*sh\b',
        r'\|\s*zsh',
        r'\beval\s*\(',
        r'\beval\s+"',
        r"\beval\s+'",
        r'\beval\s+\$',
        r'\\x[0-9a-fA-F]{2}',
        r'%[0-9a-fA-F]{2}.*%[0-9a-fA-F]{2}.*%[0-9a-fA-F]{2}',
        r'printf\s+.*\\x',
        r'\$\(echo\s+.*\|.*base64',
        r'python[23]?\s+-c\s+["\'].*exec\(',
        r'ruby\s+-e\s+["\'].*eval\(',
        r'perl\s+-e\s+["\'].*eval\(',
    ]
    for pattern in patterns:
        if re.search(pattern, command, re.IGNORECASE):
            return True
    return False

def check_credential_exposure(command):
    """NEVER rule 1: Never transmit credentials externally."""
    # Detect commands that read secrets and pipe/redirect them externally
    secret_patterns = [
        r'cat\s+.*\.env',
        r'cat\s+.*\.pem',
        r'cat\s+.*id_rsa',
        r'cat\s+.*\.ssh/',
        r'echo\s+\$\w*(KEY|TOKEN|SECRET|PASSWORD|PASS|CRED)',
        r'printenv\s+\w*(KEY|TOKEN|SECRET|PASSWORD)',
    ]
    transmit_patterns = [
        r'\|\s*curl',
        r'\|\s*wget',
        r'\|\s*nc\b',
        r'\|\s*netcat',
        r'>\s*/dev/tcp/',
        r'\|\s*mail\b',
        r'\|\s*sendmail',
    ]
    has_secret = any(re.search(p, command, re.IGNORECASE) for p in secret_patterns)
    has_transmit = any(re.search(p, command, re.IGNORECASE) for p in transmit_patterns)
    if has_secret and has_transmit:
        return True
    # Direct curl/wget posting of secret files
    upload_patterns = [
        r'curl\s+.*(-d|--data|--data-binary|--data-raw)\s+@.*\.(env|pem|key)',
        r'curl\s+.*(-F|--form)\s+.*\.(env|pem|key)',
        r'curl\s+.*(-H|--header)\s+["\']Authorization:.*\$',
    ]
    for pattern in upload_patterns:
        if re.search(pattern, command, re.IGNORECASE):
            return True
    # Variable-staging exfiltration: credential-named variable used in network transmission
    # Catches single-command patterns like: SECRET=$(cat .env) && curl -d "$SECRET" ...
    # and: curl -d "$API_KEY" ..., wget --post-data="$TOKEN" ...
    var_staging_patterns = [
        # Variable assignment of secret file combined with outbound transmission in same command
        r'\w*(KEY|TOKEN|SECRET|PASSWORD|PASS|CRED|API)\w*=\$\(.*\).*\b(curl|wget|nc|netcat)\b',
        r'\b(curl|wget|nc|netcat)\b.*\$\{?\w*(KEY|TOKEN|SECRET|PASSWORD|PASS|CRED|API)\w*\}?',
    ]
    for pattern in var_staging_patterns:
        if re.search(pattern, command, re.IGNORECASE):
            return True
    return False

def check_bash_self_modification(command):
    """NEVER rule 3: Never self-modify guardrails files via Bash."""
    # Normalize backslashes so Windows paths match too
    cmd = command.replace("\\", "/")
    if not any(marker in cmd for marker in PLUGIN_DIR_MARKERS):
        return False
    # Redirect writes: > or >> targeting a guardrails path
    if re.search(r'>{1,2}\s*\S*(?:agent-guardrails|gouvernai)', cmd):
        return True
    # sed -i editing a guardrails file
    if re.search(r'sed\s+.*-[a-zA-Z]*i[a-zA-Z]*.*(?:agent-guardrails|gouvernai)', cmd, re.IGNORECASE):
        return True
    # cp / mv / tee writing into a guardrails path
    if re.search(r'\b(cp|mv|tee)\b.*(?:agent-guardrails|gouvernai)', cmd, re.IGNORECASE):
        return True
    return False

def check_dangerous_system_commands(command):
    """Additional safety: block rm -rf / and similar catastrophic commands."""
    catastrophic = [
        r'rm\s+(-[a-zA-Z]*f[a-zA-Z]*\s+)?(-[a-zA-Z]*r[a-zA-Z]*\s+)?/',
        r'rm\s+(-[a-zA-Z]*r[a-zA-Z]*\s+)?(-[a-zA-Z]*f[a-zA-Z]*\s+)?/',
        r'rm\s+-rf\s+~/?$',
        r'rm\s+-rf\s+\$HOME/?$',
        r'mkfs\.',
        r'dd\s+.*of=/dev/',
        r'chmod\s+-R\s+777\s+/',
        r':\(\)\{\s*:\|:&\s*\};:',  # fork bomb
    ]
    for pattern in catastrophic:
        if re.search(pattern, command, re.IGNORECASE):
            return True
    return False

PLUGIN_DIR_MARKERS = ["agent-guardrails", "gouvernai"]

def is_guardrails_path(file_path):
    """Return True if file_path contains a known guardrails plugin dir marker."""
    normalized = file_path.replace("\\", "/")
    return any(marker in normalized for marker in PLUGIN_DIR_MARKERS)

def check_file_write(file_path, content=""):
    """Check file writes for credential exposure in committed content."""
    # Block writing secrets to files likely to be committed
    secret_indicators = [
        r'(?:api[_-]?key|token|secret|password|credential)\s*[:=]\s*["\']?[A-Za-z0-9+/=_-]{20,}',
        r'(?:sk|pk|rk)-[a-zA-Z0-9-]{20,}',
        r'-----BEGIN (?:RSA |EC )?PRIVATE KEY-----',
        r'AKIA[0-9A-Z]{16}',  # AWS access key
    ]
    if content:
        for pattern in secret_indicators:
            if re.search(pattern, content, re.IGNORECASE):
                # Only block if writing to files that are likely committed
                skip_dirs = ['scratch/', 'temp/', 'tmp/']
                skip_files = ['.env']
                basename = os.path.basename(file_path)
                if basename not in skip_files and not any(d in file_path for d in skip_dirs):
                    return True
    return False

def main():
    try:
        # Use binary-mode read to avoid Git Bash on Windows mangling stdin
        # when the JSON payload contains shell metacharacters (|, &, ;, etc.)
        raw = sys.stdin.buffer.read().decode("utf-8", errors="replace")
        data = json.loads(raw)
    except (json.JSONDecodeError, Exception):
        sys.exit(0)  # can't parse input, allow through

    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})

    auto_approve_output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
            "permissionDecisionReason": "Guardrails internal read"
        }
    }

    # ── Read tool checks ──
    if tool_name == "Read":
        file_path = tool_input.get("file_path", tool_input.get("path", ""))
        basename = os.path.basename(file_path)
        skill_files = {"SKILL.md", "ACTIONS.md", "TIERS.md", "POLICY.md", "GUIDE.md", "guardrails_log.md", "README.md"}
        if basename in skill_files and is_guardrails_path(file_path):
            print(json.dumps(auto_approve_output))
            sys.exit(0)
        # Mode config is a plain project-level file — always safe to read
        if basename == "guardrails-mode.json":
            print(json.dumps(auto_approve_output))
            sys.exit(0)

    # ── Bash tool checks ──
    if tool_name == "Bash":
        command = tool_input.get("command", "")
        if not command:
            sys.exit(0)

        if check_obfuscated_command(command):
            block(
                "Obfuscated command detected",
                f"Command contains encoded/obfuscated execution patterns. Decode and review before running."
            )

        if check_credential_exposure(command):
            block(
                "Credential transmission detected",
                f"Command reads secrets and transmits them externally. This violates NEVER rule 1."
            )

        if check_dangerous_system_commands(command):
            block(
                "Catastrophic system command detected",
                f"Command could cause irreversible system damage."
            )

        if check_bash_self_modification(command):
            block(
                "Guardrails self-modification blocked",
                f"Bash command writes to guardrails path. NEVER rule 3."
            )

    # ── Write/Edit tool checks ──
    elif tool_name in ("Write", "Edit"):
        file_path = tool_input.get("file_path", tool_input.get("path", ""))
        content = tool_input.get("content", tool_input.get("new_str", ""))

        # Auto-approve writes to guardrails_log.md and guardrails-mode.json
        basename = os.path.basename(file_path)
        if basename == "guardrails_log.md" and is_guardrails_path(file_path):
            print(json.dumps(auto_approve_output))
            sys.exit(0)
        if basename == "guardrails-mode.json":
            print(json.dumps(auto_approve_output))
            sys.exit(0)

        # Block self-modification of guardrails files
        guardrails_files = ["SKILL.md", "ACTIONS.md", "TIERS.md", "POLICY.md", "GUIDE.md"]
        basename = os.path.basename(file_path)
        if basename in guardrails_files and is_guardrails_path(file_path):
            block(
                "Guardrails self-modification blocked",
                f"Cannot modify guardrails skill file: {basename}. NEVER rule 3."
            )

        if check_file_write(file_path, content):
            block(
                "Credential in file write detected",
                f"Content appears to contain secrets/credentials being written to {file_path}."
            )

    # No violation detected
    sys.exit(0)

if __name__ == "__main__":
    main()
