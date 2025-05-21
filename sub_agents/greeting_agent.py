# @title Define Greeting Sub-Agent
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from config import get_settings
from tools.greetings import say_hello

greeting_agent = None
try:
    greeting_agent = Agent(
        model=get_settings().MODEL_GEMINI_2_0_FLASH,
        name="greeting_agent",
        description="Handles simple greetings and hellos using the 'say_hello' tool.",  # Crucial for delegation
        instruction="You are the Greeting Agent. Your ONLY task is to provide a friendly greeting to the user. "
        "Use the 'say_hello' tool to generate the greeting. "
        "If the user provides their name, make sure to pass it to the tool. "
        "Do not engage in any other conversation or tasks.",
        tools=[say_hello],
    )
    print(
        f"✅ Agent '{greeting_agent.name}' created using model '{greeting_agent.model}'."
    )
except Exception as e:
    print(f"❌ Could not create Greeting agent. Error: {e}")
