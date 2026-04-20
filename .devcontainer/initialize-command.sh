#!/usr/bin/env bash
# Runs on the devcontainer *host* during initializeCommand (before the container exists).
# Reads a 1Password service-account token and writes it to .env.development so the
# container can authenticate with Snyk / other tools.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

OP_REF='op://Private/1Password op CLI Service Account for DevContainers/password'
ENV_FILE="$ROOT/.env.development"

# ── Fast path: token already in the environment ──────────────────────────────
if [[ -n "${OP_SERVICE_ACCOUNT_TOKEN:-}" ]]; then
	printf '%s\n' "OP_SERVICE_ACCOUNT_TOKEN=$OP_SERVICE_ACCOUNT_TOKEN" >"$ENV_FILE"
	echo "initializeCommand: OP_SERVICE_ACCOUNT_TOKEN already set; wrote $ENV_FILE"
	exit 0
fi

# ── Ensure op is available ───────────────────────────────────────────────────
if ! command -v op >/dev/null 2>&1; then
	echo "ERROR: op (1Password CLI) not found on PATH" >&2
	exit 1
fi

# IDE-spawned processes (Cursor, VS Code) don't inherit OP_BIOMETRIC_UNLOCK_ENABLED
# from your shell profile, but the desktop-app integration requires it.
export OP_BIOMETRIC_UNLOCK_ENABLED=true

# Verify the CLI can see at least one account via the desktop app bridge.
if ! op account list 2>/dev/null | grep -q .; then
	cat >&2 <<-'MSG'
	ERROR: 1Password CLI has no reachable accounts in this process.

	The desktop-app integration needs OP_BIOMETRIC_UNLOCK_ENABLED=true and a
	running, unlocked 1Password app. If both are true and this still fails:
	  • Ensure Cursor has Full Disk Access (System Settings → Privacy & Security)
	  • Restart Cursor after changing permissions
	  • Or export OP_SERVICE_ACCOUNT_TOKEN so the fast-path above is used instead
	MSG
	exit 1
fi

# ── Read the secret (stdin closed to prevent interactive prompts) ────────────
token="$(op read "$OP_REF" </dev/null 2>&1)" || {
	echo "ERROR: op read failed:" >&2
	echo "$token" >&2
	exit 1
}

if [[ -z "$token" ]]; then
	echo "ERROR: op read succeeded but returned empty output" >&2
	exit 1
fi

printf '%s\n' "OP_SERVICE_ACCOUNT_TOKEN=$token" >"$ENV_FILE"
echo "initializeCommand: wrote $ENV_FILE (token length ${#token})"
