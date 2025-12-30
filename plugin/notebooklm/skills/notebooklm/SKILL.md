---
name: NotebookLM Integration
description: Query Google NotebookLM notebooks for source-grounded, citation-backed answers from Gemini. Automatically activates when users ask about documentation, research topics, or need answers from their knowledge base.
triggers:
  - User mentions NotebookLM or asks about documentation
  - Questions requiring source-grounded answers
  - Research or investigation requests
  - Need to query uploaded documents or knowledge base
---

# NotebookLM Integration Skill

Query your Google NotebookLM notebooks directly from Claude Code for source-grounded, citation-backed answers from Gemini.

## 🎯 Core Capability

This skill enables Claude to:
- Query your NotebookLM notebooks via browser automation
- Get answers exclusively from your uploaded documents
- Build a local library of notebooks with tags
- Automatically select relevant notebooks based on context
- Conduct deep research with automatic follow-up questions

**Zero hallucinations** - answers only from your documents.

## 📋 Prerequisites

1. **Python 3.10+** with virtual environment support
2. **Google Chrome** installed (not Chromium)
3. **NotebookLM Account** with notebooks created
4. **First-time auth**: Browser will open for Google login

## 🚀 Quick Start

### Step 1: Check Authentication
```python
python scripts/run.py auth_manager.py status
```

### Step 2: Setup (First Time Only)
```python
# Browser will open for manual Google login
python scripts/run.py auth_manager.py setup
```

### Step 3: Add a Notebook
```python
# Smart Add (recommended): Auto-discover content
python scripts/run.py notebook_manager.py add \
  --url "https://notebooklm.google.com/notebook/YOUR_ID" \
  --discover

# Or Manual Add: Specify metadata
python scripts/run.py notebook_manager.py add \
  --url "https://notebooklm.google.com/notebook/YOUR_ID" \
  --name "FastAPI Documentation" \
  --description "FastAPI official docs with OAuth, WebSockets, async" \
  --topics "fastapi,python,api,oauth"
```

### Step 4: Query
```python
python scripts/run.py ask_question.py \
  --question "How do I implement OAuth in FastAPI?"
```

## 📚 Workflow Patterns

### Pattern 1: Smart Discovery
When Claude needs to query NotebookLM:

1. **Check Auth**
   ```python
   python scripts/run.py auth_manager.py status
   ```

2. **If Not Authenticated**
   ```python
   python scripts/run.py auth_manager.py setup
   ```

3. **Discover Notebook Content** (before adding)
   ```python
   python scripts/run.py ask_question.py \
     --question "What is the content of this notebook? What topics are covered?" \
     --notebook-url "https://notebooklm.google.com/notebook/YOUR_ID"
   ```

4. **Add with Discovered Metadata**
   ```python
   python scripts/run.py notebook_manager.py add \
     --url "https://notebooklm.google.com/notebook/YOUR_ID" \
     --name "FastAPI Docs" \
     --description "Comprehensive FastAPI documentation" \
     --topics "fastapi,python,oauth,websockets"
   ```

5. **Query for Answers**
   ```python
   python scripts/run.py ask_question.py \
     --question "How do I implement WebSockets?"
   ```

### Pattern 2: Deep Research
For comprehensive understanding:

```python
# Ask initial question
python scripts/run.py ask_question.py \
  --question "Explain OAuth implementation"

# Automatically ask follow-ups:
# 1. What are security best practices?
# 2. How do I handle token refresh?
# 3. What about scope validation?
# 4. Show me a complete example
# 5. What are common mistakes?

# Synthesize all answers into comprehensive response
```

### Pattern 3: Library Management
```python
# List all notebooks
python scripts/run.py notebook_manager.py list

# Search by topic
python scripts/run.py notebook_manager.py search --query "python async"

# Activate specific notebook
python scripts/run.py notebook_manager.py activate --id notebook-123

# Remove notebook
python scripts/run.py notebook_manager.py remove --id notebook-123
```

## 🎓 Usage Rules

### CRITICAL: Always Use run.py
❌ **NEVER** call scripts directly:
```python
# WRONG
python scripts/auth_manager.py status
python scripts/ask_question.py --question "..."
```

✅ **ALWAYS** use run.py wrapper:
```python
# CORRECT
python scripts/run.py auth_manager.py status
python scripts/run.py ask_question.py --question "..."
```

**Why?** run.py handles:
- Virtual environment activation
- Dependency installation
- Path resolution
- Error handling

### Required Metadata for Adding Notebooks
When adding notebooks, ALL metadata is REQUIRED:
- `--url`: NotebookLM URL
- `--name`: Descriptive name
- `--description`: What the notebook contains
- `--topics`: Comma-separated tags

