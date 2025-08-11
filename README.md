# DhanHQ Trading Assistant

An AI-powered trading assistant for DhanHQ broker built with Model Context Protocol (MCP). This project enables natural language interaction with the DhanHQ trading platform, allowing you to place orders, check your portfolio, and manage your trading activities through simple conversational commands.

## ✨ New Features & Improvements

### 🚀 Easy Setup & Configuration
- **One-command setup**: `python cli.py setup`
- **Environment-based configuration** with `.env` file support
- **Demo mode** for safe testing without real API calls
- **Automatic configuration validation**

### 🎛️ Unified Server & CLI
- **Single unified server** combining all tools
- **Powerful CLI** for easy management
- **Individual tool servers** for specific needs
- **Health checks and status monitoring**

### 🔒 Enhanced Security
- **Environment variable support**
- **Secure credential management** 
- **No hardcoded secrets**
- **Demo mode for testing**

### 📚 Better Documentation
- **MCP client configuration examples**
- **Comprehensive troubleshooting guide**
- **Step-by-step setup instructions**

## Features

### Order Management
- Regular orders (market/limit) via `order_placement_tool.py`
- Super orders with target and stop-loss via `super-order.py`
- After-market orders via `after_market_order_tool.py`
- Access order book and trade history via `order_book_tool.py`

### Portfolio Management
- View holdings and positions via `holdings_positions_tool.py`
- Convert positions (e.g., intraday to delivery)

### Account Information
- Check fund balance via `fund_balance_tool.py`
- Calculate margin requirements via `margin_calculator_tool.py`

## Setup and Installation

### Prerequisites
- Python 3.9 or higher
- A DhanHQ trading account
- DhanHQ API credentials (client ID and access token)

### Quick Setup

1. **Clone this repository**
   ```bash
   git clone https://github.com/rahulmr/Dhan-MCP-Trades.git
   cd Dhan-MCP-Trades
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup configuration (Easy Way)**
   ```bash
   python cli.py setup
   ```
   This will create a `.env` file from the template.

4. **Configure your credentials**
   
   Edit the `.env` file with your DhanHQ credentials:
   ```bash
   DHAN_CLIENT_ID=your_client_id_here
   DHAN_ACCESS_TOKEN=your_access_token_here
   ```
   
   You can get your credentials from [DhanHQ API Portal](https://api.dhan.co/).

5. **Test your setup**
   ```bash
   python cli.py status
   python cli.py test
   ```

6. **Start the server**
   ```bash
   python cli.py start
   ```

### Alternative Setup Methods

#### Method 1: Unified MCP Server (Recommended)
```bash
# Start the unified server with all tools
python mcp_server.py
```

#### Method 2: Individual Tools
```bash
# Start specific tools using the CLI
python cli.py tool order        # Order placement only
python cli.py tool portfolio    # Portfolio management only
python cli.py tool fund         # Fund balance only
```

#### Method 3: MCP CLI Integration
```bash
# Use with MCP CLI
python -m mcp.server.cli dev mcp_server.py
```

### Demo Mode

For testing without real trading:
```bash
# Set in .env file
DEMO_MODE=true

# Or start with demo mode
DEMO_MODE=true python cli.py start
```

### Configuration Options

All configuration is handled through environment variables or the `.env` file:

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| `DHAN_CLIENT_ID` | Yes | Your DhanHQ Client ID | - |
| `DHAN_ACCESS_TOKEN` | Yes | Your DhanHQ Access Token | - |
| `DHAN_API_BASE_URL` | No | DhanHQ API Base URL | `https://api.dhan.co/v2` |
| `DEMO_MODE` | No | Enable demo mode | `false` |
| `LOG_LEVEL` | No | Logging level | `INFO` |

## Using with MCP Clients

### Claude Desktop

Add this to your Claude Desktop configuration:

```json
{
  "mcpServers": {
    "dhan-trading": {
      "command": "python",
      "args": ["/path/to/Dhan-MCP-Trades/mcp_server.py"]
    }
  }
}
```

For detailed MCP client configuration, see [MCP_CLIENT_CONFIG.md](MCP_CLIENT_CONFIG.md).

## CLI Commands

The repository includes a powerful CLI for easy management:

```bash
python cli.py setup           # Setup configuration
python cli.py status          # Check configuration status
python cli.py start           # Start unified server
python cli.py test            # Test API connection
python cli.py tool <name>     # Start individual tool
python cli.py mcp <args>      # Run with MCP CLI
```

### Running the Tools

#### Unified Server (Recommended)
```bash
python cli.py start
```

#### Individual Tools
```bash
python cli.py tool order       # Order placement
python cli.py tool portfolio   # Portfolio management  
python cli.py tool fund        # Fund balance
python cli.py tool holdings    # Holdings & positions
python cli.py tool margin      # Margin calculator
python cli.py tool orderbook   # Order book & trades
python cli.py tool aftermarket # After-market orders
python cli.py tool super       # Super orders
```

#### MCP CLI Integration
```bash
python cli.py mcp mcp_server.py           # Unified server
python cli.py mcp order_placement_tool.py # Individual tool
```

## Using the Assistant

📈 Expanded Example Trading Commands
🛒 Basic Order Placement
- "Buy 10 shares of Infosys at market price"

- "Sell 5 shares of TCS at limit price of ₹3500"

- "Place a GTT order to buy 20 shares of HDFC Bank at ₹1450"

🎯 Orders with Stop-Loss and Targets
- "Buy Reliance with 2% target and 1% stop-loss"

- "Place a trailing stop-loss buy order for Tata Motors"

- "Short sell Axis Bank with 5% target and 2% stop-loss"

