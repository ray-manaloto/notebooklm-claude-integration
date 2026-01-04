# NotebookLM Claude Integration

Complete integration of Google NotebookLM with Claude AI through both Claude Desktop (MCP) and Claude Code (Plugin).

> **Status**: Production-ready ✅ | **Built**: Dec 2024 | **Tested**: Fully functional

## What This Is

This project provides **two complete integrations** for using NotebookLM with Claude:

1. **Claude Desktop** - MCP Server for conversational interface
2. **Claude Code CLI** - Plugin for development workflow

Both allow you to query your NotebookLM notebooks directly from Claude, getting citation-backed answers from Gemini without leaving your workflow.

## Quick Start

Project plan lives at `docs/PROJECT_PLAN.md` with topic-specific items under `docs/plans/`.
CI details live at `docs/CI.md`.

Keep Pixi dependencies current (updates the lockfile, then installs from it):
```bash
pixi run pixi-sync
```

NotebookLM end-to-end integration (uses your local Chrome auth):
```bash
NOTEBOOK_IDS=pytest-patterns \
QUESTION="Summarize the key sources in this notebook." \
pixi run notebooklm-integration
```

### AI Agent Step-by-Step (Codex CLI)

Use this sequence when an agent needs to verify the NotebookLM integration end-to-end.

1. Install and enable the MCP server:
   ```bash
   uv tool install notebooklm-mcp-server
   codex mcp add notebooklm-rpc notebooklm-mcp
   ```
2. Authenticate once (browser login) and persist cookies:
   ```bash
   pixi run notebooklm-auth-rpc
   ```
3. Run the full E2E test (downloads the skill from GitHub into a temp repo and queries a notebook):
   ```bash
   pixi run codex-skill-e2e
   ```
4. Optional overrides:
   ```bash
   NOTEBOOK_URL="https://notebooklm.google.com/notebook/<id>" \
   NOTEBOOK_NAME="My Test Notebook" \
   NOTEBOOK_DESC="Notebook for testing Codex + NotebookLM." \
   NOTEBOOK_ID="my-test-notebook" \
   pixi run codex-skill-e2e
   ```

### AI Agent Step-by-Step (Codex SDK)

Use this sequence when a Codex SDK agent must validate the setup and produce a confirmed response.

1. Ensure Codex CLI + MCP are set up (same as CLI steps above).
2. Run the SDK verification (temp workspace, streaming output):
   ```bash
   SDK_ROOT=/tmp/codex-sdk-verify
   rm -rf "$SDK_ROOT" && mkdir -p "$SDK_ROOT"
   cd "$SDK_ROOT"

   cat <<'EOF' > package.json
   {
     "name": "codex-sdk-verify",
     "version": "0.1.0",
     "private": true,
     "type": "module",
     "scripts": { "run": "node run.mjs" },
     "dependencies": { "@openai/codex-sdk": "^0.77.0" }
   }
   EOF

   cat <<'EOF' > run.mjs
   import { Codex } from "@openai/codex-sdk";

   const prompt = [
     "Use the notebooklm-patterns skill.",
     "List all notebooks, then ask each notebook (via notebook_id) this question:",
     "'How can we improve the Codex implementation in this repo?'.",
     "Aggregate responses labeled by notebook name and include citations.",
    "If any notebook_query times out, retry once. If it still times out, record a timeout for that notebook and continue.",
   ].join(" ");

   const codex = new Codex();
   const thread = codex.startThread({
     workingDirectory: "/tmp/codex-skill-verify",
     sandboxMode: "read-only",
     approvalPolicy: "never",
   });

   const { events } = await thread.runStreamed(prompt);
   for await (const event of events) {
     if (event.type === "item.completed" && event.item?.type === "agent_message") {
       console.log(event.item.text);
     }
     if (event.type === "turn.failed") {
       console.error("Codex SDK turn failed:", event.error?.message ?? event.error);
     }
   }
   EOF

   npm install
   npm run run
   ```

