#!/usr/bin/env python3
"""Test script for the MCP TradingView server."""

import asyncio
import sys
sys.path.append('src')

from tradingview_server import get_indicators, get_specific_indicators, get_indicator_resource


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


if __name__ == "__main__":
    asyncio.run(test_server())