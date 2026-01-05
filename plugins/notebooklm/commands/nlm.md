---
name: nlm
description: Query and manage NotebookLM notebooks for source-grounded answers
argument-hint: "<ask|ask-all|create|rename|delete|list|source|research|studio|describe|configure|auth> [arguments]"
allowed-tools:
  - mcp__notebooklm-rpc__save_auth_tokens
  - mcp__notebooklm-rpc__notebook_list
  - mcp__notebooklm-rpc__notebook_create
  - mcp__notebooklm-rpc__notebook_get
  - mcp__notebooklm-rpc__notebook_describe
  - mcp__notebooklm-rpc__notebook_rename
  - mcp__notebooklm-rpc__notebook_delete
  - mcp__notebooklm-rpc__notebook_add_url
  - mcp__notebooklm-rpc__notebook_add_text
  - mcp__notebooklm-rpc__notebook_add_drive
  - mcp__notebooklm-rpc__notebook_query
  - mcp__notebooklm-rpc__source_list_drive
  - mcp__notebooklm-rpc__source_sync_drive
  - mcp__notebooklm-rpc__source_delete
  - mcp__notebooklm-rpc__source_describe
  - mcp__notebooklm-rpc__research_start
  - mcp__notebooklm-rpc__research_status
  - mcp__notebooklm-rpc__research_import
  - mcp__notebooklm-rpc__chat_configure
  - mcp__notebooklm-rpc__audio_overview_create
  - mcp__notebooklm-rpc__video_overview_create
  - mcp__notebooklm-rpc__infographic_create
  - mcp__notebooklm-rpc__slide_deck_create
  - mcp__notebooklm-rpc__studio_status
  - mcp__notebooklm-rpc__studio_delete
---

# /nlm - NotebookLM Integration

Query your Google NotebookLM notebooks for source-grounded, citation-backed answers from Gemini.

## Subcommands

| Subcommand | Usage | Description |
|------------|-------|-------------|
| `ask` | `/nlm ask <question>` | Ask a question to a notebook by ID |
| `ask-all` | `/nlm ask-all <question>` | Ask all notebooks in parallel, compare answers |
| `create` | `/nlm create <name>` | Create a new notebook (RPC only) |
| `rename` | `/nlm rename <id> <name>` | Rename a notebook (RPC only) |
| `delete` | `/nlm delete <id>` | Delete a notebook (RPC only, confirm) |
| `list` | `/nlm list` | List all notebooks |
| `source` | `/nlm source <add-url|add-text|add-drive|list|sync|delete> ...` | Manage notebook sources (RPC only) |
| `research` | `/nlm research <start|status|import> ...` | Discover/import sources (RPC only) |
| `studio` | `/nlm studio <audio|video|infographic|slides|status|delete> ...` | Create or manage Studio artifacts (RPC only) |
| `describe` | `/nlm describe <notebook|source> <id>` | Summarize notebook or source (RPC only) |
| `configure` | `/nlm configure <goal|length|prompt> ...` | Configure chat goal/length/custom prompt (RPC only) |
| `auth` | `/nlm auth [rpc]` | Manage authentication |

## Arguments

$ARGUMENTS

## Instructions

Parse the subcommand from arguments and execute the appropriate action:

### Server Selection (Default Behavior)

- Use the `notebooklm-rpc` tools only (expanded toolset + feature parity).

### `ask` - Ask a Question

When user runs `/nlm ask <question>`:

1. Ensure RPC auth is configured (cookies saved via `save_auth_tokens`)
2. Use `notebook_query` with `notebook_id`
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

### `ask-all` - Ask All Notebooks (Parallel)

When user runs `/nlm ask-all <question>`:

This command queries **all notebooks in your library simultaneously** using parallel subagents, then aggregates the responses with clear notebook identification.

**Execution Steps:**

1. Ensure RPC auth is configured (cookies saved via `save_auth_tokens`)
2. Use `notebook_list`
3. If no notebooks, prompt user to create one with `/nlm create <name>`
5. If only one notebook, suggest using `/nlm ask` instead for efficiency
6. **For each notebook, spawn a parallel subagent** using the Task tool:
   - Each subagent should:
     a. Ask the question using `notebook_query` with `notebook_id`
     b. Return the response with notebook name/ID
7. Wait for all subagents to complete
8. Aggregate and display responses in a comparative format:

```markdown
## Answers from All Notebooks

### 📚 [Notebook 1 Name]
> **Topics:** [topics]

[Answer text from this notebook]

**Sources:** [Citation 1], [Citation 2]

---

### 📚 [Notebook 2 Name]
> **Topics:** [topics]

[Answer text from this notebook]

**Sources:** [Citation 1], [Citation 2]

---

### 📚 [Notebook 3 Name]
> **Topics:** [topics]

[Answer text from this notebook]

**Sources:** [Citation 1], [Citation 2]

---

## Summary

| Notebook | Key Points | Relevance |
|----------|------------|-----------|
| [Name 1] | [Brief summary] | High/Medium/Low |
| [Name 2] | [Brief summary] | High/Medium/Low |
| [Name 3] | [Brief summary] | High/Medium/Low |

**Most Relevant Source:** [Notebook name] - [Reason]
```

**Subagent Prompt Template:**

For each notebook, use the Task tool with this prompt:
```
Query the notebook "[notebook_name]" (ID: [notebook_id]) with this question: "[user_question]"

Steps:
1. Use notebook_query with the question and notebook_id "[notebook_id]"
3. Return the full response including any citations

Format your response as:
NOTEBOOK: [notebook_name]
TOPICS: [notebook_topics]
ANSWER: [the answer]
SOURCES: [citations if any]
```

