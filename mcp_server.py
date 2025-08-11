#!/usr/bin/env python3
"""
Unified MCP Server for DhanHQ Trading Assistant.
This server combines all trading tools into a single MCP endpoint.
"""
import logging
from mcp.server.fastmcp import FastMCP
from config import (
    validate_config, 
    setup_logging, 
    print_config_status, 
    DEMO_MODE,
    MCP_SERVER_PORT,
    MCP_SERVER_HOST
)

# Import all tool functions
from order_placement_tool import place_order, list_available_stocks, load_stocks_data, find_stock_code
from fund_balance_tool import check_fund_balance, calculate_margin as calculate_margin_tool
from holdings_positions_tool import get_holdings, get_positions, convert_position
from margin_calculator_tool import calculate_margin_by_stock_name
from order_book_tool import get_order_book, get_trade_book, cancel_order
from after_market_order_tool import place_after_market_order

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Create the unified MCP server
mcp = FastMCP("DhanHQ Trading Assistant")


def demo_response(operation: str, **kwargs):
    """Generate demo response when in demo mode."""
    return {
        "status": "demo",
        "message": f"Demo mode: {operation} operation simulated",
        "demo_data": kwargs,
        "note": "This is a simulated response. Set DEMO_MODE=false for real trading."
    }


# === ORDER MANAGEMENT TOOLS ===

@mcp.tool()
def place_stock_order(stock_name: str, quantity: int, transaction_type: str, 
                     product_type: str = "INTRADAY", order_type: str = "MARKET"):
    """
    Place a new order for a stock.
    
    Args:
        stock_name: The name of the stock (e.g., "ADANIENT", "HDFC")
        quantity: Number of shares to buy/sell
        transaction_type: "BUY" or "SELL"
        product_type: Product type ("INTRADAY", "CNC", "MARGIN", etc.)
        order_type: Order type ("MARKET" or "LIMIT")
    
    Returns:
        Order status information
    """
    if DEMO_MODE:
        return demo_response("place_order", stock_name=stock_name, quantity=quantity, 
                           transaction_type=transaction_type, product_type=product_type)
    
    return place_order(stock_name, quantity, transaction_type, product_type, order_type)


@mcp.tool()
def place_after_market_stock_order(stock_name: str, quantity: int, transaction_type: str, 
                                  price: float, product_type: str = "CNC"):
    """
    Place an after-market order for a stock.
    
    Args:
        stock_name: The name of the stock
        quantity: Number of shares to buy/sell
        transaction_type: "BUY" or "SELL"
        price: Price per share
        product_type: Product type (default: "CNC")
    
    Returns:
        Order status information
    """
    if DEMO_MODE:
        return demo_response("after_market_order", stock_name=stock_name, quantity=quantity,
                           transaction_type=transaction_type, price=price)
    
    return place_after_market_order(stock_name, quantity, transaction_type, price, product_type)


@mcp.tool()
def get_order_history():
    """Get order book/history."""
    if DEMO_MODE:
        return demo_response("get_order_book")
    
    return get_order_book()


@mcp.tool()
def get_trade_history():
    """Get trade book/history."""
    if DEMO_MODE:
        return demo_response("get_trade_book")
    
    return get_trade_book()


@mcp.tool()
def cancel_stock_order(order_id: str):
    """Cancel an existing order."""
    if DEMO_MODE:
        return demo_response("cancel_order", order_id=order_id)
    
    return cancel_order(order_id)


# === PORTFOLIO MANAGEMENT TOOLS ===

@mcp.tool()
def get_portfolio_holdings():
    """Get a list of all holdings in your demat account."""
    if DEMO_MODE:
        return demo_response("get_holdings")
    
    return get_holdings()


@mcp.tool()
def get_open_positions():
    """Get a list of all open positions for the day."""
    if DEMO_MODE:
        return demo_response("get_positions")
    
    return get_positions()


@mcp.tool()
def convert_stock_position(from_product_type: str, to_product_type: str, 
                          exchange_segment: str, position_type: str, 
                          security_id: str, convert_qty: int, trading_symbol: str = ""):
    """Convert a position from one product type to another."""
    if DEMO_MODE:
        return demo_response("convert_position", from_product_type=from_product_type,
                           to_product_type=to_product_type, convert_qty=convert_qty)
    
    return convert_position(from_product_type, to_product_type, exchange_segment,
                          position_type, security_id, convert_qty, trading_symbol)


# === ACCOUNT INFORMATION TOOLS ===

@mcp.tool()
def get_account_balance():
    """Check fund balance and margin information."""
    if DEMO_MODE:
        return demo_response("get_fund_balance")
    
    return check_fund_balance()


@mcp.tool()
def calculate_margin(stock_name: str, transaction_type: str, quantity: int, 
                    product_type: str = "INTRADAY", price: float = 0):
    """Calculate margin requirements for a potential trade."""
    if DEMO_MODE:
        return demo_response("calculate_margin", stock_name=stock_name, 
                           quantity=quantity, product_type=product_type)
    
    return calculate_margin_by_stock_name(stock_name, transaction_type, quantity, 
                                        product_type, price)


# === UTILITY TOOLS ===

@mcp.tool()
def get_available_stocks():
    """List all available stocks in the system."""
    return list_available_stocks()


@mcp.tool()
def search_stock(stock_name: str):
    """Search for a stock by name and get its details."""
    stocks = load_stocks_data()
    results = []
    search_term = stock_name.lower()
    
    for stock in stocks:
        if (search_term in stock.get('stock_name', '').lower() or 
            search_term in stock.get('company_name', '').lower()):
            results.append({
                'stock_name': stock.get('stock_name'),
                'company_name': stock.get('company_name'),
                'stock_code': stock.get('stock_code')
            })
    
    return {
        "status": "success",
        "message": f"Found {len(results)} stocks matching '{stock_name}'",
        "stocks": results[:10]  # Limit to top 10 results
    }


@mcp.tool()
def get_server_status():
    """Get server configuration and status information."""
    config_valid = validate_config()
    
    return {
        "status": "online",
        "demo_mode": DEMO_MODE,
        "config_valid": config_valid,
        "total_stocks": len(load_stocks_data()),
        "server_info": {
            "host": MCP_SERVER_HOST,
            "port": MCP_SERVER_PORT
        },
        "available_tools": [
            "place_stock_order", "place_after_market_stock_order",
            "get_order_history", "get_trade_history", "cancel_stock_order",
            "get_portfolio_holdings", "get_open_positions", "convert_stock_position",
            "get_account_balance", "calculate_margin",
            "get_available_stocks", "search_stock", "get_server_status"
        ]
    }


def main():
    """Main entry point for the server."""
    print_config_status()
    
    if not validate_config() and not DEMO_MODE:
        logger.error("Configuration is incomplete. Please set up your credentials or enable demo mode.")
        return False
    
    logger.info(f"Starting DhanHQ MCP Trading Assistant server on {MCP_SERVER_HOST}:{MCP_SERVER_PORT}")
    logger.info(f"Demo mode: {'Enabled' if DEMO_MODE else 'Disabled'}")
    
    # Run the server
    mcp.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")