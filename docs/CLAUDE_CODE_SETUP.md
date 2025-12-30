# Claude Code Plugin Setup

Complete guide for installing and using the NotebookLM plugin for Claude Code.

## Prerequisites

1. **Claude Code CLI** - Install if not already present:
   ```bash
   npm install -g @anthropic/claude-code
   ```

2. **NotebookLM MCP Server** - The plugin requires this MCP server:
   ```bash
   claude mcp add notebooklm -- npx -y notebooklm-mcp@latest
   ```

3. **Google Chrome** - Required for browser automation

4. **Google Account** - With NotebookLM access

## Installation

### Step 1: Add the Marketplace

```bash
# From the repository directory
claude plugin marketplace add ./plugins/notebooklm

# Or from absolute path
claude plugin marketplace add /path/to/notebooklm-claude-integration/plugins/notebooklm
```

### Step 2: Install the Plugin

Choose your installation scope:

```bash
# Project scope (recommended) - available in current project
claude plugin install notebooklm@notebooklm-plugin --scope project

# User scope - available in all projects
claude plugin install notebooklm@notebooklm-plugin --scope user

# Local scope - project-specific, gitignored
claude plugin install notebooklm@notebooklm-plugin --scope local
```

### Step 3: Restart Claude Code

```bash
# Exit and restart to load the plugin
claude
```

## First-Time Authentication

```bash
# Check authentication status
/nlm auth

# Setup authentication (opens browser)
/nlm auth setup
```

A Chrome browser will open for Google login. Complete the login and return to Claude Code.

## Commands

| Command | Description |
|---------|-------------|
| `/nlm ask <question>` | Ask a question to the active notebook |
| `/nlm add <url>` | Add a notebook to library (auto-selects as active) |
| `/nlm list` | List all notebooks in library |
| `/nlm select <name>` | Set active notebook for queries |
| `/nlm auth` | Check authentication status |
| `/nlm auth setup` | First-time authentication |
| `/nlm auth reset` | Clear and re-authenticate |

## Usage Examples

### Add Your First Notebook

```bash
/nlm add https://notebooklm.google.com/notebook/YOUR_NOTEBOOK_ID
```

The plugin will:
1. Query the notebook to discover its content
2. Extract name, description, and topics
3. Add it to your library
4. Set it as the active notebook

### Ask Questions

```bash
/nlm ask "How do I implement OAuth2 in FastAPI?"
```

Response includes:
- Answer from NotebookLM (powered by Gemini)
- Citations from your uploaded documents
- Source references

### Manage Multiple Notebooks

```bash
# List all notebooks
/nlm list

# Switch to a different notebook
/nlm select "FastAPI Documentation"

# Search notebooks by topic
/nlm select python
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
/nlm auth setup
```

### Rate Limited (50 queries/day free tier)
- Wait for daily reset, or
- Use `/nlm auth reset` to switch Google accounts
- Consider Google AI Pro/Ultra for 5x limits

### Wrong Notebook Being Queried
```bash
/nlm list           # See all notebooks
/nlm select <name>  # Switch to correct one
```

### Browser Issues
```bash
/nlm auth reset     # Clears browser state and re-authenticates
```

### Plugin Not Loading
1. Verify installation:
   ```bash
   claude plugin marketplace list
   ```
2. Check plugin is installed with correct scope
3. Restart Claude Code

## MCP Tools Reference

The plugin uses these NotebookLM MCP tools:

| Tool | Purpose |
|------|---------|
| `ask_question` | Query a notebook |
| `add_notebook` | Add notebook to library |
| `list_notebooks` | List all notebooks |
| `select_notebook` | Set active notebook |
| `get_notebook` | Get notebook details |
| `search_notebooks` | Search by query |
| `get_health` | Check auth status |
| `setup_auth` | Initial authentication |
| `re_auth` | Reset authentication |

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
