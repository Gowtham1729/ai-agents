# AI Agents Showcase (Google ADK)

This repository contains a collection of AI agents built using the Google Agent Development Kit (ADK). These agents demonstrate various capabilities, from code generation and review to specialized tasks like providing weather information and performing Google searches.

## Table of Contents
- [Project Setup](#project-setup)
- [Code Structure](#code-structure)
- [Agent Configuration](#agent-configuration)
- [How to Run Agents](#how-to-run-agents)
- [Key Agents and Their Functionality](#key-agents-and-their-functionality)
- [Tools](#tools)

---

## Project Setup

This section guides you through setting up the project environment.

### 1. Environment Variables

This project uses a `.env` file to manage API keys and other sensitive configurations.

1.  **Create the `.env` file:**
    Copy the example file `.env.example` to a new file named `.env` in the root of the project:
    ```bash
    cp .env.example .env
    ```
2.  **Edit `.env`:**
    Open the `.env` file and add your API keys and any other required configurations. Based on `config.py`, you might need the following:

    *   `GOOGLE_API_KEY`: Your Google API key for Gemini models and other Google services.
    *   `OPENAI_API_KEY`: Your OpenAI API key if you plan to use OpenAI models.
    *   `OPENAI_API_BASE`: (Optional) If you use a proxy or a non-standard base URL for OpenAI.
    *   `ANTHROPIC_API_KEY`: Your Anthropic API key if you plan to use Anthropic models.
    *   `LM_STUDIO_API_BASE`: If you are using local models served via LM Studio, set this to your LM Studio server address (e.g., `http://127.0.0.1:1234`).

    **Note:** Fill in only the keys for the services you intend to use.

### 2. Install Dependencies

This project uses `uv` for fast dependency management and to create a virtual environment. Dependencies are listed in `pyproject.toml`, and a `uv.lock` file is provided for reproducible builds.

1.  **Create a virtual environment and install dependencies:**
    Navigate to the project root directory and run:
    ```bash
    uv venv # Create a virtual environment (e.g., .venv)
    uv pip install -r requirements.txt # Install dependencies
    ```
    *(Note: If `requirements.txt` is not current, it might need regeneration from `pyproject.toml`. Alternatively, install with `uv pip install .` if `pyproject.toml` supports it. We assume `requirements.txt` is the primary method for now.)*

2.  **Activate the virtual environment:**
    On macOS and Linux:
    ```bash
    source .venv/bin/activate
    ```
    On Windows:
    ```bash
    .venv\Scripts\activate
    ```
    Your shell prompt should change to indicate that the virtual environment is active.

---
## Code Structure

The project is organized as follows:

*   **Agent Implementations**: Agent-specific logic is primarily located in directories ending with `_agent/`. For example:
    *   `coding_agent/`: Contains a sequential agent for code generation workflows.
    *   `sub_agents/`: Houses various individual agents, often used as components.
    *   `test_google_search_agent/`: Example agent for Google Search.
    *   `test_weather_agent/`: Example agent for weather and time.
    *   `test_weather_agent_non_gemini/`: Variation of the weather agent.
    *   `test_weather_multi_agent/`: Example of a more complex weather-related agent.
    *   *(Specifics on each agent are in "Key Agents and Their Functionality" and "How to Run Agents".)*

*   **`tools/`**:
    *   Contains custom tools that agents can use to interact with external services or perform specific actions. Examples:
        *   `weather.py`: Provides a (mock) weather information service.
        *   `time.py`: Provides current time information.
        *   `greetings.py`: Contains functions for generating greetings and farewells.
    *   The ADK also provides built-in tools like `google_search` which are leveraged by some agents.

*   **`config.py`**:
    *   Centralized configuration for the application. It manages API keys, model selections (e.g., Gemini, OpenAI, Anthropic models), environment settings (development, staging, production), and debug flags. Uses `pydantic-settings` for loading configurations.

*   **`main.py`**:
    *   A basic entry point for the Python application. Agents are typically run using the ADK web interface.

*   **`.env.example`**:
    *   An example template for the `.env` file, showing the environment variables that can be set.

*   **`.gitignore`**:
    *   Specifies intentionally untracked files that Git should ignore.

*   **`pyproject.toml`**:
    *   Project metadata and dependencies, used by modern Python packaging tools like `uv` and `pip`.
*   **`uv.lock`**: Lock file from `uv` for reproducible builds.

---
## Agent Configuration

Agent behavior, especially the Large Language Models (LLMs) they use, is primarily configured in `config.py`.

### Key Configuration Aspects:

1.  **Model Selection:**
    *   The `Settings` class in `config.py` defines model identifiers (e.g., `MODEL_GEMINI_2_0_FLASH`, `MODEL_GPT_4O`, `MODEL_CLAUDE_SONNET`, local models like `MODEL_GEMMA_3_27B`).
    *   Agents are instantiated with a specific model, e.g., in `sub_agents/code_writer_agent.py`:
        ```python
        from config import get_settings
        # ...
        code_writer_agent = Agent(
            model=get_settings().MODEL_GEMINI_2_0_FLASH, 
            # ...
        )
        ```
2.  **API Keys:**
    *   Loaded from `.env` via `config.py` for services like Google, OpenAI, Anthropic.
3.  **Environment Settings:**
    *   `config.py` manages settings like `ENVIRONMENT: EnvironmentType` and `DEBUG: bool`.
4.  **Accessing Settings:**
    *   The `get_settings()` function in `config.py` provides cached access to settings.

### Customizing Agent Instructions and Tools:
Each agent is also configured with:
*   **`name`**: A unique agent identifier.
*   **`description`**: Human-readable explanation of the agent's function.
*   **`instruction`**: The core prompt guiding the LLM, often with placeholders (e.g., `{generated_code}`).
*   **`tools`**: A list of functions (tools) the agent can use (e.g., `google_search`, `get_weather`).
*   **`output_key`**: Specifies where the agent's primary output is stored in its state.

These are set during agent instantiation (see various `agent.py` files).

---
## How to Run Agents

The primary way to interact with and run the agents in this project is through the Google ADK web interface.

1.  **Activate your Python virtual environment** where you've installed the dependencies:
    On macOS and Linux:
    ```bash
    source .venv/bin/activate
    ```
    On Windows:
    ```bash
    .venv\Scripts\activate
    ```

2.  **Start the ADK web interface:**
    Navigate to the project root directory and run the following command:
    ```bash
    uv run adk web
    ```
    This will typically start a local web server. Open the URL provided in your terminal (usually something like `http://127.0.0.1:8000`) in your web browser.

3.  **Interacting with Agents via the Web Interface:**
    The web interface should provide a way to select and interact with the available agents. You can use this interface to send queries to the agents and view their responses. For example, you can test the `coding_agent` by providing a coding task, or query the `test_weather_agent` for weather information.

    **Note:** Ensure your `.env` file is correctly set up with the necessary API keys before running agents that rely on external model providers, as these will be used by the agents running via the web interface.

---
## Key Agents and Their Functionality

### 1. `coding_agent`
*   **Location:** `coding_agent/agent.py` (instance: `root_agent`)
*   **Type:** `SequentialAgent`
*   **Description:** Pipeline for code generation: write -> review -> refactor.
    1.  `code_writer_agent`: Generates initial Python code.
    2.  `code_reviewer_agent`: Reviews code and provides feedback.
    3.  `code_refactor_agent`: Refactors code based on feedback.
*   **Output:** State includes `generated_code`, `review_comments`, `refactored_code`.

### 2. `test_google_search_agent`
*   **Location:** `test_google_search_agent/agent.py` (instance: `root_agent`)
*   **Type:** `Agent`
*   **Description:** Answers questions using Google Search; instructed as an expert researcher.
*   **Tools:** `google_search` (ADK built-in).

### 3. `test_weather_agent`
*   **Location:** `test_weather_agent/agent.py` (instance: `root_agent`)
*   **Type:** `Agent`
*   **Description:** Provides current time and weather for a city.
*   **Tools:** `get_weather` (from `tools/weather.py`), `get_current_time` (from `tools/time.py`).

### 4. Sub-Agents (`sub_agents/`)

These are component agents, primarily used within more complex agentic systems. Their individual functionality can be explored further by examining their configurations and instructions.

*   **`code_writer_agent.py`** (instance: `code_writer_agent`):
    *   Generates Python code. Output key: `generated_code`.
*   **`code_reviewer_agent.py`** (instance: `code_reviewer_agent`):
    *   Reviews Python code. Expects `{generated_code}`. Output key: `review_comments`.
*   **`code_refactor_agent.py`** (instance: `code_refactor_agent`):
    *   Refactors code. Expects `{generated_code}`, `{review_comments}`. Output key: `refactored_code`.
*   **`greeting_agent.py`** (instance: `greeting_agent`):
    *   Provides greetings. Tool: `say_hello` (from `tools/greetings.py`).
*   **`farewell_agent.py`** (instance: `farewell_agent`):
    *   Provides goodbyes. Tool: `say_goodbye` (from `tools/greetings.py`).

---
## Tools

Agents use custom and built-in ADK tools.

### Custom Tools (in `tools/`)

*   **`get_weather(city: str) -> dict`** (in `tools/weather.py`):
    *   Retrieves weather for a city (mock data).
*   **`get_current_time() -> dict`** (in `tools/time.py`):
    *   Returns current date/time.
*   **`say_hello(name: Optional[str] = None) -> str`** (in `tools/greetings.py`):
    *   Generates a greeting.
*   **`say_goodbye() -> str`** (in `tools/greetings.py`):
    *   Generates a farewell.

These are passed to agents during initialization.

### Built-in ADK Tools

*   **`google_search`**:
    *   Used by `test_google_search_agent` for web searches.
    *   Consult ADK documentation for other available tools.

Tools enable agents to interact with their environment and perform diverse tasks.

---
