#!/usr/bin/env bash
set -euo pipefail

QUESTION=${QUESTION:-"Summarize the key sources in this notebook."}
NOTEBOOK_IDS=${NOTEBOOK_IDS:-"pytest-patterns"}

if [[ -n "${NOTEBOOKLM_PROFILE:-}" ]]; then
  export NOTEBOOKLM_PROFILE
fi

codex --enable skills exec "Use the notebooklm-patterns skill. Run get_health. If authenticated is false, run setup_auth with show_browser=true, then re-run get_health and confirm authentication. Then list notebooks and filter to these notebook IDs (comma-separated): '${NOTEBOOK_IDS}'. Ask each selected notebook (via notebook_id) this question: '${QUESTION}'. Aggregate responses labeled by notebook name and include citations. If any ask_question times out, retry once with browser_options timeout_ms=60000. If any response is off-topic, retry once with a narrower prompt that starts with: 'Answer ONLY about: ${QUESTION}'. If it still drifts, report a likely notebook-content mismatch."
