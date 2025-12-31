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

## Tool Profiles (Minimal/Standard)

When supported, use smaller profiles to reduce context load:
- **Minimal**: query-only flows (list/select/ask).
- **Standard**: library management (add/search/update) plus query tools.

You can set `NOTEBOOKLM_PROFILE=minimal` or `NOTEBOOKLM_PROFILE=standard` in the environment before starting Codex.

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

### Research-First Prompt Templates

- **Research → Synthesize → Code**: “Research this in NotebookLM first, summarize with citations, then propose changes.”
- **Plan & Verify**: “Explain the implementation based on sources before writing code.”
- **Explain-back**: “Explain the concept in your own words to confirm understanding before edits.”

## Data Quality & Triangulation

To reduce hallucinations, curate sources per notebook with a triangulated set:
- **Theory**: official docs or PDFs.
- **Practice**: video tutorials (YouTube URLs).
- **Context**: articles/notes about pitfalls and real-world use.

Keep notebooks domain-specific and tag them consistently so Codex can “smart select” the right notebook.

## Reliability Tips

- If `ask_question` times out, retry once with `browser_options.timeout_ms=60000`.
- If a query repeatedly fails, re-auth with `mcp__notebooklm__re_auth`.
- If supported by the server, enable browser visibility to debug (e.g., `show_browser: true` in auth flows).
- If the answer is off-topic, reset or abandon the session and re-ask with a narrower prompt that names the exact subject, required outputs, and “do not answer about unrelated topics.”

## Tool Access Guardrails

When possible, scope tool access to the minimum needed for the task. If your Codex setup supports tool allowlists, prefer them for NotebookLM skills to reduce blast radius. Keep destructive tools (write/delete) out of research-only flows.

## Multi-Notebook Query (Codex)

When you need the same question answered across all notebooks, prefer `ask_question` with `notebook_id` to avoid race conditions from global `select_notebook` state.

1. `mcp__notebooklm__list_notebooks` to get all notebook IDs.
2. For each notebook, call `mcp__notebooklm__ask_question` with `notebook_id` and the same `question`.
3. Aggregate responses, labeling each answer with notebook name/ID and citations.

Notes:
- Parallel calls are fine, but keep within rate limits (each notebook query counts).
- Avoid `select_notebook` inside parallel workers since it mutates shared active state.

## Multi-Agent Usage (Best Practice)

For complex tasks, split responsibilities:
- **Research agent**: gather NotebookLM answers (single or multi-notebook).
- **Builder agent**: implement changes based on cited sources.
- **Reviewer agent**: check for gaps, missing citations, and regressions.

If the runtime supports subagents or task parallelism, prefer spawning subagents for multi-notebook queries and aggregating results in the main agent.

### Example: Add and Query

If a notebook is not yet in the library:

1. Add it via `mcp__notebooklm__add_notebook` with a clear name, description, and topics.
2. Select it: `mcp__notebooklm__select_notebook`.
3. Ask a discovery question with `mcp__notebooklm__ask_question` to validate content.

## Response Expectations

- Include citations returned by NotebookLM.
- Keep answers concise; offer to drill down with follow-up questions.
- If a notebook lacks relevant sources, suggest adding or switching notebooks.
- If a response drifts off-topic after a retry, report a likely notebook-content mismatch rather than guessing.

## References

For deeper workflows and orchestration patterns, see:
- `references/agent-gating-checklist.md` for multi-agent handoff checks.
## Troubleshooting Quick Hits

- **Not authenticated:** run `mcp__notebooklm__setup_auth`.
- **Auth keeps failing:** run `mcp__notebooklm__re_auth`, then re-login.
- **CDP not detected:** ensure Chrome is started with `--remote-debugging-port=9222`.
- **Rate limit reached:** wait for reset or switch Google account via `mcp__notebooklm__re_auth`.

## Notes for This Repo

- See `auth-layer/README.md` for backend details (CDP, Keychain, persistent profile).
- Keep secrets out of source control; auth state is stored locally.
