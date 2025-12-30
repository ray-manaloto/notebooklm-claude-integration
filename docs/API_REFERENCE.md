# API Reference

Complete reference for all NotebookLM Claude Integration commands and features.

## Table of Contents

- [Slash Commands](#slash-commands)
- [Python Scripts](#python-scripts)
- [Configuration](#configuration)
- [Data Structures](#data-structures)

---

## Slash Commands

### `/notebook-auth`

Manage NotebookLM authentication.

**Usage:**
```bash
/notebook-auth <command>
```

**Commands:**

#### `status`
Check authentication status.

```bash
/notebook-auth status

# Returns:
{
  "status": "authenticated|not_authenticated",
  "email": "user@example.com",
  "expires": "2025-02-15",
  "last_check": "2024-12-29T10:30:00Z"
}
```

#### `setup`
Interactive authentication setup. Opens Chrome for Google login.

```bash
/notebook-auth setup

# Process:
# 1. Launches Chrome browser
# 2. Navigates to NotebookLM
# 3. Prompts for Google login
# 4. Saves session state
# 5. Returns authentication confirmation
```

#### `reset`
Clear authentication and browser state.

```bash
/notebook-auth reset

# Returns:
{
  "status": "reset_complete",
  "message": "Authentication cleared. Run setup to re-authenticate."
}
```

---

### `/notebook`

Main notebook management command.

**Usage:**
```bash
/notebook <subcommand> [args...]
```

**Subcommands:**

#### `add`
Add a notebook to your library.

```bash
/notebook add <url> [name] [description] [topics...]

# Examples:
/notebook add https://notebooklm.google.com/notebook/abc123

/notebook add https://notebooklm.google.com/notebook/abc123 "API Docs"

/notebook add https://notebooklm.google.com/notebook/abc123 \
  "Security Guide" \
  "OAuth, JWT, security best practices" \
  "authentication,security"

# Returns:
{
  "id": "abc123",
  "name": "API Docs",
  "url": "https://notebooklm.google.com/notebook/abc123",
  "added": "2024-12-29T10:30:00Z",
  "active": false
}
```

**Parameters:**
- `url` (required) - Full NotebookLM notebook URL
- `name` (optional) - Display name, auto-extracted if not provided
- `description` (optional) - Notebook description
- `topics` (optional) - Comma-separated topics for search

---

#### `list`
List all notebooks in library.

```bash
/notebook list

# Returns:
[
  {
    "id": "abc123",
    "name": "API Docs",
    "description": "FastAPI documentation",
    "topics": ["fastapi", "python", "rest"],
    "active": true,
    "added": "2024-12-29T10:30:00Z"
  },
  {
    "id": "def456",
    "name": "Security Guide",
    "topics": ["oauth", "jwt", "security"],
    "active": false,
    "added": "2024-12-28T15:20:00Z"
  }
]
```

---

#### `activate`
Set active notebook for queries.

```bash
/notebook activate <identifier>

# By ID:
/notebook activate abc123

# By name (partial match):
/notebook activate "API Docs"

# By index (from list):
/notebook activate 1

# Returns:
{
  "id": "abc123",
  "name": "API Docs",
  "status": "activated",
  "previous": "def456"
}
```

---

#### `ask`
Query the active notebook.

```bash
/notebook ask "<question>"

# Examples:
/notebook ask "How do I implement OAuth2?"

/notebook ask "What are the rate limiting best practices?"

# Returns:
{
  "question": "How do I implement OAuth2?",
  "answer": "To implement OAuth2 in FastAPI...",
  "citations": [
    {
      "source": "auth-guide.pdf",
      "page": 12,
      "excerpt": "OAuth2 with Password (and hashing)..."
    }
  ],
  "follow_up_questions": [
    "What are the security considerations for OAuth2?",
    "How do I handle token refresh?"
  ],
  "notebook": "API Docs",
  "timestamp": "2024-12-29T10:35:00Z"
}
```

---

#### `search`
Search library by topic.

```bash
/notebook search <topic>

# Examples:
/notebook search authentication
/notebook search "rate limiting"

# Returns:
[
  {
    "id": "abc123",
    "name": "API Docs",
    "relevance": 0.95,
    "matching_topics": ["authentication", "oauth"]
  },
  {
    "id": "ghi789",
    "name": "Security Guide",
    "relevance": 0.78,
    "matching_topics": ["authentication", "jwt"]
  }
]
```

---

## Python Scripts

All scripts located in: `~/.claude/plugins/installed/notebooklm/skills/notebooklm/scripts/`

### `run.py`

Main command router.

```python
python3 run.py <command> [args...]
```

**Commands:**
- `auth status|setup|reset`
- `add <url> [name] [description] [topics]`
- `list`
- `activate <identifier>`
- `ask <question>`
- `search <topic>`

---

### `auth_manager.py`

Authentication management module.

```python
from auth_manager import AuthManager

auth = AuthManager()

# Check status
status = auth.get_status()

# Setup authentication
success = auth.setup()

# Reset
auth.reset()
```

**Methods:**
- `get_status()` → dict
- `setup()` → bool
- `reset()` → None
- `is_authenticated()` → bool

---

### `notebook_manager.py`

Library management module.

```python
from notebook_manager import NotebookManager

manager = NotebookManager()

# Add notebook
notebook = manager.add_notebook(
    url="https://notebooklm.google.com/notebook/abc123",
    name="API Docs",
    description="FastAPI documentation",
    topics=["fastapi", "python"]
)

# List notebooks
notebooks = manager.list_notebooks()

# Activate notebook
active = manager.activate_notebook("abc123")

# Search
results = manager.search_by_topic("authentication")
```

**Methods:**
- `add_notebook(url, name=None, description=None, topics=None)` → dict
- `list_notebooks()` → list[dict]
- `activate_notebook(identifier)` → dict
- `search_by_topic(topic)` → list[dict]
- `get_active_notebook()` → dict | None

---

### `ask_question.py`

Query execution module.

```python
from ask_question import ask_notebook

result = ask_notebook(
    question="How do I implement OAuth2?",
    notebook_id="abc123"
)

print(result["answer"])
print(result["citations"])
```

**Methods:**
- `ask_notebook(question, notebook_id=None)` → dict

**Response Structure:**
```python
{
    "question": str,
    "answer": str,
    "citations": [
        {
            "source": str,
            "page": int,
            "excerpt": str
        }
    ],
    "follow_up_questions": list[str],
    "notebook": str,
    "timestamp": str
}
```

---

## Configuration

### Directory Structure

```
~/.claude/plugins/installed/notebooklm/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   ├── notebook-auth.md
│   └── notebook.md
├── agents/
│   └── research-agent.md
└── skills/notebooklm/
    ├── SKILL.md
    ├── scripts/
    │   ├── run.py
    │   ├── auth_manager.py
    │   ├── notebook_manager.py
    │   ├── ask_question.py
    │   └── requirements.txt
    └── data/
        ├── library.json
        ├── auth_info.json
        └── browser_state/
```

---

### Plugin Configuration

**File:** `.claude-plugin/plugin.json`

```json
{
  "name": "notebooklm",
  "version": "1.0.0",
  "description": "Query your NotebookLM notebooks",
  "author": "Raymond Manaloto",
  "commands": ["notebook", "notebook-auth"],
  "agents": ["research-agent"],
  "skills": ["notebooklm"]
}
```

---

## Data Structures

### Library Schema

**File:** `data/library.json`

```json
{
  "notebooks": [
    {
      "id": "abc123",
      "name": "API Docs",
      "url": "https://notebooklm.google.com/notebook/abc123",
      "description": "FastAPI documentation",
      "topics": ["fastapi", "python", "rest"],
      "added": "2024-12-29T10:30:00Z",
      "last_accessed": "2024-12-29T14:20:00Z",
      "query_count": 42
    }
  ],
  "active_notebook": "abc123",
  "settings": {
    "auto_activate_on_add": false,
    "citation_format": "full"
  }
}
```

---

### Auth Info Schema

**File:** `data/auth_info.json`

```json
{
  "authenticated": true,
  "email": "user@example.com",
  "auth_date": "2024-12-29T10:00:00Z",
  "expires": "2025-02-15T10:00:00Z",
  "browser_state_path": "data/browser_state",
  "last_check": "2024-12-29T14:30:00Z"
}
```

---

## Error Codes

| Code | Message | Resolution |
|------|---------|------------|
| `AUTH_REQUIRED` | Not authenticated | Run `/notebook-auth setup` |
| `NO_ACTIVE_NOTEBOOK` | No notebook activated | Run `/notebook activate <id>` |
| `NOTEBOOK_NOT_FOUND` | Invalid notebook ID | Check `/notebook list` |
| `BROWSER_ERROR` | Chrome automation failed | Check Chrome installation |
| `NETWORK_ERROR` | NotebookLM unreachable | Check internet connection |
| `INVALID_URL` | Malformed notebook URL | Verify URL format |

---

## Environment Variables

Create `.env` in scripts directory:

```bash
# Browser settings
CHROME_PATH=/usr/bin/google-chrome
HEADLESS=false
BROWSER_TIMEOUT=30000

# NotebookLM settings
NOTEBOOKLM_URL=https://notebooklm.google.com
QUERY_TIMEOUT=10000

# Debug
DEBUG=false
LOG_LEVEL=INFO
```

---

## Rate Limits

| Operation | Limit | Window |
|-----------|-------|--------|
| Queries | 10 | 1 minute |
| Add notebook | 5 | 1 minute |
| Auth setup | 3 | 1 hour |

---

## Examples

### Complete Workflow

```bash
# 1. Setup authentication
/notebook-auth setup
# → Opens Chrome, login with Google

# 2. Add notebooks
/notebook add https://notebooklm.google.com/notebook/api-docs "API Docs"
/notebook add https://notebooklm.google.com/notebook/security "Security Guide"

# 3. List and activate
/notebook list
/notebook activate "API Docs"

# 4. Query
/notebook ask "How do I implement rate limiting?"

# 5. Switch notebooks
/notebook activate "Security Guide"
/notebook ask "What are OAuth2 best practices?"
```

### Programmatic Usage

```python
#!/usr/bin/env python3

from notebook_manager import NotebookManager
from ask_question import ask_notebook

# Initialize
manager = NotebookManager()

# Add notebook
manager.add_notebook(
    url="https://notebooklm.google.com/notebook/abc123",
    name="Tech Docs",
    topics=["python", "api"]
)

# Activate
manager.activate_notebook("abc123")

# Query
result = ask_notebook("How do I handle errors?")

print(f"Answer: {result['answer']}")
for citation in result['citations']:
    print(f"Source: {citation['source']}")
```

---

For more examples, see the [examples/](../examples/) directory.
