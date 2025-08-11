# Troubleshooting Guide

## Common Issues and Solutions

### 1. Configuration Issues

#### "Configuration incomplete" error
```bash
# Solution: Run setup and configure credentials
python cli.py setup
# Edit .env file with your DhanHQ credentials
```

#### Can't find .env file
```bash
# Make sure .env.example exists, then run:
python cli.py setup
```

### 2. Server Startup Issues

#### Import errors
```bash
# Make sure all dependencies are installed:
pip install -r requirements.txt --user
```

#### Port already in use
```bash
# Change port in .env file:
MCP_SERVER_PORT=8001
```

### 3. API Connection Issues

#### "Connection failed" error
```bash
# Test your connection:
python cli.py test

# Check your credentials are correct in .env file
# Verify your DhanHQ API access token is valid
```

#### Invalid credentials
- Get fresh credentials from https://api.dhan.co/
- Make sure to copy them exactly to .env file
- Check for extra spaces or quotes

### 4. Demo Mode Issues

#### Demo mode not working
```bash
# Ensure demo mode is enabled in .env:
DEMO_MODE=true

# Check status:
python cli.py status
```

### 5. MCP Client Configuration

#### Claude Desktop not recognizing server
- Check the path in your configuration file
- Make sure server is running
- Verify JSON syntax in config file

#### Stock not found errors
```bash
# Search for correct stock name:
# In your MCP client, ask: "search for HDFC stocks"
# Or check stocks.json file directly
```

### 6. Permission Issues

#### Can't write to log file
```bash
# Change log file location in .env:
LOG_FILE=~/dhan_mcp.log
```

#### Python import errors
```bash
# Install in user directory:
pip install -r requirements.txt --user

# Or use virtual environment:
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### 7. Development Issues

#### Want to modify code
```bash
# Use demo mode for testing:
DEMO_MODE=true python cli.py start

# Check logs for detailed error information:
tail -f dhan_mcp.log
```

## Getting Help

1. Check the logs first:
   ```bash
   tail -f dhan_mcp.log
   ```

2. Verify configuration:
   ```bash
   python cli.py status
   ```

3. Test in demo mode:
   ```bash
   # Add to .env file:
   DEMO_MODE=true
   ```

4. Enable debug logging:
   ```bash
   # Add to .env file:
   LOG_LEVEL=DEBUG
   ```

## Useful Commands

```bash
# Quick setup
./install.sh

# Check everything
python cli.py status

# Test API connection
python cli.py test

# Start server
python cli.py start

# Start in demo mode
DEMO_MODE=true python cli.py start

# Check logs
tail -f dhan_mcp.log

# Clean restart
rm .env && python cli.py setup
```

## FAQ

**Q: Do I need real DhanHQ credentials to test?**
A: No, set `DEMO_MODE=true` in your .env file to test without real credentials.

**Q: Can I use this in production?**
A: Yes, but ensure you secure your credentials and use proper logging.

**Q: Which MCP clients are supported?**
A: Any MCP-compatible client, including Claude Desktop, MCP CLI, etc.

**Q: Can I add custom stocks?**
A: Yes, edit the stocks.json file to add more stocks.

**Q: How do I get DhanHQ credentials?**
A: Visit https://api.dhan.co/ and login with your DhanHQ account.

**Q: Is this safe to use?**
A: Demo mode is completely safe. For real trading, ensure you understand the risks.

**Q: Can I run multiple servers?**
A: Yes, use different ports by setting MCP_SERVER_PORT in .env files.