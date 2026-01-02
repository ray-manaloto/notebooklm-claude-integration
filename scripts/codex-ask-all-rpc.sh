#!/usr/bin/env bash
set -euo pipefail

QUESTION=${QUESTION:-"How can we improve the Codex implementation in this repo?"}
NOTEBOOK_IDS=${NOTEBOOK_IDS:-""}

if [[ -n "${NOTEBOOK_IDS}" ]]; then
  codex --enable skills exec "Use the notebooklm-patterns skill. For the notebooklm-rpc server, assume cookies were created via notebooklm-mcp-auth. List notebooks with mcp__notebooklm-rpc__notebook_list, then filter to these notebook IDs (comma-separated): '${NOTEBOOK_IDS}'. Ask each selected notebook via mcp__notebooklm-rpc__notebook_query using '${QUESTION}'. Aggregate responses labeled by notebook name and include citations. If any response is off-topic, retry once with a narrower prompt that starts with: 'Answer ONLY about: ${QUESTION}'. If it still drifts, report a likely notebook-content mismatch."
else
  codex --enable skills exec "Use the notebooklm-patterns skill. For the notebooklm-rpc server, assume cookies were created via notebooklm-mcp-auth. List notebooks with mcp__notebooklm-rpc__notebook_list, then ask each notebook via mcp__notebooklm-rpc__notebook_query using '${QUESTION}'. Aggregate responses labeled by notebook name and include citations. If any response is off-topic, retry once with a narrower prompt that starts with: 'Answer ONLY about: ${QUESTION}'. If it still drifts, report a likely notebook-content mismatch."
fi
