# Instructions for Claude Code CLI

## Project Overview

This repository contains a complete NotebookLM integration for Claude, providing two integration paths:

1. **Claude Code Plugin** (`plugins/notebooklm/`) - Commands, agents, and skills for Claude Code CLI
2. **Claude Desktop MCP** - Direct MCP server integration

Both integrations use the **NotebookLM MCP Server** (`notebooklm-mcp`) which handles browser automation, authentication, and notebook queries.

## Repository Structure

```
notebooklm-claude-integration/
├── .claude-plugin/                  # Marketplace manifest (repo root)
│   └── marketplace.json             # Points to plugins in this repo
├── plugins/                         # Claude Code Plugin
│   └── notebooklm/
│       ├── .claude-plugin/
│       │   └── plugin.json          # Plugin manifest
│       ├── commands/
│       │   └── nlm.md               # /nlm command (ask, add, list, select, auth)
│       ├── agents/
│       │   └── research-agent.md    # Proactive research agent
│       ├── skills/
│       │   └── notebooklm-patterns/
│       │       └── SKILL.md         # MCP tools reference & troubleshooting
│       └── README.md
│
├── mcp-config/                      # MCP configuration utilities
│   ├── servers.json                 # Unified MCP server config
│   ├── env.example                  # Environment variable template
│   └── README.md                    # Pixi-first install instructions
│
├── docs/                            # Documentation
│   ├── CLAUDE_DESKTOP_SETUP.md
│   ├── CLAUDE_CODE_SETUP.md
│   ├── API_REFERENCE.md
│   └── TROUBLESHOOTING.md
│
├── examples/                        # Usage examples
│
└── tests/                           # Test suite
```

## Plugin Commands

The plugin provides a single `/nlm` command with subcommands:

| Command | Description |
|---------|-------------|
| `/nlm ask <question>` | Ask a question to a notebook by ID |
| `/nlm list` | List all notebooks |
| `/nlm create <name>` | Create a new notebook |
| `/nlm auth rpc` | Save RPC auth cookies |

## MCP Tools Reference

The plugin uses these NotebookLM MCP tools:

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

## Plugin Installation

### Prerequisites

1. **Claude Code CLI** - Install if not already present:
   ```bash
   npm install -g @anthropic-ai/claude-code
   ```

2. **NotebookLM MCP Server (RPC)** - Required for full feature parity:
   ```bash
   uv tool install notebooklm-mcp-server
   claude mcp add --scope user notebooklm-rpc notebooklm-mcp
   ```

3. **Google Chrome** - Required for Playwright automation

4. **Google Account** - With NotebookLM access

### Installation Methods

#### Method 1: From GitHub (Recommended for End Users)

Use this method if you want to install the plugin directly without cloning the repository:

```bash
# 1. Add the marketplace from GitHub
claude plugin marketplace add ray-manaloto/notebooklm-claude-integration

# 2. Install the plugin
claude plugin install notebooklm@notebooklm-plugin --scope project

# 3. Restart Claude Code
claude

# 4. First-time authentication
/nlm auth rpc
```

#### Method 2: From Local Clone (For Development)

Use this method if you've cloned the repository locally:

```bash
# 1. Clone the repository (if not already done)
git clone https://github.com/ray-manaloto/notebooklm-claude-integration.git
cd notebooklm-claude-integration

# 2. Add the marketplace from local path
claude plugin marketplace add .

# 3. Install the plugin
claude plugin install notebooklm@notebooklm-plugin --scope project

# 4. Restart Claude Code
claude

# 5. First-time authentication
/nlm auth rpc
```

### Verifying Installation

```bash
# List registered marketplaces
claude plugin marketplace list

# List installed plugins
claude plugin list

# The output should show:
# - Marketplace: notebooklm-plugin
# - Plugin: notebooklm (with scope: project, user, or local)
```

### Installation Scopes

| Scope | Command Flag | Description |
|-------|--------------|-------------|
| **project** | `--scope project` | Available in current project (recommended) |
| **user** | `--scope user` | Available in all your projects |
| **local** | `--scope local` | Project-specific, gitignored |

