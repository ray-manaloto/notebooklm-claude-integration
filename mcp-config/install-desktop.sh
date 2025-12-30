#!/bin/bash

# ============================================================================
# Install MCP Servers to Claude Desktop
# ============================================================================

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}  Installing MCP Servers to Claude Desktop${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
echo ""

# Determine config file location based on OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    CONFIG_FILE="$HOME/Library/Application Support/Claude/claude_desktop_config.json"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    # Windows
    CONFIG_FILE="$APPDATA/Claude/claude_desktop_config.json"
else
    # Linux
    CONFIG_FILE="$HOME/.config/Claude/claude_desktop_config.json"
fi

echo -e "${BLUE}→${NC} Config file: $CONFIG_FILE"

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
    echo -e "${YELLOW}⚠️  Source file not found: $SOURCE_FILE${NC}"
    exit 1
fi

echo -e "${BLUE}→${NC} Source file: $SOURCE_FILE"
echo ""

# Create backup of existing config
if [ -f "$CONFIG_FILE" ]; then
    BACKUP_FILE="${CONFIG_FILE}.backup.$(date +%Y%m%d_%H%M%S)"
    cp "$CONFIG_FILE" "$BACKUP_FILE"
    echo -e "${GREEN}✓${NC} Created backup: $BACKUP_FILE"
fi

# Create config directory if it doesn't exist
mkdir -p "$(dirname "$CONFIG_FILE")"

# Transform source file to Claude Desktop format
echo -e "${BLUE}→${NC} Installing MCP servers..."
jq '{mcpServers: .}' "$SOURCE_FILE" > "$CONFIG_FILE"

echo ""
echo -e "${GREEN}✓${NC} Successfully installed MCP servers to Claude Desktop!"
echo ""

# Show what was installed
echo -e "${BLUE}Installed servers:${NC}"
jq -r '.mcpServers | keys[]' "$CONFIG_FILE" | while read -r server; do
    desc=$(jq -r ".mcpServers.\"$server\".description // \"No description\"" "$CONFIG_FILE")
    echo -e "  ${GREEN}•${NC} $server - $desc"
done

echo ""
echo -e "${YELLOW}⚠️  IMPORTANT:${NC}"
echo -e "   1. Restart Claude Desktop for changes to take effect"
echo -e "   2. Look for MCP indicator in bottom-right of chat input"
echo -e "   3. Check environment variables are set (see README)"
echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════════════${NC}"
