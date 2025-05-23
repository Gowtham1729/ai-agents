import os

from google.adk.agents import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters

# This is a comment added by the agent to test the edit_file tool

TARGET_FOLDER_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "/home/gowtham/ai-agents/ai-agents"
)

root_agent = Agent(
    name="filesystem_assistant_agent",
    model="gemini-2.0-flash-lite",
    description="Help the user manage their files. You can list files, read files, etc.",
    instruction="you are an expert researcher. You always stick to the facts.",
    tools=[
        MCPToolset(
            connection_params=StdioServerParameters(
                command="npx",
                args=[
                    "-y",
                    "@modelcontextprotocol/server-filesystem",
                    os.path.abspath(TARGET_FOLDER_PATH),
                ],
            ),
        )
    ],
)
