import asyncio
import logging
import os

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from config import get_settings
from sub_agents.farewell_agent import farewell_agent
from sub_agents.greeting_agent import greeting_agent
from tools.weather import get_weather

logging.basicConfig(level=logging.INFO)

settings = get_settings()

# MODEL_GEMINI_2_0_FLASH = settings.MODEL_GEMINI_2_0_FLASH
MODEL_GPT_4O = settings.MODEL_GPT_4O
# MODEL_CLAUDE_SONNET = settings.MODEL_CLAUDE_SONNET
# MODEL_GEMMA_3_27B = settings.MODEL_GEMMA_3_27B
# MODEL_GEMMA_3_4B = settings.MODEL_GEMMA_3_4B
# MODEL_QWEN3_0_6B = settings.MODEL_QWEN3_0_6B


root_agent = Agent(
    name="weather_agent_v2",
    model=LiteLlm(model=MODEL_GPT_4O),
    description="The main coordinator agent. Handles weather requests and delegates greetings/farewells to specialists.",
    instruction="You are the main Weather Agent coordinating a team. Your primary responsibility is to provide weather information. "
    "Use the 'get_weather' tool ONLY for specific weather requests (e.g., 'weather in London'). "
    "You have specialized sub-agents: "
    "1. 'greeting_agent': Handles simple greetings like 'Hi', 'Hello'. Delegate to it for these. "
    "2. 'farewell_agent': Handles simple farewells like 'Bye', 'See you'. Delegate to it for these. "
    "Analyze the user's query. If it's a greeting, delegate to 'greeting_agent'. If it's a farewell, delegate to 'farewell_agent'. "
    "If it's a weather request, handle it yourself using 'get_weather'. "
    "For anything else, respond appropriately or state you cannot handle it.",
    tools=[get_weather],
    sub_agents=[greeting_agent, farewell_agent],
)
