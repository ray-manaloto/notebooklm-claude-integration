#!/usr/bin/env bash
set -euo pipefail

QUESTION="${QUESTION:-Summarize improvements we can make to the Codex NotebookLM integration.}"

export NOTEBOOK_PROFILE_STRATEGY="${NOTEBOOK_PROFILE_STRATEGY:-auto}"
export NOTEBOOK_CLONE_PROFILE="${NOTEBOOK_CLONE_PROFILE:-true}"
export NOTEBOOK_INSTANCE_MAX_COUNT="${NOTEBOOK_INSTANCE_MAX_COUNT:-20}"
export NOTEBOOK_IDS="${NOTEBOOK_IDS:-}"

echo "Bootstrapping NotebookLM login (if needed)..."
codex --enable skills exec "Use the notebooklm-patterns skill. Run get_health. If authenticated is false, run setup_auth with show_browser=true, then re-run get_health. Confirm authentication status before proceeding."

echo "Running parallel-capable multi-notebook query..."
QUESTION="${QUESTION}" NOTEBOOK_IDS="${NOTEBOOK_IDS}" scripts/codex-ask-all-subagents.sh
