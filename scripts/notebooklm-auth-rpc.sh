#!/usr/bin/env bash
set -euo pipefail

MODE=${MODE:-"auto"}
COOKIE_FILE=${COOKIE_FILE:-""}

if ! command -v notebooklm-mcp-auth >/dev/null 2>&1; then
  echo "notebooklm-mcp-auth not found. Install first:" >&2
  echo "  uv tool install notebooklm-mcp-server" >&2
  echo "  # or: pipx install notebooklm-mcp-server" >&2
  exit 1
fi

if [[ "${MODE}" == "file" ]]; then
  if [[ -n "${COOKIE_FILE}" ]]; then
    notebooklm-mcp-auth --file "${COOKIE_FILE}"
  else
    notebooklm-mcp-auth --file
  fi
else
  notebooklm-mcp-auth
fi

cat <<'EOF'
Auth complete. Cookies stored at:
  ~/.notebooklm-mcp/auth.json

If you haven't added the RPC MCP server yet:
  codex mcp add notebooklm-rpc -- notebooklm-mcp
EOF
