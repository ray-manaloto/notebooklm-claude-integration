# /notebook - Query NotebookLM notebooks

Query your Google NotebookLM notebooks with source-grounded, citation-backed answers from Gemini.

## Usage

```
/notebook ask <question>
/notebook add <url>
/notebook list
/notebook activate <name or id>
/notebook search <topic>
```

## Examples

### Ask a question
```
/notebook ask "How do I implement OAuth in FastAPI?"
```

### Add a new notebook
```
/notebook add https://notebooklm.google.com/notebook/abc123
```

### List all notebooks
```
/notebook list
```

### Search notebooks by topic
```
/notebook search "python async"
```

### Activate a notebook
```
/notebook activate "FastAPI Documentation"
```

## How it works

1. **Browser Automation**: Uses Patchright (patched Playwright) to interact with NotebookLM
2. **Persistent Auth**: Login once, credentials saved locally
3. **Smart Selection**: Claude automatically picks the relevant notebook
4. **Deep Research**: Automatic follow-up questions for comprehensive answers
5. **Zero Hallucinations**: Answers only from your uploaded documents

## Arguments

- `ask <question>` - Ask a question to the active or most relevant notebook
- `add <url>` - Add a NotebookLM URL to your library
- `list` - Show all notebooks in your library
- `activate <name>` - Set a notebook as active for queries
- `search <topic>` - Find notebooks by topic or tag

## Notes

- First run will open Chrome for Google login
- Credentials stored locally in `~/.claude/skills/notebooklm/data/`
- Uses real Chrome (not Chromium) for better Google compatibility
- Humanization features included (realistic typing, natural delays)
- Recommend using a dedicated Google account

## See Also

- `/notebook-auth` - Manage authentication
- `/notebook-library` - Advanced library management
