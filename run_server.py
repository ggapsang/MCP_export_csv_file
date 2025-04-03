"""
MCP Server entry point
"""
from mcp_server.stdio_server import MCPServerStdio
from mcp_server.tools.csv_tool import CSVTool
import sys

def main():
    # Create server instance
    server = MCPServerStdio("csv_mcp_server")
    
    # Register tools
    csv_tool = CSVTool(server)
    
    # Start server
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()
        print("Server stopped", file=sys.stderr)

if __name__ == "__main__":
    main() 