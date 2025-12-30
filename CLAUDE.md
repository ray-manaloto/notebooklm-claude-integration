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
│   ├── install-desktop.sh           # Deploy to Claude Desktop
│   ├── install-code.sh              # Deploy to Claude Code
│   └── update-all.sh                # Update both environments
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
| `/nlm ask <question>` | Ask a question to the active notebook |
| `/nlm add <url>` | Add a notebook to your library (auto-selects as active) |
| `/nlm list` | List all notebooks in your library |
| `/nlm select <name>` | Set active notebook for queries |
| `/nlm auth` | Check authentication status |
| `/nlm auth setup` | First-time authentication (opens browser) |
| `/nlm auth reset` | Clear and re-authenticate |

## MCP Tools Reference

The plugin uses these NotebookLM MCP tools:

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

## Plugin Installation

### Prerequisites

1. **Claude Code CLI** - Install if not already present:
   ```bash
   npm install -g @anthropic-ai/claude-code
   ```

2. **NotebookLM MCP Server** - Required for browser automation:
   ```bash
   claude mcp add notebooklm -- npx -y notebooklm-mcp@latest
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
/nlm auth setup
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
/nlm auth setup
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
                        │ MCP Tools    │         │  Playwright │
                        │ - ask_question│        │   Browser   │
                        │ - add_notebook│        └─────────────┘
                        │ - list_notebooks│             │
                        │ - select_notebook│            v
                        └──────────────┘         ┌─────────────┐
                                                 │ NotebookLM  │
                                                 │   (Gemini)  │
                                                 └─────────────┘
```

The plugin uses MCP tools to communicate with the NotebookLM MCP server, which handles:
- Browser automation via Playwright
- Google authentication
- Session management
- Notebook library storage

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
# Should show: notebooklm

# 2. If missing, add the MCP server
claude mcp add notebooklm -- npx -y notebooklm-mcp@latest

# 3. Restart Claude Code
claude
```

### Not Authenticated

```bash
# Check authentication status
/nlm auth

# Setup authentication (opens browser)
/nlm auth setup
```

### Rate Limited (50 queries/day free tier)
- Wait for daily reset (midnight UTC), or
- Use `/nlm auth reset` to switch Google accounts
- Consider Google AI Pro/Ultra for 5x limits

### Wrong Notebook Being Queried

```bash
/nlm list           # See all notebooks with [ACTIVE] marker
/nlm select <name>  # Switch to correct one
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
