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

**Solution:**

```bash
# Run authentication setup
/nlm auth setup
```

A Chrome browser window will open. Complete the Google login and return to Claude Code.

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

## Known Limitations

| Limitation | Description |
|------------|-------------|
| Browser dependency | Requires Chrome/Chromium |
| Network required | No offline mode |
| Session persistence | ~30 days before re-auth needed |
| Rate limits | 50 queries/day (free), 250 (Pro/Ultra) |
| One notebook at a time | Must select active notebook |

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
