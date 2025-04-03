"""
CSV file creation and management tools for MCP
"""
from typing import Dict, List, Union
import pandas as pd
from pathlib import Path
from ..server import MCPServer

class CSVTool:
    def __init__(self, server: MCPServer, output_dir: str = "output"):
        self.server = server
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self._register_tools()

    def _register_tools(self):
        @self.server.tool()
        def create_csv(filename: str, data: Union[List[Dict], Dict], columns: List[str] = None) -> str:
            """Create a CSV file with the given data
            
            Args:
                filename: Name of the CSV file to create
                data: Data to write to the CSV file. Can be a list of dictionaries or a single dictionary
                columns: Optional list of column names. If not provided, will be inferred from data

            Returns:
                Path to the created CSV file
            """
            if not filename.endswith('.csv'):
                filename = f"{filename}.csv"
            
            filepath = self.output_dir / filename
            
            # Convert data to DataFrame
            if isinstance(data, dict):
                df = pd.DataFrame([data])
            else:
                df = pd.DataFrame(data)
            
            # Use specified columns if provided
            if columns:
                df = df[columns]
            
            # Save to CSV
            df.to_csv(filepath, index=False)
            return str(filepath) 