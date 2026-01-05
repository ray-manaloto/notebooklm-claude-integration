# NotebookLM Plugin for Claude Code

> Query Google NotebookLM notebooks for source-grounded, citation-backed answers powered by Gemini AI.

**1 command** | **1 agent** | **1 skill** | **31 MCP tools**

## Overview

This plugin integrates NotebookLM with Claude Code, enabling you to:

- **Query notebooks** for hallucination-free answers with citations
- **Manage notebooks and sources** by topic
- **Research deeply** with automatic follow-up questions
- **Switch contexts** seamlessly between documentation sources

## Quick Start

```bash
# 1. Install the MCP server (prerequisite)
uv tool install notebooklm-mcp-server
claude mcp add notebooklm-rpc -- notebooklm-mcp

# 2. Add the marketplace from GitHub
claude plugin marketplace add ray-manaloto/notebooklm-claude-integration

# 3. Install the plugin
claude plugin install notebooklm@notebooklm-plugin --scope project

# 4. Authenticate (one-time)
notebooklm-mcp-auth
/nlm auth rpc

# 5. List notebooks and note the ID
/nlm list

# 6. Start querying
/nlm ask "How do I implement authentication?"
```

### Verify Installation

```bash
claude plugin marketplace list  # Should show: notebooklm-plugin
claude plugin list              # Should show: notebooklm
```

## Components

### Commands (1)

| Command | Description |
|---------|-------------|
| `/nlm` | Unified command for querying notebooks, managing library, and authentication |

**Subcommands:**

| Subcommand | Usage | Description |
|------------|-------|-------------|
| `ask` | `/nlm ask "question"` | Query a notebook by ID |
| `ask-all` | `/nlm ask-all "question"` | Query all notebooks in parallel |
| `list` | `/nlm list` | List all notebooks |
| `create` | `/nlm create <name>` | Create a new notebook |
| `rename` | `/nlm rename <id> <name>` | Rename a notebook |
| `delete` | `/nlm delete <id>` | Delete a notebook (confirm) |
| `source` | `/nlm source <add-url|add-text|add-drive|list|sync|delete> ...` | Manage notebook sources |
| `research` | `/nlm research <start|status|import> ...` | Discover/import sources |
| `studio` | `/nlm studio <audio|video|infographic|slides|status|delete> ...` | Create/manage Studio artifacts |
| `describe` | `/nlm describe <notebook|source> <id>` | Summarize notebook or source |
| `configure` | `/nlm configure <goal|length|prompt> ...` | Configure chat settings |
| `auth` | `/nlm auth rpc` | Save RPC auth cookies |

Notes:
- `add-drive` expects a Google Doc URL; the document ID is extracted from `/d/<id>`.
- Source sync/delete and Studio create/delete require confirmation.

### Agents (1)

| Agent | Model | Trigger | Description |
|-------|-------|---------|-------------|
| `research-agent` | sonnet | PROACTIVE | Deep research with automatic follow-up questions. Triggers on "research", "investigate", "explore", "deep dive" |

### Skills (1)

| Skill | Description |
|-------|-------------|
| `notebooklm-patterns` | MCP tools reference, troubleshooting guide, and usage patterns |

## MCP Tools Reference

The plugin uses these NotebookLM MCP server tools:

| Tool | Purpose |
|------|---------|
| `mcp__notebooklm-rpc__save_auth_tokens` | Persist auth cookies |
| `mcp__notebooklm-rpc__notebook_list` | List all notebooks |
| `mcp__notebooklm-rpc__notebook_create` | Create a new notebook |
| `mcp__notebooklm-rpc__notebook_get` | Get notebook details |
| `mcp__notebooklm-rpc__notebook_describe` | Summarize notebook content |
| `mcp__notebooklm-rpc__notebook_query` | Ask a question |
| `mcp__notebooklm-rpc__notebook_add_url` | Add URL/YouTube source |
| `mcp__notebooklm-rpc__notebook_add_text` | Add text source |
| `mcp__notebooklm-rpc__notebook_add_drive` | Add Drive source |
| `mcp__notebooklm-rpc__source_list_drive` | List Drive sources w/ freshness |
| `mcp__notebooklm-rpc__source_sync_drive` | Sync stale Drive sources |
| `mcp__notebooklm-rpc__source_delete` | Delete a source |
| `mcp__notebooklm-rpc__source_describe` | Summarize a source |
| `mcp__notebooklm-rpc__research_start` | Start research |
| `mcp__notebooklm-rpc__research_status` | Poll research progress |
| `mcp__notebooklm-rpc__research_import` | Import research sources |
| `mcp__notebooklm-rpc__chat_configure` | Configure chat behavior |
| `mcp__notebooklm-rpc__audio_overview_create` | Generate audio overview |
| `mcp__notebooklm-rpc__video_overview_create` | Generate video overview |
| `mcp__notebooklm-rpc__infographic_create` | Generate infographic |
| `mcp__notebooklm-rpc__slide_deck_create` | Generate slide deck |
| `mcp__notebooklm-rpc__studio_status` | Check studio job status |
| `mcp__notebooklm-rpc__studio_delete` | Delete studio artifacts |

