# API Reference

Complete reference for all NotebookLM Claude Integration commands and MCP tools.

## Table of Contents

- [Slash Commands](#slash-commands)
- [MCP Tools](#mcp-tools)
- [Pixi Tasks (RPC Runner)](#pixi-tasks-rpc-runner)
- [Data Structures](#data-structures)
- [Error Handling](#error-handling)

---

## Slash Commands

### `/nlm`

Main command for NotebookLM RPC interactions. Subcommands cover notebooks, sources, research, and studio artifacts.

**Common usage:**
```bash
/nlm list
/nlm ask "What does this notebook say about OAuth?"
/nlm create "API Research"
/nlm source add-url <notebook_id> <url>
/nlm research start <notebook_id> <query>
/nlm studio audio <notebook_id>
/nlm auth rpc
```

**Notes:**
- Use `/nlm list` to fetch notebook IDs for `/nlm ask`.
- Authentication is cookie-based via notebooklm-mcp-auth, then `/nlm auth rpc` to save tokens.

---

## MCP Tools (notebooklm-mcp RPC)

The plugin uses the `notebooklm-mcp` RPC toolset for full feature parity:

### Authentication
- `mcp__notebooklm-rpc__save_auth_tokens`

### Notebooks
- `mcp__notebooklm-rpc__notebook_list`
- `mcp__notebooklm-rpc__notebook_create`
- `mcp__notebooklm-rpc__notebook_get`
- `mcp__notebooklm-rpc__notebook_describe`
- `mcp__notebooklm-rpc__notebook_rename`
- `mcp__notebooklm-rpc__notebook_delete`
- `mcp__notebooklm-rpc__notebook_query`

### Sources
- `mcp__notebooklm-rpc__notebook_add_url`
- `mcp__notebooklm-rpc__notebook_add_text`
- `mcp__notebooklm-rpc__notebook_add_drive`
- `mcp__notebooklm-rpc__source_list_drive`
- `mcp__notebooklm-rpc__source_sync_drive`
- `mcp__notebooklm-rpc__source_delete`
- `mcp__notebooklm-rpc__source_describe`

### Research
- `mcp__notebooklm-rpc__research_start`
- `mcp__notebooklm-rpc__research_status`
- `mcp__notebooklm-rpc__research_import`

### Chat Configuration
- `mcp__notebooklm-rpc__chat_configure`

### Studio
- `mcp__notebooklm-rpc__audio_overview_create`
- `mcp__notebooklm-rpc__video_overview_create`
- `mcp__notebooklm-rpc__infographic_create`
- `mcp__notebooklm-rpc__slide_deck_create`
- `mcp__notebooklm-rpc__studio_status`
- `mcp__notebooklm-rpc__studio_delete`

---

## Pixi Tasks (RPC Runner)

Each RPC tool is mapped to a `pixi run nlm-*` task using `tools/nlm_tasks.py`.  
Pass arguments via `NLM_ARGS_JSON` or `--args`. Destructive tools require `NLM_CONFIRM=1`.

**Examples:**
```bash
NLM_ARGS_JSON='{"notebook_id":"abc","question":"What changed?"}' \
pixi run nlm-notebook-query

NLM_CONFIRM=1 NLM_ARGS_JSON='{"notebook_id":"abc"}' \
pixi run nlm-notebook-delete
```

**Task map (1:1 with MCP tools):**
```text
pixi run nlm-save-auth-tokens
pixi run nlm-notebook-list
pixi run nlm-notebook-create
pixi run nlm-notebook-get
pixi run nlm-notebook-describe
pixi run nlm-source-describe
pixi run nlm-notebook-rename
pixi run nlm-chat-configure
pixi run nlm-notebook-delete
pixi run nlm-notebook-add-url
pixi run nlm-notebook-add-text
pixi run nlm-notebook-add-drive
pixi run nlm-notebook-query
pixi run nlm-source-list-drive
pixi run nlm-source-sync-drive
pixi run nlm-source-delete
pixi run nlm-research-start
pixi run nlm-research-status
pixi run nlm-research-import
pixi run nlm-audio-overview-create
pixi run nlm-video-overview-create
pixi run nlm-infographic-create
pixi run nlm-slide-deck-create
pixi run nlm-studio-status
pixi run nlm-studio-delete
```

## Data Structures

### Notebook Object

```json
{
  "id": "string",
  "name": "string",
  "description": "string",
  "url": "string",
  "topics": ["string"],
  "added": "ISO8601 timestamp",
  "active": "boolean"
}
```

### Query Response

```json
{
  "answer": "string",
  "citations": [
    {
      "source": "string",
      "excerpt": "string"
    }
  ],
  "notebook_id": "string",
  "session_id": "string"
}
```

### Health Status

```json
{
  "authenticated": "boolean",
  "activeSessions": "number",
  "ready": "boolean"
}
```

---

## Error Handling

### Common Errors

| Error | Cause | Resolution |
|-------|-------|------------|
| `Not authenticated` | No valid session | Run `notebooklm-mcp-auth` then `/nlm auth rpc` |
| `Notebook not found` | Invalid notebook ID | Check `/nlm list` for valid IDs |
| `Rate limit exceeded` | 50 daily queries (free tier) | Wait for reset or re-auth with another account |
| `Browser error` | Auth helper issue | Check Chrome installation |
| `Network error` | NotebookLM unreachable | Check internet connection |

### Rate Limits

| Resource | Free Tier | Pro/Ultra |
|----------|-----------|-----------|
| Daily Queries | 50 | 250 |
| Notebooks | 100 | 500 |
| Sources per Notebook | 50 | 100 |

---

## Examples

### Complete Workflow

```bash
# 1. Setup authentication (first time only)
notebooklm-mcp-auth
/nlm auth rpc

# 2. List notebooks
/nlm list

# 3. Query the notebook
/nlm ask "Notebook ID: <id>. How do I implement rate limiting?"
```

### Research Agent Trigger

The research agent activates automatically for research-related queries:

```
Research authentication patterns from my documentation
```

The agent will:
1. Query the active notebook
2. Generate follow-up questions
3. Synthesize a comprehensive answer with citations

---

## Plugin Structure

```
plugins/notebooklm/
├── .claude-plugin/
│   ├── plugin.json          # Plugin manifest
│   └── marketplace.json     # Marketplace manifest
├── commands/
│   └── nlm.md               # /nlm command definition
├── agents/
│   └── research-agent.md    # Proactive research agent
├── skills/
│   └── notebooklm-patterns/
│       └── SKILL.md         # MCP tools reference
└── README.md
```

---

For more help, see:
- [Claude Code Setup](CLAUDE_CODE_SETUP.md) - Installation guide
- [Troubleshooting](TROUBLESHOOTING.md) - Common issues
- [Main README](../README.md) - Project overview
