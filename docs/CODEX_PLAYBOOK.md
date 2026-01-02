# Codex NotebookLM Playbook

This playbook is optimized for Codex CLI/SDK agents to follow step by step and validate the NotebookLM integration.

## 1) Setup Checklist

- `codex` CLI installed
- NotebookLM MCP server configured:
  ```bash
  codex mcp add notebooklm -- npx -y notebooklm-mcp@latest
  ```
- Optional: choose a smaller tool profile to reduce context load:
  ```bash
  export NOTEBOOKLM_PROFILE=standard
  ```
- Authentication completed once (scripts will open Chrome when auth is missing and stop if auth still fails):
  ```bash
  codex --enable skills exec "Use the notebooklm-patterns skill. Check auth with mcp__notebooklm__get_health. If not authenticated, run mcp__notebooklm__setup_auth with show_browser=true, then re-check."
  ```

### Optional: HTTP/RPC NotebookLM MCP (Expanded Tools)

If you want notebook creation, Drive sync, and Studio artifacts, use the `jacob-bd/notebooklm-mcp` server:

```bash
uv tool install notebooklm-mcp-server
scripts/notebooklm-auth-rpc.sh
codex mcp add notebooklm-rpc -- notebooklm-mcp
```

This server uses cookie extraction (`notebooklm-mcp-auth`) instead of `setup_auth`, and tool names differ (e.g., `notebook_list`, `notebook_query`, `source_sync_drive`).

### Recommended Hybrid Setup

Configure both `notebooklm` and `notebooklm-rpc`. Use `notebooklm` for the standard ask/list flow and switch to `notebooklm-rpc` when you need Drive sync, notebook creation, or Studio artifacts.

## 2) Validate (Fresh Repo)

Run an end-to-end validation in a clean temp directory:

```bash
scripts/codex-validate-setup.sh
```

Expected results:
- `get_health` shows `authenticated: true`
- At least one notebook is found
- Multi-notebook query returns labeled responses with citations

## 3) Research-First Workflow

Always query NotebookLM before changing code:

1. `list_notebooks`
2. `ask_question` with `notebook_id`
3. Summarize with citations
4. Only then proceed to edits

Recommended prompt patterns:
- **Research → Synthesize → Code:** “Research this in NotebookLM first, summarize with citations, then propose changes.”
- **Plan & Verify:** “Explain the implementation based on sources before writing code.”
- **Explain-back (Feynman):** “Explain the concept in your own words to confirm understanding before edits.”

## 4) Multi-Notebook Query (Safe Parallelization)

- Use `ask_question` with `notebook_id` for each notebook.
- Avoid `select_notebook` inside parallel workers (shared state).
- Retry once with `browser_options.timeout_ms=60000` on timeouts.

## 5) Multi-Agent Loop (Best Practice)

Use a three-pass loop even if you run it in a single CLI session:

1. **Research** (NotebookLM): gather facts with citations.
2. **Build**: implement changes based on the cited facts.
3. **Review**: validate against citations, check regressions.

If subagents or task parallelism are available, use them for the research pass across notebooks.

Planner → Subagents → Aggregator outline:
1. **Planner**: list notebooks, map each to a sub-question.
2. **Per-notebook subagents**: ask via `notebook_id` (parallel if supported).
3. **Aggregator**: merge answers, keep citations per notebook, note gaps/off-topic responses.

### Gating Checklist (Required)

Before handing off between agents, enforce these checks:
- Artifact paths/IDs exist.
- If tests were run, command + output summary are recorded.
- NotebookLM answers include citations or session IDs.

For more detail, see `.codex/skills/notebooklm-patterns/references/agent-gating-checklist.md`.

Example CLI prompt:
```bash
codex --enable skills exec "Use notebooklm-patterns. List notebooks. If subagents are available, spawn one per notebook to answer: 'Summarize auth flow changes with citations'. Otherwise run sequentially. Aggregate answers by notebook name with citations."
```

## Parallel Auth Bootstrap

Use a single interactive login first, then allow parallel workers to reuse the profile:

```bash
NOTEBOOK_PROFILE_STRATEGY=auto \
NOTEBOOK_CLONE_PROFILE=true \
make codex-bootstrap-parallel
```

Bootstrap only (no query):
```bash
make codex-bootstrap-auth
```

SDK example:
```bash
cd codex-sdk-test
QUESTION="Summarize auth flow changes." npm run test:notebooklm-ask-all
```

## Targeted Notebook Queries

Avoid off-topic answers by filtering to specific notebook IDs:

```bash
NOTEBOOK_IDS=pytest-patterns \
QUESTION="Provide modern best practices for integration tests without mocks." \
make codex-ask-all
```

### Targeted Queries (HTTP/RPC Server)

If using `notebooklm-rpc`:
```bash
NOTEBOOK_IDS=pytest-patterns \
QUESTION="Provide modern best practices for integration tests without mocks." \
scripts/codex-ask-all-rpc.sh
```

## Local NotebookLM Integration Test

Run the local end-to-end NotebookLM script (uses your stored Chrome auth):

```bash
NOTEBOOK_IDS=pytest-patterns \
QUESTION="Summarize the key sources in this notebook." \
tests/notebooklm-integration.sh
```

## 6) Data Quality & Triangulation

To reduce hallucinations, curate NotebookLM sources using a triangulated set:
- **Theory**: official docs or PDFs
- **Practice**: video tutorials (YouTube URLs)
- **Context**: articles/notes on pitfalls or real-world usage

Keep notebooks domain-specific and tag them consistently. Prefer one notebook per domain to avoid context dilution.

## 7) Troubleshooting

- If queries time out, retry once with `browser_options.timeout_ms=60000`.
- If auth fails repeatedly, run `mcp__notebooklm__re_auth`.
- If output looks unrelated, the notebook likely doesn’t cover the question—switch notebooks or refine the question.
