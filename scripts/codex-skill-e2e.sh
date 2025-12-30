#!/usr/bin/env bash
set -euo pipefail

CODEX_HOME=${CODEX_HOME:-"$HOME/.codex"}
INSTALLER="$CODEX_HOME/skills/.system/skill-installer/scripts/install-skill-from-github.py"
SKILL_URL=${SKILL_URL:-"https://github.com/ray-manaloto/notebooklm-claude-integration/tree/main/.codex/skills/notebooklm-patterns"}
NOTEBOOK_URL=${NOTEBOOK_URL:-"https://notebooklm.google.com/notebook/e15da715-d381-4766-9106-08e1444a9dc3"}
NOTEBOOK_NAME=${NOTEBOOK_NAME:-"NotebookLM Secondary Test"}
NOTEBOOK_DESC=${NOTEBOOK_DESC:-"Second test notebook for Codex + NotebookLM integration."}
NOTEBOOK_ID=${NOTEBOOK_ID:-"notebooklm-secondary-test"}

TEST_ROOT=${TEST_ROOT:-"/tmp/codex-skill-e2e"}
SKILL_TMP=${SKILL_TMP:-"/tmp/skill-download-e2e"}

if [[ ! -f "$INSTALLER" ]]; then
  echo "Skill installer not found at $INSTALLER" >&2
  echo "Ensure Codex is installed and CODEX_HOME is set correctly." >&2
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

codex --enable skills exec "Use the notebooklm-patterns skill. Check auth with mcp__notebooklm__get_health. If not authenticated, run mcp__notebooklm__setup_auth and wait. List notebooks and add ${NOTEBOOK_URL} only if it is not already present (use name '${NOTEBOOK_NAME}', description '${NOTEBOOK_DESC}', topics ['notebooklm','codex','mcp','integration','testing']). Select ${NOTEBOOK_ID}, then ask: 'What is this notebook about?' Return a 3-bullet summary with citations."
