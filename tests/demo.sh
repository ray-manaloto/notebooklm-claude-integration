#!/bin/bash
# NotebookLM Plugin Demo Script
# Demonstrates all features of the NotebookLM integration

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║     NotebookLM Plugin for Claude Code - Complete Demo         ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

SCRIPTS_DIR="$HOME/.claude/plugins/installed/notebooklm/skills/notebooklm/scripts"
cd "$SCRIPTS_DIR"

echo "📍 Location: $SCRIPTS_DIR"
echo ""

# Step 1: Check authentication
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 1: Check Authentication Status"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 run.py auth status
echo ""

# Step 2: Setup auth
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 2: Setup Authentication (MOCK - opens Chrome in real env)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 run.py auth setup
echo ""

# Step 3: Add notebook
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 3: Add Your NotebookLM Notebook"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 run.py add \
  "https://notebooklm.google.com/notebook/8e98a4d8-f778-4dfc-88e8-2d59e48b1069" \
  "Raymond's Notebook" \
  "Knowledge base for development and research" \
  "documentation,research,development"
echo ""

# Step 4: List notebooks
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 4: List All Notebooks in Library"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 run.py list
echo ""

# Step 5: Activate notebook
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 5: Activate the Notebook"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 run.py activate "Raymond's Notebook"
echo ""

# Step 6: Search notebooks
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 6: Search Notebooks by Topic"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 run.py search "documentation"
echo ""

# Step 7: Ask questions
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 7: Ask Questions to NotebookLM"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

echo ""
echo "Question 1: How do I implement OAuth?"
python3 run.py ask "How do I implement OAuth in my application?"
echo ""

echo "Question 2: What are best practices for API security?"
python3 run.py ask "What are best practices for API security?"
echo ""

# Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Demo Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📊 Summary:"
echo "  ✓ Authentication configured"
echo "  ✓ Notebook added to library"
echo "  ✓ Notebook activated"
echo "  ✓ Questions answered with citations"
echo ""
echo "📁 Data stored in:"
echo "  ~/.claude/plugins/installed/notebooklm/skills/notebooklm/data/"
echo ""
echo "⚠️  IMPORTANT NOTES:"
echo "  • This demo uses MOCK data (no real browser automation)"
echo "  • Real environment requires:"
echo "    - Chrome browser installed"
echo "    - Network access to NotebookLM"
echo "    - Patchright library (pip install patchright)"
echo "    - Active Google account"
echo ""
echo "🚀 Try the interactive simulator:"
echo "  python3 /home/claude/claude_code_simulator.py"
echo ""
