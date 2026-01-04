# NotebookLM Integration Tests (Local Only)

These tests run the real NotebookLM flows using your local Chrome authentication profile. They are not intended for hosted CI.

## Run

```bash
NOTEBOOK_IDS=pytest-patterns \
QUESTION="Summarize the key sources in this notebook." \
pixi run notebooklm-integration
```

Pixi task:
```bash
NOTEBOOK_IDS=pytest-patterns \
QUESTION="Summarize the key sources in this notebook." \
pixi run codex-ask-all
```

## What It Does

- Ensures RPC auth is available (fail fast if cookies are missing).
- Filters to the requested notebook IDs.
- Runs `notebook_query` with retry and off-topic guardrails.

## Guardrails

- Keep notebook IDs narrow for targeted checks.
- Re-ask once with a tighter prompt if a response drifts off-topic.
- Fail fast if NotebookLM does not provide citations.

## Notes

- Requires a local Chrome login for NotebookLM (via notebooklm-mcp-auth).
- Use `pixi run notebooklm-auth-rpc` to bootstrap the RPC auth flow if needed.
- You can set the default account for RPC auth via `GOOGLE_ACCOUNT=your@email`.
