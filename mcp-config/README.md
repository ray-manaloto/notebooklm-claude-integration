# MCP Configuration Management

This directory contains a centralized approach to managing MCP servers for both Claude Desktop and Claude Code.

## 📁 Files

- **servers.json** - Single source of truth for all MCP server definitions
- **install-desktop.sh** - Deploy to Claude Desktop
- **install-code.sh** - Deploy to Claude Code CLI
- **update-all.sh** - Update both environments at once
- **env.example** - Template for environment variables

## 🚀 Quick Start

### 1. Set Up Environment Variables

```bash
# Copy the example file
cp env.example ~/.mcp-env

# Edit with your actual credentials
nano ~/.mcp-env

# Add to your shell config
echo "source ~/.mcp-env" >> ~/.zshrc  # or ~/.bashrc

# Reload shell
source ~/.zshrc
```

### 2. Install to Both Environments

```bash
# Install to both Claude Desktop and Claude Code
./update-all.sh

# Or install individually:
./install-desktop.sh
./install-code.sh
```

### 3. Verify Installation

```bash
# For Claude Desktop: Look for MCP icon in chat input
# (Restart Claude Desktop first!)

# For Claude Code:
claude mcp list
claude  # Start CLI, then use /mcp command
```

## 📝 Managing Servers

### Add a New MCP Server

Edit `servers.json`:

```json
{
  "my-new-server": {
    "command": "npx",
    "args": ["-y", "my-mcp-package"],
    "env": {
      "API_KEY": "${MY_API_KEY}"
    },
    "description": "What this server does"
  }
}
```

Then update both environments:

```bash
./update-all.sh
```

### Remove a Server

1. Remove from `servers.json`
2. Run `./update-all.sh`
3. For Claude Code only: `claude mcp remove server-name`

### Update a Server

1. Edit the server definition in `servers.json`
2. Run `./update-all.sh`

## 🔧 Customization

### Modify for Your Setup

Edit `servers.json` to customize:

1. **File system access path**:
   ```json
   "filesystem": {
     "args": ["-y", "@modelcontextprotocol/server-filesystem", "/YOUR/PATH"]
   }
   ```

2. **Add/remove servers** based on your needs

3. **Set environment variables** in `~/.mcp-env`

## 🎯 Server Descriptions

| Server | Purpose | Requires |
|--------|---------|----------|
| **notebooklm** | Query NotebookLM notebooks | - |
| **github** | GitHub repo/PR/issue management | GITHUB_TOKEN |
| **brave-search** | Web search via Brave API | BRAVE_API_KEY |
| **context7** | Up-to-date library documentation | - |
| **filesystem** | Local file system access | - |

## 🔒 Security Best Practices

1. **Never commit secrets**:
   ```bash
   # Add to .gitignore
   echo "~/.mcp-env" >> ../.gitignore
   echo "mcp-config/env.local" >> ../.gitignore
   ```

2. **Use environment variables** for all credentials

3. **Rotate tokens regularly**

4. **Use minimum required scopes** for tokens

## 🐛 Troubleshooting

### Servers not appearing in Claude Desktop

1. Check config file location:
   ```bash
   # macOS
   cat "$HOME/Library/Application Support/Claude/claude_desktop_config.json"
   ```

2. Restart Claude Desktop completely

3. Look for MCP indicator (should be in bottom-right)

### Servers failing in Claude Code

1. Check server status:
   ```bash
   claude mcp list
   ```

2. Verify environment variables:
   ```bash
   echo $GITHUB_TOKEN
   ```

3. Check logs:
   ```bash
   # Inside Claude Code
   /mcp
   ```

### Environment variables not working

1. Make sure you sourced the config:
   ```bash
   source ~/.zshrc
   ```

2. Verify in new terminal:
   ```bash
   echo $GITHUB_TOKEN
   ```

3. Check shell config was modified:
   ```bash
   tail ~/.zshrc
   ```

## 📚 Related Documentation

- [MCP Config Best Practices](../MCP_CONFIG_BEST_PRACTICES.md) - Complete guide
- [Claude Code MCP Docs](https://code.claude.com/docs/en/mcp)
- [Model Context Protocol](https://modelcontextprotocol.io)

## 🔄 Workflow

```
Edit servers.json
        ↓
./update-all.sh
        ↓
    ┌───┴───┐
    ↓       ↓
Desktop   Code
    ↓       ↓
Restart  Verify
```

---

**Pro Tip**: Keep `servers.json` in version control, but keep credentials in `~/.mcp-env` (not in git!)
