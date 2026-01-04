# Setup NotebookLM in YOUR Claude Desktop

## Your Specific Notebook
**URL:** https://notebooklm.google.com/notebook/8e98a4d8-f778-4dfc-88e8-2d59e48b1069

---

## Quick Setup (5 minutes)

### Step 1: Install the MCP Server

Open your terminal and run:

```bash
uv tool install notebooklm-mcp-server
```

**Expected output:**
```
added 67 packages in 15s
```

### Step 2: Configure Claude Desktop

#### For macOS:
```bash
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

#### For Windows:
```bash
notepad %APPDATA%/Claude/claude_desktop_config.json
```

#### For Linux:
```bash
nano ~/.config/Claude/claude_desktop_config.json
```

### Step 3: Add This Configuration

**If the file is empty or doesn't exist**, paste this:

```json
{
  "mcpServers": {
    "notebooklm-rpc": {
      "command": "notebooklm-mcp",
      "env": {}
    }
  }
}
```

**If the file already has content**, just add the `notebooklm-rpc` section inside `mcpServers`:

```json
{
  "mcpServers": {
    "existing-server": { ... },
    "notebooklm-rpc": {
      "command": "notebooklm-mcp",
      "env": {}
    }
  }
}
```

Save and close the file.

### Step 4: Restart Claude Desktop

1. **Completely quit** Claude Desktop (not just close the window)
   - macOS: Cmd+Q
   - Windows: Right-click tray icon → Exit
   - Linux: Close all windows

2. **Reopen** Claude Desktop

### Step 5: Verify MCP Server is Loaded

In a new conversation in Claude Desktop, type:

```
What MCP tools do you have available?
```

You should see Claude respond with a list including NotebookLM tools like:
- `notebook_list`
- `notebook_query`
- `notebook_add_url`
- `source_list_drive`
- `studio_status`

---

## Testing with Your Notebook

### First-Time Authentication

1) Run `notebooklm-mcp-auth` in a terminal and complete Google login.
2) In Claude Desktop, send this message:

```
List my NotebookLM notebooks
```
2. You'll see Google login page
3. Log in with your Google account
4. Chrome will navigate to your notebook
5. The MCP server will discover notebook metadata
6. Claude will suggest a name and topics
7. You confirm and it's added to your library

**Important:** This login is **one-time only**. The session is saved locally.

### Query Your Notebook

After adding it, you can ask questions naturally:

```
What are the main topics covered in my notebook?
```

```
How do I implement [specific feature] according to my notebook?
```

```
Search my notebook for information about [topic]
```

Claude will automatically:
1. Activate your notebook
2. Query NotebookLM
3. Return the answer with citations

---

## Expected Behavior

### ✅ Success Indicators

**Configuration loaded:**
```
User: What MCP tools do you have available?

Claude: I have access to several MCP tools including:
- NotebookLM tools (notebook_list, notebook_query, notebook_add_url, etc.)
- [other tools if you have them]
```

**Querying works:**
```
User: What does my notebook say about [topic]?

Claude: [Uses notebook_query tool]
        According to your notebook:
        [Answer from NotebookLM with citations]
```

---

## Troubleshooting

### Problem: "I don't see NotebookLM tools"

**Solution 1:** Check config file syntax
```bash
# Validate JSON (macOS/Linux)
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json | python3 -m json.tool

# Should show valid JSON without errors
```

**Solution 2:** Check MCP server installation
```bash
npm list -g notebooklm-mcp

# Should show: notebooklm-mcp@1.1.1 (or latest version)
```

**Solution 3:** Check Claude Desktop logs
- macOS: `~/Library/Logs/Claude/`
- Windows: `%APPDATA%/Claude/logs/`
- Linux: `~/.config/Claude/logs/`

Look for errors mentioning "notebooklm" or "MCP"

### Problem: "Chrome opens but login fails"

**Solution 1:** Clear browser state
```bash
# Remove saved browser data
rm -rf ~/.notebooklm-mcp/browser_state/

# Next time will re-authenticate
```

**Solution 2:** Use a different Google account
Consider using a dedicated Google account for automation (not your primary account)

**Solution 3:** Check Chrome installation
```bash
# macOS
ls /Applications/Google\ Chrome.app

# Linux
which google-chrome

# Windows
dir "C:\Program Files\Google\Chrome\Application\chrome.exe"
```

### Problem: "Notebook added but queries fail"

**Check authentication status:**
```bash
cat ~/.notebooklm-mcp/auth_info.json

# Should show: {"authenticated": true}
```

**Re-authenticate if needed:**
In Claude Desktop:
```
Reset my NotebookLM authentication
```

Then re-add your notebook.

---

## Advanced Usage

### Multiple Notebooks

You can add multiple notebooks:

```
Add this notebook: [URL1]
Add this notebook: [URL2]
Add this notebook: [URL3]
```

Claude will automatically select the right notebook based on your questions.

### Smart Selection

```
User: How do I implement authentication in FastAPI?

Claude: [Automatically activates FastAPI notebook if you have one]
        [Queries NotebookLM]
        [Returns answer]
```

### Explicit Notebook Selection

```
Use my FastAPI notebook to answer: How do I handle OAuth?
```

### Library Management

```
Show me all my notebooks

Remove notebook: [name]

Update notebook metadata: [name]
```

---

## Configuration File Location

Your config file will be at:

**macOS:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

**Linux:**
```
~/.config/Claude/claude_desktop_config.json
```

---

## Data Storage

After setup, your data will be at:

```
~/.notebooklm-mcp/
├── library.json           # Your notebook library
├── auth_info.json        # Authentication status
└── browser_state/        # Chrome session data
```

---

## Next Steps After Setup

1. ✅ Add your notebook (already have the URL)
2. ✅ Test with a simple question
3. ✅ Add more notebooks if needed
4. ✅ Use naturally in conversations

---

## Security Notes

- Browser state is stored locally
- Only you have access to the data
- Consider using a dedicated Google account
- Authentication persists for 30+ days

---

## Getting Help

**GitHub Issues:**
https://github.com/PleasePrompto/notebooklm-mcp/issues

**Documentation:**
https://github.com/PleasePrompto/notebooklm-mcp

**Check for updates:**
```bash
npm update -g notebooklm-mcp
```

---

## Quick Reference Card

### Installation
```bash
npm install -g notebooklm-mcp
```

### Config (add to claude_desktop_config.json)
```json
{
  "mcpServers": {
    "notebooklm-rpc": {
      "command": "notebooklm-mcp"
    }
  }
}
```

### First Use (in Claude Desktop)
```
List my NotebookLM notebooks
```

### Query
```
What does my notebook say about [topic]?
```

---

## ✅ You're Ready!

Once you complete these steps in YOUR Claude Desktop application, you'll be able to query your NotebookLM notebook directly in conversations!

The setup takes about 5 minutes, and then it works seamlessly.
