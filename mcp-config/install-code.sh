#!/bin/bash

# ============================================================================
# Install MCP Servers to Claude Code
# ============================================================================

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Installing MCP Servers to Claude Code${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""

# Check if Claude Code CLI is installed
if ! command -v claude &> /dev/null; then
    echo -e "${RED}✗${NC} Claude Code CLI not found!"
    echo ""
    echo -e "   Install with: ${BLUE}npm install -g @anthropic/claude-code${NC}"
    exit 1
fi

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo -e "${YELLOW}⚠️  jq is not installed. Install it with:${NC}"
    echo -e "   ${BLUE}macOS:${NC}   brew install jq"
    echo -e "   ${BLUE}Ubuntu:${NC}  sudo apt-get install jq"
    echo -e "   ${BLUE}Windows:${NC} choco install jq"
    exit 1
fi

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SOURCE_FILE="$SCRIPT_DIR/servers.json"

# Check if source file exists
if [ ! -f "$SOURCE_FILE" ]; then
    echo -e "${RED}✗${NC} Source file not found: $SOURCE_FILE"
    exit 1
fi

echo -e "${BLUE}→${NC} Source file: $SOURCE_FILE"
echo -e "${BLUE}→${NC} Installing to: User scope (available in all projects)"
echo ""

# Get list of servers
SERVERS=$(jq -r 'keys[]' "$SOURCE_FILE")

# Install each server
for server in $SERVERS; do
    echo -e "${BLUE}→${NC} Installing ${GREEN}$server${NC}..."
    
    # Get server configuration
    SERVER_CONFIG=$(jq -c ".\"$server\"" "$SOURCE_FILE")
    
    # Remove from description field if it exists (not part of MCP spec)
    SERVER_CONFIG=$(echo "$SERVER_CONFIG" | jq 'del(.description)')
    
    # Remove existing server if it exists
    claude mcp remove "$server" 2>/dev/null || true
    
    # Add the server
    if claude mcp add-json "$server" "$SERVER_CONFIG" --scope user 2>&1; then
        desc=$(jq -r ".\"$server\".description // \"No description\"" "$SOURCE_FILE")
        echo -e "  ${GREEN}✓${NC} $server - $desc"
    else
        echo -e "  ${RED}✗${NC} Failed to install $server"
    fi
    
    echo ""
done

echo -e "${GREEN}✓${NC} Installation complete!"
echo ""

# Verify installation
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Verification${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "Run ${GREEN}claude mcp list${NC} to verify installation"
echo -e "Run ${GREEN}claude${NC} to start Claude Code and check /mcp for status"
echo ""
echo -e "${YELLOW}⚠️  IMPORTANT:${NC}"
echo -e "   1. Make sure environment variables are set (see README)"
echo -e "   2. Run ${GREEN}claude mcp list${NC} to verify servers are registered"
echo -e "   3. Inside Claude Code, use ${GREEN}/mcp${NC} to check connection status"
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
