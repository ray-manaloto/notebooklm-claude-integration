# MCP Server Configuration: Modern Best Practices (2024/2025)

## TL;DR - The Reality

❌ **You CANNOT directly share one config file** between Claude Desktop and Claude Code  
✅ **You CAN centralize MCP server definitions** using modern approaches  
✅ **Best Practice: Single source of truth with scope-based distribution**

---

## 📁 Config File Locations (Dec 2024)

### Claude Desktop
```
macOS:   ~/Library/Application Support/Claude/claude_desktop_config.json
Windows: %APPDATA%\Claude\claude_desktop_config.json
Linux:   ~/.config/Claude/claude_desktop_config.json
```

### Claude Code
```
User scope:    ~/.claude.json
Project scope: <project>/.mcp.json
```

**Key Insight:** Different file locations and potentially different formats mean you can't use symlinks to share one file.

---

## 🎯 Modern Best Practice: Centralized Definition with Scoped Distribution

### Strategy 1: Single Source + Pixi Tasks (Recommended)

Create a **single source of truth** for your MCP servers, then distribute to both Claude Desktop and Claude Code:

```bash
# Your centralized MCP definitions
~/mcp-servers/
├── servers.json              # Source of truth
├── env.example               # Credential template
└── pixi.toml                 # Task runner
```

**mcp-servers.json** (Your single source):
```json
{
  "github": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-github"],
    "env": {
      "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
    }
  },
  "notebooklm-rpc": {
    "command": "notebooklm-mcp",
    "args": []
  },
  "brave-search": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-brave-search"],
    "env": {
      "BRAVE_API_KEY": "${BRAVE_API_KEY}"
    }
  }
}
```

**Pixi Tasks**:
```bash
pixi run mcp-install-desktop
pixi run mcp-install-code
```

**Why This Works:**
- ✅ Single source of truth
- ✅ Easy updates (edit one file, run two tasks)
- ✅ Version control friendly
- ✅ Environment variable support
- ✅ Team sharing via git

---

### Strategy 2: Environment Variable Approach

Use environment variables for all sensitive data, making configs safe to share:

**~/.zshrc** or **~/.bashrc**:
```bash
# MCP Server Credentials
export GITHUB_TOKEN="ghp_xxxxxxxxxxxx"
export BRAVE_API_KEY="BSA_xxxxxxxxxxxx"
export NOTEBOOKLM_SESSION="session_data"
```