❌ **NEVER** use generic metadata:
```python
# BAD
--name "Docs"
--description "Documentation"
--topics "docs,stuff"
```

✅ **ALWAYS** be specific:
```python
# GOOD
--name "FastAPI Official Documentation"
--description "FastAPI 0.104 docs covering OAuth2, WebSockets, async patterns"
--topics "fastapi,python,oauth,websockets,async"
```

### Discovery Before Adding
**ALWAYS** discover content before adding:

```python
# Step 1: Ask what's in the notebook
python scripts/run.py ask_question.py \
  --question "What topics does this notebook cover? Provide a complete overview" \
  --notebook-url "https://notebooklm.google.com/notebook/abc123"

# Step 2: Use that information to add it properly
python scripts/run.py notebook_manager.py add \
  --url "https://notebooklm.google.com/notebook/abc123" \
  --name "[Based on discovery]" \
  --description "[Based on discovery]" \
  --topics "[Based on discovery]"
```

## 🔧 Available Commands

### Authentication (auth_manager.py)
```python
# Check status
python scripts/run.py auth_manager.py status

# Setup (opens browser for login)
python scripts/run.py auth_manager.py setup

# Reset session
python scripts/run.py auth_manager.py reset
```

### Library Management (notebook_manager.py)
```python
# List all notebooks
python scripts/run.py notebook_manager.py list

# Add notebook (all params required!)
python scripts/run.py notebook_manager.py add \
  --url "URL" \
  --name "Name" \
  --description "Description" \
  --topics "topic1,topic2"

# Search notebooks
python scripts/run.py notebook_manager.py search --query "keyword"

# Activate notebook
python scripts/run.py notebook_manager.py activate --id ID

# Remove notebook
python scripts/run.py notebook_manager.py remove --id ID
```

### Querying (ask_question.py)
```python
# Query active notebook
python scripts/run.py ask_question.py --question "Your question"

# Query specific notebook
python scripts/run.py ask_question.py \
  --question "Your question" \
  --notebook-url "https://notebooklm.google.com/notebook/abc123"
```

## 📁 Data Storage

All data stored in `skills/notebooklm/data/`:
```
data/
├── library.json         # Your notebook library
├── auth_info.json      # Auth status
└── browser_state/      # Chrome session data
```

**Security**: All data is local. Credentials never leave your machine.

## ⚙️ Configuration

Edit `.env` file if needed:
```bash
HEADLESS=false              # Show browser (false for debugging)
SHOW_BROWSER=false          # Default display
STEALTH_ENABLED=true        # Human-like behavior
TYPING_WPM_MIN=160         # Typing speed
TYPING_WPM_MAX=240
DEFAULT_NOTEBOOK_ID=        # Optional default
```

## 🐛 Troubleshooting

### Chrome Crashes
```python
# Clear browser data
rm -rf skills/notebooklm/data/browser_state
python scripts/run.py auth_manager.py setup
```

### Authentication Failed
```python
# Reset and re-authenticate
python scripts/run.py auth_manager.py reset
python scripts/run.py auth_manager.py setup
```

### Dependencies Issues
```bash
# Clean virtual environment
rm -rf skills/notebooklm/.venv
# Run any command - venv will be recreated
python scripts/run.py auth_manager.py status
```

## 🎯 Activation Triggers

Claude automatically uses this skill when:
- User mentions "NotebookLM" explicitly
- Questions about documentation or research
- User asks to query their knowledge base
- Need for source-grounded answers
- Research or investigation requests

## 🔗 Integration with Agents

This skill works with specialized agents:
- **Research Agent**: Automatic follow-up questions
- **Library Manager**: Smart notebook organization
- **Query Optimizer**: Best question formulation

## ⚠️ Important Notes

### Browser Automation Disclaimer
- Uses humanization (realistic typing, delays, mouse movements)
- Google **may** detect automation
- Recommend dedicated Google account
- Similar to web scraping: use responsibly

### Stateless Operation
- Each query opens fresh browser session
- No persistent chat context between questions
- For multi-turn conversations, ask comprehensive questions

### Performance
- First query: ~10-15 seconds (browser startup)
- Subsequent queries: ~5-8 seconds
- Authentication: One-time, persists 30+ days

## 📚 Resources

- **MCP Server**: https://github.com/PleasePrompto/notebooklm-mcp
- **Original Skill**: https://github.com/PleasePrompto/notebooklm-skill
- **NotebookLM**: https://notebooklm.google.com
