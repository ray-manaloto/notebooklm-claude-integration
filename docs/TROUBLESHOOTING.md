# Troubleshooting Guide

Common issues and solutions for NotebookLM Claude Integration.

## Quick Diagnostics

Run this command to check system health:

```bash
cd ~/.claude/plugins/installed/notebooklm/skills/notebooklm/scripts
python3 run.py auth status
python3 run.py list
```

---

## Common Issues

### 1. Plugin Not Found

**Symptom:**
```
Error: Unknown command '/notebook'
```

**Solution:**

```bash
# Check if plugin is installed
ls ~/.claude/plugins/installed/notebooklm

# If missing, reinstall
cd /path/to/notebooklm-claude-integration
cp -r plugin/notebooklm ~/.claude/plugins/installed/

# Restart Claude Code
```

---

### 2. Authentication Fails

**Symptom:**
```
Error: Authentication required. Run /notebook-auth setup
```

**Solutions:**

**A. Clear and re-authenticate:**
```bash
/notebook-auth reset
/notebook-auth setup
```

**B. Check browser state:**
```bash
ls ~/.claude/plugins/installed/notebooklm/skills/notebooklm/data/browser_state/
# If corrupted, delete:
rm -rf ~/.claude/plugins/installed/notebooklm/skills/notebooklm/data/browser_state/
/notebook-auth setup
```

**C. Manually verify auth file:**
```bash
cat ~/.claude/plugins/installed/notebooklm/skills/notebooklm/data/auth_info.json
# Should show: "authenticated": true
```

---

### 3. Chrome Browser Issues

**Symptom:**
```
Error: Could not launch Chrome browser
```

**Solutions:**

**A. Verify Chrome installation:**
```bash
which google-chrome
which chromium-browser
which chrome

# Install if missing (Ubuntu/Debian):
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
```

**B. Check Patchright installation:**
```bash
cd ~/.claude/plugins/installed/notebooklm/skills/notebooklm/scripts
pip show patchright

# Reinstall if needed:
pip install --upgrade patchright
```

**C. Set custom Chrome path:**
```bash
# Create .env file
cd ~/.claude/plugins/installed/notebooklm/skills/notebooklm/scripts
cat > .env << 'EOF'
CHROME_PATH=/usr/bin/google-chrome
EOF
```

---

### 4. Import Errors

**Symptom:**
```
ModuleNotFoundError: No module named 'patchright'
```

**Solution:**

```bash
cd ~/.claude/plugins/installed/notebooklm/skills/notebooklm/scripts
pip install -r requirements.txt

# If using virtual environment:
source venv/bin/activate
pip install -r requirements.txt
```

---

### 5. No Active Notebook

**Symptom:**
```
Error: No notebook is currently active
```

**Solution:**

```bash
# List available notebooks
/notebook list

# Activate one
/notebook activate <id or name>

# Verify
/notebook list
# Should show "active": true
```

---

### 6. Notebook Not Found

**Symptom:**
```
Error: Notebook 'abc123' not found in library
```

**Solutions:**

**A. Check library:**
```bash
/notebook list
# Note the exact ID

/notebook activate <exact-id>
```

**B. Re-add notebook:**
```bash
/notebook add https://notebooklm.google.com/notebook/YOUR_ID
/notebook activate YOUR_ID
```

**C. Check library file:**
```bash
cat ~/.claude/plugins/installed/notebooklm/skills/notebooklm/data/library.json
# Verify notebook exists in JSON
```

---

### 7. Query Timeout

**Symptom:**
```
Error: Query timed out after 30 seconds
```

**Solutions:**

**A. Increase timeout:**
```bash
# Edit .env
cd ~/.claude/plugins/installed/notebooklm/skills/notebooklm/scripts
cat >> .env << 'EOF'
QUERY_TIMEOUT=60000
EOF
```

**B. Check NotebookLM availability:**
```bash
# Test in regular browser
open https://notebooklm.google.com
```

**C. Simplify question:**
```bash
# Instead of complex multi-part questions:
/notebook ask "What is OAuth2?"

# Better than:
/notebook ask "Explain OAuth2 implementation with JWT tokens, refresh tokens, and PKCE flow including security considerations"
```

---

### 8. Python Version Issues

**Symptom:**
```
SyntaxError: invalid syntax
```

**Solution:**

```bash
# Check Python version (need 3.10+)
python3 --version

# Use correct Python
python3.10 run.py list
# or
python3.11 run.py list

# Update default if needed
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
```

---

### 9. Permission Errors

**Symptom:**
```
PermissionError: [Errno 13] Permission denied
```

**Solution:**

```bash
# Fix permissions
chmod -R u+w ~/.claude/plugins/installed/notebooklm/skills/notebooklm/data/

# Check ownership
ls -la ~/.claude/plugins/installed/notebooklm/skills/notebooklm/data/
```

---

### 10. JSON Decode Errors

**Symptom:**
```
JSONDecodeError: Expecting value: line 1 column 1
```

**Solutions:**

**A. Reset library:**
```bash
cd ~/.claude/plugins/installed/notebooklm/skills/notebooklm/data/
mv library.json library.json.backup
cat > library.json << 'EOF'
{
  "notebooks": [],
  "active_notebook": null,
  "settings": {}
}
EOF
```

