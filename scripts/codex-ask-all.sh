#!/usr/bin/env bash
set -euo pipefail

QUESTION=${QUESTION:-"How can we improve the Codex implementation in this repo?"}

codex --enable skills exec "Use the notebooklm-patterns skill. List all notebooks, then ask each notebook (via notebook_id) this question: '${QUESTION}'. Aggregate responses labeled by notebook name and include citations. If any ask_question times out, retry once with browser_options timeout_ms=60000."
