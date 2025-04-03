"""
MCP Server implementation with JSON-RPC 2.0
"""
from typing import Any, Dict, List, Optional, Union
import json
from dataclasses import dataclass

@dataclass
class RPCRequest:
    """JSON-RPC 2.0 request"""
    jsonrpc: str
    id: int
    method: str
    params: Dict[str, Any]

@dataclass
class RPCResponse:
    """JSON-RPC 2.0 response"""
    jsonrpc: str = "2.0"
    id: Optional[int] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, Any]] = None

class MCPServer:
    """MCP Server implementation"""
    def __init__(self, name: str):
        self.name = name
        self.tools: Dict[str, Any] = {}
        self.resources: Dict[str, Any] = {}

    def tool(self):
        """Tool decorator for registering MCP tools"""
        def decorator(func):
            self.tools[func.__name__] = {
                "name": func.__name__,
                "description": func.__doc__ or "",
                "function": func,
                "schema": self._get_function_schema(func)
            }
            return func
        return decorator

    def _get_function_schema(self, func) -> Dict[str, Any]:
        """Extract function schema from type hints and docstring"""
        import inspect
        sig = inspect.signature(func)
        
        properties = {}
        required = []
        
        for name, param in sig.parameters.items():
            param_type = param.annotation.__name__ if hasattr(param.annotation, '__name__') else str(param.annotation)
            properties[name] = {"type": param_type}
            
            if param.default == inspect.Parameter.empty:
                required.append(name)
        
        return {
            "type": "object",
            "properties": properties,
            "required": required
        }

    def handle_request(self, request_data: Union[str, Dict]) -> Dict:
        """Handle incoming JSON-RPC request"""
        if isinstance(request_data, str):
            request_data = json.loads(request_data)
            
        request = RPCRequest(**request_data)
        
        if request.method == "tool/list":
            return self._handle_tool_list()
        elif request.method == "tool/call":
            return self._handle_tool_call(request.params)
            
        return RPCResponse(
            id=request.id,
            error={"code": -32601, "message": f"Method {request.method} not found"}
        ).__dict__

    def _handle_tool_list(self) -> Dict:
        """Handle tool/list method"""
        tools = []
        for tool_info in self.tools.values():
            tools.append({
                "name": tool_info["name"],
                "description": tool_info["description"],
                "inputSchema": tool_info["schema"]
            })
            
        return RPCResponse(
            result={"tools": tools}
        ).__dict__

    def _handle_tool_call(self, params: Dict) -> Dict:
        """Handle tool/call method"""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        if tool_name not in self.tools:
            return RPCResponse(
                error={"code": -32601, "message": f"Tool {tool_name} not found"}
            ).__dict__
            
        try:
            tool = self.tools[tool_name]["function"]
            result = tool(**arguments)
            
            return RPCResponse(
                result={
                    "content": [{
                        "type": "text",
                        "text": str(result),
                        "annotations": {"audience": ["assistant"]}
                    }]
                }
            ).__dict__
        except Exception as e:
            return RPCResponse(
                error={"code": -32603, "message": str(e)}
            ).__dict__ 