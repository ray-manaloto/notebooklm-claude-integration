---
name: nlm
description: Query NotebookLM notebooks for source-grounded answers
argument-hint: "<ask|add|list|select|auth> [arguments]"
allowed-tools:
  - mcp__notebooklm__ask_question
  - mcp__notebooklm__add_notebook
  - mcp__notebooklm__list_notebooks
  - mcp__notebooklm__select_notebook
  - mcp__notebooklm__get_notebook
  - mcp__notebooklm__search_notebooks
  - mcp__notebooklm__get_health
  - mcp__notebooklm__setup_auth
  - mcp__notebooklm__re_auth
---

# /nlm - NotebookLM Integration

Query your Google NotebookLM notebooks for source-grounded, citation-backed answers from Gemini.

## Subcommands

| Subcommand | Usage | Description |
|------------|-------|-------------|
| `ask` | `/nlm ask <question>` | Ask a question to the active notebook |
| `add` | `/nlm add <url>` | Add a notebook to your library |
| `list` | `/nlm list` | List all notebooks in library |
| `select` | `/nlm select <name or id>` | Set active notebook |
| `auth` | `/nlm auth [setup\|status\|reset]` | Manage authentication |

## Arguments

$ARGUMENTS

## Instructions

Parse the subcommand from arguments and execute the appropriate action:

### `ask` - Ask a Question

When user runs `/nlm ask <question>`:

1. Check if authenticated using `get_health`
2. If not authenticated, prompt user to run `/nlm auth setup`
3. Use `ask_question` tool with the question
4. Display the answer with citations formatted clearly:

```markdown
## Answer

[Answer text from NotebookLM]

### Sources
- [Citation 1]
- [Citation 2]
```

**Example:**
```
/nlm ask How do I implement OAuth in FastAPI?
```

### `add` - Add Notebook

When user runs `/nlm add <url>`:

1. Extract the NotebookLM URL from arguments
2. Use `ask_question` with the URL to discover content:
   - Question: "What is this notebook about? List the main topics covered."
3. Parse the response to extract:
   - Suggested name (from content)
   - Description (brief summary)
   - Topics (main subjects)
4. Use `add_notebook` with discovered metadata
5. Automatically select the new notebook as active using `select_notebook`
6. Confirm to user:

```markdown
## Notebook Added

**Name:** [discovered name]
**Topics:** [topics]
**Status:** Active (selected)

You can now ask questions with `/nlm ask <question>`
```

**Example:**
```
/nlm add https://notebooklm.google.com/notebook/8e98a4d8-f778-4dfc-88e8-2d59e48b1069
```

### `list` - List Notebooks

When user runs `/nlm list`:

1. Use `list_notebooks` to get all notebooks
2. Display as formatted table:

```markdown
## Your Notebooks

| Name | Topics | Last Used | Active |
|------|--------|-----------|--------|
| FastAPI Docs | fastapi, python | 2 hours ago | * |
| n8n Guide | n8n, workflows | 1 day ago | |
```

3. If no notebooks, suggest adding one:
   ```
   No notebooks in library. Add one with:
   /nlm add <notebooklm-url>
   ```

### `select` - Select Active Notebook

When user runs `/nlm select <name or id>`:

1. Use `list_notebooks` to find matching notebook
2. Match by:
   - Exact ID match
   - Partial name match (case-insensitive)
   - Topic match
3. If multiple matches, show options and ask user to be more specific
4. Use `select_notebook` with the matched ID
5. Confirm selection:

```markdown
## Notebook Selected

**[Notebook Name]** is now active.

Ask questions with `/nlm ask <question>`
```

**Example:**
```
/nlm select fastapi
```

### `auth` - Authentication Management

When user runs `/nlm auth [action]`:

**`/nlm auth` or `/nlm auth status`:**
1. Use `get_health` to check authentication status
2. Display status:

```markdown
## NotebookLM Status

- **Authenticated:** Yes/No
- **Active Sessions:** X
- **Headless Mode:** Yes/No
```

**`/nlm auth setup`:**
1. Use `setup_auth` tool (will open browser)
2. Inform user: "Browser opened for Google login. Complete login and return here."
3. After completion, confirm authentication

**`/nlm auth reset`:**
1. Use `re_auth` tool to clear and re-authenticate
2. Inform user about the reset process

## Response Format

Always format responses with clear headers and structure:

- Use markdown tables for lists
- Include status indicators
- Show next steps or suggestions
- Display citations when showing answers

## Error Handling

- **Not authenticated:** Prompt `/nlm auth setup`
- **No active notebook:** Prompt `/nlm select <name>` or `/nlm add <url>`
- **Notebook not found:** Show available notebooks from library
- **Rate limited:** Inform user and suggest waiting

## Tips

- First time? Run `/nlm auth setup` to authenticate
- Add notebooks with descriptive URLs
- Use `/nlm list` to see all available notebooks
- The active notebook is used for all `/nlm ask` queries
