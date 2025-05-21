from google.adk.agents import Agent

from config import get_settings

# Code Refactor Agent
# Takes the original code and the review comments (read from state) and refactors the code.
code_refactor_agent = None
try:
    code_refactor_agent = Agent(
        model=get_settings().MODEL_GEMINI_2_0_FLASH,
        name="code_refactor_agent",
        instruction="""You are a Python Code Refactoring AI.
Your goal is to improve the given Python code based on the provided review comments.

  **Original Code:**
  ```python
  {generated_code}
  ```

  **Review Comments:**
  {review_comments}

**Task:**
Carefully apply the suggestions from the review comments to refactor the original code.
If the review comments state "No major issues found," return the original code unchanged.
Ensure the final code is complete, functional, and includes necessary imports and docstrings.

**Output:**
Output *only* the final, refactored Python code block, enclosed in triple backticks (```python ... ```). 
Do not add any other text before or after the code block.
""",
        description="Refactors code based on review comments.",
        output_key="refactored_code",  # Stores output in state['refactored_code']
    )
    print(
        f"✅ Agent '{code_refactor_agent.name}' created using model '{code_refactor_agent.model}'."
    )
except Exception as e:
    print(f"❌ Could not create Code Refactor agent. Error: {e}")
