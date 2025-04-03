"""
MCP Server implementation with stdio communication
"""
import sys
import json
from typing import Any, Dict
from .server import MCPServer

class MCPServerStdio(MCPServer):
    """MCP Server that communicates via stdin/stdout"""
    def __init__(self, name: str):
        super().__init__(name)
        self.running = False

    def start(self):
        """Start the server and listen for requests on stdin"""
        self.running = True
        print(f"MCP Server '{self.name}' started", file=sys.stderr)
        
        while self.running:
            try:
                # Read request from stdin
                request_line = sys.stdin.readline().strip()
                if not request_line:
                    continue
                    
                # Parse request
                request = json.loads(request_line)
                
                # Process request
                response = self.handle_request(request)
                
                # Send response to stdout
                print(json.dumps(response), flush=True)
                
            except json.JSONDecodeError:
                print(json.dumps({
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32700,
                        "message": "Parse error"
                    }
                }), flush=True)
            except Exception as e:
                print(json.dumps({
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32603,
                        "message": str(e)
                    }
                }), flush=True)

    def stop(self):
        """Stop the server"""
        self.running = False 