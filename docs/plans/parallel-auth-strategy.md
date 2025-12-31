# Parallel Auth Strategy (NotebookLM MCP)

## Goal

Enable one login process to establish credentials and allow parallel subagents/processes to reuse them without re-login.

## Recommended Approach (Current MCP Capabilities)

- Use a **persistent Chrome profile** as the base login profile.
- Set **multi-instance strategy** to allow parallel workers while preserving auth:
  - `NOTEBOOK_PROFILE_STRATEGY=auto`
  - `NOTEBOOK_CLONE_PROFILE=true`
- Run a **single login bootstrap** first to populate the base profile.
- Launch parallel workers after the bootstrap completes.

## Why This Works

- The MCP server uses a shared persistent context, so all sessions within one process share auth.
- With `clone_profile_on_isolated`, isolated profiles inherit the logged-in state from the base profile.
- Avoids needing multiple interactive logins.

## Proposed Workflow

1. **Bootstrap login** (single process, interactive once).
2. **Spawn parallel workers** with `NOTEBOOK_PROFILE_STRATEGY=auto` and `NOTEBOOK_CLONE_PROFILE=true`.
3. **Cleanup** isolated profiles via `NOTEBOOK_INSTANCE_TTL_HOURS` / `NOTEBOOK_INSTANCE_MAX_COUNT`.

## Open Decisions

- Whether to default `NOTEBOOK_CLONE_PROFILE=true` in examples/scripts.
- Whether to add a script that performs bootstrap + fan-out in a single command.
