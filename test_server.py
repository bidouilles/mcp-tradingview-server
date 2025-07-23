#!/usr/bin/env python3
"""Test script for the MCP TradingView server."""

import asyncio
import sys
sys.path.append('src')

from tradingview_server import get_indicators, get_specific_indicators, get_indicator_resource, get_historical_data


async def test_server():
    print("Testing MCP TradingView Server\n")
    
    # Test 1: Get all indicators
    print("Test 1: Getting all indicators for BTCUSD...")
    result = await get_indicators("BTCUSD", exchange="BINANCE", timeframe="4h")
    if result["success"]:
        print(f"✓ Success! Retrieved {len(result['indicators'])} indicators")
        print(f"Sample indicators: {list(result['indicators'].keys())[:5]}")
    else:
        print(f"✗ Failed: {result['error']}")
    
    print("\n" + "-"*50 + "\n")
    
    # Test 2: Get specific indicators
    print("Test 2: Getting specific indicators (RSI, MACD) for AAPL...")
    result = await get_specific_indicators(
        "AAPL", 
        indicators=["RSI", "MACD"],
        exchange="NASDAQ",
        timeframe="1d"
    )
    if result["success"]:
        print(f"✓ Success! Retrieved {len(result['indicators'])} matching indicators")
        for key, value in result['indicators'].items():
            print(f"  {key}: {value}")
    else:
        print(f"✗ Failed: {result['error']}")
    
    print("\n" + "-"*50 + "\n")
    
    # Test 3: Get resource
    print("Test 3: Getting indicator resource for ETHUSD...")
    resource_text = await get_indicator_resource("ETHUSD")
    print("Resource output (first 500 chars):")
    print(resource_text[:500] + "..." if len(resource_text) > 500 else resource_text)
    
    print("\n" + "-"*50 + "\n")
    
    # Test 4: Get historical data
    print("Test 4: Getting historical OHLC data for BTCUSD (5m timeframe)...")
    result = await get_historical_data(
        symbol="BTCUSD",
        exchange="BINANCE", 
        timeframe="5m",
        max_records=3,
        export_result=False
    )
    if result["success"]:
        print(f"✓ Success! Retrieved {result['records_collected']} {result['timeframe']} candles")
        if result["data"]:
            sample_candle = result["data"][0]
            print(f"Sample candle: timestamp={sample_candle.get('timestamp')}, "
                  f"open={sample_candle.get('open')}, high={sample_candle.get('high')}, "
                  f"low={sample_candle.get('low')}, close={sample_candle.get('close')}")
    else:
        print(f"✗ Failed: {result['error']}")
    
    print("\n" + "-"*50 + "\n")
    
    # Test 5: Get historical data with export
    print("Test 5: Getting historical OHLC data for ETHUSD (1h timeframe) with export...")
    result = await get_historical_data(
        symbol="ETHUSD",
        exchange="BINANCE",
        timeframe="1h", 
        max_records=2,
        export_result=True
    )
    if result["success"]:
        print(f"✓ Success! Retrieved {result['records_collected']} {result['timeframe']} candles")
        if result["export_file"]:
            print(f"✓ Exported to: {result['export_file']}")
    else:
        print(f"✗ Failed: {result['error']}")


if __name__ == "__main__":
    asyncio.run(test_server())