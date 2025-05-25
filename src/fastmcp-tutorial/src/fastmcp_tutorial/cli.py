#!/usr/bin/env python3
"""Command-line interface for FastMCP Tutorial Server."""

import argparse
import sys
from .server import mcp


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="FastMCP Tutorial Server - A comprehensive MCP server example"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0"
    )
    parser.add_argument(
        "--host",
        default="localhost",
        help="Host to bind to (default: localhost)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=3000,
        help="Port to bind to (default: 3000)"
    )
    
    args = parser.parse_args()
    
    print("Starting FastMCP Tutorial Server...")
    print(f"Tools: 3 | Resources: 4 | Prompts: 4")
    print("Press Ctrl+C to stop the server")
    
    try:
        mcp.run()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        sys.exit(0)


if __name__ == "__main__":
    main()