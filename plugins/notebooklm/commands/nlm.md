---
name: nlm
description: Query NotebookLM notebooks for source-grounded answers
argument-hint: "<ask|ask-all|add|list|select|auth> [arguments]"
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
| `ask-all` | `/nlm ask-all <question>` | Ask all notebooks in parallel, compare answers |
| `add` | `/nlm add <url>` | Add a notebook to your library |
| `list` | `/nlm list` | List all notebooks in library |
| `select` | `/nlm select <name or id>` | Set active notebook |
| `auth` | `/nlm auth [setup\|status\|reset\|cdp\|keychain]` | Manage authentication |

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

### `ask-all` - Ask All Notebooks (Parallel)

When user runs `/nlm ask-all <question>`:

This command queries **all notebooks in your library simultaneously** using parallel subagents, then aggregates the responses with clear notebook identification.

**Execution Steps:**

1. Check if authenticated using `get_health`
2. If not authenticated, prompt user to run `/nlm auth setup`
3. Use `list_notebooks` to get all notebooks in library
4. If no notebooks, prompt user to add one with `/nlm add <url>`
5. If only one notebook, suggest using `/nlm ask` instead for efficiency
6. **For each notebook, spawn a parallel subagent** using the Task tool:
   - Each subagent should:
     a. Ask the question using `ask_question` with `notebook_id` (avoid `select_notebook` to prevent shared-state races)
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
1. Use ask_question with the question and notebook_id "[notebook_id]"
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
- If a notebook query times out, retry once with a longer timeout (e.g., browser_options.timeout_ms=60000)

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
2. Display status with backend information:

```markdown
## NotebookLM Authentication Status

- **Authenticated:** Yes/No
- **Active Sessions:** X
- **Headless Mode:** Yes/No

### Authentication Backends (tried in order)
| Backend | Status | Description |
|---------|--------|-------------|
| CDP | ✅/❌ | Chrome with --remote-debugging-port=9222 |
| Keychain | ✅/❌ | macOS Keychain stored cookies |
| Persistent | ✅/❌ | Browser profile at ~/.notebooklm-auth |
| Manual | ⚪ | Interactive browser login (fallback) |
```

**`/nlm auth setup`:**
1. Use `setup_auth` tool (will open browser)
2. Inform user: "Browser opened for Google login. Complete login and return here."
3. After completion, confirm authentication

**`/nlm auth reset`:**
1. Use `re_auth` tool to clear and re-authenticate
2. Inform user about the reset process

**`/nlm auth cdp`:**
Show instructions for Chrome CDP setup (best authentication experience):

```markdown
## Chrome Remote Debugging Setup

For seamless authentication, start Chrome with remote debugging:

**macOS:**
\`\`\`bash
open -a "Google Chrome" --args --remote-debugging-port=9222
\`\`\`

**Windows:**
\`\`\`bash
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
\`\`\`

**Linux:**
\`\`\`bash
google-chrome --remote-debugging-port=9222
\`\`\`

**Benefits:**
- Uses your existing Google login (no separate auth needed)
- Faster - no browser automation delay
- Works with your Chrome extensions

**Tip:** Add an alias to your shell profile:
\`\`\`bash
alias chrome-debug='open -a "Google Chrome" --args --remote-debugging-port=9222'
\`\`\`
```

**`/nlm auth keychain`:**
Show macOS Keychain status:

```markdown
## Keychain Authentication

Cookies are securely stored in macOS Keychain.

**Status:** Stored/Not Stored
**Saved At:** [timestamp]

**Commands:**
- Cookies auto-save after successful login
- Clear with: `/nlm auth reset`
```

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

- **Best auth experience:** Run `/nlm auth cdp` for Chrome remote debugging setup
- First time? Run `/nlm auth setup` to authenticate
- Add notebooks with descriptive URLs
- Use `/nlm list` to see all available notebooks
- The active notebook is used for all `/nlm ask` queries
- On macOS, cookies are automatically saved to Keychain for headless use
- Run Chrome with `--remote-debugging-port=9222` for seamless session reuse
