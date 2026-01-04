# Claude Code Plugin Setup

Complete guide for installing and using the NotebookLM plugin for Claude Code.

## Prerequisites

1. **Claude Code CLI** - Install if not already present:
   ```bash
   npm install -g @anthropic/claude-code
   ```

2. **NotebookLM MCP Server** - The plugin requires this MCP server:
   ```bash
   uv tool install notebooklm-mcp-server
   claude mcp add notebooklm-rpc -- notebooklm-mcp
   ```

3. **Google Chrome** - Required for browser automation

4. **Google Account** - With NotebookLM access

## Installation

### Method 1: From GitHub (Recommended)

This is the easiest way to install - no need to clone the repository:

```bash
# 1. Add the marketplace from GitHub
claude plugin marketplace add ray-manaloto/notebooklm-claude-integration

# 2. Install the plugin
claude plugin install notebooklm@notebooklm-plugin --scope project

# 3. Restart Claude Code
claude
```

### Method 2: From Local Clone (For Development)

Use this method if you're contributing to the plugin or need to modify it:

```bash
# 1. Clone the repository
git clone https://github.com/ray-manaloto/notebooklm-claude-integration.git
cd notebooklm-claude-integration

# 2. Add the marketplace from local path
claude plugin marketplace add .

# 3. Install the plugin
claude plugin install notebooklm@notebooklm-plugin --scope project

# 4. Restart Claude Code
claude
```

### Installation Scopes

| Scope | Command | Description |
|-------|---------|-------------|
| `project` | `--scope project` | Available in current project (recommended) |
| `user` | `--scope user` | Available in all projects |
| `local` | `--scope local` | Project-specific, gitignored |

### Verifying Installation

```bash
# Check marketplace is added
claude plugin marketplace list
# Should show: notebooklm-plugin

# Check plugin is installed
claude plugin list
# Should show: notebooklm with your chosen scope
```

## First-Time Authentication

```bash
# Run notebooklm-mcp-auth and complete login
notebooklm-mcp-auth

# Save RPC auth cookies
/nlm auth rpc
```

A Chrome browser will open for Google login. Complete the login and return to Claude Code.

## Commands

| Command | Description |
|---------|-------------|
| `/nlm ask <question>` | Ask a question to a notebook by ID |
| `/nlm list` | List all notebooks |
| `/nlm create <name>` | Create a new notebook |
| `/nlm auth rpc` | Save RPC auth cookies |

## Usage Examples

### List Notebooks

```bash
/nlm list
```

### Ask Questions

```bash
/nlm ask "Notebook ID: <id>. How do I implement OAuth2 in FastAPI?"
```

Response includes:
- Answer from NotebookLM (powered by Gemini)
- Citations from your uploaded documents
- Source references

### Manage Multiple Notebooks

```bash
# List all notebooks
/nlm list

# Use notebook_id in your ask prompt
/nlm ask "Notebook ID: <id>. Summarize the key sources."
```

## Research Agent

The plugin includes a research agent that triggers proactively when you ask to:
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

## Plugin Structure

```
plugins/notebooklm/
├── .claude-plugin/
│   ├── plugin.json          # Plugin manifest
│   └── marketplace.json     # Marketplace manifest
├── commands/
│   └── nlm.md               # /nlm command with subcommands
├── agents/
│   └── research-agent.md    # Proactive research agent
├── skills/
│   └── notebooklm-patterns/
│       └── SKILL.md         # MCP tools reference & troubleshooting
└── README.md
```

## Troubleshooting

### Not Authenticated
```bash
notebooklm-mcp-auth
/nlm auth rpc
```

### Rate Limited (50 queries/day free tier)
- Wait for daily reset, or
- Re-run `notebooklm-mcp-auth` with a different Google account
- Consider Google AI Pro/Ultra for 5x limits

### Wrong Notebook Being Queried
```bash
/nlm list           # See all notebooks
# Re-run /nlm ask with the correct notebook_id
```

### Browser Issues
```bash
notebooklm-mcp-auth # Refresh cookies
```

### Plugin Not Loading
1. Verify marketplace is added:
   ```bash
   claude plugin marketplace list
   # Should show: notebooklm-plugin
   ```
2. Verify plugin is installed:
   ```bash
   claude plugin list
   # Should show: notebooklm
   ```
3. Restart Claude Code
4. If still not working, try reinstalling:
   ```bash
   claude plugin uninstall notebooklm
   claude plugin marketplace remove notebooklm-plugin
   # Then follow installation steps again
   ```

### MCP Server Not Connected
```bash
# Verify MCP server is added
claude mcp list
# Should show: notebooklm

# If not present, add it
uv tool install notebooklm-mcp-server
claude mcp add notebooklm-rpc -- notebooklm-mcp

# Restart Claude Code after adding
claude
```

## Uninstalling

```bash
# Remove the plugin
claude plugin uninstall notebooklm

# Remove the marketplace
claude plugin marketplace remove notebooklm-plugin

# Optionally remove the MCP server
claude mcp remove notebooklm-rpc
```

## MCP Tools Reference

The plugin uses these NotebookLM MCP tools:

| Tool | Purpose |
|------|---------|
| `notebook_list` | List all notebooks |
| `notebook_create` | Create a new notebook |
| `notebook_get` | Get notebook details |
| `notebook_describe` | Summarize notebook content |
| `notebook_query` | Ask a question |
| `notebook_add_url` | Add URL/YouTube source |
| `notebook_add_text` | Add text source |
| `notebook_add_drive` | Add Drive source |
| `source_list_drive` | List Drive sources w/ freshness |
| `source_sync_drive` | Sync stale Drive sources |
| `source_delete` | Delete a source |
| `source_describe` | Summarize a source |
| `research_start` | Start research |
| `research_status` | Poll research progress |
| `research_import` | Import research sources |
| `chat_configure` | Configure chat behavior |
| `audio_overview_create` | Generate audio overview |
| `video_overview_create` | Generate video overview |
| `infographic_create` | Generate infographic |
| `slide_deck_create` | Generate slide deck |
| `studio_status` | Check studio job status |
| `studio_delete` | Delete studio artifacts |

## Limits

| Resource | Free Tier | Pro/Ultra |
|----------|-----------|-----------|
| Daily Queries | 50 | 250 |
| Notebooks | 100 | 500 |
| Sources per Notebook | 50 | 100 |

## Security

- All credentials stored locally by MCP server
- Browser session managed by Playwright
- No data sent to third parties
- Consider using a dedicated Google account

## Related Documentation

- [Main README](../README.md) - Project overview
- [Troubleshooting](TROUBLESHOOTING.md) - Common issues
- [API Reference](API_REFERENCE.md) - All commands
- [Claude Desktop Setup](CLAUDE_DESKTOP_SETUP.md) - MCP server setup
