# Troubleshooting Guide

Common issues and solutions for NotebookLM Claude Integration.

## Quick Diagnostics

Check system health with these commands:

```bash
# Check authentication status
/nlm auth

# List notebooks
/nlm list
```

---

## Common Issues

### 1. Plugin Not Found

**Symptom:**
```
Error: Unknown command '/nlm'
```

**Solution:**

```bash
# Check if marketplace is added
claude plugin marketplace list

# If missing, add the marketplace
claude plugin marketplace add /path/to/notebooklm-claude-integration/plugins/notebooklm

# Install the plugin
claude plugin install notebooklm@notebooklm-plugin --scope project

# Restart Claude Code
claude
```

---

### 2. Not Authenticated

**Symptom:**
```
Error: Not authenticated. Run /nlm auth setup
```

**Solutions (try in order):**

**A. Best: Use Chrome Remote Debugging (no popups)**
```bash
# Start Chrome with remote debugging
open -a "Google Chrome" --args --remote-debugging-port=9222

# Login to NotebookLM in Chrome (one-time)
# Navigate to https://notebooklm.google.com

# Now queries use your existing session automatically!
```

**B. Alternative: Interactive setup**
```bash
# Run authentication setup
/nlm auth setup
```
A Chrome browser window will open. Complete the Google login and return to Claude Code.

**C. Check status and available backends:**
```bash
/nlm auth
# Shows: CDP, Keychain, Persistent, Manual backend status
```

---

### 3. Rate Limited

**Symptom:**
```
Error: Rate limit exceeded (50 queries/day for free tier)
```

**Solutions:**

**A. Wait for daily reset**
- Rate limits reset at midnight UTC

**B. Switch Google accounts:**
```bash
/nlm auth reset
```
Then login with a different Google account.

**C. Upgrade to Google AI Pro/Ultra**
- 5x higher limits (250 queries/day)

---

### 4. No Active Notebook

**Symptom:**
```
Error: No notebook is currently active
```

**Solution:**

```bash
# List available notebooks
/nlm list

# Select one
/nlm select <name>
```

If no notebooks exist:
```bash
/nlm add https://notebooklm.google.com/notebook/YOUR_NOTEBOOK_ID
```

---

### 5. Notebook Not Found

**Symptom:**
```
Error: Notebook not found in library
```

**Solution:**

```bash
# Check available notebooks
/nlm list

# Re-add the notebook
/nlm add https://notebooklm.google.com/notebook/YOUR_NOTEBOOK_ID
```

---

### 6. Browser/Chrome Issues

**Symptom:**
```
Error: Could not launch browser
```

**Solutions:**

**A. Verify Chrome is installed:**
```bash
# macOS
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version

# Linux
google-chrome --version

# Windows
"C:\Program Files\Google\Chrome\Application\chrome.exe" --version
```

**B. Reset browser state:**
```bash
/nlm auth reset
```

**C. Check MCP server:**
```bash
claude mcp list
# Should show 'notebooklm' server
```

---

### 7. MCP Server Not Available

**Symptom:**
```
Error: MCP server 'notebooklm' not found
```

**Solution:**

```bash
# Add the MCP server
claude mcp add notebooklm -- npx -y notebooklm-mcp@latest

# Restart Claude Code
claude
```

---

### 8. Query Timeout

**Symptom:**
```
Error: Query timed out
```

**Solutions:**

**A. Check NotebookLM availability:**
Open https://notebooklm.google.com in a browser to verify it's working.

**B. Simplify your question:**
```bash
# Instead of complex multi-part questions:
/nlm ask "What is OAuth2?"

# Better than:
/nlm ask "Explain OAuth2 implementation with JWT tokens, refresh tokens, and PKCE flow including security considerations"
```

**C. Check internet connection:**
```bash
ping google.com
```

---

### 9. Wrong Notebook Being Queried

**Symptom:**
Answers don't match expected content.

**Solution:**

```bash
# Check which notebook is active
/nlm list

# The [ACTIVE] marker shows current notebook

# Switch if needed
/nlm select "Correct Notebook Name"
```

---

### 10. Authentication Expired

**Symptom:**
```
Error: Session expired
```

**Solution:**

```bash
# Re-authenticate
/nlm auth setup
```

Sessions typically last 30+ days but may expire sooner.

---

## Debugging

### Check Authentication Status

```bash
/nlm auth
```

**Expected output:**
```
Authentication Status:
- Authenticated: true
- Ready to query notebooks
```

### Check Notebook Library

```bash
/nlm list
```

**Expected output:**
```
Notebooks in library:
1. [ACTIVE] My Documentation
   Topics: api, python, fastapi
```

