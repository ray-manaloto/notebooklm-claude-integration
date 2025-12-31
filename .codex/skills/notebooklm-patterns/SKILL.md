---
name: notebooklm-patterns
description: NotebookLM integration patterns and troubleshooting for Codex CLI. Use when connecting/authenticating via browser login, managing the notebook library, or querying notebooks for citation-backed answers.
---

# NotebookLM Codex Skill

Provide a reliable, repeatable workflow to authenticate with NotebookLM (no public API) and automate queries against a notebook.

## Tool Reference (MCP)

Use these tools when available:
- `mcp__notebooklm__get_health` — check auth status and readiness
- `mcp__notebooklm__setup_auth` — interactive login (opens browser)
- `mcp__notebooklm__re_auth` — reset and re-authenticate
- `mcp__notebooklm__add_notebook` — add a NotebookLM URL to the library
- `mcp__notebooklm__list_notebooks` — list notebooks
- `mcp__notebooklm__select_notebook` — set active notebook by id
- `mcp__notebooklm__get_notebook` — fetch notebook details
- `mcp__notebooklm__search_notebooks` — search library by query
- `mcp__notebooklm__ask_question` — ask a question (optionally with `session_id`)

If the tools are missing or error with “tool not found,” ask the user to configure the MCP server using `mcp-config/README.md` and retry.

## Authentication Workflow (Browser-Based)

NotebookLM has no API/SDK. You must authenticate through a browser session:

1. Call `mcp__notebooklm__get_health`.
2. If not authenticated, run `mcp__notebooklm__setup_auth` and instruct the user to complete Google login.
3. If auth repeatedly fails or rate-limited, run `mcp__notebooklm__re_auth` to clear state and re-login.

Best experience (reuse existing Google login):
- Start Chrome with remote debugging:
  ```bash
  open -a "Google Chrome" --args --remote-debugging-port=9222
  ```
- Then run `mcp__notebooklm__setup_auth`.

## Core Query Workflow

Use this sequence to automate connecting and querying:

1. Verify auth: `mcp__notebooklm__get_health`.
2. Ensure a notebook is active:
   - `mcp__notebooklm__list_notebooks`
   - If needed, `mcp__notebooklm__search_notebooks` then `mcp__notebooklm__select_notebook`.
3. Ask a question:
   - `mcp__notebooklm__ask_question` with `question`.
4. For follow-ups, pass `session_id` from the prior response.

## Research-First Behavior

For changes that impact code or decisions, always query NotebookLM first and cite sources in the response. Avoid “best guesses” when the notebook can answer directly.

## Reliability Tips

- If `ask_question` times out, retry once with `browser_options.timeout_ms=60000`.
- If a query repeatedly fails, re-auth with `mcp__notebooklm__re_auth`.
- If supported by the server, enable browser visibility to debug (e.g., `show_browser: true` in auth flows).

## Multi-Notebook Query (Codex)

When you need the same question answered across all notebooks, prefer `ask_question` with `notebook_id` to avoid race conditions from global `select_notebook` state.

1. `mcp__notebooklm__list_notebooks` to get all notebook IDs.
2. For each notebook, call `mcp__notebooklm__ask_question` with `notebook_id` and the same `question`.
3. Aggregate responses, labeling each answer with notebook name/ID and citations.

Notes:
- Parallel calls are fine, but keep within rate limits (each notebook query counts).
- Avoid `select_notebook` inside parallel workers since it mutates shared active state.

### Example: Add and Query

If a notebook is not yet in the library:

1. Add it via `mcp__notebooklm__add_notebook` with a clear name, description, and topics.
2. Select it: `mcp__notebooklm__select_notebook`.
3. Ask a discovery question with `mcp__notebooklm__ask_question` to validate content.

## Response Expectations

- Include citations returned by NotebookLM.
- Keep answers concise; offer to drill down with follow-up questions.
- If a notebook lacks relevant sources, suggest adding or switching notebooks.

## Troubleshooting Quick Hits

- **Not authenticated:** run `mcp__notebooklm__setup_auth`.
- **Auth keeps failing:** run `mcp__notebooklm__re_auth`, then re-login.
- **CDP not detected:** ensure Chrome is started with `--remote-debugging-port=9222`.
- **Rate limit reached:** wait for reset or switch Google account via `mcp__notebooklm__re_auth`.

## Notes for This Repo

- See `auth-layer/README.md` for backend details (CDP, Keychain, persistent profile).
- Keep secrets out of source control; auth state is stored locally.
