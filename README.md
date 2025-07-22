# MCP TradingView Server

An MCP (Model Context Protocol) server that provides access to TradingView technical indicators using the tradingview_scraper library.

## Features

- Fetch all technical indicators for any trading symbol
- Retrieve specific indicators by name
- Support for multiple exchanges and timeframes
- Resource-based access to indicator data

## Installation

### Prerequisites

- Python 3.8 or higher
- uv (recommended for fast Python package and environment management)

### Setup with uv

1. **Install uv** (if not already installed):
   ```bash
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Or with Homebrew
   brew install uv
   
   # Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

2. **Create and setup the project**:
   ```bash
   # Navigate to the project directory
   cd /path/to/mcp-tradingview-server
   
   # Create a virtual environment with Python 3.11
   uv venv --python 3.11
   
   # Activate the environment (optional, uv can work without activation)
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install the package**:
   ```bash
   # Install in development mode with uv
   uv pip install -e .
   
   # Or install dependencies directly
   uv pip install mcp tradingview-scraper
   ```

## MCP Server Configuration

### Claude Desktop Setup

1. **Locate Claude Desktop configuration**:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - Linux: `~/.config/Claude/claude_desktop_config.json`

2. **Edit the configuration file**:
   ```json
   {
     "mcpServers": {
       "tradingview": {
         "command": "/path/to/mcp-tradingview-server/.venv/bin/python",
         "args": ["/path/to/mcp-tradingview-server/src/tradingview_server.py"],
         "cwd": "/path/to/mcp-tradingview-server"
       }
     }
   }
   ```

   **Important**: 
   - Replace `/path/to/mcp-tradingview-server` with the ABSOLUTE path to this project
   - Use absolute paths only (e.g., `/Users/username/projects/mcp-tradingview-server`)
   - Do NOT use `~` or relative paths as Claude Desktop won't expand them

3. **Alternative configuration using uv (requires full path)**:
   ```json
   {
     "mcpServers": {
       "tradingview": {
         "command": "/Users/username/.local/bin/uv",
         "args": ["run", "python", "-m", "tradingview_server"],
         "cwd": "/path/to/mcp-tradingview-server/src"
       }
     }
   }
   ```
   
   **Note**: You must use the full path to uv (find it with `which uv` in terminal)

4. **Restart Claude Desktop** after updating the configuration.

### Verifying the Setup

1. **Test the server locally**:
   ```bash
   cd /path/to/mcp-tradingview-server
   python test_server.py
   ```

2. **Check server is running in Claude**:
   - Open Claude Desktop
   - Look for "tradingview" in the available MCP servers
   - Try using the tools with example prompts below

## Usage

### Example Prompts for Claude Desktop

Once configured, you can use these prompts in Claude Desktop:

**Basic Indicators:**
- "Get Bitcoin indicators using the tradingview server"
- "Show me all technical indicators for AAPL"
- "What are the current indicators for EURUSD?"

**Specific Indicators:**
- "Fetch RSI and MACD for Tesla using the tradingview tool"
- "Get the RSI, Stochastic, and Bollinger Bands for BTCUSD"
- "Show me momentum indicators for ETHUSD"

**With Timeframes:**
- "Get 4-hour indicators for Bitcoin on Binance"
- "Show daily indicators for SPY on NYSE"
- "Fetch 15-minute indicators for GBPUSD"

**Technical Analysis:**
- "Analyze SOLUSDT using tradingview indicators on the 1-hour timeframe"
- "What do the technical indicators say about MSFT?"
- "Get indicators for gold (XAUUSD) and interpret them"

### Available Tools

#### `get_indicators`
Retrieve all technical indicators for a symbol.

Parameters:
- `symbol` (required): Trading symbol (e.g., "BTCUSD", "AAPL")
- `exchange`: Exchange name (default: "BINANCE")
- `timeframe`: Timeframe (default: "1h") - Options: "1m", "5m", "15m", "30m", "1h", "4h", "1d", "1w", "1M"
- `all_indicators`: Fetch all indicators (default: true)
- `export_result`: Export to JSON file (default: false)

#### `get_specific_indicators`
Retrieve specific indicators for a symbol.

Parameters:
- `symbol` (required): Trading symbol
- `indicators` (required): List of indicators to fetch (e.g., ["RSI", "MACD", "BB"])
- `exchange`: Exchange name (default: "BINANCE")
- `timeframe`: Timeframe (default: "1h")
- `export_result`: Export to JSON file (default: false)

### Available Resources

- `indicators/{symbol}`: Get current indicator values as a formatted text resource

## Example Usage

```python
# Get all indicators for Bitcoin
result = await get_indicators("BTCUSD", exchange="BINANCE", timeframe="4h")

# Get specific indicators
result = await get_specific_indicators(
    "AAPL", 
    indicators=["RSI", "MACD"], 
    exchange="NASDAQ"
)
```

## Claude AI Integration

This MCP server includes a `CLAUDE.md` file that provides detailed documentation for Claude AI, including:
- Tool usage examples
- Best practices for indicator analysis
- Common prompt patterns
- Exchange and timeframe recommendations

When using this server with Claude Desktop, Claude will automatically reference this documentation to provide better assistance with technical analysis.

## Supported Exchanges

The server supports all exchanges available in TradingView, including:
- BINANCE
- COINBASE
- KRAKEN
- NASDAQ
- NYSE
- And many more...

## Timeframes

- 1m, 5m, 15m, 30m (minutes)
- 1h, 4h (hours)
- 1d (daily)
- 1w (weekly)
- 1M (monthly)

## Troubleshooting

### Common Issues

1. **"spawn python ENOENT" or "spawn uv ENOENT" error**:
   - This means Claude Desktop can't find the command in its PATH
   - Solution: Use ABSOLUTE paths in your configuration
   - Example: Instead of `"command": "python"`, use `"command": "/Users/yourname/project/.venv/bin/python"`
   - Find the correct path by running `which python` or `pwd` in your project directory

2. **"Module not found" error**:
   - Ensure you're in the correct directory with the `.venv`
   - Verify installation with: `uv pip list | grep tradingview`

3. **MCP server not showing in Claude**:
   - Check the configuration file path is correct
   - Ensure ALL paths in the config are absolute (no `~` or relative paths)
   - Restart Claude Desktop after configuration changes

4. **Permission errors**:
   - Make sure the Python script is executable: `chmod +x src/tradingview_server.py`

### Debug Mode

To run the server in debug mode for troubleshooting:
```bash
cd /path/to/mcp-tradingview-server
uv run python -m tradingview_server

# Or with activated environment
source .venv/bin/activate
python -m tradingview_server
```

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is provided as-is for educational and research purposes.