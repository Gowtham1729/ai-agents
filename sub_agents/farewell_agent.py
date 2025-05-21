# @title Define Farewell Sub-Agents
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from config import get_settings
from tools.greetings import say_goodbye

farewell_agent = None
try:
    farewell_agent = Agent(
        model=get_settings().MODEL_GEMINI_2_0_FLASH,
        name="farewell_agent",
        description="Handles simple farewells and goodbyes using the 'say_goodbye' tool.",  # Crucial for delegation
        instruction="You are the Farewell Agent. Your ONLY task is to provide a polite goodbye message. "
        "Use the 'say_goodbye' tool when the user indicates they are leaving or ending the conversation "
        "(e.g., using words like 'bye', 'goodbye', 'thanks bye', 'see you'). "
        "Do not perform any other actions.",
        tools=[say_goodbye],
    )
    print(
        f"✅ Agent '{farewell_agent.name}' created using model '{farewell_agent.model}'."
    )
except Exception as e:
    print(f"❌ Could not create Farewell agent. Error: {e}")
