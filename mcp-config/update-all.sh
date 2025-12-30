#!/bin/bash

# ============================================================================
# Update ALL MCP Servers (Both Claude Desktop and Claude Code)
# ============================================================================

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Update MCP Servers from Single Source${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo -e "${BLUE}→${NC} Source: $SCRIPT_DIR/servers.json"
echo ""

# Update Claude Desktop
echo -e "${GREEN}1/2${NC} Updating Claude Desktop..."
echo -e "${BLUE}─────────────────────────────────────────────────────────${NC}"
"$SCRIPT_DIR/install-desktop.sh"
echo ""

# Update Claude Code
echo -e "${GREEN}2/2${NC} Updating Claude Code..."
echo -e "${BLUE}─────────────────────────────────────────────────────────${NC}"
"$SCRIPT_DIR/install-code.sh"
echo ""

echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✓${NC} All MCP servers updated!"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo -e "  1. ${BLUE}Restart Claude Desktop${NC} for changes to take effect"
echo -e "  2. ${BLUE}Run 'claude mcp list'${NC} to verify Claude Code installation"
echo -e "  3. ${BLUE}Test servers${NC} in both environments"
echo ""
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
