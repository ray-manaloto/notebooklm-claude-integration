---
name: notebooklm-patterns
description: NotebookLM integration patterns aligned to notebooklm-mcp (RPC tool names, auth flow, and troubleshooting). Use when listing/creating/querying notebooks, managing sources, running research, or generating studio artifacts.
---

# NotebookLM Integration Patterns

Master NotebookLM integration for source-grounded research with citation-backed answers from Gemini.

## When to Use This Skill

- Setting up NotebookLM authentication for notebooklm-mcp
- Listing/creating/querying notebooks and managing sources
- Running research workflows (web/drive) and importing sources
- Generating studio artifacts (audio, video, slides, infographics)
- Troubleshooting authentication, timeouts, or rate limits

## MCP Tools Reference

### Query Tools (RPC)

#### `notebook_query`
Ask a question to a specific notebook by `notebook_id`.

```
Parameters:
- notebook_id (required): Notebook ID from notebook_list
- question (required): The question to ask
- session_id (optional): For contextual follow-up questions
```

**Usage Pattern:**
```python
# Query specific notebook by ID
notebook_query(
    notebook_id="abc123",
    question="What topics are covered?"
)

# Continue a session
notebook_query(
    notebook_id="abc123",
    question="Show an example.",
    session_id="previous_session_id"
)
```

**Timeout Handling:**
- If a notebook query times out, retry once.
- If it still times out, record a timeout for that notebook and continue.

### Library & Source Tools (RPC)

#### Notebooks
- `notebook_list`: list all notebooks
- `notebook_create`: create a new notebook
- `notebook_get`: get notebook details with sources
- `notebook_describe`: AI summary of notebook content
- `notebook_rename`: rename a notebook
- `notebook_delete`: delete a notebook (confirmation required)

#### Sources
- `notebook_add_url`: add URL/YouTube as source
- `notebook_add_text`: add pasted text as source
- `notebook_add_drive`: add Google Drive doc as source
- `source_list_drive`: list sources with freshness status
- `source_sync_drive`: sync stale Drive sources (confirmation required)
- `source_delete`: delete a source (confirmation required)
- `source_describe`: AI summary and keywords for a source

### Authentication Tools (RPC)

#### `save_auth_tokens`
Persist auth cookies for notebooklm-mcp. Required before using RPC tools.

**Default flow:** run `notebooklm-mcp-auth` once, then `save_auth_tokens`.

**File mode:** use `notebooklm-mcp-auth --file` to manually extract cookies, then `save_auth_tokens`.

### Research & Studio Tools (RPC)

#### Research
- `research_start`: start web/drive research
- `research_status`: poll progress (built-in wait)
- `research_import`: import discovered sources into a notebook

#### Studio
- `audio_overview_create`
- `video_overview_create`
- `infographic_create`
- `slide_deck_create`
- `studio_status`
- `studio_delete`

## Workflow Patterns

### Pattern 1: First-Time Setup

```
1. Authenticate: run `notebooklm-mcp-auth`, then `save_auth_tokens`
2. List notebooks: `notebook_list`
3. Query: `notebook_query(notebook_id, question)`
```

### Pattern 2: Smart Notebook Discovery

Before adding a notebook, discover its content:

```
1. Query by notebook ID with `notebook_query`
2. Use response to name/describe with `notebook_rename` or `notebook_describe`
```

### Pattern 3: Multi-Notebook Research

```
1. `notebook_list` to see all available
2. Select IDs and run `notebook_query` per notebook
3. Synthesize answers with notebook names/IDs labeled
```

### Pattern 4: Session Continuity

For follow-up questions in the same context:

```
1. First query: response = notebook_query(question)
2. Extract session_id from response
3. Follow-up: notebook_query(follow_up, session_id=session_id)
```

## Troubleshooting Guide

### Authentication Issues

**Problem: "Not authenticated" error**
```
Solution:
1. Run notebooklm-mcp-auth (auto mode) and log in once
2. Call save_auth_tokens
3. Retry the RPC call
```

**Problem: Authentication keeps failing**
```
Solution:
1. Re-run notebooklm-mcp-auth (auto or file mode)
2. Call save_auth_tokens
```

**Problem: Session expired**
```
Solution:
1. Re-run notebooklm-mcp-auth
2. Call save_auth_tokens
```

**Problem: CDP not detecting Chrome**
```
Solution:
1. Ensure Chrome started with --remote-debugging-port=9222
2. Check if port is listening: curl http://localhost:9222/json/version
3. Only one Chrome instance can use debugging port at a time
4. Close other Chrome instances and restart with flag
```

### Rate Limiting

**Problem: "Rate limit reached" (50 queries/day free tier)**
```
Solutions:
1. Wait until daily reset
2. Re-run notebooklm-mcp-auth with a different Google account
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
3. Re-run notebooklm-mcp-auth and call save_auth_tokens
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
1. Use notebook_list to see notebooks
2. Re-run query with the correct notebook_id
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