**Example:**
```
/nlm ask-all What are the best practices for error handling?
```

**Notes:**
- Queries run in parallel for speed
- Each notebook is queried independently
- Results are aggregated with clear source attribution
- A summary table helps compare answers across sources
- Rate limits apply (50 queries/day free tier counts each notebook query separately)
- If a notebook query times out, retry once. If it still times out, record a timeout and continue.

### `create` - Create Notebook (RPC)

When user runs `/nlm create <name>`:
1. Use `notebook_create` with the name
2. Confirm and display the new notebook ID

### `rename` - Rename Notebook (RPC)

When user runs `/nlm rename <id> <name>`:
1. Use `notebook_rename` with notebook ID and new name
2. Confirm update

### `delete` - Delete Notebook (RPC)

When user runs `/nlm delete <id>`:
1. Confirm deletion intent
2. Use `notebook_delete` with confirmation
3. Report success

### `list` - List Notebooks

When user runs `/nlm list`:

1. Use `notebook_list`
2. Display as formatted table:

```markdown
## Your Notebooks

| Name | Topics | Last Used | Active |
|------|--------|-----------|--------|
| FastAPI Docs | fastapi, python | 2 hours ago | * |
| n8n Guide | n8n, workflows | 1 day ago | |
```

3. If no notebooks, suggest creating one:
   ```
   No notebooks found. Create one with:
   /nlm create <name>
   ```

### `auth` - Authentication Management

When user runs `/nlm auth [action]`:

**`/nlm auth` or `/nlm auth rpc`:**
1. Ensure cookies are available (via notebooklm-mcp-auth)
2. Call `save_auth_tokens` to persist cookies
3. Report success or failure

```markdown
## NotebookLM Authentication

Use notebooklm-mcp auth (cookie extraction), then persist cookies:

```markdown
## RPC Authentication

1) Run notebooklm-mcp-auth (auto or file mode)
2) Call save_auth_tokens
3) Re-run your /nlm command

Auth tokens are stored at:
~/.notebooklm-mcp/auth.json
```

### `source` - Manage Sources (RPC)

Subcommands:
- `/nlm source add-url <notebook_id> <url>`
- `/nlm source add-text <notebook_id> <text>`
- `/nlm source add-drive <notebook_id> <drive_doc_url> [title]`
- `/nlm source list <notebook_id>`
- `/nlm source sync <source_id> [source_id...]`
- `/nlm source delete <source_id>`

Use the corresponding RPC tools: `notebook_add_url`, `notebook_add_text`, `notebook_add_drive`, `source_list_drive`, `source_sync_drive`, `source_delete`.

Notes:
- `add-drive` expects a Google Doc ID + title. Extract the ID from the URL and pass it as `document_id`. If a title isn't provided, use the document title.
- `source sync` and `source delete` require `confirm=true` and operate on `source_id` values (use `/nlm source list` to get them).

### `research` - Research (RPC)

Subcommands:
- `/nlm research start <notebook_id> <query>`
- `/nlm research status <notebook_id>`
- `/nlm research import <notebook_id> <task_id>`

Use `research_start`, `research_status`, and `research_import`.
Notes:
- `research_start` returns a `task_id`.
- `research_status` polls by `notebook_id` (optional: poll_interval, max_wait, compact).
- `research_import` requires both `notebook_id` and `task_id`.

### `studio` - Studio Artifacts (RPC)

Subcommands:
- `/nlm studio audio <notebook_id>`
- `/nlm studio video <notebook_id>`
- `/nlm studio infographic <notebook_id>`
- `/nlm studio slides <notebook_id>`
- `/nlm studio status <notebook_id>`
- `/nlm studio delete <artifact_id>`

Use `audio_overview_create`, `video_overview_create`, `infographic_create`, `slide_deck_create`, `studio_status`, `studio_delete`.
Notes:
- Studio create/delete require `confirm=true`.
- `studio_status` lists artifacts by `notebook_id`.

### `describe` - Summaries (RPC)

- `/nlm describe notebook <notebook_id>` → `notebook_describe`
- `/nlm describe source <source_id>` → `source_describe`

### `configure` - Chat Settings (RPC)

- `/nlm configure goal <default|learning_guide|custom>`
- `/nlm configure length <default|shorter|longer>`
- `/nlm configure prompt <text>` (maps to `custom_prompt` when goal=custom)

**`/nlm auth rpc`:**
Show notebooklm-mcp auth steps:

```markdown
## NotebookLM RPC Authentication

1) Run notebooklm-mcp-auth (auto or file mode)
2) Call save_auth_tokens
3) Re-run your /nlm command

Auth tokens are stored at:
~/.notebooklm-mcp/auth.json
```

## Response Format

Always format responses with clear headers and structure:

- Use markdown tables for lists
- Include status indicators
- Show next steps or suggestions
- Display citations when showing answers

## Error Handling

- **Not authenticated:** Prompt `/nlm auth rpc`
- **Notebook not found:** Show available notebooks from library
- **Rate limited:** Inform user and suggest waiting
- **RPC tools missing:** Prompt user to add `notebooklm-rpc` MCP server or use `/nlm auth rpc`

## Tips

- First time? Run `/nlm auth rpc` to authenticate
- Prefer `notebooklm-rpc` for Drive sync and Studio tools
- Add notebooks with descriptive names
- Use `/nlm list` to see all available notebooks
- Use `notebook_id` to target a specific notebook for `/nlm ask`
