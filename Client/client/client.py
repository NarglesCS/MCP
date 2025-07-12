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
        is_python = server_script_path.endswith('.py')
        is_js = server_script_path.endswith('.js')
        if not (is_python or is_js):
            raise ValueError("Server script must be a .py or .js file")
        
        command = "python" if is_python else "node"
        server_params = StdioServerParameters(command=command, args=[server_script_path], env = None)

        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

        await self.session.initialize()

        #List of availiable tools
        response = await self.session.list_tools()
        tools = response.tools
        print("\nConnected to server with tools:", [tool.name for tool in tools])

async def process_query(self, query: str) -> str:
    """Process a query using Gemini and availiable tools"""
    messages = [
            {'contents': [{'parts': [{'text': 'Write a short poem about a cloud.'}]}]},
            {'contents': [{'parts': [{'text': 'Write a short poem about a cat.'}]}], 'system_instructions': {'parts': [{'text': 'You are a cat. Your name is Neko.'}]}}
    ]

    response = await self.session.list_tools()
    availiable_tools = [{
        "name": tool.name,
        "description": tool.description,
        "input_schema": tool.inputSchema
    } for tool in response.tools]

    #initial gemini api call
    job = gemini.models.generate_content(
        model="gemini-2.5-flash",
        contents=query
    )

