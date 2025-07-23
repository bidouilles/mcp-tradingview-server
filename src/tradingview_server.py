#!/usr/bin/env python3
"""MCP server for TradingView indicators using tradingview_scraper."""

import asyncio
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add the src directory to Python path if not already there
src_dir = Path(__file__).parent
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from mcp import Resource, Tool
from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent

from tradingview_scraper.symbols.technicals import Indicators
from tradingview_scraper.symbols.stream import Streamer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("TradingView Indicators Server")


@mcp.tool()
async def get_indicators(
    symbol: str,
    exchange: str = "BINANCE",
    timeframe: str = "1h",
    all_indicators: bool = True,
    export_result: bool = False
) -> Dict[str, Any]:
    """
    Retrieve technical indicators for a given symbol from TradingView.
    
    Args:
        symbol: Trading symbol (e.g., "BTCUSD", "AAPL")
        exchange: Exchange name (default: "BINANCE")
        timeframe: Timeframe for indicators (e.g., "1m", "5m", "15m", "30m", "1h", "4h", "1d", "1w", "1M")
        all_indicators: Whether to fetch all indicators (default: True)
        export_result: Whether to export results to file (default: False)
    
    Returns:
        Dictionary containing the technical indicators data
    """
    try:
        logger.info(f"Fetching indicators for {symbol} on {exchange} ({timeframe})")
        
        # Create indicators scraper instance
        indicators_scraper = Indicators(
            export_result=export_result,
            export_type='json' if export_result else None
        )
        
        # Scrape indicators
        indicators = indicators_scraper.scrape(
            symbol=symbol,
            exchange=exchange,
            timeframe=timeframe,
            allIndicators=all_indicators
        )
        
        logger.info(f"Successfully fetched indicators for {symbol}")
        return {
            "success": True,
            "symbol": symbol,
            "exchange": exchange,
            "timeframe": timeframe,
            "indicators": indicators
        }
        
    except Exception as e:
        logger.error(f"Error fetching indicators for {symbol}: {str(e)}")
        return {
            "success": False,
            "symbol": symbol,
            "exchange": exchange,
            "timeframe": timeframe,
            "error": str(e)
        }


@mcp.tool()
async def get_specific_indicators(
    symbol: str,
    indicators: List[str],
    exchange: str = "BINANCE",
    timeframe: str = "1h",
    export_result: bool = False
) -> Dict[str, Any]:
    """
    Retrieve specific technical indicators for a given symbol.
    
    Args:
        symbol: Trading symbol (e.g., "BTCUSD", "AAPL")
        indicators: List of specific indicators to fetch. Available indicators include:
                   - Moving Averages: "EMA10", "EMA20", "EMA50", "EMA100", "EMA200", 
                     "SMA10", "SMA20", "SMA50", "SMA100", "SMA200", "HullMA9", "VWMA"
                   - Momentum: "RSI", "Stoch.K", "Stoch.D", "Stoch.RSI.K", "CCI20", 
                     "Mom", "UO", "W.R"
                   - Trend: "ADX", "ADX+DI", "ADX-DI", "MACD.macd", "MACD.signal", "AO"
                   - Other: "BBPower", "Ichimoku.BLine", "close"
                   - Pivot Points: "Pivot.M.Classic.*", "Pivot.M.Fibonacci.*", etc.
                   - Recommendations: "Recommend.All", "Recommend.MA", "Recommend.Other"
                   Example: ["RSI", "MACD.macd", "EMA20"]
        exchange: Exchange name (default: "BINANCE")
        timeframe: Timeframe for indicators (e.g., "1h", "4h", "1d")
        export_result: Whether to export results to file (default: False)
    
    Returns:
        Dictionary containing the requested technical indicators
    """
    try:
        logger.info(f"Fetching specific indicators {indicators} for {symbol}")
        
        # Create indicators scraper instance
        indicators_scraper = Indicators(
            export_result=export_result,
            export_type='json' if export_result else None
        )
        
        # Scrape all indicators first (API limitation)
        all_indicators = indicators_scraper.scrape(
            symbol=symbol,
            exchange=exchange,
            timeframe=timeframe,
            allIndicators=True
        )
        
        # Filter requested indicators
        filtered_indicators = {}
        for key, value in all_indicators.items():
            for requested in indicators:
                if requested.lower() in key.lower():
                    filtered_indicators[key] = value
        
        logger.info(f"Successfully fetched {len(filtered_indicators)} indicators for {symbol}")
        return {
            "success": True,
            "symbol": symbol,
            "exchange": exchange,
            "timeframe": timeframe,
            "requested_indicators": indicators,
            "indicators": filtered_indicators
        }
        
    except Exception as e:
        logger.error(f"Error fetching indicators for {symbol}: {str(e)}")
        return {
            "success": False,
            "symbol": symbol,
            "exchange": exchange,
            "timeframe": timeframe,
            "error": str(e)
        }


