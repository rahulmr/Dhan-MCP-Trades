#!/usr/bin/env python3
"""
CLI for DhanHQ MCP Trading Assistant.
Provides easy commands for setup, configuration, and server management.
"""
import argparse
import sys
import os
import subprocess
import shutil
from pathlib import Path
from config import validate_config, print_config_status, DEMO_MODE


def setup_config():
    """Setup configuration wizard."""
    print("🔧 DhanHQ MCP Trading Assistant Configuration Setup")
    print("=" * 50)
    
    env_file = Path('.env')
    env_example = Path('.env.example')
    
    if env_file.exists():
        response = input("⚠️  .env file already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Setup cancelled.")
            return
    
    if not env_example.exists():
        print("❌ .env.example file not found. Cannot proceed with setup.")
        return
    
    print("\nCopying .env.example to .env...")
    shutil.copy(env_example, env_file)
    
    print("""
✅ Created .env file from template.

Next steps:
1. Edit the .env file with your actual DhanHQ credentials
2. Set DHAN_CLIENT_ID to your DhanHQ client ID
3. Set DHAN_ACCESS_TOKEN to your DhanHQ access token
4. Optionally configure other settings like logging and demo mode

You can get your DhanHQ credentials from:
https://api.dhan.co/

Run 'python cli.py status' to check your configuration.
""")


def check_status():
    """Check configuration and server status."""
    print_config_status()
    
    if validate_config():
        print("\n✅ Configuration is valid. You can start the server.")
    elif DEMO_MODE:
        print("\n🔧 Demo mode is enabled. You can test without real credentials.")
    else:
        print("\n❌ Configuration is incomplete. Run 'python cli.py setup' to configure.")


def start_server():
    """Start the MCP server."""
    print("🚀 Starting DhanHQ MCP Trading Assistant server...")
    
    if not validate_config() and not DEMO_MODE:
        print("❌ Configuration is incomplete. Run 'python cli.py setup' first.")
        return
    
    try:
        subprocess.run([sys.executable, "mcp_server.py"], check=True)
    except KeyboardInterrupt:
        print("\n⏹️  Server stopped by user.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Server failed to start: {e}")


def start_individual_tool(tool_name):
    """Start an individual tool server."""
    tool_files = {
        'order': 'order_placement_tool.py',
        'portfolio': 'portfolio_server.py',
        'fund': 'fund_balance_tool.py',
        'holdings': 'holdings_positions_tool.py',
        'margin': 'margin_calculator_tool.py',
        'orderbook': 'order_book_tool.py',
        'aftermarket': 'after_market_order_tool.py',
        'super': 'super-order.py'
    }
    
    if tool_name not in tool_files:
        print(f"❌ Unknown tool: {tool_name}")
        print(f"Available tools: {', '.join(tool_files.keys())}")
        return
    
    tool_file = tool_files[tool_name]
    print(f"🚀 Starting {tool_name} tool server ({tool_file})...")
    
    try:
        subprocess.run([sys.executable, tool_file], check=True)
    except KeyboardInterrupt:
        print(f"\n⏹️  {tool_name} tool stopped by user.")
    except subprocess.CalledProcessError as e:
        print(f"❌ {tool_name} tool failed to start: {e}")


def run_mcp_cli(args):
    """Run MCP CLI with the specified tool."""
    if not args:
        print("❌ Please specify a tool to run with MCP CLI")
        return
    
    try:
        cmd = [sys.executable, "-m", "mcp.server.cli", "dev"] + args
        print(f"🚀 Running: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n⏹️  MCP CLI stopped by user.")
    except subprocess.CalledProcessError as e:
        print(f"❌ MCP CLI failed: {e}")


def test_connection():
    """Test connection to DhanHQ API."""
    from config import DHAN_CLIENT_ID, DHAN_ACCESS_TOKEN, DHAN_API_BASE_URL
    import requests
    
    if not validate_config():
        print("❌ Configuration is incomplete. Cannot test connection.")
        return
    
    print("🔌 Testing connection to DhanHQ API...")
    
    try:
        headers = {
            "Content-Type": "application/json",
            "access-token": DHAN_ACCESS_TOKEN
        }
        
        response = requests.get(f"{DHAN_API_BASE_URL}/fundlimit", headers=headers, timeout=10)
        
        if response.status_code == 200:
            print("✅ Connection successful! DhanHQ API is accessible.")
            data = response.json()
            if 'dhanClientId' in data:
                print(f"📊 Connected to account: {data.get('dhanClientId')}")
        else:
            print(f"❌ Connection failed: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.RequestException as e:
        print(f"❌ Connection error: {e}")


def show_help():
    """Show help information."""
    print("""
🔧 DhanHQ MCP Trading Assistant CLI

Commands:
  setup           Setup configuration (.env file)
  status          Check configuration and status
  start           Start the unified MCP server
  test            Test connection to DhanHQ API
  
  tool <name>     Start individual tool server
                  Tools: order, portfolio, fund, holdings, margin, orderbook, aftermarket, super
  
  mcp <args>      Run MCP CLI with specified arguments
                  Example: cli.py mcp order_placement_tool.py

Examples:
  python cli.py setup                    # Initial setup
  python cli.py status                   # Check configuration
  python cli.py start                    # Start unified server
  python cli.py tool order               # Start order tool only
  python cli.py mcp portfolio_server.py  # Run with MCP CLI

Environment Variables:
  Set these in your .env file:
  - DHAN_CLIENT_ID: Your DhanHQ client ID
  - DHAN_ACCESS_TOKEN: Your DhanHQ access token
  - DEMO_MODE: Set to 'true' for testing without real API calls

For more information, visit:
https://github.com/rahulmr/Dhan-MCP-Trades
""")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description='DhanHQ MCP Trading Assistant CLI')
    parser.add_argument('command', nargs='?', help='Command to execute')
    parser.add_argument('args', nargs='*', help='Additional arguments')
    
    if len(sys.argv) == 1:
        show_help()
        return
    
    args = parser.parse_args()
    
    if args.command == 'setup':
        setup_config()
    elif args.command == 'status':
        check_status()
    elif args.command == 'start':
        start_server()
    elif args.command == 'test':
        test_connection()
    elif args.command == 'tool':
        if args.args:
            start_individual_tool(args.args[0])
        else:
            print("❌ Please specify a tool name")
    elif args.command == 'mcp':
        run_mcp_cli(args.args)
    elif args.command == 'help':
        show_help()
    else:
        print(f"❌ Unknown command: {args.command}")
        show_help()


if __name__ == "__main__":
    main()