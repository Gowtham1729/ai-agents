from google.adk.agents import SequentialAgent

from sub_agents.code_refactor_agent import code_refactor_agent
from sub_agents.code_reviewer_agent import code_reviewer_agent
from sub_agents.code_writer_agent import code_writer_agent

root_agent = SequentialAgent(
    name="code_pipeline_agent",
    description="Executes a sequence of code writing, reviewing, and refactoring.",
    sub_agents=[code_writer_agent, code_reviewer_agent, code_refactor_agent],
)
