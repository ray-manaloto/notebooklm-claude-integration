#!/usr/bin/env bash
set -euo pipefail

MODE=${MODE:-"auto"}
COOKIE_FILE=${COOKIE_FILE:-""}
GOOGLE_ACCOUNT=${GOOGLE_ACCOUNT:-"ray.manaloto@gmail.com"}

if ! command -v notebooklm-mcp-auth >/dev/null 2>&1; then
  echo "notebooklm-mcp-auth not found. Install first:" >&2
  echo "  uv tool install notebooklm-mcp-server" >&2
  echo "  # or: pipx install notebooklm-mcp-server" >&2
  exit 1
fi

if [[ "${MODE}" == "file" ]]; then
  echo "Target Google account: ${GOOGLE_ACCOUNT}"
  echo "Make sure Chrome is signed into this account before copying cookies."
  if [[ -n "${COOKIE_FILE}" ]]; then
    notebooklm-mcp-auth --file "${COOKIE_FILE}"
  else
    notebooklm-mcp-auth --file
  fi
else
  echo "Target Google account: ${GOOGLE_ACCOUNT}"
  echo "Make sure Chrome is signed into this account before continuing."
  notebooklm-mcp-auth
fi

cat <<'EOF'
Auth complete. Cookies stored at:
  ~/.notebooklm-mcp/auth.json

If you haven't added the RPC MCP server yet:
  codex mcp add notebooklm-rpc -- notebooklm-mcp
EOF
