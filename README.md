# NotebookLM Claude Integration

Complete integration of Google NotebookLM with Claude AI through both Claude Desktop (MCP) and Claude Code (Plugin).

> **Status**: Production-ready ✅ | **Built**: Dec 2024 | **Tested**: Fully functional

## What This Is

This project provides **two complete integrations** for using NotebookLM with Claude:

1. **Claude Desktop** - MCP Server for conversational interface
2. **Claude Code CLI** - Plugin for development workflow

Both allow you to query your NotebookLM notebooks directly from Claude, getting citation-backed answers from Gemini without leaving your workflow.

## Quick Start

### AI Agent Step-by-Step (Codex CLI)

Use this sequence when an agent needs to verify the NotebookLM integration end-to-end.

1. Install and enable the MCP server:
   ```bash
   codex mcp add notebooklm -- npx -y notebooklm-mcp@latest
   ```
2. Authenticate once (browser login). The auth layer will persist cookies:
   ```bash
   codex --enable skills exec "Use the notebooklm-patterns skill. Check auth with mcp__notebooklm__get_health. If not authenticated, run mcp__notebooklm__setup_auth and wait."
   ```
3. Run the full E2E test (downloads the skill from GitHub into a temp repo and queries a notebook):
   ```bash
   make codex-skill-e2e
   ```
4. Optional overrides:
   ```bash
   NOTEBOOK_URL="https://notebooklm.google.com/notebook/<id>" \
   NOTEBOOK_NAME="My Test Notebook" \
   NOTEBOOK_DESC="Notebook for testing Codex + NotebookLM." \
   NOTEBOOK_ID="my-test-notebook" \
   make codex-skill-e2e
   ```

### For Claude Code (Plugin)

```bash
# 1. Ensure NotebookLM MCP server is configured
claude mcp add notebooklm -- npx -y notebooklm-mcp@latest

# 2. Add the plugin marketplace from GitHub
claude plugin marketplace add ray-manaloto/notebooklm-claude-integration/plugins/notebooklm

# 3. Install the plugin (project scope)
claude plugin install notebooklm@notebooklm-plugin --scope project

# 4. Verify installation
claude plugin marketplace list  # Should show: notebooklm-plugin
claude plugin list              # Should show: notebooklm

# 5. Restart Claude Code, then:
/nlm auth setup                    # First-time authentication
/nlm add <notebooklm-url>          # Add a notebook
/nlm ask "Your question"           # Query the notebook
```

**For local development** (if you cloned this repo):
```bash
claude plugin marketplace add ./plugins/notebooklm
```

### For Claude Desktop (MCP)

```bash
npm install -g notebooklm-mcp
```

Add to `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "notebooklm": {
      "command": "npx",
      "args": ["-y", "notebooklm-mcp@latest"]
    }
  }
}
```

Restart Claude Desktop, then:
```
Add my notebook: https://notebooklm.google.com/notebook/YOUR_ID
```

## Repository Structure

```
notebooklm-claude-integration/
├── plugins/                         # Claude Code Plugin
│   └── notebooklm/
│       ├── .claude-plugin/
│       │   ├── plugin.json          # Plugin manifest
│       │   └── marketplace.json     # Marketplace manifest
│       ├── commands/
│       │   └── nlm.md               # /nlm command (ask, add, list, select, auth)
│       ├── agents/
│       │   └── research-agent.md    # Proactive research agent
│       ├── skills/
│       │   └── notebooklm-patterns/
│       │       └── SKILL.md         # MCP tools reference & troubleshooting
│       └── README.md
│
├── auth-layer/                      # Multi-backend authentication (NEW)
│   ├── src/
│   │   ├── backends/
│   │   │   ├── cdp.ts               # Chrome DevTools Protocol
│   │   │   ├── keychain.ts          # macOS Keychain storage
│   │   │   └── persistent.ts        # Playwright persistent context
│   │   ├── auth-manager.ts          # Main orchestrator
│   │   ├── cli.ts                   # nlm-auth CLI tool
│   │   └── types.ts                 # TypeScript types
│   ├── package.json
│   └── README.md
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

## Codex Skill E2E Test

Use this script to download the skill from GitHub into a temp repo, load it, and run an end-to-end NotebookLM query through Codex CLI.

Prereqs:
- `codex` CLI installed
- NotebookLM MCP server added: `codex mcp add notebooklm -- npx -y notebooklm-mcp@latest`
- NotebookLM authentication completed at least once

Run:
```bash
scripts/codex-skill-e2e.sh
```

Optional overrides:
```bash
NOTEBOOK_URL="https://notebooklm.google.com/notebook/<id>" \
NOTEBOOK_NAME="My Test Notebook" \
NOTEBOOK_DESC="Notebook for testing Codex + NotebookLM." \
NOTEBOOK_ID="my-test-notebook" \
scripts/codex-skill-e2e.sh
```

## Plugin Commands

| Command | Description |
|---------|-------------|
| `/nlm ask <question>` | Ask a question to the active notebook |
| `/nlm add <url>` | Add a notebook to your library (auto-selects as active) |
| `/nlm list` | List all notebooks in your library |
| `/nlm select <name>` | Set active notebook for queries |
| `/nlm auth` | Check authentication status |
| `/nlm auth setup` | First-time authentication (opens browser) |
| `/nlm auth reset` | Clear and re-authenticate |

## Features

### Claude Code Plugin
- ✅ `/nlm` command with subcommands
- ✅ Research agent with automatic follow-up questions
- ✅ Library management (add, list, select, search)
- ✅ Uses existing NotebookLM MCP server
- ✅ Citation-backed answers from Gemini
- ✅ Troubleshooting skill with MCP tools reference

### Claude Desktop (MCP)
- ✅ Natural language notebook queries
- ✅ Automatic notebook discovery
- ✅ Citation-backed answers
- ✅ Multi-notebook support
- ✅ Persistent authentication

## Architecture

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   Claude    │────────>│   Plugin     │────────>│ NotebookLM  │
│  Code CLI   │         │  Commands    │         │ MCP Server  │
└─────────────┘         └──────────────┘         └─────────────┘
                               │                        │
                               │                        v
                               │                 ┌─────────────┐
                               │                 │  Playwright │
                               v                 │   Browser   │
                        ┌──────────────┐         └─────────────┘
                        │ MCP Tools    │                │
                        │ - ask_question│               v
                        │ - add_notebook│        ┌─────────────┐
                        │ - list_notebooks│      │ NotebookLM  │
                        │ - select_notebook│     │   (Gemini)  │
                        │ - get_health  │        └─────────────┘
                        └──────────────┘
```

