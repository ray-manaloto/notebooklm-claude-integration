#!/usr/bin/env bash
set -euo pipefail

export NOTEBOOK_PROFILE_STRATEGY="${NOTEBOOK_PROFILE_STRATEGY:-auto}"
export NOTEBOOK_CLONE_PROFILE="${NOTEBOOK_CLONE_PROFILE:-true}"

codex --enable skills exec "Use the notebooklm-patterns skill. Run get_health. If authenticated is false, run setup_auth with show_browser=true, then re-run get_health. Confirm authentication status before proceeding."
