import asyncio
import logging
import os

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.genai import types

from config import get_settings
from tools.weather import get_weather

logging.basicConfig(level=logging.INFO)

settings = get_settings()

MODEL_GEMINI_2_0_FLASH = settings.MODEL_GEMINI_2_0_FLASH
MODEL_GPT_4O = settings.MODEL_GPT_4O
MODEL_CLAUDE_SONNET = settings.MODEL_CLAUDE_SONNET
MODEL_GEMMA_3_27B = settings.MODEL_GEMMA_3_27B
MODEL_GEMMA_3_4B = settings.MODEL_GEMMA_3_4B

root_agent = Agent(
    name="weather_agent_v1",
    model=LiteLlm(model=MODEL_GEMMA_3_4B),
    description="Provides weather information for specific cities.",
    instruction="You are a helpful weather assistant. "
    "When the user asks for the weather in a specific city, "
    "use the 'get_weather' tool to find the information. "
    "If the tool returns an error, inform the user politely. "
    "If the tool is successful, present the weather report clearly.",
    tools=[get_weather],
)
