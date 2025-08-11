# MCP Client Configuration Guide

This document provides detailed instructions for configuring MCP clients to work with the DhanHQ Trading Assistant.

## Quick Start

1. **Setup Configuration**:
   ```bash
   python cli.py setup
   # Edit the created .env file with your DhanHQ credentials
   ```

2. **Start the Server**:
   ```bash
   python cli.py start
   ```

3. **Configure your MCP client** (see examples below)

## Claude Desktop Configuration

Add this to your Claude Desktop configuration file:

### macOS Location
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

### Windows Location
```
%APPDATA%\Claude\claude_desktop_config.json
```

### Configuration JSON
```json
{
  "mcpServers": {
    "dhan-trading": {
      "command": "python",
      "args": ["/path/to/your/Dhan-MCP-Trades/mcp_server.py"],
      "env": {
        "DHAN_CLIENT_ID": "your_client_id",
        "DHAN_ACCESS_TOKEN": "your_access_token",
        "DEMO_MODE": "false"
      }
    }
  }
}
```

**Alternative using CLI tool**:
```json
{
  "mcpServers": {
    "dhan-trading": {
      "command": "python",
      "args": ["/path/to/your/Dhan-MCP-Trades/cli.py", "start"]
    }
  }
}
```

## MCP CLI Configuration

### Using the Unified Server
```bash
# Start the unified server with all tools
python -m mcp.server.cli dev mcp_server.py
```

### Using Individual Tools
```bash
# Order placement tool only
python -m mcp.server.cli dev order_placement_tool.py

# Portfolio management
python -m mcp.server.cli dev portfolio_server.py

# Fund balance
python -m mcp.server.cli dev fund_balance_tool.py
```

## Environment Variables

Set these in your `.env` file or environment:

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| `DHAN_CLIENT_ID` | Yes | Your DhanHQ Client ID | - |
| `DHAN_ACCESS_TOKEN` | Yes | Your DhanHQ Access Token | - |
| `DHAN_API_BASE_URL` | No | DhanHQ API Base URL | `https://api.dhan.co/v2` |
| `DEMO_MODE` | No | Enable demo mode (no real trades) | `false` |
| `MCP_SERVER_PORT` | No | Server port | `8000` |
| `MCP_SERVER_HOST` | No | Server host | `localhost` |
| `LOG_LEVEL` | No | Logging level | `INFO` |
| `LOG_FILE` | No | Log file name | `dhan_mcp.log` |

## Demo Mode

For testing without real trading:

```bash
# Set in .env file
DEMO_MODE=true

# Or start with demo mode
DEMO_MODE=true python cli.py start
```

In demo mode:
- No real API calls are made
- All operations return simulated responses
- Safe for testing and development

## Docker Configuration

### Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "mcp_server.py"]
```

### docker-compose.yml
```yaml
version: '3.8'
services:
  dhan-mcp:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DHAN_CLIENT_ID=${DHAN_CLIENT_ID}
      - DHAN_ACCESS_TOKEN=${DHAN_ACCESS_TOKEN}
      - DEMO_MODE=false
    volumes:
      - ./logs:/app/logs
```

## Available Tools

The unified server provides these tools:

### Order Management
- `place_stock_order` - Place market/limit orders
- `place_after_market_stock_order` - Place after-market orders
- `get_order_history` - Get order book
- `get_trade_history` - Get trade history
- `cancel_stock_order` - Cancel orders

### Portfolio Management
- `get_portfolio_holdings` - Get holdings
- `get_open_positions` - Get positions
- `convert_stock_position` - Convert positions

### Account Information
- `get_account_balance` - Get fund balance
- `calculate_margin` - Calculate margin requirements

### Utilities
- `get_available_stocks` - List all stocks
- `search_stock` - Search for stocks
- `get_server_status` - Server status and info

## Example Commands

Once configured with an MCP client (like Claude), you can use natural language:

### Basic Trading
- "Buy 10 shares of HDFC Bank at market price"
- "Sell 5 shares of TCS at ₹3500"
- "Check my portfolio holdings"
- "What's my account balance?"

### Advanced Operations
- "Place an after-market order for 100 shares of Infosys at ₹1500"
- "Convert my HDFC position from intraday to delivery"
- "Calculate margin required for buying 50 shares of Reliance"
- "Cancel order ID 12345"

### Information Queries
- "Search for Adani stocks"
- "Show me all available banking stocks"
- "What's the server status?"

## Troubleshooting

### Configuration Issues
```bash
# Check configuration status
python cli.py status

# Test API connection
python cli.py test
```

### Common Problems

1. **"Configuration incomplete" error**:
   - Run `python cli.py setup`
   - Edit `.env` file with your credentials

2. **"Connection failed" error**:
   - Check your DhanHQ credentials
   - Verify API access token is valid
   - Ensure internet connectivity

3. **"Stock not found" error**:
   - Use `search_stock` tool to find correct stock names
   - Check if stock is in `stocks.json`

4. **Permission errors**:
   - Ensure proper file permissions
   - Check if ports are available

### Logs

Check logs for detailed error information:
```bash
# View logs
tail -f dhan_mcp.log

# Change log level
LOG_LEVEL=DEBUG python cli.py start
```

## Security Notes

- Never commit your `.env` file to version control
- Use environment variables in production
- Consider using API key authentication for MCP access
- Regularly rotate your DhanHQ access tokens

## Getting DhanHQ Credentials

1. Visit [DhanHQ API Portal](https://api.dhan.co/)
2. Login with your DhanHQ account
3. Generate API credentials
4. Copy Client ID and Access Token to your `.env` file

## Support

For issues and questions:
- Check the logs first
- Use demo mode for testing
- Review this configuration guide
- Submit issues on GitHub repository