### For Claude Code (Plugin)

```bash
# 1. Ensure NotebookLM MCP server is configured
uv tool install notebooklm-mcp-server
claude mcp add notebooklm-rpc -- notebooklm-mcp

# 2. Add the plugin marketplace from GitHub
claude plugin marketplace add ray-manaloto/notebooklm-claude-integration

# 3. Install the plugin (project scope)
claude plugin install notebooklm@notebooklm-plugin --scope project

# 4. Verify installation
claude plugin marketplace list  # Should show: notebooklm-plugin
claude plugin list              # Should show: notebooklm

# 5. Restart Claude Code, then:
/nlm auth rpc                      # First-time authentication
/nlm list                          # List notebooks
/nlm ask "Your question"           # Query the notebook
```

**For local development** (if you cloned this repo):
```bash
claude plugin marketplace add .
```

### For Claude Desktop (MCP)

```bash
npm install -g notebooklm-mcp
```

## Alternate NotebookLM MCP (HTTP/RPC, jacob-bd)

This repo also supports the HTTP/RPC-based MCP server from `jacob-bd/notebooklm-mcp`, which exposes additional tools (notebook creation, Drive sync, Studio artifacts).

Install + auth:
```bash
uv tool install notebooklm-mcp-server
GOOGLE_ACCOUNT=ray.manaloto@gmail.com pixi run notebooklm-auth-rpc
```

Pixi task (recommended for repeatable runs):
```bash
pixi run notebooklm-auth-rpc
```
Override account:
```bash
GOOGLE_ACCOUNT=your@email pixi run notebooklm-auth-rpc
```

Register the MCP server:
```bash
codex mcp add notebooklm-rpc -- notebooklm-mcp
```

Notes:
- This server uses cookie extraction; persist cookies with `save_auth_tokens`.
- Tool names include `notebook_list`, `notebook_query`, and `source_sync_drive`.
- Use `notebooklm-patterns` for RPC-first guidance.
- Override the account used for cookie extraction with `GOOGLE_ACCOUNT=your@email`.

### Recommended Setup (RPC-first)

Use `notebooklm-rpc` as the default server for full feature parity:
- `notebooklm-rpc` (expanded toolset, Drive sync, Studio artifacts)

If auth fails, re-run `pixi run notebooklm-auth-rpc` and retry.

## When to Use This Repo vs. jacob-bd Only

You can use `jacob-bd/notebooklm-mcp` directly if you only need the RPC server tools.
This repo adds:
- Codex/Claude CLI wiring (`/nlm` commands, skills, tool routing).
- Repeatable Pixi tasks for validation and multi-notebook queries.
- Centralized MCP configuration and agent playbooks.

