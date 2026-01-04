# NotebookLM MCP Timeouts

## Summary

Some notebooks consistently time out in `notebook_query`. The MCP server uses a fixed 120s wait for streaming answers.

## Current Evidence

- `notebook_query` uses a hardcoded 120s wait for streaming answers.
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
