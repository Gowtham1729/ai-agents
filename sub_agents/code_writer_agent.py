from google.adk.agents import Agent

from config import get_settings

# Code Writer Agent
# Takes the initial specification (from user query) and writes code.
code_writer_agent = None
try:
    code_writer_agent = Agent(
        model=get_settings().MODEL_GEMINI_2_0_FLASH,
        name="code_writer_agent",
        instruction="""You are a Python Code Generator.
Based *only* on the user's request, write Python code that fulfills the requirement.
Output *only* the complete Python code block, enclosed in triple backticks (```python ... ```). 
Do not add any other text before or after the code block.
""",
        description="Writes initial Python code based on a specification.",
        output_key="generated_code",  # Stores output in state['generated_code']
    )
    print(
        f"✅ Agent '{code_writer_agent.name}' created using model '{code_writer_agent.model}'."
    )
except Exception as e:
    print(f"❌ Could not create Code Writer agent. Error: {e}")