The plugin uses the NotebookLM MCP server which handles:
- Browser automation via Playwright
- Google authentication
- Notebook library management
- Session handling

## Use Cases

**Quick Research:**
```bash
/nlm ask "How do I implement OAuth2 in FastAPI?"
# Get instant answer with citations from your docs
```

**Add Documentation:**
```bash
/nlm add https://notebooklm.google.com/notebook/YOUR_ID
# Automatically discovers content and sets as active
```

**Deep Research (via agent):**
```
"Research authentication patterns from my documentation"
# research-agent activates, asks follow-up questions, synthesizes answer
```

## Requirements

**For Claude Code Plugin:**
- Claude Code CLI
- NotebookLM MCP server (`npx -y notebooklm-mcp@latest`)
- Google Chrome browser
- Google account with NotebookLM access

**For Claude Desktop:**
- Claude Desktop
- `notebooklm-mcp` package

## Installation Options

### Project Scope (Recommended)
```bash
claude plugin install notebooklm@notebooklm-plugin --scope project
```

### User Scope (All Projects)
```bash
claude plugin install notebooklm@notebooklm-plugin --scope user
```

### Local Scope (Gitignored)
```bash
claude plugin install notebooklm@notebooklm-plugin --scope local
```

## Authentication Options

The plugin supports multiple authentication backends (tried in priority order):

| Backend | Platform | Description |
|---------|----------|-------------|
| **CDP** | All | Connect to existing Chrome session (best UX) |
| **Keychain** | macOS | Stored cookies in system keychain |
| **Persistent** | All | Playwright browser profile |
| **Manual** | All | Interactive browser login (fallback) |

### Recommended: Chrome Remote Debugging (No Popups!)

```bash
# 1. Start Chrome with remote debugging
open -a "Google Chrome" --args --remote-debugging-port=9222  # macOS

# 2. Login to NotebookLM in Chrome (one-time)
# Navigate to https://notebooklm.google.com and login with Google

# 3. Now queries use your existing session - no popups!
/nlm ask "How do I implement OAuth?"
```

**Tip:** Add to `~/.zshrc` or `~/.bashrc`:
```bash
alias chrome-debug='open -a "Google Chrome" --args --remote-debugging-port=9222'
```

## Troubleshooting

### Not Authenticated
```bash
# Best: Start Chrome with remote debugging first
open -a "Google Chrome" --args --remote-debugging-port=9222

# Or: Interactive setup
/nlm auth setup

# Check status
/nlm auth
```

### Rate Limited (50 queries/day free tier)
- Wait for daily reset, or
- Use `/nlm auth reset` to switch Google accounts

### Wrong Notebook
```bash
/nlm list           # See all notebooks
/nlm select <name>  # Switch to correct one
```

See [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for complete guide.

## Documentation

- [**Claude Code Setup**](docs/CLAUDE_CODE_SETUP.md) - Plugin installation guide
- [**Claude Desktop Setup**](docs/CLAUDE_DESKTOP_SETUP.md) - MCP setup guide
- [**API Reference**](docs/API_REFERENCE.md) - All commands and options
- [**Troubleshooting**](docs/TROUBLESHOOTING.md) - Common issues and solutions

## Security & Privacy

- ✅ All data stored locally by MCP server
- ✅ No data sent to third parties
- ✅ Browser session managed by MCP server
- ✅ Credentials never logged
- ⚠️ Consider dedicated Google account
- ⚠️ NotebookLM terms of service apply

## License

MIT License - see [LICENSE](LICENSE)

## Related Projects

- [NotebookLM MCP Server](https://github.com/PleasePrompto/notebooklm-mcp) - MCP server implementation
- [Claude Code](https://www.anthropic.com/claude/code) - Official Claude Code CLI
- [wshobson/agents](https://github.com/wshobson/agents) - Plugin patterns reference

---

**Built with ❤️ for efficient development workflows**

*Last Updated: December 2024*
