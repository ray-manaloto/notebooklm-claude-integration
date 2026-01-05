# Codex NotebookLM Playbook

This playbook is optimized for Codex CLI/SDK agents to follow step by step and validate the NotebookLM integration.

## 1) Setup Checklist

- `codex` CLI installed
- NotebookLM MCP server (RPC) configured:
  ```bash
  uv tool install notebooklm-mcp-server
  codex mcp add notebooklm-rpc notebooklm-mcp
  ```
- Authentication completed once:
  ```bash
  pixi run notebooklm-auth-rpc
  ```
Override the account used for cookie extraction with `GOOGLE_ACCOUNT=your@email`.

## 2) Validate (Fresh Repo)

Run an end-to-end validation in a clean temp directory:

```bash
pixi run codex-validate-setup
```

Expected results:
- RPC auth is valid (cookies persisted via `save_auth_tokens`)
- At least one notebook is found
- Multi-notebook query returns labeled responses with citations

## 3) Research-First Workflow

Always query NotebookLM before changing code:

1. `notebook_list`
2. `notebook_query` with `notebook_id`
3. Summarize with citations
4. Only then proceed to edits

Recommended prompt patterns:
- **Research → Synthesize → Code:** “Research this in NotebookLM first, summarize with citations, then propose changes.”
- **Plan & Verify:** “Explain the implementation based on sources before writing code.”
- **Explain-back (Feynman):** “Explain the concept in your own words to confirm understanding before edits.”

## 4) Multi-Notebook Query (Safe Parallelization)

- Use `notebook_query` with `notebook_id` for each notebook.
- Retry once on timeouts, then record a timeout and continue.

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

Use a single interactive login first, then allow parallel workers to reuse cookies:

```bash
pixi run notebooklm-auth-rpc
```

## Targeted Notebook Queries

Avoid off-topic answers by filtering to specific notebook IDs:

```bash
NOTEBOOK_IDS=pytest-patterns \
QUESTION="Provide modern best practices for integration tests without mocks." \
pixi run codex-ask-all
```

### Targeted Queries (RPC)

```bash
NOTEBOOK_IDS=pytest-patterns \
QUESTION="Provide modern best practices for integration tests without mocks." \
pixi run codex-ask-all-rpc
```

## Local NotebookLM Integration Test

Run the local end-to-end NotebookLM script (uses your stored Chrome auth):

```bash
NOTEBOOK_IDS=pytest-patterns \
QUESTION="Summarize the key sources in this notebook." \
pixi run notebooklm-integration
```

## Pixi RPC Task Quickstart

Run NotebookLM MCP tools directly via Pixi tasks (1:1 with RPC tools):

```bash
pixi run nlm-notebook-list

NLM_ARGS_JSON='{"notebook_id":"<id>","question":"Summarize sources."}' \
pixi run nlm-notebook-query
```

Destructive tools require an explicit confirmation flag:

```bash
NLM_CONFIRM=1 NLM_ARGS_JSON='{"notebook_id":"<id>"}' \
pixi run nlm-notebook-delete
```

See `docs/API_REFERENCE.md` for the full task list and argument conventions.

## 6) Data Quality & Triangulation

To reduce hallucinations, curate NotebookLM sources using a triangulated set:
- **Theory**: official docs or PDFs
- **Practice**: video tutorials (YouTube URLs)
- **Context**: articles/notes on pitfalls or real-world usage

Keep notebooks domain-specific and tag them consistently. Prefer one notebook per domain to avoid context dilution.

## 7) Troubleshooting

- If queries time out, retry once, then record a timeout and continue.
- If auth fails repeatedly, rerun `pixi run notebooklm-auth-rpc`.
- If output looks unrelated, the notebook likely doesn’t cover the question—switch notebooks or refine the question.