🌙 After-Market & Scheduled Orders
- "Create an after-market order to buy 100 shares of ONGC at ₹180"

- "Schedule a buy order for Tech Mahindra tomorrow at 9:15 AM"

💼 Account Insights
- "What are my current holdings?"

- "Check my available balance and margin"

- "Show me my open positions and unrealized profits"

📊 Portfolio & P&L Analysis
- "Analyze my portfolio performance this month"

- "Give me a P&L report on all banking sector trades"

- "What was my best-performing stock in the last 30 days?"

🤖 Smart, Context-Aware Voice Commands
- "Buy all PSU bank stocks"

- "Short all private sector banks today"

- "Go long on top 5 Nifty IT companies"

- "Buy 2 shares of the company whose promoter's son just had a grand wedding"

- "Tail the stop-loss of all chemical sector stocks"

📌 Contextual & Thematic Trading
- "Buy all companies headquartered in Mumbai"

- "Buy companies where promoter stake is increasing quarter-on-quarter"

- "Short all companies dependent heavily on China for raw materials"

- "Buy the top 5 companies based on market cap in India"

📈 Technical Signal-Based Trading
- "Buy breakout stocks above 200-day moving average"

- "Short stocks that broke below lower Bollinger Band"

- "Buy stocks where RSI crossed above 70"

- "Enter trades in mean reversion stocks with tight stop-loss"

🔍 Advanced Filtering & Signal Scanning
- "Buy companies where profits grew more than 10% quarter-on-quarter"

- "Buy stocks down more than 20% from all-time highs with high volume"

- "Sell all stocks affected by global crude oil prices"

🔁 Pairs & Strategy-Based Trading
- "Buy 3 shares of Reliance and sell 2 shares of Bharti Airtel"

- "Do pair trading between ICICI Bank and Axis Bank"



## Available Tools & Commands

The unified server provides these tools through natural language commands:

### 📈 Order Management
| Tool | Description | Example Commands |
|------|-------------|-----------------|
| `place_stock_order` | Place market/limit orders | "Buy 10 shares of HDFC Bank" |
| `place_after_market_stock_order` | After-market orders | "Place AMO for 100 Infosys at ₹1500" |
| `get_order_history` | View order book | "Show my order history" |
| `get_trade_history` | View trade history | "What trades did I make today?" |
| `cancel_stock_order` | Cancel orders | "Cancel order ID 12345" |

### 💼 Portfolio Management
| Tool | Description | Example Commands |
|------|-------------|-----------------|
| `get_portfolio_holdings` | View holdings | "What are my current holdings?" |
| `get_open_positions` | View positions | "Show my open positions" |
| `convert_stock_position` | Convert positions | "Convert HDFC from intraday to delivery" |

### 💰 Account Information
| Tool | Description | Example Commands |
|------|-------------|-----------------|
| `get_account_balance` | Check fund balance | "What's my account balance?" |
| `calculate_margin` | Calculate margins | "What margin is needed for 50 Reliance shares?" |

### 🔍 Utilities
| Tool | Description | Example Commands |
|------|-------------|-----------------|
| `get_available_stocks` | List all stocks | "Show all available stocks" |
| `search_stock` | Search for stocks | "Search for Adani stocks" |
| `get_server_status` | Server status | "What's the server status?" |

## Tool Descriptions

### order_placement_tool.py
Handles basic order placement (market and limit orders). Supports buying and selling stocks by name.

### super-order.py
Manages super orders with target and stop-loss limits that can be specified in absolute values or percentages.

### after_market_order_tool.py
Places orders outside market hours to be executed on the next trading day.

### fund_balance_tool.py
Retrieves account fund information and calculates margin requirements.

### holdings_positions_tool.py
Retrieves holdings and positions information, allows conversion between product types.

### margin_calculator_tool.py
Calculates margin requirements for potential trades.

### order_book_tool.py
Provides access to order history, trade book, and enables order cancellation.

### portfolio_server.py
Main interface for portfolio management.

## Stock Information

The project uses a `stocks.json` file to map stock names to their security IDs. The file follows this structure:

```json
{
  "companies": [
    {
      "stock_code": "1333",
      "company_name": "HDFC Bank Ltd.",
      "stock_name": "HDFCBANK",
      "description": "Description of the company..."
    }
  ]
}
```

## Project Structure

```
Dhan-MCP-Trades/
├── 📄 README.md                    # Main documentation
├── 🔧 cli.py                       # Command-line interface
├── 🌐 mcp_server.py                # Unified MCP server
├── ⚙️  config.py                   # Configuration management
├── 📋 requirements.txt             # Python dependencies
├── 📦 pyproject.toml               # Modern Python project config
├── 🔒 .env.example                 # Environment template
├── 🚫 .gitignore                   # Git ignore file
├── 🛠️  install.sh                  # Installation script
├── 📚 MCP_CLIENT_CONFIG.md         # MCP client configuration guide
├── 🆘 TROUBLESHOOTING.md           # Troubleshooting guide
├── 📊 stocks.json                  # Stock database
└── Individual tool files:
    ├── order_placement_tool.py     # Order placement
    ├── portfolio_server.py         # Portfolio management
    ├── fund_balance_tool.py        # Fund balance
    ├── holdings_positions_tool.py  # Holdings & positions
    ├── margin_calculator_tool.py   # Margin calculator
    ├── order_book_tool.py          # Order book & trades
    ├── after_market_order_tool.py  # After-market orders
    └── super-order.py              # Super orders
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This software is for educational purposes only. Use at your own risk. The creators are not responsible for any financial losses incurred through the use of this software. Always verify all trading actions before execution.
