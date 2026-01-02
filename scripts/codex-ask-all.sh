#!/usr/bin/env bash
set -euo pipefail

QUESTION=${QUESTION:-"How can we improve the Codex implementation in this repo?"}
NOTEBOOK_IDS=${NOTEBOOK_IDS:-""}

if [[ -n "${NOTEBOOKLM_PROFILE:-}" ]]; then
  export NOTEBOOKLM_PROFILE
fi

if [[ -n "${NOTEBOOK_IDS}" ]]; then
  codex --enable skills exec "Use the notebooklm-patterns skill. Call mcp__notebooklm__get_health. If authenticated is false, run mcp__notebooklm__setup_auth with show_browser=true, then call mcp__notebooklm__get_health again. If still not authenticated, stop and report the failure. List all notebooks, then filter to these notebook IDs (comma-separated): '${NOTEBOOK_IDS}'. Ask each selected notebook (via notebook_id) this question: '${QUESTION}'. Aggregate responses labeled by notebook name and include citations. If any ask_question times out, retry once with browser_options timeout_ms=60000. If any response is off-topic, retry once with a narrower prompt that starts with: 'Answer ONLY about: ${QUESTION}'. If it still drifts, report a likely notebook-content mismatch."
else
  codex --enable skills exec "Use the notebooklm-patterns skill. Call mcp__notebooklm__get_health. If authenticated is false, run mcp__notebooklm__setup_auth with show_browser=true, then call mcp__notebooklm__get_health again. If still not authenticated, stop and report the failure. List all notebooks, then ask each notebook (via notebook_id) this question: '${QUESTION}'. Aggregate responses labeled by notebook name and include citations. If any ask_question times out, retry once with browser_options timeout_ms=60000. If any response is off-topic, retry once with a narrower prompt that starts with: 'Answer ONLY about: ${QUESTION}'. If it still drifts, report a likely notebook-content mismatch."
fi
