# Claude MCP TradingView Server Documentation

This document provides guidance for Claude AI when working with the MCP TradingView Server.

## Overview

This MCP server provides access to TradingView technical indicators through two main tools:
- `get_indicators`: Fetches all technical indicators for a trading symbol
- `get_specific_indicators`: Retrieves specific named indicators

## Available Tools

### 1. get_indicators
Retrieves all available technical indicators for a given symbol.

**Parameters:**
- `symbol` (required): Trading symbol (e.g., "BTCUSD", "AAPL", "EURUSD")
- `exchange` (optional): Exchange name (default: "BINANCE")
- `timeframe` (optional): Chart timeframe (default: "1h")
- `all_indicators` (optional): Whether to fetch all indicators (default: true)
- `export_result` (optional): Export to JSON file (default: false)

**Example usage:**
```python
await get_indicators("BTCUSD", exchange="BINANCE", timeframe="4h")
```

### 2. get_specific_indicators
Retrieves specific technical indicators by name.

**Parameters:**
- `symbol` (required): Trading symbol
- `indicators` (required): List of indicator names to fetch (e.g., ["RSI", "MACD", "BB"])
- `exchange` (optional): Exchange name (default: "BINANCE")
- `timeframe` (optional): Chart timeframe (default: "1h")
- `export_result` (optional): Export to JSON file (default: false)

**Example usage:**
```python
await get_specific_indicators("AAPL", indicators=["RSI", "MACD"], exchange="NASDAQ")
```

## Available Resources

### indicators/{symbol}
Returns formatted text output of current indicator values for a symbol.

**Example:** `indicators/BTCUSD`

## Supported Exchanges

Common exchanges include:
- Crypto: BINANCE, COINBASE, KRAKEN, BYBIT, KUCOIN, OKX
- Stock: NASDAQ, NYSE, AMEX
- Forex: FX, OANDA
- And many more available on TradingView

## Supported Timeframes

- Minutes: 1m, 5m, 15m, 30m
- Hours: 1h, 4h
- Days: 1d
- Weeks: 1w
- Months: 1M

## Common Indicators Returned

The server returns various technical indicators including:
- Trend: EMA, SMA, MACD, ADX
- Momentum: RSI, Stochastic, CCI, Williams %R
- Volatility: Bollinger Bands, ATR
- Volume: OBV, Volume
- And many more

## Usage Guidelines

1. **Symbol Format**: Use standard TradingView symbol notation
   - Crypto: "BTCUSD", "ETHUSD", "SOLUSDT"
   - Stocks: "AAPL", "TSLA", "MSFT"
   - Forex: "EURUSD", "GBPUSD"

2. **Exchange Selection**: Choose the appropriate exchange for accurate data
   - For crypto, BINANCE is usually a good default
   - For US stocks, use NASDAQ or NYSE
   - For forex, use FX or OANDA

3. **Timeframe Selection**: Match timeframe to analysis needs
   - Scalping: 1m, 5m
   - Day trading: 15m, 30m, 1h
   - Swing trading: 4h, 1d
   - Long-term: 1w, 1M

4. **Error Handling**: The tools return success/error status
   - Check the "success" field in responses
   - Error messages are provided in the "error" field

## Example Prompts

When users ask about technical indicators, you can use these patterns:

1. "What are the indicators for Bitcoin?"
   → Use `get_indicators("BTCUSD")`

2. "Show me the RSI and MACD for Apple stock"
   → Use `get_specific_indicators("AAPL", indicators=["RSI", "MACD"], exchange="NASDAQ")`

3. "Get 4-hour chart indicators for Ethereum"
   → Use `get_indicators("ETHUSD", timeframe="4h")`

## Best Practices

1. Always specify the exchange when known for more accurate data
2. Use appropriate timeframes based on the user's trading style
3. When users ask for "analysis", provide both the raw indicators and interpretation
4. For crypto pairs, default to BINANCE unless specified otherwise
5. For specific indicators, use get_specific_indicators to reduce data overhead

## Limitations

- The server fetches real-time data from TradingView
- Some exotic symbols or exchanges might not be available
- Data accuracy depends on TradingView's data feed
- Rate limiting may apply for excessive requests

## Testing

To verify the server is working:
```
get_indicators("BTCUSD", exchange="BINANCE", timeframe="1h")
```

This should return a comprehensive set of technical indicators for Bitcoin.