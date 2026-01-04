---
name: notebooklm-patterns
description: NotebookLM integration patterns aligned to notebooklm-mcp (RPC tool names, auth flow, and troubleshooting). Use when listing/creating/querying notebooks, managing sources, running research, or generating studio artifacts.
---

# NotebookLM Codex Skill (RPC)

Provide a reliable, repeatable workflow to authenticate with NotebookLM and automate queries using notebooklm-mcp.

## Tool Reference (RPC)

### Authentication
- `mcp__notebooklm-rpc__save_auth_tokens`

### Notebooks
- `mcp__notebooklm-rpc__notebook_list`
- `mcp__notebooklm-rpc__notebook_create`
- `mcp__notebooklm-rpc__notebook_get`
- `mcp__notebooklm-rpc__notebook_describe`
- `mcp__notebooklm-rpc__notebook_rename`
- `mcp__notebooklm-rpc__notebook_delete`
- `mcp__notebooklm-rpc__notebook_query`

### Sources
- `mcp__notebooklm-rpc__notebook_add_url`
- `mcp__notebooklm-rpc__notebook_add_text`
- `mcp__notebooklm-rpc__notebook_add_drive`
- `mcp__notebooklm-rpc__source_list_drive`
- `mcp__notebooklm-rpc__source_sync_drive`
- `mcp__notebooklm-rpc__source_delete`
- `mcp__notebooklm-rpc__source_describe`

### Research
- `mcp__notebooklm-rpc__research_start`
- `mcp__notebooklm-rpc__research_status`
- `mcp__notebooklm-rpc__research_import`

### Chat Configuration
- `mcp__notebooklm-rpc__chat_configure`

### Studio
- `mcp__notebooklm-rpc__audio_overview_create`
- `mcp__notebooklm-rpc__video_overview_create`
- `mcp__notebooklm-rpc__infographic_create`
- `mcp__notebooklm-rpc__slide_deck_create`
- `mcp__notebooklm-rpc__studio_status`
- `mcp__notebooklm-rpc__studio_delete`

If tools are missing, ask the user to run `pixi run mcp-install-code` and ensure cookies are saved via `notebooklm-mcp-auth` + `save_auth_tokens`.

## Authentication Workflow

NotebookLM has no public API; authentication is cookie-based:

1. Run `notebooklm-mcp-auth` and complete Google login.
2. Call `save_auth_tokens` to persist cookies to `~/.notebooklm-mcp/auth.json`.
3. Retry NotebookLM RPC tools.

## Core Query Workflow

1. List notebooks: `notebook_list`.
2. Ask a question: `notebook_query` with `notebook_id` + `question`.
3. For follow-ups, pass `session_id` from the prior response.

## Multi-Notebook Query

1. `notebook_list` to get IDs.
2. Query each notebook via `notebook_query` with the same question.
3. Aggregate responses labeled by notebook name/ID and citations.

Notes:
- Retry a timed-out query once; then record a timeout and continue.
- Avoid shared mutable state; always use `notebook_id` explicitly.

## Research-First Behavior

Always query NotebookLM first and cite sources before making code changes. Prefer concise, citation-backed summaries.

## Reliability Tips

- If answers drift, retry once with a narrower prompt.
- Re-run `notebooklm-mcp-auth` when cookies expire.
- Keep notebooks domain-specific to reduce off-topic answers.
