---
name: notebooklm-patterns
description: NotebookLM integration patterns, MCP tools reference, and troubleshooting. Use when working with NotebookLM notebooks, managing library, handling authentication issues, or understanding rate limits.
---

# NotebookLM Integration Patterns

Master NotebookLM integration for source-grounded research with citation-backed answers from Gemini.

## When to Use This Skill

- Setting up NotebookLM authentication
- Managing notebook library (add, list, select, search)
- Querying notebooks for research
- Troubleshooting authentication or rate limit issues
- Understanding NotebookLM MCP tool capabilities
- Organizing notebooks for efficient research workflows

## MCP Tools Reference

### Query Tools

#### `ask_question`
Ask a question to a NotebookLM notebook.

```
Parameters:
- question (required): The question to ask
- notebook_id (optional): Specific notebook ID (uses active if omitted)
- notebook_url (optional): Direct URL (overrides notebook_id)
- session_id (optional): For contextual follow-up questions
- browser_options (optional): {headless, show, timeout_ms, stealth}
```

**Usage Pattern:**
```python
# Query active notebook
ask_question(question="How do I implement OAuth?")

# Query specific notebook by URL
ask_question(
    question="What topics are covered?",
    notebook_url="https://notebooklm.google.com/notebook/abc123"
)

# Continue conversation in same session
ask_question(
    question="Can you show an example?",
    session_id="previous_session_id"
)
```

### Library Management Tools

#### `add_notebook`
Add a notebook to your library.

```
Parameters:
- url (required): NotebookLM notebook URL
- name (required): Display name
- description (required): What the notebook contains
- topics (required): Array of topic strings
- use_cases (optional): When to use this notebook
- tags (optional): Organization tags
- content_types (optional): Types of content
```

#### `list_notebooks`
List all notebooks in library. Returns array of notebook objects with metadata.

#### `select_notebook`
Set a notebook as active for queries.

```
Parameters:
- id (required): Notebook ID from library
```

#### `get_notebook`
Get detailed information about a specific notebook.

```
Parameters:
- id (required): Notebook ID
```

#### `search_notebooks`
Search library by query matching name, description, topics, tags.

```
Parameters:
- query (required): Search query string
```

#### `remove_notebook`
Remove a notebook from library (requires user confirmation).

```
Parameters:
- id (required): Notebook ID to remove
```

#### `update_notebook`
Update notebook metadata.

```
Parameters:
- id (required): Notebook ID
- name, description, topics, tags, use_cases (optional): Fields to update
```

### Authentication Tools

#### `get_health`
Check server status and authentication state.

Returns:
- status: "ok" or error
- authenticated: boolean
- active_sessions: count
- headless: boolean
- stealth_enabled: boolean

#### `setup_auth`
Initial authentication setup. Opens browser for Google login.

```
Parameters:
- show_browser (optional): Show browser window (default: true)
- browser_options (optional): Advanced browser settings
```

#### `re_auth`
Reset and re-authenticate. Use when:
- Rate limit reached (50 queries/day free tier)
- Switching Google accounts
- Authentication broken

### Session Tools

#### `list_sessions`
List all active NotebookLM sessions with stats.

#### `close_session`
Close a specific session by ID.

#### `reset_session`
Clear session history while keeping session ID.

## Workflow Patterns

### Pattern 1: First-Time Setup

```
1. Check status: get_health()
2. If not authenticated: setup_auth()
3. Add notebook: add_notebook(url, name, description, topics)
4. Query: ask_question(question)
```

### Pattern 2: Smart Notebook Discovery

Before adding a notebook, discover its content:

```
1. Query the URL directly:
   ask_question(
     question="What is this notebook about? List main topics.",
     notebook_url="<url>"
   )

2. Use response to populate metadata:
   add_notebook(
     url="<url>",
     name="<from discovery>",
     description="<from discovery>",
     topics=["<from discovery>"]
   )
```

### Pattern 3: Multi-Notebook Research

```
1. list_notebooks() to see all available
2. search_notebooks(query) to find relevant ones
3. select_notebook(id) to set active
4. ask_question(question) for each relevant notebook
5. Synthesize answers from multiple sources
```

### Pattern 4: Session Continuity

For follow-up questions in the same context:

```
1. First query: response = ask_question(question)
2. Extract session_id from response
3. Follow-up: ask_question(follow_up, session_id=session_id)
```

## Troubleshooting Guide

### Authentication Issues

**Problem: "Not authenticated" error**
```
Solution:
1. Run get_health() to confirm status
2. Run setup_auth() to open browser login
3. Complete Google login in browser
4. Verify with get_health()
```

**Problem: Authentication keeps failing**
```
Solution:
1. Close ALL Chrome/Chromium instances
2. Run cleanup_data(confirm=true, preserve_library=true)
3. Run setup_auth() for fresh start
```

**Problem: Session expired**
```
Solution:
1. Run re_auth() to clear and re-authenticate
2. Sessions typically last 30+ days
```

### Rate Limiting

**Problem: "Rate limit reached" (50 queries/day free tier)**
```
Solutions:
1. Wait until daily reset
2. Use re_auth() to switch Google accounts
3. Upgrade to Google AI Pro/Ultra for 5x limits
```

**Rate Limit Details:**
- Free tier: 50 queries/day, 100 notebooks, 50 sources each
- Pro/Ultra: 250 queries/day, 500 notebooks

### Browser Issues

**Problem: Chrome crashes or hangs**
```
Solution:
1. Close all Chrome instances
2. Clear browser state:
   cleanup_data(confirm=true, preserve_library=true)
3. Re-authenticate: setup_auth()
```

**Problem: "Browser not installed" error**
```
Solution:
1. Ensure Chrome (not Chromium) is installed
2. Check browser_install tool if available
```

### Query Issues

**Problem: Empty or poor responses**
```
Solutions:
1. Rephrase question to be more specific
2. Check notebook has relevant content
3. Try different notebook from library
```

**Problem: Wrong notebook being queried**
```
Solution:
1. list_notebooks() to see library
2. select_notebook(correct_id) to set active
3. Re-run query
```

## Best Practices

### Notebook Organization

1. **Descriptive Names**: Use clear, searchable names
2. **Specific Topics**: Tag with precise topics for search
3. **One Domain Per Notebook**: Don't mix unrelated content
4. **Regular Cleanup**: Remove outdated notebooks

### Query Optimization

1. **Specific Questions**: "How do I implement X?" not "Tell me about X"
2. **Follow-up Sessions**: Use session_id for related questions
3. **Multiple Angles**: Ask same topic from different perspectives
4. **Verify Sources**: Check citations in responses

### Research Workflows

1. **Discovery First**: Always discover content before adding
2. **Organize by Project**: Group notebooks by use case
3. **Regular Updates**: Re-discover notebooks when source content changes
4. **Cross-Reference**: Query multiple notebooks for comprehensive answers

## Limits and Quotas

| Resource | Free Tier | Pro/Ultra |
|----------|-----------|-----------|
| Daily Queries | 50 | 250 |
| Notebooks | 100 | 500 |
| Sources per Notebook | 50 | 100 |
| Words per Source | 500,000 | 1,000,000 |

## Security Notes

- All credentials stored locally
- Browser state encrypted
- Never share browser_state directory
- Consider dedicated Google account for automation
- NotebookLM terms of service apply
