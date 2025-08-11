#!/bin/bash
# Install script for DhanHQ MCP Trading Assistant

echo "🔧 DhanHQ MCP Trading Assistant - Installation Script"
echo "======================================================="

# Check Python version
python_version=$(python3 --version 2>/dev/null | grep -Po "(?<=Python )[0-9].[0-9]")
if [[ -z "$python_version" ]]; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

echo "✅ Python $python_version detected"

# Check if we're in the right directory
if [[ ! -f "requirements.txt" ]]; then
    echo "❌ Please run this script from the Dhan-MCP-Trades directory"
    exit 1
fi

# Install dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt --user

if [[ $? -ne 0 ]]; then
    echo "❌ Failed to install dependencies. Please check your Python setup."
    exit 1
fi

echo "✅ Dependencies installed successfully"

# Setup configuration
echo "🔧 Setting up configuration..."
python3 cli.py setup

echo ""
echo "🎉 Installation completed!"
echo ""
echo "Next steps:"
echo "1. Edit the .env file with your DhanHQ credentials"
echo "2. Run 'python3 cli.py status' to check configuration"
echo "3. Run 'python3 cli.py start' to start the server"
echo ""
echo "For help: python3 cli.py help"
echo "Demo mode: Set DEMO_MODE=true in .env for testing"
echo ""
echo "Get your DhanHQ credentials from: https://api.dhan.co/"