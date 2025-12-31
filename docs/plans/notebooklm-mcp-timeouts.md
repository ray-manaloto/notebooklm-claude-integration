# NotebookLM MCP Timeouts

## Summary

Some notebooks consistently time out in `ask_question`. The MCP server uses a fixed 120s wait for streaming answers, which ignores `browser_options.timeout_ms`.

## Current Evidence

- `ask_question` passes `browser_options.timeout_ms` → `CONFIG.browserTimeout`, but that only affects page navigation, not answer wait.
- `waitForLatestAnswer` uses a hardcoded 120s timeout in `src/session/browser-session.ts` (upstream `notebooklm-mcp`).
- Iceoryx notebook timed out repeatedly; other notebooks returned successfully.

## Options

1. **Fork + pin**: Add an `answer_timeout_ms` option (or reuse `browser_options.timeout_ms`) in the MCP server and document it in this repo.
2. **Vendor**: Copy the MCP server into this repo and maintain changes here.
3. **Live with it**: Keep a retry strategy and document the limit.

## Next Steps (Deferred)

- Decide on fork vs vendor.
- If forking, add configurable answer timeout + new env var for default.
- Update README/docs to reflect the new knob and troubleshooting guidance.