Add to `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "notebooklm-rpc": {
      "command": "notebooklm-mcp"
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

## Codex Skill E2E Test

Use the Pixi task to download the skill from GitHub into a temp repo, load it, and run an end-to-end NotebookLM query through Codex CLI.

Prereqs:
- `codex` CLI installed
- NotebookLM MCP server added: `codex mcp add notebooklm-rpc notebooklm-mcp`
- NotebookLM authentication completed at least once

Run:
```bash
pixi run codex-skill-e2e
```

Optional overrides:
```bash
NOTEBOOK_URL="https://notebooklm.google.com/notebook/<id>" \
NOTEBOOK_NAME="My Test Notebook" \
NOTEBOOK_DESC="Notebook for testing Codex + NotebookLM." \
NOTEBOOK_ID="my-test-notebook" \
pixi run codex-skill-e2e
```

Validation checklist (expected results):
- RPC auth is valid (cookies persisted via `save_auth_tokens`)
- The target notebook exists in `notebook_list`
- A response is returned with citations

See `docs/CODEX_PLAYBOOK.md` for a full Codex CLI/SDK validation runbook.

Recommended validation run:
```bash
pixi run codex-validate-setup
```

### Codex Improvement Notes

- Use `notebook_id` for multi-notebook queries to avoid shared state.
- Retry a timed-out `notebook_query` once, then record a timeout and continue.

### Codex Multi-Notebook Query

Run a single question across all notebooks and aggregate results (uses notebook_id to avoid shared state conflicts):

```bash
pixi run codex-ask-all
```

Optional override:
```bash
QUESTION="What are the key risks in this architecture?" pixi run codex-ask-all
```

### RPC Auth Refresh

If RPC auth expires, refresh cookies:
```bash
pixi run notebooklm-auth-rpc
```

Use the `notebooklm-rpc` server after the file-mode auth:
```bash
NOTEBOOK_IDS=pytest-patterns \
QUESTION="Summarize the key sources in this notebook." \
pixi run codex-ask-all-rpc
```

Filter by notebook IDs (comma-separated):
```bash
NOTEBOOK_IDS=pytest-patterns \
QUESTION="Provide modern best practices for integration tests without mocks." \
pixi run codex-ask-all
```

Validation checklist (expected results):
- Each notebook returns a labeled section
- Citations are included when NotebookLM provides them
- Timeouts are retried once and reported

### Repo Hygiene (Pixi-Only)

Install the pre-commit hook to block bash scripts and non-Pixi commands:
```bash
pixi run hooks-install
```

Run locally on demand:
```bash
pixi run hooks-run
```

### Codex Multi-Notebook Query (Subagent-aware)

If Codex supports subagents or task parallelism, this script asks a subagent per notebook; otherwise it falls back to sequential queries:

```bash
pixi run codex-ask-all-subagents
```

SDK example:
```bash
cd codex-sdk-test
QUESTION="Summarize auth flow changes." npm run test:notebooklm-ask-all
```

### Auth Bootstrap (Recommended for Multi-Process)

Run the auth flow once, then fan out workers that reuse the cookie file:

```bash
pixi run notebooklm-auth-rpc
```

## Plugin Commands

| Command | Description |
|---------|-------------|
| `/nlm ask <question>` | Ask a question to a notebook by ID |
| `/nlm list` | List all notebooks |
| `/nlm create <name>` | Create a new notebook |
| `/nlm auth rpc` | Save RPC auth cookies |

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
                               │                 │ Auth Helper │
                               v                 │ (cookies)   │
                        ┌──────────────┐         └─────────────┘
                        │ MCP Tools    │                │
                        │ - notebook_list│              v
                        │ - notebook_query│     ┌─────────────┐
                        │ - notebook_add_url│   │ NotebookLM  │
                        │ - research_start│     │   (Gemini)  │
                        │ - studio_status│      └─────────────┘
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
/nlm source add-url <notebook_id> <url>
# Adds a URL source to a notebook
```

**Deep Research (via agent):**
```
"Research authentication patterns from my documentation"
# research-agent activates, asks follow-up questions, synthesizes answer
```

## Requirements

**For Claude Code Plugin:**
- Claude Code CLI
- NotebookLM MCP server (`notebooklm-mcp-server`)
- Google Chrome browser (for auth)
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

### RPC Server (Default: File Mode)

For the HTTP/RPC server, default to file-mode auth:
```bash
notebooklm-mcp-auth --file
```
This writes cookies to `~/.notebooklm-mcp/auth.json` for RPC use.

**Reuse on future runs:** if `~/.notebooklm-mcp/auth.json` exists, you can skip login.  
**If auth breaks:** re-run `notebooklm-mcp-auth --file` to refresh cookies.

**Validate auth without re-login:**
```bash
pixi run notebooklm-auth-check-rpc
```

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
# Run notebooklm-mcp-auth and complete login
notebooklm-mcp-auth

# Save RPC auth cookies
/nlm auth rpc
```

### Rate Limited (50 queries/day free tier)
- Wait for daily reset, or
- Re-run `notebooklm-mcp-auth` with a different Google account

### Wrong Notebook
```bash
/nlm list           # See all notebooks
# Re-run /nlm ask with the correct notebook_id
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
