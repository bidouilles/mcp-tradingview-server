"""Entry point for running as a module with python -m src"""
from .tradingview_server import mcp

if __name__ == "__main__":
    mcp.run()