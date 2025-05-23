# AI Agents Showcase (Google ADK)

AI agents built with Google Agent Development Kit (ADK).

## Table of Contents
- [Project Setup](#project-setup)
- [Code Structure](#code-structure)
- [Agent Configuration](#agent-configuration)
- [How to Run Agents](#how-to-run-agents)
- [Key Agents and Their Functionality](#key-agents-and-their-functionality)
- [Tools](#tools)

---

## Project Setup

Setup the environment and install dependencies.

### 1. Environment Variables

Create `.env` file with your API keys:

```bash
cp .env.example .env
```

Edit `.env` and add your keys:
- `GOOGLE_API_KEY`: For Gemini models
- `OPENAI_API_KEY`: For OpenAI models (optional)
- `ANTHROPIC_API_KEY`: For Anthropic models (optional)

### 2. Install Dependencies

Using uv:
```bash
uv venv
source .venv/bin/activate  # Linux/Mac
# or .venv\Scripts\activate  # Windows
uv sync
```

---
## Code Structure

*   **`coding_agent/`**: Sequential agent for code generation workflows
*   **`sub_agents/`**: Individual agents used as components
*   **`test_*_agent/`**: Example agents for different use cases (weather, search, etc.)
*   **`tools/`**: Custom tools for external services and actions
*   **`config.py`**: Centralized configuration and API key management
*   **`main.py`**: Basic entry point

---
## Agent Configuration

Agents are configured in `config.py` with:

- **Models**: Gemini, OpenAI, Anthropic, or local models
- **API Keys**: Loaded from `.env` file
- **Instructions**: Core prompts that guide the LLM
- **Tools**: Functions the agent can use

Access settings with `get_settings()` from `config.py`.

---
## How to Run Agents

1. **Activate virtual environment:**
   ```bash
   source .venv/bin/activate  # Linux/Mac
   # or .venv\Scripts\activate  # Windows
   ```

2. **Start ADK web interface:**
   ```bash
   uv run adk web
   ```

3. **Open in browser:** Navigate to the URL shown in terminal (usually `http://127.0.0.1:8000`)

4. **Interact with agents:** Select agents and send queries through the web interface.

---
## Key Agents and Their Functionality

### 1. `coding_agent`
**Type:** SequentialAgent  
**Purpose:** Complete code pipeline: write → review → refactor  
**Output:** Generated, reviewed, and refactored Python code

### 2. `test_google_search_agent`
**Type:** Agent  
**Purpose:** Research assistant using Google Search  
**Tools:** `google_search`

### 3. `test_weather_agent`
**Type:** Agent  
**Purpose:** Current time and weather information  
**Tools:** `get_weather`, `get_current_time`

### 4. Sub-Agents (`sub_agents/`)
Component agents used in complex workflows:
- **`code_writer_agent`**: Generates Python code
- **`code_reviewer_agent`**: Reviews code quality  
- **`code_refactor_agent`**: Improves code based on feedback
- **`greeting_agent`**: Provides greetings
- **`farewell_agent`**: Provides farewells

---
## Tools

### Custom Tools
- **`get_weather(city)`**: Weather info for a city (mock data)
- **`get_current_time()`**: Current date and time
- **`say_hello(name)`**: Generate greeting
- **`say_goodbye()`**: Generate farewell

### Built-in ADK Tools
- **`google_search`**: Web search functionality

---
