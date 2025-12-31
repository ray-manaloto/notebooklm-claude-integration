# CI Overview

This repo uses GitHub Actions for fast, deterministic checks that do not require live NotebookLM access.

## What Runs

- **auth-layer**: `npm ci`, `npm run lint`, `npm run build`, `npm test`
- **simulations**: `python3 tests/run_simulation.py` (mocked, no browser)
- **scripts**: `bash -n` over `scripts/*.sh`

## Why No Live NotebookLM Tests

NotebookLM requires browser-based authentication. CI avoids live logins by default. Use the local runner script in `docs/NOTEBOOKLM_INTEGRATION_TESTS.md` for end-to-end validation.
