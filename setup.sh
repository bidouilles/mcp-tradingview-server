#!/bin/bash
# Quick setup script for MCP TradingView Server

echo "Setting up MCP TradingView Server with uv..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "uv is not installed. Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    echo "Please restart your terminal or run 'source ~/.bashrc' (or ~/.zshrc) and run this script again."
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
uv venv --python 3.11

# Install dependencies
echo "Installing dependencies..."
if ! uv pip install -e .; then
    echo "❌ Installation failed. Please check the error message above."
    exit 1
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To configure with Claude Desktop, add this to your claude_desktop_config.json:"
echo ""
echo "📍 Config file location:"
echo "   macOS: ~/Library/Application Support/Claude/claude_desktop_config.json"
echo "   Windows: %APPDATA%\\Claude\\claude_desktop_config.json"
echo "   Linux: ~/.config/Claude/claude_desktop_config.json"
echo ""
echo "{"
echo "  \"mcpServers\": {"
echo "    \"tradingview\": {"
echo "      \"command\": \"$(pwd)/.venv/bin/python\","
echo "      \"args\": [\"$(pwd)/src/tradingview_server.py\"],"
echo "      \"cwd\": \"$(pwd)\""
echo "    }"
echo "  }"
echo "}"
echo ""
echo "Alternative configuration with uv (if uv is in PATH):"
echo "{"
echo "  \"mcpServers\": {"
echo "    \"tradingview\": {"
echo "      \"command\": \"$(which uv)\","
echo "      \"args\": [\"run\", \"python\", \"-m\", \"tradingview_server\"],"
echo "      \"cwd\": \"$(pwd)/src\""
echo "    }"
echo "  }"
echo "}"
echo ""
echo "⚠️  Remember to restart Claude Desktop after updating the configuration!"