# CI Overview

This repo uses GitHub Actions for fast, deterministic checks that do not require live NotebookLM access.

## What Runs

- **auth-layer**: `npm ci`, `npm run lint`, `npm run build`, `npm test`
- **simulations**: `pixi run simulation` (mocked, no browser)
- **repo hygiene**: `pixi run hooks-run` (blocks bash scripts and non-pixi calls)

## Why No Live NotebookLM Tests

NotebookLM requires browser-based authentication. CI avoids live logins by default. Use the local runner script in `docs/NOTEBOOKLM_INTEGRATION_TESTS.md` for end-to-end validation.
