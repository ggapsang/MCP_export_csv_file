"""
MCP (Model Context Protocol) Server Implementation
"""
from typing import Any, Callable, Dict, List, Optional, Union

class MCPServer:
    """MCP Server base class"""
    def __init__(self, name: str):
        self.name = name
        self.tools: Dict[str, Callable] = {}
        self.resources: Dict[str, Callable] = {}

    def tool(self):
        """Tool decorator for registering MCP tools"""
        def decorator(func: Callable) -> Callable:
            self.tools[func.__name__] = func
            return func
        return decorator

    def resource(self, url_pattern: str):
        """Resource decorator for registering MCP resources"""
        def decorator(func: Callable) -> Callable:
            self.resources[url_pattern] = func
            return func
        return decorator 