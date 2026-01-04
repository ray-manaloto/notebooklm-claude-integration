# Parallel Auth Strategy (NotebookLM MCP)

## Goal

Enable one login process to establish credentials and allow parallel subagents/processes to reuse them without re-login.

## Recommended Approach (Current MCP Capabilities)

- Use the **notebooklm-mcp** cookie file (`~/.notebooklm-mcp/auth.json`) as the shared auth source.
- Run a **single login bootstrap** (`notebooklm-mcp-auth` + `save_auth_tokens`) to populate cookies.
- Launch parallel workers after the bootstrap completes; all workers read the same cookie file.

## Why This Works

- The MCP server reads a single cookie file, so all sessions share auth state.
- Avoids needing multiple interactive logins.

## Proposed Workflow

1. **Bootstrap login** (single process, interactive once).
2. **Spawn parallel workers** that read `~/.notebooklm-mcp/auth.json`.
3. **Re-auth** only when cookies expire.

## Open Decisions

- Whether to add a script that performs bootstrap + fan-out in a single command.
