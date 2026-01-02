# NotebookLM Integration Tests (Local Only)

These tests run the real NotebookLM flows using your local Chrome authentication profile. They are not intended for hosted CI.

## Run

```bash
NOTEBOOK_IDS=pytest-patterns \
QUESTION="Summarize the key sources in this notebook." \
tests/notebooklm-integration.sh
```

Pixi task:
```bash
NOTEBOOK_IDS=pytest-patterns \
QUESTION="Summarize the key sources in this notebook." \
pixi run codex-ask-all
```

## What It Does

- Checks auth status and triggers `setup_auth` with a visible Chrome window if needed (fails fast if auth still does not resolve).
- Filters to the requested notebook IDs.
- Runs `ask_question` with retry and off-topic guardrails.

## Guardrails

- Keep notebook IDs narrow for targeted checks.
- Re-ask once with a tighter prompt if a response drifts off-topic.
- Fail fast if NotebookLM does not provide citations.

## Notes

- Requires a local Chrome login for NotebookLM.
- Uses `NOTEBOOKLM_PROFILE` if provided.
- The alternate `notebooklm-rpc` server uses `notebooklm-mcp-auth` and different tool names; these scripts target the `notebooklm` server.
- Use `scripts/notebooklm-auth-rpc.sh` to bootstrap the RPC auth flow if needed.
- You can set the default account for RPC auth via `GOOGLE_ACCOUNT=your@email`.
