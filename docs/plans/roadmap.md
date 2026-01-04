# Roadmap (NotebookLM → Codex Integration)

This roadmap condenses NotebookLM research into prioritized, actionable steps.

## Quick Wins (1–2 weeks)

- **Bootstrap + fan-out workflow**: Default to single login then parallel ask (already scripted). Document it as the canonical flow in README/Codex playbook.  
- **Auth reuse**: Encourage cookie-based reuse via `~/.notebooklm-mcp/auth.json` for multi-process fan‑out.
- **Visible debug mode**: Add a troubleshooting snippet for `show_browser=true` when a query hangs.
- **Notebook tagging**: Adopt consistent tags (domain, scope, source) so planners can auto-select notebooks.

## Near-Term (2–6 weeks)

- **Session state hardening**: Extend auth layer to persist and restore `sessionStorage` reliably (not just cookies).  
- **Shared cookie strategy**: Document that all workers read the same auth.json and only re-auth on expiry.
- **Orchestrator script**: Build a deterministic, sequential “planner → ask → aggregate” CLI for cases where parallel browser control is flaky.
- **Test harness**: Add a minimal integration test path for `notebook_query` (smoke test + timeouts).

## Medium-Term (6–12 weeks)

- **Configurable answer timeout**: Patch/fork `notebooklm-mcp` to honor `browser_options.timeout_ms` for answer waits.
- **Token safety**: Enforce output caps and progressive disclosure for large notebooks; document chunking patterns.
- **Stability scoring**: Introduce “judgment” pass to compare NotebookLM outputs with repository state.
- **Bun migration (post-verify)**: Evaluate Bun after the Node-based flow is stable end-to-end; avoid dual lockfiles.

## Long-Term / R&D

- **Session pool + login worker**: Dedicated auth refresher that distributes credentials to workers.
- **Blackboard‑style shared state**: Evaluate iceoryx2-style shared memory for auth/session data (one writer, many readers).
- **Agent gateway**: Centralize auth + routing for multiple tools and notebooks.

## Ownership & Milestones

Assign an owner and milestone once you decide who’s driving each track.

- Quick Wins: Owner TBD · Milestone TBD
- Near-Term: Owner TBD · Milestone TBD
- Medium-Term: Owner TBD · Milestone TBD
- Long-Term: Owner TBD · Milestone TBD
