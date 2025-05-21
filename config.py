from enum import Enum
from functools import lru_cache
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class EnvironmentType(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class Settings(BaseSettings):
    ENVIRONMENT: EnvironmentType = Field(
        default=EnvironmentType.DEVELOPMENT,
        description="The environment the application is running in",
    )
    DEBUG: bool = Field(default=True, description="Debug mode flag")

    # Google API settings
    GOOGLE_API_KEY: Optional[str] = Field(
        default=None,
        description="Google API key for accessing Google services",
    )
    GOOGLE_GENAI_USE_VERTEXAI: bool = Field(
        default=False,
        description="Use Vertex AI for Google GenAI",
    )

    # OpenAI API settings
    OPENAI_API_KEY: Optional[str] = Field(
        default=None,
        description="OpenAI API key for accessing OpenAI services",
    )
    OPENAI_API_BASE: Optional[str] = Field(
        default=None,
        description="Base URL for OpenAI API",
    )

    # Anthropic API settings
    ANTHROPIC_API_KEY: Optional[str] = Field(
        default=None,
        description="Anthropic API key for accessing Anthropic services",
    )

    # Local model settings
    LM_STUDIO_API_BASE: str = Field(
        default="http://127.0.0.1:1234",
        description="Base URL for Local Model Studio API",
    )

    # Models
    MODEL_GEMINI_2_0_FLASH: str = Field(
        default="gemini-2.0-flash",
        description="Default Google Gemini model to use",
    )
    MODEL_GPT_4O: str = Field(
        default="openai/gpt-4o",
        description="Default OpenAI model to use",
    )
    MODEL_CLAUDE_SONNET: str = Field(
        default="anthropic/claude-3-sonnet-20240229",
        description="Default Anthropic model to use",
    )
    MODEL_GEMMA_3_27B: str = Field(
        default="lm_studio/gemma-3-27b-it-qat",
        description="Default Gemma model to use",
    )
    MODEL_GEMMA_3_4B: str = Field(
        default="lm_studio/gemma-3-4b-it-qat",
        description="Default Gemma model to use",
    )
    MODEL_QWEN3_0_6B: str = Field(
        default="lm_studio/qwen3-0.6b",
        description="Default Qwen3 model to use",
    )

    # Other default configuration
    DEFAULT_TEMPERATURE: float = Field(
        default=0.7,
        description="Default temperature for model inference",
    )


@lru_cache()
def get_settings() -> Settings:
    """
    Get the application settings.

    Returns:
        Settings: The application settings.
    """
    return Settings()
