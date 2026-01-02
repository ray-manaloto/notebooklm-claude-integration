#!/usr/bin/env bash
set -euo pipefail

SKILL_URL=${SKILL_URL:-"https://github.com/ray-manaloto/notebooklm-claude-integration/tree/main/.codex/skills/notebooklm-patterns"}
QUESTION=${QUESTION:-"How can we improve the Codex implementation in this repo? Please cite sources."}
NOTEBOOK_IDS=${NOTEBOOK_IDS:-""}

TEST_ROOT=${TEST_ROOT:-"/tmp/codex-skill-validate"}
SKILL_TMP=${SKILL_TMP:-"/tmp/skill-download-validate"}

CODEX_HOME=${CODEX_HOME:-"$HOME/.codex"}
INSTALLER="$CODEX_HOME/skills/.system/skill-installer/scripts/install-skill-from-github.py"

if [[ ! -f "$INSTALLER" ]]; then
  echo "Skill installer not found at $INSTALLER" >&2
  exit 1
fi

rm -rf "$TEST_ROOT" "$SKILL_TMP"
mkdir -p "$TEST_ROOT" "$SKILL_TMP"

python3 "$INSTALLER" \
  --url "$SKILL_URL" \
  --dest "$SKILL_TMP"

mkdir -p "$TEST_ROOT/.codex/skills"
cp -R "$SKILL_TMP/notebooklm-patterns" "$TEST_ROOT/.codex/skills/"

cd "$TEST_ROOT"

git init -q

touch README.md

git add README.md

git commit -q -m "init"

if [[ -n "${NOTEBOOK_IDS}" ]]; then
  codex --enable skills exec "Use the notebooklm-patterns skill. First call mcp__notebooklm__get_health and report the status. If authenticated is false, run mcp__notebooklm__setup_auth with show_browser=true, then call mcp__notebooklm__get_health again. If still not authenticated, stop and report the failure. Then list all notebooks, filter to these notebook IDs (comma-separated): '${NOTEBOOK_IDS}'. Ask each selected notebook (via notebook_id): '${QUESTION}'. Aggregate responses labeled by notebook name and include citations. If any ask_question times out, retry once with browser_options timeout_ms=60000. If any response is off-topic, retry once with a narrower prompt that starts with: 'Answer ONLY about: ${QUESTION}'. If it still drifts, report a likely notebook-content mismatch."
else
  codex --enable skills exec "Use the notebooklm-patterns skill. First call mcp__notebooklm__get_health and report the status. If authenticated is false, run mcp__notebooklm__setup_auth with show_browser=true, then call mcp__notebooklm__get_health again. If still not authenticated, stop and report the failure. Then list all notebooks, then ask each notebook (via notebook_id): '${QUESTION}'. Aggregate responses labeled by notebook name and include citations. If any ask_question times out, retry once with browser_options timeout_ms=60000. If any response is off-topic, retry once with a narrower prompt that starts with: 'Answer ONLY about: ${QUESTION}'. If it still drifts, report a likely notebook-content mismatch."
fi