## Installation Options

```bash
# Project scope (recommended) - available in current project
claude plugin install notebooklm@notebooklm-plugin --scope project

# User scope - available in all projects
claude plugin install notebooklm@notebooklm-plugin --scope user

# Local scope - project-specific, gitignored
claude plugin install notebooklm@notebooklm-plugin --scope local
```

## Usage Examples

### Basic Workflow

```bash
# Check authentication
/nlm auth rpc

# List notebooks and note an ID
/nlm list

# Ask questions (use the notebook_id)
/nlm ask "How do I implement OAuth2?"
/nlm ask "What are the rate limiting strategies?"
```

### Multiple Notebooks

```bash
# List and compare
/nlm list
```

### Research Agent (Proactive)

The research agent activates automatically:

```
"Research authentication patterns from my documentation"
"Investigate the error handling approaches"
"Deep dive into the caching strategies"
```

The agent will:
1. Query the active notebook with your question
2. Generate follow-up questions based on initial findings
3. Synthesize comprehensive research results with citations

## Rate Limits

| Resource | Free Tier | Pro/Ultra |
|----------|-----------|-----------|
| Daily Queries | 50 | 250 |
| Notebooks | 100 | 500 |
| Sources per Notebook | 50 | 100 |

## Authentication Options

The plugin supports multiple authentication backends, tried in priority order:

| Backend | Priority | Description | Best For |
|---------|----------|-------------|----------|
| **CDP** | 1 | Connect to existing Chrome session | Daily use - seamless |
| **Keychain** | 2 | macOS Keychain stored cookies | Headless/automation |
| **Persistent** | 3 | Playwright browser profile | Cross-platform fallback |
| **Manual** | 4 | Interactive browser login | First-time setup |

### Recommended Setup (Best Experience)

```bash
# 1. Start Chrome with remote debugging
open -a "Google Chrome" --args --remote-debugging-port=9222

# 2. Login to NotebookLM in Chrome (one-time)
# Navigate to https://notebooklm.google.com and login

# 3. Now queries use your existing session - no popups!
/nlm ask "How do I implement OAuth?"
```

### Add to Shell Profile (Optional)

```bash
# Add to ~/.zshrc or ~/.bashrc
alias chrome-debug='open -a "Google Chrome" --args --remote-debugging-port=9222'

# Then just run: chrome-debug
```

## Troubleshooting

### Authentication Issues

```bash
# Check status (shows all backends)
/nlm auth

# View CDP setup instructions
/nlm auth cdp

# Check keychain status (macOS)
# Save cookies for RPC
/nlm auth rpc
```

### Rate Limit Exceeded

- Wait for daily reset (midnight UTC), or
- Re-run `notebooklm-mcp-auth` with a different Google account

### Wrong Notebook

```bash
/nlm list           # See all notebooks and their IDs
# Re-run /nlm ask with the correct notebook_id
```

### MCP Server Not Found

```bash
uv tool install notebooklm-mcp-server
claude mcp add notebooklm-rpc -- notebooklm-mcp
# Restart Claude Code
```

## Plugin Structure

```
plugins/notebooklm/
├── .claude-plugin/
│   ├── plugin.json          # Plugin manifest
│   └── marketplace.json     # Marketplace manifest
├── agents/
│   └── research-agent.md    # Proactive research agent
├── commands/
│   └── nlm.md               # /nlm command with subcommands
├── skills/
│   └── notebooklm-patterns/
│       └── SKILL.md         # MCP tools & troubleshooting
└── README.md

auth-layer/                   # Multi-backend authentication layer
├── src/
│   ├── backends/
│   │   ├── cdp.ts           # Chrome DevTools Protocol
│   │   ├── keychain.ts      # macOS Keychain storage
│   │   └── persistent.ts    # Playwright persistent context
│   ├── auth-manager.ts      # Main orchestrator
│   ├── cli.ts               # nlm-auth CLI tool
│   └── types.ts             # TypeScript types
├── package.json
└── README.md
```

## Requirements

- **Claude Code CLI** - v1.0+
- **NotebookLM MCP Server** - `notebooklm-mcp-server`
- **Google Chrome** - For browser automation
- **Google Account** - With NotebookLM access

## Security

- All credentials stored locally by MCP server
- Browser session managed by Playwright
- No data sent to third parties
- Consider using a dedicated Google account

## Related Documentation

- [Claude Code Setup Guide](../../docs/CLAUDE_CODE_SETUP.md)
- [API Reference](../../docs/API_REFERENCE.md)
- [Troubleshooting Guide](../../docs/TROUBLESHOOTING.md)
- [NotebookLM MCP Server](https://github.com/PleasePrompto/notebooklm-mcp)

## License

MIT