**Claude Desktop Config** (`claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

**Claude Code Config** (`~/.claude.json`):
```bash
# Install using CLI with env vars
claude mcp add github \
  --transport stdio \
  --scope user \
  -- npx -y @modelcontextprotocol/server-github \
  --env GITHUB_PERSONAL_ACCESS_TOKEN="${GITHUB_TOKEN}"
```

**Benefits:**
- ✅ Credentials separate from config
- ✅ Configs can be committed to git
- ✅ Easy credential rotation
- ⚠️ Requires shell restart for env var changes

---

### Strategy 3: Project-Specific MCP (Claude Code Only)

Claude Code supports project-specific MCP servers via `.mcp.json` in your project root.

```bash
my-project/
├── .mcp.json              # Project-specific MCP servers
├── .git/
└── src/
```

**.mcp.json**:
```json
{
  "mcpServers": {
    "project-docs": {
      "command": "npx",
      "args": ["-y", "context7-mcp"]
    },
    "project-db": {
      "command": "node",
      "args": ["./scripts/db-mcp-server.js"]
    }
  }
}
```

**When to use:**
- ✅ Team projects (committed to git)
- ✅ Project-specific tools
- ✅ Different MCP needs per project
- ❌ Personal tools (use `--scope user` instead)

---

## 🔧 Modern MCP Installation Methods (Claude Code)

### Method 1: CLI Wizard (Interactive)
```bash
claude mcp add github --scope user
# Interactive prompts walk you through setup
```

### Method 2: Direct JSON (Best for automation)
```bash
claude mcp add-json github '{
  "type": "stdio",
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-github"],
  "env": {"GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxx"}
}' --scope user
```

### Method 3: Direct Config Edit (Most control)
Edit `~/.claude.json` directly for complex setups with lots of parameters

```bash
code ~/.claude.json
```

---

## 📊 Comparison Table

| Approach | Pros | Cons | Best For |
|----------|------|------|----------|
| **Single Source + Scripts** | ✅ One source of truth<br>✅ Easy updates<br>✅ Version control | ⚠️ Need to run scripts<br>⚠️ Two files to maintain | Teams, multiple machines |
| **Environment Variables** | ✅ Secure<br>✅ Git-friendly<br>✅ Easy rotation | ⚠️ Shell restart needed<br>⚠️ Platform differences | Production, security-focused |
| **Project .mcp.json** | ✅ Team sharing<br>✅ Project-specific<br>✅ Automatic | ⚠️ Code only<br>⚠️ Duplicate for Desktop | Development teams |
| **Direct Edit** | ✅ Full control<br>✅ No CLI needed<br>✅ Fast | ⚠️ Manual sync<br>⚠️ Error-prone | Power users, debugging |

---

## 🎓 Real-World Example: Full Setup

Here's how to set up GitHub + NotebookLM + Brave Search for both Claude Desktop and Claude Code:

### Step 1: Set Environment Variables
```bash
# Add to ~/.zshrc or ~/.bashrc
export GITHUB_TOKEN="ghp_your_token_here"
export BRAVE_API_KEY="BSA_your_key_here"
```

### Step 2: Create Source File
```bash
mkdir ~/mcp-config
cat > ~/mcp-config/servers.json << 'EOF'
{
  "github": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-github"],
    "env": {"GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"}
  },
  "notebooklm-rpc": {
    "command": "notebooklm-mcp",
    "args": []
  },
  "brave-search": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-brave-search"],
    "env": {"BRAVE_API_KEY": "${BRAVE_API_KEY}"}
  }
}
EOF
```

### Step 3: Install to Claude Desktop
```bash
pixi run mcp-install-desktop
```

### Step 4: Install to Claude Code
```bash
pixi run mcp-install-code
```

### Step 5: Update Both Environments
```bash
pixi run mcp-update-all
```

---

## 🚨 Common Pitfalls

### ❌ Don't: Use symlinks
```bash
# This WON'T work - different file formats
ln -s ~/.claude.json "~/Library/Application Support/Claude/claude_desktop_config.json"
```

### ❌ Don't: Hardcode credentials
```json
{
  "env": {
    "API_KEY": "sk-1234567890abcdef"  // ❌ Never commit this!
  }
}
```

### ❌ Don't: Forget scope in Claude Code
```bash
claude mcp add github  # ❌ Which scope? Unclear!
claude mcp add github --scope user  # ✅ Clear intent
```

### ✅ Do: Version control your configs (without secrets)
```bash
git add ~/mcp-config/servers.json
git commit -m "Add MCP server definitions"
```

---

## 🔍 Verification

### Check Claude Desktop
```bash
# macOS
cat "$HOME/Library/Application Support/Claude/claude_desktop_config.json"

# Look for MCP indicator in bottom-right of Claude Desktop
```

### Check Claude Code
```bash
claude mcp list

# Expected output:
# MCP Servers:
#   github (user) - connected
#   notebooklm (user) - connected
#   brave-search (user) - connected
```

---

## 📚 Advanced Topics

### Enterprise MCP Management

Organizations can use `managed-mcp.json` for centralized control with allowlists/denylists

**managed-mcp.json** (IT controlled):
```json
{
  "mcpServers": {
    "approved-github": {
      "command": "npx",
      "args": ["-y", "@company/approved-github-mcp"]
    }
  }
}
```

**allowlist.json**:
```json
{
  "allowedServers": [
    "approved-github",
    "company-internal-tools"
  ]
}
```

### Dynamic MCP Loading

```bash
# Load different MCPs based on context
if [ "$PROJECT_TYPE" = "web" ]; then
    claude mcp add brave-search --scope project
elif [ "$PROJECT_TYPE" = "data" ]; then
    claude mcp add postgres --scope project
fi
```

---

## 🎯 Decision Tree: Which Strategy?

```
Are you working alone?
├─ Yes → Direct edit ~/.claude.json + claude_desktop_config.json
└─ No → Are you on a team?
    ├─ Yes → .mcp.json per project + shared env vars
    └─ No → Multiple machines?
        ├─ Yes → Single source + update scripts
        └─ No → Direct CLI installation
```

---

## 📖 References

- Scott Spence - Configuring MCP Tools in Claude Code
- Claude Code Docs - Connect to MCP Tools
- MCP Official Docs - Connect to Local Servers

---

**Last Updated:** December 2024  
**Claude Code Version:** Research Preview  
**Claude Desktop Version:** Latest