### Uninstalling

```bash
# Remove the plugin
claude plugin uninstall notebooklm

# Remove the marketplace (optional)
claude plugin marketplace remove notebooklm-plugin
```

## Architecture

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   Claude    │────────>│   Plugin     │────────>│ NotebookLM  │
│  Code CLI   │         │  Commands    │         │ MCP Server  │
└─────────────┘         └──────────────┘         └─────────────┘
                               │                        │
                               v                        v
                        ┌──────────────┐         ┌─────────────┐
                        │ MCP Tools    │         │ Auth Helper │
                        │ - notebook_list│       │ (cookies)   │
                        │ - notebook_query│      └─────────────┘
                        │ - notebook_add_url│            │
                        │ - studio_status│               v
                        └──────────────┘         ┌─────────────┐
                                                 │ NotebookLM  │
                                                 │   (Gemini)  │
                                                 └─────────────┘
```

The plugin uses MCP tools to communicate with the NotebookLM MCP server, which handles:
- Cookie-based authentication
- Notebook and source management
- Research and Studio artifact generation

## Research Agent

The plugin includes a research agent (`research-agent.md`) that triggers proactively when you ask to:
- "Research" a topic
- "Investigate" something
- "Explore" a concept
- Get a "deep dive" on a subject

Example:
```
Research authentication patterns from my documentation
```

The agent will:
1. Query your active notebook
2. Generate follow-up questions
3. Synthesize a comprehensive answer

## Troubleshooting

### Plugin Not Found / Not Loading

If commands like `/nlm` aren't working:

```bash
# 1. Verify the marketplace is registered
claude plugin marketplace list
# Should show: notebooklm-plugin

# 2. Verify the plugin is installed
claude plugin list
# Should show: notebooklm with your chosen scope

# 3. If marketplace is missing, re-add it:
claude plugin marketplace add ray-manaloto/notebooklm-claude-integration

# 4. If plugin is missing, re-install it:
claude plugin install notebooklm@notebooklm-plugin --scope project

# 5. Restart Claude Code
claude
```

### MCP Server Not Connected

If you see errors about missing MCP tools:

```bash
# 1. Verify MCP server is configured
claude mcp list
# Should show: notebooklm-rpc

# 2. If missing, add the MCP server
uv tool install notebooklm-mcp-server
claude mcp add notebooklm-rpc -- notebooklm-mcp

# 3. Restart Claude Code
claude
```

### Not Authenticated

```bash
# Save RPC auth cookies
/nlm auth rpc

# Run notebooklm-mcp-auth to refresh cookies if needed
notebooklm-mcp-auth
```

### Rate Limited (50 queries/day free tier)
- Wait for daily reset (midnight UTC), or
- Re-run `notebooklm-mcp-auth` with a different Google account
- Consider Google AI Pro/Ultra for 5x limits

### Wrong Notebook Being Queried

```bash
/nlm list           # See all notebooks and IDs
# Re-run /nlm ask with the correct notebook_id
```

### Common Installation Mistakes

| Issue | Solution |
|-------|----------|
| Wrong marketplace path | Use `.` from repo root (marketplace.json is at `.claude-plugin/marketplace.json`) |
| Plugin not found during install | Ensure marketplace is added first with `marketplace add` |
| Scope confusion | Use `--scope project` for most cases |
| Old plugin version | Remove and re-add marketplace to update |

## Limits

| Resource | Free Tier | Pro/Ultra |
|----------|-----------|-----------|
| Daily Queries | 50 | 250 |
| Notebooks | 100 | 500 |
| Sources per Notebook | 50 | 100 |

## GitHub Repository

- **URL**: https://github.com/ray-manaloto/notebooklm-claude-integration
- **License**: MIT
- **Version**: 1.0.0

## Related Projects

- [NotebookLM MCP Server](https://github.com/PleasePrompto/notebooklm-mcp) - MCP server implementation
- [Claude Code](https://www.anthropic.com/claude/code) - Official Claude Code CLI
- [wshobson/agents](https://github.com/wshobson/agents) - Plugin patterns reference
