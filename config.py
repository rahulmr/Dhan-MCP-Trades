# config.py
"""
Configuration management for DhanHQ MCP Trading Assistant.
Supports environment variables and .env files for secure credential management.
"""
import os
import logging
from pathlib import Path
from typing import Optional

# Try to load environment variables from .env file
try:
    from dotenv import load_dotenv
    
    # Look for .env file in the same directory as this config file
    env_file = Path(__file__).parent / '.env'
    if env_file.exists():
        load_dotenv(env_file)
        print(f"Loaded configuration from {env_file}")
    else:
        print("No .env file found. Using environment variables or defaults.")
except ImportError:
    print("python-dotenv not installed. Using environment variables only.")


class ConfigError(Exception):
    """Raised when configuration is invalid or missing."""
    pass


def get_env_var(name: str, default: Optional[str] = None, required: bool = True) -> str:
    """Get environment variable with validation."""
    value = os.getenv(name, default)
    if required and (not value or value.strip() in ("", "your_client_id_here", "your_access_token_here")):
        raise ConfigError(
            f"Required environment variable {name} is not set or has placeholder value. "
            f"Please set it in your .env file or environment."
        )
    return value or ""


# DhanHQ API Configuration
try:
    DHAN_CLIENT_ID = get_env_var("DHAN_CLIENT_ID", required=True)
    DHAN_ACCESS_TOKEN = get_env_var("DHAN_ACCESS_TOKEN", required=True)
    DHAN_API_BASE_URL = get_env_var("DHAN_API_BASE_URL", "https://api.dhan.co/v2", required=False)
except ConfigError as e:
    print(f"Configuration Error: {e}")
    print("Please copy .env.example to .env and configure your credentials.")
    # Set empty defaults to prevent import errors
    DHAN_CLIENT_ID = ""
    DHAN_ACCESS_TOKEN = ""
    DHAN_API_BASE_URL = "https://api.dhan.co/v2"

# MCP Server Configuration
MCP_SERVER_PORT = int(get_env_var("MCP_SERVER_PORT", "8000", required=False))
MCP_SERVER_HOST = get_env_var("MCP_SERVER_HOST", "localhost", required=False)

# Demo/Development Mode
DEMO_MODE = get_env_var("DEMO_MODE", "false", required=False).lower() == "true"

# Logging Configuration
LOG_LEVEL = get_env_var("LOG_LEVEL", "INFO", required=False)
LOG_FILE = get_env_var("LOG_FILE", "dhan_mcp.log", required=False)

# Security Settings
ENABLE_AUTH = get_env_var("ENABLE_AUTH", "false", required=False).lower() == "true"
API_KEY = get_env_var("API_KEY", "", required=False)


def validate_config() -> bool:
    """Validate that all required configuration is present."""
    if not DHAN_CLIENT_ID or not DHAN_ACCESS_TOKEN:
        return False
    
    if DHAN_CLIENT_ID.strip() in ("", "your_client_id_here"):
        return False
        
    if DHAN_ACCESS_TOKEN.strip() in ("", "your_access_token_here"):
        return False
        
    return True


def setup_logging():
    """Setup logging configuration."""
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler()
        ]
    )


def print_config_status():
    """Print current configuration status."""
    print("\n=== DhanHQ MCP Configuration Status ===")
    print(f"Client ID: {'✓ Set' if DHAN_CLIENT_ID and DHAN_CLIENT_ID != 'your_client_id_here' else '✗ Not configured'}")
    print(f"Access Token: {'✓ Set' if DHAN_ACCESS_TOKEN and DHAN_ACCESS_TOKEN != 'your_access_token_here' else '✗ Not configured'}")
    print(f"API Base URL: {DHAN_API_BASE_URL}")
    print(f"Demo Mode: {'✓ Enabled' if DEMO_MODE else '✗ Disabled'}")
    print(f"MCP Server: {MCP_SERVER_HOST}:{MCP_SERVER_PORT}")
    print(f"Log Level: {LOG_LEVEL}")
    
    if not validate_config() and not DEMO_MODE:
        print("\n⚠️  Configuration incomplete! Please set your DhanHQ credentials.")
        print("Copy .env.example to .env and configure your credentials.")
    elif DEMO_MODE:
        print("\n🔧 Demo mode enabled - API calls will be simulated")
    else:
        print("\n✅ Configuration looks good!")
    print("=" * 45)
