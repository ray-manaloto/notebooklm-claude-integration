# NotebookLM Plugin for Claude Code

> Query Google NotebookLM notebooks for source-grounded, citation-backed answers powered by Gemini AI.

**1 command** | **1 agent** | **1 skill** | **9 MCP tools**

## Overview

This plugin integrates NotebookLM with Claude Code, enabling you to:

- **Query notebooks** for hallucination-free answers with citations
- **Manage a library** of multiple notebooks by topic
- **Research deeply** with automatic follow-up questions
- **Switch contexts** seamlessly between documentation sources

## Quick Start

```bash
# 1. Install the MCP server (prerequisite)
claude mcp add notebooklm -- npx -y notebooklm-mcp@latest

# 2. Add the marketplace
claude plugin marketplace add https://github.com/ray-manaloto/notebooklm-claude-integration/plugins/notebooklm

# 3. Install the plugin
claude plugin install notebooklm@notebooklm-plugin --scope project

# 4. Restart Claude Code and authenticate
/nlm auth setup

# 5. Add your first notebook
/nlm add https://notebooklm.google.com/notebook/YOUR_ID

# 6. Start querying
/nlm ask "How do I implement authentication?"
```

## Components

### Commands (1)

| Command | Description |
|---------|-------------|
| `/nlm` | Unified command for querying notebooks, managing library, and authentication |

**Subcommands:**

| Subcommand | Usage | Description |
|------------|-------|-------------|
| `ask` | `/nlm ask "question"` | Query the active notebook |
| `add` | `/nlm add <url>` | Add notebook to library (auto-selects as active) |
| `list` | `/nlm list` | List all notebooks in library |
| `select` | `/nlm select <name>` | Set active notebook for queries |
| `auth` | `/nlm auth [setup\|reset]` | Manage Google authentication |

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
| `mcp__notebooklm__ask_question` | Query a notebook |
| `mcp__notebooklm__add_notebook` | Add notebook to library |
| `mcp__notebooklm__list_notebooks` | List all notebooks |
| `mcp__notebooklm__select_notebook` | Set active notebook |
| `mcp__notebooklm__get_notebook` | Get notebook details |
| `mcp__notebooklm__search_notebooks` | Search by query |
| `mcp__notebooklm__get_health` | Check auth status |
| `mcp__notebooklm__setup_auth` | Initial authentication |
| `mcp__notebooklm__re_auth` | Reset authentication |

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
/nlm auth

# Add a documentation notebook
/nlm add https://notebooklm.google.com/notebook/abc123

# Ask questions
/nlm ask "How do I implement OAuth2?"
/nlm ask "What are the rate limiting strategies?"
```

### Multiple Notebooks

```bash
# Add multiple notebooks
/nlm add https://notebooklm.google.com/notebook/docs1
/nlm add https://notebooklm.google.com/notebook/docs2

# List and switch
/nlm list
/nlm select "API Documentation"
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

## Troubleshooting

### Authentication Issues

```bash
# Check status
/nlm auth

# Setup (opens browser)
/nlm auth setup

# Reset and re-authenticate
/nlm auth reset
```

### Rate Limit Exceeded

- Wait for daily reset (midnight UTC), or
- Use `/nlm auth reset` to switch Google accounts

### Wrong Notebook

```bash
/nlm list           # See all notebooks with [ACTIVE] marker
/nlm select <name>  # Switch to correct one
```

### MCP Server Not Found

```bash
claude mcp add notebooklm -- npx -y notebooklm-mcp@latest
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
```

## Requirements

- **Claude Code CLI** - v1.0+
- **NotebookLM MCP Server** - `npx -y notebooklm-mcp@latest`
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