### Verify MCP Server

```bash
claude mcp list
```

**Expected output:**
```
notebooklm: npx -y notebooklm-mcp@latest
```

---

## Complete Reset

If all else fails, perform a complete reset:

```bash
# 1. Reset authentication
/nlm auth reset

# 2. Remove and re-add MCP server
claude mcp remove notebooklm
claude mcp add notebooklm -- npx -y notebooklm-mcp@latest

# 3. Restart Claude Code
claude

# 4. Re-authenticate
/nlm auth setup

# 5. Re-add notebooks
/nlm add https://notebooklm.google.com/notebook/YOUR_NOTEBOOK_ID
```

---

## Session Cap Reached

**Symptoms:**
- `ask_question` requests time out unexpectedly
- `get_health` shows `active_sessions` equal to `max_sessions` (default 10)

**Fix:**
- Close old sessions via MCP tools (`list_sessions` → `close_session`) or
- Restart the NotebookLM MCP server to clear inactive sessions

If you’re using Codex/Claude tools, ask the agent to run:
`mcp__notebooklm__list_sessions` and close inactive session IDs.

---

## Getting Help

### Collect Debug Info

When reporting issues, include:

1. **Authentication status:** `/nlm auth`
2. **Notebook list:** `/nlm list`
3. **MCP server status:** `claude mcp list`
4. **Error message** (full text)
5. **Steps to reproduce**

### Report Issues

**GitHub:** https://github.com/ray-manaloto/notebooklm-claude-integration/issues

---

## Authentication Backends

The plugin supports multiple authentication backends, tried in priority order:

| Backend | Priority | Platform | Description |
|---------|----------|----------|-------------|
| **CDP** | 1 | All | Connect to Chrome with `--remote-debugging-port=9222` |
| **Keychain** | 2 | macOS | Stored cookies in macOS Keychain |
| **Persistent** | 3 | All | Playwright browser profile at `~/.notebooklm-auth` |
| **Manual** | 4 | All | Interactive browser login (fallback) |

### Setting Up CDP (Recommended)

```bash
# macOS
open -a "Google Chrome" --args --remote-debugging-port=9222

# Windows
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222

# Linux
google-chrome --remote-debugging-port=9222

# Verify it's working
curl http://localhost:9222/json/version
```

**Tip:** Add an alias to your shell profile:
```bash
alias chrome-debug='open -a "Google Chrome" --args --remote-debugging-port=9222'
```

### Keychain Storage (macOS)

Cookies are automatically saved to macOS Keychain after successful login.

If headless runs show a “User interaction is not allowed” popup, clear the
keychain entry and re-login so cookies are saved with trusted-app access:

```bash
nlm-auth logout
nlm-auth login
```

```bash
# Check if cookies are stored
security find-generic-password -s "notebooklm-claude-auth" -a "$USER-cookies"

# Clear stored cookies
security delete-generic-password -s "notebooklm-claude-auth" -a "$USER-cookies"
```

### Persistent Profile

Browser state stored at `~/.notebooklm-auth/chrome-profile/`.

```bash
# Clear persistent profile
rm -rf ~/.notebooklm-auth/chrome-profile
```

---

## Known Limitations

| Limitation | Description |
|------------|-------------|
| Browser dependency | Requires Chrome/Chromium |
| Network required | No offline mode |
| Session persistence | ~30 days before re-auth needed (Keychain extends this) |
| Rate limits | 50 queries/day (free), 250 (Pro/Ultra) |
| One notebook at a time | Must select active notebook |
| CDP single instance | Only one Chrome can use debugging port |
| Session cap | Max 10 active sessions; close or restart to clear |

---

## FAQ

**Q: Can I use Firefox instead of Chrome?**
A: No. The MCP server uses Playwright which requires Chromium-based browsers.

**Q: Does this work on Windows?**
A: Yes, with Chrome installed.

**Q: Can I use multiple Google accounts?**
A: Yes, but only one at a time. Use `/nlm auth reset` to switch accounts.

**Q: Is my data stored remotely?**
A: No. All data (library, auth) is stored locally by the MCP server.

**Q: Can I query multiple notebooks at once?**
A: No. You must select one active notebook at a time.

**Q: How do I update the plugin?**
A: Pull the latest from GitHub and reinstall:
```bash
claude plugin install notebooklm@notebooklm-plugin --scope project
```

---

For more help, see:
- [API Reference](API_REFERENCE.md) - All commands and tools
- [Claude Code Setup](CLAUDE_CODE_SETUP.md) - Installation guide
- [Main README](../README.md) - Project overview
