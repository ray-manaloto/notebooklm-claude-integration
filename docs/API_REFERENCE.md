# API Reference

Complete reference for all NotebookLM Claude Integration commands and MCP tools.

## Table of Contents

- [Slash Commands](#slash-commands)
- [MCP Tools](#mcp-tools)
- [Data Structures](#data-structures)
- [Error Handling](#error-handling)

---

## Slash Commands

### `/nlm`

Main command for NotebookLM interactions. Provides subcommands for all operations.

**Usage:**
```bash
/nlm <subcommand> [arguments]
```

---

### `/nlm ask`

Query the active notebook with a question.

**Usage:**
```bash
/nlm ask "<question>"
```

**Examples:**
```bash
/nlm ask "How do I implement OAuth2 in FastAPI?"
/nlm ask "What are the rate limiting best practices?"
/nlm ask "Explain the authentication flow"
```

**Response includes:**
- Answer from NotebookLM (powered by Gemini)
- Citations from your uploaded documents
- Source references

**Note:** Requires an active notebook. Use `/nlm list` to see available notebooks.

---

### `/nlm add`

Add a notebook to your library and set it as active.

**Usage:**
```bash
/nlm add <url>
```

**Example:**
```bash
/nlm add https://notebooklm.google.com/notebook/8e98a4d8-f778-4dfc-88e8-2d59e48b1069
```

**Behavior:**
1. Queries the notebook to discover its content
2. Extracts name, description, and topics automatically
3. Adds it to your library
4. Sets it as the active notebook

---

### `/nlm list`

List all notebooks in your library.

**Usage:**
```bash
/nlm list
```

**Output:**
```
Notebooks in library:
1. [ACTIVE] FastAPI Documentation
   Topics: fastapi, python, rest, api

2. Security Guide
   Topics: oauth, jwt, security
```

---

### `/nlm select`

Set a notebook as active for queries.

**Usage:**
```bash
/nlm select <name or partial match>
```

**Examples:**
```bash
/nlm select "FastAPI Documentation"
/nlm select fastapi
/nlm select security
```

**Note:** Supports partial matching - "fastapi" matches "FastAPI Documentation".

---

### `/nlm auth`

Check authentication status.

**Usage:**
```bash
/nlm auth
```

**Output:**
```
Authentication Status:
- Authenticated: true
- Ready to query notebooks
```

---

### `/nlm auth setup`

First-time authentication. Opens browser for Google login.

**Usage:**
```bash
/nlm auth setup
```

**Process:**
1. Opens Chrome browser window
2. Navigates to NotebookLM
3. Prompts for Google login
4. Saves session state locally
5. Returns confirmation

**Note:** Credentials stored locally by MCP server. No data sent to third parties.

---

### `/nlm auth reset`

Clear authentication and re-authenticate with a different account.

**Usage:**
```bash
/nlm auth reset
```

**Use cases:**
- Switch to a different Google account
- Rate limit reached on current account
- Clear corrupted browser state

---

## MCP Tools

The plugin uses these MCP tools from the NotebookLM MCP server:

### `mcp__notebooklm__ask_question`

Query a notebook with a question.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `question` | string | Yes | The question to ask |
| `notebook_id` | string | No | Specific notebook ID (uses active if omitted) |
| `session_id` | string | No | Session for contextual conversations |

**Response:**
```json
{
  "answer": "To implement OAuth2...",
  "citations": [
    {
      "source": "auth-guide.pdf",
      "excerpt": "OAuth2 with Password flow..."
    }
  ],
  "notebook_id": "abc123"
}
```

---

### `mcp__notebooklm__add_notebook`

Add a notebook to the library.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `url` | string | Yes | Full NotebookLM notebook URL |
| `name` | string | No | Display name (auto-extracted if omitted) |
| `description` | string | No | Notebook description |
| `topics` | array | No | Topics for search/organization |

**Response:**
```json
{
  "id": "abc123",
  "name": "API Documentation",
  "url": "https://notebooklm.google.com/notebook/abc123",
  "topics": ["api", "rest", "fastapi"]
}
```

---

### `mcp__notebooklm__list_notebooks`

List all notebooks in the library.

**Parameters:** None

**Response:**
```json
{
  "notebooks": [
    {
      "id": "abc123",
      "name": "API Documentation",
      "topics": ["api", "rest"],
      "active": true
    },
    {
      "id": "def456",
      "name": "Security Guide",
      "topics": ["oauth", "jwt"],
      "active": false
    }
  ]
}
```

---

### `mcp__notebooklm__select_notebook`

Set a notebook as active.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string | Yes | Notebook ID to activate |

**Response:**
```json
{
  "id": "abc123",
  "name": "API Documentation",
  "active": true
}
```

---

### `mcp__notebooklm__get_notebook`

Get detailed information about a specific notebook.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | string | Yes | Notebook ID |

**Response:**
```json
{
  "id": "abc123",
  "name": "API Documentation",
  "description": "FastAPI documentation and guides",
  "topics": ["api", "rest", "fastapi"],
  "url": "https://notebooklm.google.com/notebook/abc123",
  "added": "2024-12-29T10:30:00Z"
}
```

---

### `mcp__notebooklm__search_notebooks`

Search notebooks by query.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | string | Yes | Search query |

**Response:**
```json
{
  "notebooks": [
    {
      "id": "abc123",
      "name": "API Documentation",
      "relevance": 0.95
    }
  ]
}
```

---

### `mcp__notebooklm__get_health`

Check authentication and server health.

**Parameters:** None

**Response:**
```json
{
  "authenticated": true,
  "activeSessions": 1,
  "ready": true
}
```

---

### `mcp__notebooklm__setup_auth`

Initial authentication setup.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `show_browser` | boolean | No | Show browser window (default: true for setup) |

**Behavior:** Opens browser for Google login.

---

### `mcp__notebooklm__re_auth`

Clear and re-authenticate.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `show_browser` | boolean | No | Show browser window (default: true) |

**Behavior:** Clears browser state and opens new login.

---

## Alternate MCP (HTTP/RPC, jacob-bd)

If you configure the `notebooklm-rpc` server (`jacob-bd/notebooklm-mcp`), tool names differ and authentication uses cookie extraction:

- **Auth:** `notebooklm-mcp-auth` (writes `~/.notebooklm-mcp/auth.json`)
- **Core tools:** `notebook_list`, `notebook_get`, `notebook_query`, `notebook_add_url`, `notebook_add_drive`, `notebook_add_text`
- **Drive sync:** `source_list_drive`, `source_sync_drive`
- **Studio artifacts:** `audio_overview_create`, `video_overview_create`, `infographic_create`, `slide_deck_create`

These tools are prefixed by the server name when used via MCP (e.g., `mcp__notebooklm-rpc__notebook_query`).

### Recommended Default

When both servers are configured, prefer `notebooklm-rpc` for daily usage and fall back to `notebooklm` only when RPC tools are unavailable or auth fails.

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
| `Not authenticated` | No valid session | Run `/nlm auth setup` |
| `No active notebook` | No notebook selected | Run `/nlm list` and `/nlm select` |
| `Notebook not found` | Invalid notebook ID | Check `/nlm list` for valid IDs |
| `Rate limit exceeded` | 50 daily queries (free tier) | Wait for reset or use `/nlm auth reset` |
| `Browser error` | Playwright issue | Check Chrome installation |
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
/nlm auth setup

# 2. Add a notebook
/nlm add https://notebooklm.google.com/notebook/YOUR_NOTEBOOK_ID

# 3. List notebooks
/nlm list

# 4. Query the notebook
/nlm ask "How do I implement rate limiting?"

# 5. Switch notebooks
/nlm select "Security Guide"
/nlm ask "What are OAuth2 best practices?"
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
