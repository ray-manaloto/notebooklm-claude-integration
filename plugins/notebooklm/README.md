# NotebookLM Plugin for Claude Code

Query your Google NotebookLM notebooks directly from Claude Code for source-grounded, citation-backed answers from Gemini.

## Features

- **`/nlm` Command**: Single command with subcommands for all operations
- **Research Agent**: Proactive deep research with automatic follow-ups
- **Library Management**: Organize and search your notebook collection
- **Zero Hallucinations**: Answers sourced exclusively from your documents

## Prerequisites

1. **NotebookLM MCP Server** must be configured:
   ```bash
   claude mcp add notebooklm -- npx -y notebooklm-mcp@latest
   ```

2. **Google Account** with NotebookLM access

## Installation

### From Local Path
```bash
claude plugin add /path/to/notebooklm-claude-integration/plugins/notebooklm
```

### From Marketplace (if published)
```bash
claude plugin install notebooklm@your-marketplace
```

### Installation Scopes
```bash
# User scope (default) - available in all projects
claude plugin add ./plugins/notebooklm

# Project scope - shared with team via version control
claude plugin add ./plugins/notebooklm --scope project

# Local scope - project-specific, gitignored
claude plugin add ./plugins/notebooklm --scope local
```

## Quick Start

```bash
# 1. Authenticate (first time only)
/nlm auth setup

# 2. Add a notebook
/nlm add https://notebooklm.google.com/notebook/YOUR_ID

# 3. Ask questions
/nlm ask "How do I implement OAuth?"
```

## Commands

### `/nlm ask <question>`
Ask a question to the active notebook.

```
/nlm ask "What are the best practices for error handling?"
```

### `/nlm add <url>`
Add a NotebookLM notebook to your library. Automatically discovers content and sets as active.

```
/nlm add https://notebooklm.google.com/notebook/8e98a4d8-f778-4dfc-88e8-2d59e48b1069
```

### `/nlm list`
List all notebooks in your library.

```
/nlm list
```

### `/nlm select <name or id>`
Set a notebook as active for queries.

```
/nlm select "FastAPI Documentation"
/nlm select fastapi
```

### `/nlm auth [setup|status|reset]`
Manage authentication.

```
/nlm auth          # Check status
/nlm auth setup    # Initial setup (opens browser)
/nlm auth reset    # Clear and re-authenticate
```

## Research Agent

The research agent triggers proactively when you ask to research, investigate, or explore a topic:

```
"Research how to implement authentication in my docs"
"Investigate the error handling patterns"
"Deep dive into the API structure"
```

The agent will:
1. Query your active notebook
2. Generate follow-up questions
3. Synthesize comprehensive findings

## Plugin Structure

```
plugins/notebooklm/
├── .claude-plugin/
│   └── plugin.json
├── agents/
│   └── research-agent.md
├── commands/
│   └── nlm.md
├── skills/
│   └── notebooklm-patterns/
│       └── SKILL.md
└── README.md
```

## Troubleshooting

### Not Authenticated
```bash
/nlm auth setup
```

### Rate Limited (50 queries/day)
- Wait for daily reset, or
- Use `/nlm auth reset` to switch accounts

### Wrong Notebook
```bash
/nlm list           # See all notebooks
/nlm select <name>  # Switch to correct one
```

### Browser Issues
Close all Chrome instances and re-authenticate:
```bash
/nlm auth reset
```

## Requirements

- Claude Code CLI
- NotebookLM MCP server (`notebooklm-mcp`)
- Google Chrome browser
- Google account with NotebookLM access

## License

MIT
