"""
Test cases for CSV tool functionality
"""
import json
import pytest
from pathlib import Path
from mcp_server.server import MCPServer
from mcp_server.tools.csv_tool import CSVTool

@pytest.fixture
def mcp_server():
    return MCPServer("test_server")

@pytest.fixture
def csv_tool(mcp_server, tmp_path):
    return CSVTool(mcp_server, output_dir=str(tmp_path))

def test_create_csv_single_row(mcp_server, csv_tool):
    # Test data
    request_data = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tool/call",
        "params": {
            "name": "create_csv",
            "arguments": {
                "filename": "test",
                "data": {"name": "John", "age": 30}
            }
        }
    }
    
    # Send request to server
    response = mcp_server.handle_request(request_data)
    
    # Check response structure
    assert "result" in response
    assert "content" in response["result"]
    assert len(response["result"]["content"]) == 1
    assert response["result"]["content"][0]["type"] == "text"
    
    # Get created file path from response
    file_path = response["result"]["content"][0]["text"]
    assert Path(file_path).exists()

def test_create_csv_multiple_rows(mcp_server, csv_tool):
    # Test data
    request_data = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tool/call",
        "params": {
            "name": "create_csv",
            "arguments": {
                "filename": "test_multi",
                "data": [
                    {"name": "John", "age": 30},
                    {"name": "Jane", "age": 25}
                ]
            }
        }
    }
    
    # Send request to server
    response = mcp_server.handle_request(request_data)
    
    # Check response
    assert "result" in response
    file_path = response["result"]["content"][0]["text"]
    assert Path(file_path).exists()

def test_tool_list(mcp_server, csv_tool):
    # Test data
    request_data = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tool/list",
        "params": {}
    }
    
    # Get tool list
    response = mcp_server.handle_request(request_data)
    
    # Check if create_csv tool is registered
    assert "result" in response
    assert "tools" in response["result"]
    tools = response["result"]["tools"]
    
    # Find create_csv tool
    create_csv_tool = next((tool for tool in tools if tool["name"] == "create_csv"), None)
    assert create_csv_tool is not None
    
    # Check tool schema
    assert "inputSchema" in create_csv_tool
    schema = create_csv_tool["inputSchema"]
    assert "properties" in schema
    assert "filename" in schema["properties"]
    assert "data" in schema["properties"] 