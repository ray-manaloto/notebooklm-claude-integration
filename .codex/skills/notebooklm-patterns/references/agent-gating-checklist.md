# Agent Gating Checklist

Use this checklist for multi-agent workflows to prevent hallucinated completion and enforce evidence-based handoffs.

## Before Handoff (Producer Agent)

- Produce concrete artifacts (files, command outputs, or tool results).
- List the exact paths or IDs for artifacts created.
- Include citations or tool results that justify the changes.

## Handoff Validation (Coordinator)

- Verify artifacts exist (paths or tool IDs).
- If a change claims tests were run, require the exact command and output summary.
- If NotebookLM research was used, require the cited snippets or session IDs.

## Failure Modes

- If any artifact is missing, re-run or ask for clarification.
- If outputs are off-topic or cite unrelated sources, re-ask with a narrower prompt.
- If a tool failed, do not proceed until rerun is successful.
