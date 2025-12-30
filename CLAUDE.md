# Instructions for Claude Code CLI

## 🎯 Mission

You are tasked with creating and initializing a GitHub repository for the **NotebookLM Claude Integration** project. This repository contains a complete integration system that allows Claude to interact with NotebookLM (Google's AI research assistant) through both Claude Desktop (MCP server) and Claude Code (Plugin).

## 📋 What This Repository Contains

### Core Components

1. **MCP Server** (`mcp-config/`)
   - NotebookLM MCP server for Claude Desktop
   - Unified configuration system for managing MCP servers
   - Scripts for deploying configs to both Desktop and Code CLI

2. **Claude Code Plugin** (`plugin/`)
   - Complete plugin implementation for Claude Code CLI
   - Python scripts for authentication, notebook management, and queries
   - Slash commands: `/nlm ask`, `/nlm add`, `/nlm list`, `/nlm select`

3. **Documentation** (`docs/`)
   - Architecture diagrams
   - API documentation
   - Usage guides

4. **Examples** (`examples/`)
   - Sample workflows
   - Use case demonstrations
   - Integration patterns

## 🚀 What You Need to Do

### Step 1: Verify GitHub Token

Check that the GitHub MCP server is configured:

```bash
# List MCP servers
claude mcp list

# You should see 'github' in the list
# If not, the user needs to run the deploy script again
```

### Step 2: Create GitHub Repository

Create a new public repository under the organization: **ray-manaloto**

**Repository Details:**
- **Name:** `notebooklm-claude-integration`
- **Description:** `NotebookLM integration for Claude Desktop (MCP) and Claude Code (Plugin) - unified research assistant with notebook library management`
- **Visibility:** Public
- **Initialize:** Yes (with README)
- **Organization:** ray-manaloto

**Command to execute:**
```bash
# Use the github MCP tool to create the repository
# Target: https://github.com/ray-manaloto/notebooklm-claude-integration
```

### Step 3: Initialize Git Repository Locally

The current directory contains all the files. Initialize git:

```bash
cd ~/Downloads/notebooklm-claude-integration
git init
git add .
git commit -m "Initial commit: NotebookLM Claude Integration

- MCP server for Claude Desktop
- Plugin system for Claude Code CLI
- Unified configuration management
- Complete documentation and examples
- Authentication and session management
- Notebook library system"
```

### Step 4: Push to GitHub

Connect to the remote repository and push:

```bash
# Add remote (replace with actual repo URL from Step 2)
git remote add origin https://github.com/ray-manaloto/notebooklm-claude-integration.git

# Push to main branch
git branch -M main
git push -u origin main
```

### Step 5: Verify Repository

Check that everything is uploaded:

1. Visit: https://github.com/ray-manaloto/notebooklm-claude-integration
2. Verify all directories are present:
   - `/mcp-config/` - MCP server configurations
   - `/plugin/` - Claude Code plugin
   - `/docs/` - Documentation
   - `/examples/` - Usage examples
   - `/tests/` - Test files
3. Verify README.md displays correctly
4. Check that LICENSE is present

### Step 6: Create Initial Release (Optional)

If everything looks good, create a release:

```bash
# Tag the initial release
git tag -a v1.0.0 -m "Initial release: NotebookLM Claude Integration v1.0.0"
git push origin v1.0.0
```

## 📚 Repository Purpose & Context

### What Problem Does This Solve?

This integration bridges Claude (Anthropic's AI) with NotebookLM (Google's AI research assistant), creating a powerful research workflow:

1. **Knowledge Management:** Users can maintain multiple NotebookLM notebooks as specialized knowledge bases
2. **Unified Access:** Access NotebookLM from both Claude Desktop and Claude Code CLI
3. **Session Context:** Maintains conversation history within NotebookLM sessions
4. **Library System:** Organize notebooks by topic, use case, and content type

### Key Features

**For Claude Desktop (MCP):**
- Ask questions to NotebookLM notebooks
- Manage notebook library (add, list, search, select)
- Session management for contextual conversations
- Browser automation for authentication

**For Claude Code (Plugin):**
- Slash commands for quick access
- CLI-friendly workflows
- Same library and session management
- Optimized for development workflows

### Target Users

- Researchers using NotebookLM for knowledge management
- Developers integrating AI research tools
- Teams managing multiple documentation sources
- Anyone wanting to combine Claude's capabilities with NotebookLM's research features

### Technical Architecture

```
User Request
    ↓
Claude (Desktop/Code)
    ↓
MCP Server / Plugin Layer
    ↓
NotebookLM Automation
    ↓
Browser (Playwright)
    ↓
NotebookLM.google.com
    ↓
AI-powered Research Results
```

## 🔧 Configuration Files

The repository includes unified MCP configuration:

- **`mcp-config/servers.json`** - Single source of truth for all MCP servers
- **`mcp-config/install-desktop.sh`** - Deploy to Claude Desktop
- **`mcp-config/install-code.sh`** - Deploy to Claude Code
- **`mcp-config/update-all.sh`** - Update both environments

Users edit one file, deploy everywhere.

## 📖 Important Documentation

Make sure these files are prominent in the repository:

1. **README.md** - Main project overview and quick start
2. **MCP_CONFIG_BEST_PRACTICES.md** - Modern best practices for MCP configuration (Dec 2024)
3. **MCP_CONFIG_SOLUTION.md** - Technical solution details
4. **WHAT_TO_DO.md** - User setup instructions
5. **docs/ARCHITECTURE.md** - System architecture
6. **LICENSE** - MIT License

## ✅ Success Criteria

After completing these tasks, the repository should:

- [x] Be publicly accessible at https://github.com/ray-manaloto/notebooklm-claude-integration
- [x] Have a clear, comprehensive README
- [x] Include all source code and documentation
- [x] Have proper LICENSE file
- [x] Be ready for users to clone and use immediately
- [x] Have initial commit with descriptive message

## 🎯 Final Note

This repository represents a complete, production-ready integration between Claude and NotebookLM. The code has been tested, documented, and packaged for immediate use. Your job is to get it onto GitHub so the user can:

1. Share it with others
2. Version control future improvements  
3. Contribute to the open-source community
4. Preserve their work in a permanent location

## 💡 Tips for Success

- Use the GitHub MCP connector that was just configured
- Verify each step before proceeding
- If authentication fails, inform the user to check their GitHub token
- Provide the final repository URL when complete
- Offer to create additional documentation or setup GitHub Actions if requested

## 🚨 Troubleshooting

**If GitHub MCP is not available:**
- User needs to restart Claude Code CLI
- User should verify `~/.claude.json` has the github server configured
- User may need to run `claude mcp add` manually

**If git push fails:**
- Check if repository was created successfully
- Verify remote URL is correct
- Ensure user has write permissions to ray-manaloto organization

---

**You've got this! Create that repository and make it shine.** 🚀