@mcp.tool()
async def get_historical_data(
    symbol: str,
    exchange: str = "BINANCE",
    timeframe: str = "1h",
    max_records: int = 100,
    export_result: bool = False
) -> Dict[str, Any]:
    """
    Retrieve real-time OHLCV (Open, High, Low, Close, Volume) data for a given symbol.
    
    Args:
        symbol: Trading symbol (e.g., "BTCUSD", "AAPL")
        exchange: Exchange name (default: "BINANCE")
        timeframe: Timeframe for candles (default: "1h") - Options: "1m", "5m", "15m", "30m", "1h", "4h", "1d", "1w", "1M"
        max_records: Maximum number of OHLC records to collect (default: 100)
        export_result: Whether to export results to JSON file (default: False)
    
    Returns:
        Dictionary containing OHLCV data stream
    """
    try:
        logger.info(f"Starting OHLCV data collection for {symbol} on {exchange} ({timeframe})")
        
        # Always use export=True to get processed data, then optionally delete the file
        streamer = Streamer(export_result=True, export_type='json')
        
        # Stream data using the native timeframe support
        result = streamer.stream(
            exchange=exchange,
            symbol=symbol,
            timeframe=timeframe,
            numb_price_candles=max_records
        )
        
        # Extract OHLC data from the result
        ohlcv_data = result.get('ohlc', [])
        
        # Handle export file
        export_filename = None
        if export_result:
            # Keep the exported file
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            export_filename = f"export/ohlc_{symbol.lower()}_{timestamp}.json"
            logger.info(f"Data exported to {export_filename}")
        else:
            # The Streamer automatically created a file, but user doesn't want it
            # We'll let it remain as the library handles cleanup
            pass
        
        logger.info(f"Successfully collected {len(ohlcv_data)} {timeframe} candles for {symbol}")
        
        return {
            "success": True,
            "symbol": symbol,
            "exchange": exchange,
            "timeframe": timeframe,
            "records_collected": len(ohlcv_data),
            "data": ohlcv_data,
            "export_file": export_filename
        }
        
    except Exception as e:
        logger.error(f"Error collecting OHLCV data for {symbol}: {str(e)}")
        return {
            "success": False,
            "symbol": symbol,
            "exchange": exchange,
            "error": str(e)
        }


@mcp.resource("indicators/{symbol}")
async def get_indicator_resource(symbol: str) -> str:
    """
    Get current indicator values for a symbol as a resource.
    
    Args:
        symbol: Trading symbol (e.g., "BTCUSD")
    
    Returns:
        String representation of current indicators
    """
    result = await get_indicators(symbol)
    
    if result["success"]:
        indicators = result["indicators"]
        output = f"Technical Indicators for {symbol}\n"
        output += f"Exchange: {result['exchange']}\n"
        output += f"Timeframe: {result['timeframe']}\n"
        output += "-" * 50 + "\n"
        
        for key, value in indicators.items():
            output += f"{key}: {value}\n"
        
        return output
    else:
        return f"Error fetching indicators for {symbol}: {result['error']}"


# Run the server
if __name__ == "__main__":
    mcp.run()