import asyncio
from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from google import genai
from dotenv import load_dotenv

load_dotenv()

class MCPClient:
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.gemini = genai.Client(api_key=GEMINI_API_KEY)

    async def connect_to_server(self, server_script_path: str):
        """Connect to MCP Server
        
        Args:
            server_script_path: Path to the server script (.py or .js)
        """


