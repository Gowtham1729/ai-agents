import os
import asyncio
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.genai import types

import logging
logging.basicConfig(level=logging.INFO)


MODEL_GEMINI_2_0_FLASH = "gemini-2.0-flash"
MODEL_GPT_4O = "openai/gpt-4o"
MODEL_CLAUDE_SONNET = "anthropic/claude-3-sonnet-20240229"