**B. Validate JSON:**
```bash
python3 -c "import json; print(json.load(open('library.json')))"
```

---

### 11. Network Issues

**Symptom:**
```
Error: Could not reach NotebookLM
```

**Solutions:**

**A. Check internet:**
```bash
ping google.com
curl -I https://notebooklm.google.com
```

**B. Check proxy settings:**
```bash
echo $HTTP_PROXY
echo $HTTPS_PROXY

# If behind proxy, set in .env:
HTTP_PROXY=http://proxy.company.com:8080
HTTPS_PROXY=http://proxy.company.com:8080
```

**C. Check firewall:**
```bash
# Temporarily disable (Ubuntu)
sudo ufw disable
# Test, then re-enable
sudo ufw enable
```

---

### 12. Rate Limiting

**Symptom:**
```
Error: Rate limit exceeded. Try again in 60 seconds.
```

**Solution:**

```bash
# Wait the specified time
# Rate limits:
# - 10 queries per minute
# - 5 add operations per minute
# - 3 auth setups per hour
```

---

## Debugging

### Enable Debug Mode

```bash
cd ~/.claude/plugins/installed/notebooklm/skills/notebooklm/scripts
cat >> .env << 'EOF'
DEBUG=true
LOG_LEVEL=DEBUG
EOF
```

### Check Logs

```bash
# Run with verbose output
python3 run.py ask "test question" 2>&1 | tee debug.log

# Check browser console
# (Headless mode disabled shows browser window)
cat >> .env << 'EOF'
HEADLESS=false
EOF
```

### Test Individual Components

```bash
cd ~/.claude/plugins/installed/notebooklm/skills/notebooklm/scripts

# Test auth
python3 -c "from auth_manager import AuthManager; print(AuthManager().get_status())"

# Test library
python3 -c "from notebook_manager import NotebookManager; print(NotebookManager().list_notebooks())"

# Test query
python3 -c "from ask_question import ask_notebook; print(ask_notebook('test'))"
```

---

## Complete Reset

If all else fails:

```bash
# 1. Backup data
cp -r ~/.claude/plugins/installed/notebooklm/skills/notebooklm/data ~/notebooklm-backup

# 2. Remove plugin
rm -rf ~/.claude/plugins/installed/notebooklm

# 3. Reinstall
cd /path/to/notebooklm-claude-integration
cp -r plugin/notebooklm ~/.claude/plugins/installed/

# 4. Install dependencies
cd ~/.claude/plugins/installed/notebooklm/skills/notebooklm/scripts
pip install -r requirements.txt

# 5. Setup from scratch
claude
/notebook-auth setup
/notebook add https://notebooklm.google.com/notebook/YOUR_ID
```

---

## Getting Help

### Check System Status

```bash
# Python
python3 --version

# Chrome
google-chrome --version

# Claude Code
claude --version

# Dependencies
pip show patchright python-dotenv
```

### Collect Debug Info

```bash
#!/bin/bash
# debug_info.sh

echo "=== System Info ==="
uname -a
python3 --version
google-chrome --version || chromium-browser --version

echo -e "\n=== Plugin Status ==="
ls -la ~/.claude/plugins/installed/notebooklm/

echo -e "\n=== Auth Status ==="
cd ~/.claude/plugins/installed/notebooklm/skills/notebooklm/scripts
python3 run.py auth status

echo -e "\n=== Library ==="
python3 run.py list

echo -e "\n=== Dependencies ==="
pip show patchright python-dotenv

echo -e "\n=== Environment ==="
cat .env 2>/dev/null || echo "No .env file"
```

### Report Issues

Include this information:

1. Debug info output (above script)
2. Error message (full traceback)
3. Steps to reproduce
4. Expected vs actual behavior

**GitHub:** https://github.com/ray-manaloto/notebooklm-claude-integration/issues

---

## Known Limitations

- **Browser dependency**: Requires Chrome/Chromium
- **Network required**: No offline mode
- **Session persistence**: ~30 days, then re-auth needed
- **Query timeout**: Complex queries may timeout
- **Rate limits**: Built-in to prevent abuse
- **No parallel queries**: One query at a time

---

## FAQ

**Q: Can I use Firefox instead of Chrome?**  
A: Not currently. Patchright only supports Chromium-based browsers.

**Q: Does this work on Windows?**  
A: Yes, but paths are different. Use `%USERPROFILE%\.claude\plugins\...`

**Q: Can I use multiple Google accounts?**  
A: Yes, but only one at a time. Use `/notebook-auth reset` to switch.

**Q: Is my data stored remotely?**  
A: No, everything is local. Library and auth files are on your machine.

**Q: Can I query multiple notebooks simultaneously?**  
A: Not yet. You must activate one notebook at a time.

**Q: How do I update the plugin?**  
A: Pull latest from GitHub and copy files again. Data files are preserved.

---

For more help, see:
- [API Reference](API_REFERENCE.md)
- [Setup Guides](CLAUDE_CODE_SETUP.md)
- [GitHub Issues](https://github.com/ray-manaloto/notebooklm-claude-integration/issues)
