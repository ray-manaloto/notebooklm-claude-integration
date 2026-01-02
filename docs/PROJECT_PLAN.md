# Project Plan

This plan stays short for fast agent context. Each topic gets its own file in `docs/plans/`.

## Open Items

- **NotebookLM timeouts**: Some notebooks (e.g., Iceoryx) time out even with `browser_options.timeout_ms`. Upstream `notebooklm-mcp` hardcodes a 120s answer wait. Track fix options and next steps in `docs/plans/notebooklm-mcp-timeouts.md`.
- **Parallel auth strategy**: One process performs login, other parallel processes reuse credentials via profile cloning or shared storage. Track decisions and configuration in `docs/plans/parallel-auth-strategy.md`.
- **Roadmap synthesis**: Prioritized improvements based on NotebookLM research across notebooks. Track in `docs/plans/roadmap.md`.
- **Bun migration (post-verify)**: Consider migrating Node tooling to Bun only after the current flow is verified stable end-to-end.

## Roadmap Links

- NotebookLM MCP timeouts: `docs/plans/notebooklm-mcp-timeouts.md`
- Parallel auth & multi-process: `docs/plans/parallel-auth-strategy.md`
- Prioritized roadmap: `docs/plans/roadmap.md`
