from google.adk.agents import Agent, LoopAgent, SequentialAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools import FunctionTool, ToolContext, agent_tool, google_search

from config import get_settings

settings = get_settings()


def exit_loop(tool_context: ToolContext):
    """Call this function ONLY when the critique indicates no further changes are needed, signaling the iterative process should end."""
    print(f"  [Tool Call] exit_loop triggered by {tool_context.agent_name}")
    tool_context.actions.escalate = True  # Escalation signals the LoopAgent to exit
    return "Exiting refinement loop as plan is considered complete."


requirements_agent = Agent(
    model=LiteLlm(model=settings.MODEL_GPT_4O),
    name="RequirementsAgent",
    description="Elicits detailed functional and non-functional requirements from the user for the AI agent to be built. Engages in a dialogue to clarify needs and constraints.",
    instruction="""You are the Requirements Agent. Your goal is to have a detailed conversation with the user to understand exactly what kind of AI agent they want to build using the Google Agent Development Kit (ADK).

    Focus on:
    1.  **Core Functionality:** What are the primary tasks the agent should perform?
    2.  **Key Features:** What specific capabilities are needed?
    3.  **Inputs/Outputs:** What kind of data will the agent process, and what output is expected?
    4.  **Tools & Integrations:** Does the agent need to use specific tools (e.g., Google Search, APIs, databases) or integrate with other systems?
    5.  **User Interaction:** How should users interact with the agent (e.g., chat, API calls)?
    6.  **Performance & Constraints:** Are there any specific performance requirements, limitations, or non-functional aspects to consider?
    7.  **Success Criteria:** How will the user know if the agent is successful?

    Ask clarifying questions. Be thorough. Your final output should be a comprehensive 'requirements_document' that clearly outlines all gathered information, structured in a way that the PlannerAgent can use it to design the agent.
    Confirm with the user that your understanding, as captured in the 'requirements_document', is complete and accurate before concluding.
    """,
    output_key="requirements_document",
)

planner_agent = Agent(  # This is the initial planner
    model="gemini-2.5-pro-preview-05-06",
    name="PlannerAgent",
    description="Generates an initial comprehensive agent development plan based on the provided requirements document. This plan outlines the agent's architecture, ADK components, tools (prioritizing MCP tools), and overall structure.",
    instruction="""You are the Planner Agent. Your task is to create a detailed 'agent_plan_document' based on the 'requirements_document' provided.
    The 'requirements_document' is:
    {{requirements_document}}

    Your 'agent_plan_document' must be comprehensive and cover the following aspects, keeping Google ADK best practices in mind:
    1.  **Agent Name & Description:** A clear name and high-level description for the new agent.
    2.  **Primary Agent Type(s):**
        * Will it be a single `LlmAgent`, a `WorkflowAgent` (and if so, which type: `SequentialAgent`, `ParallelAgent`, `LoopAgent`), a custom `BaseAgent`, or a Multi-Agent System (MAS)?
        * Justify your choice based on the requirements.
    3.  **Sub-Agents (if MAS):**
        * If a MAS is proposed, define each sub-agent's name, role, primary type, and how they will interact.
    4.  **Core Logic / Instruction Prompt:** For each `LlmAgent` (main or sub-agent), draft a detailed instruction prompt.
    5.  **Tools Required:**
        * **Prioritize MCP Tools:** First, use Google Search to identify if existing MCP (Managed Component Platform) agents or tools can fulfill the required functionalities. List these MCP tools if available.
        * **Custom `FunctionTool`s (as a fallback):** Only if suitable MCP tools are NOT found after searching, propose custom `FunctionTool`s. For these, provide:
            * A clear function name.
            * A detailed docstring explaining its purpose, arguments, and return values (this will be used by the LLM).
            * A brief description of the logic needed.
        * Built-in ADK tools (e.g., `google_search` itself, if needed for the agent's operation beyond your own planning use).
        * `AgentTool`s (if sub-agents are used as tools).
    6.  **State Variables:** Identify any key pieces of information that need to be maintained in the agent's state (`tool_context.state`) during a session.
    7.  **Data Flow:** Briefly describe how data will flow through the agent or MAS.
    8.  **Key Python Files to be Generated:** List the main Python files that will need to be created (e.g., `main_agent.py`, `tools.py`, `sub_agents/`).
    9.  **Assumptions & Clarifications:** Note any assumptions made or areas where requirements might need further clarification.

    Your output must be the 'planning_document'. Use Google Search extensively to find MCP tools before resorting to custom tool definitions.
    """,
    output_key="planning_document",
    tools=[google_search],
)


plan_critic_agent = Agent(
    model="gemini-2.5-flash-preview-05-20",
    name="PlanCriticAgent",
    description="Critically evaluates an agent plan against the original requirements, identifying potential issues, gaps, inconsistencies, or areas for improvement. Specifically checks if MCP tools were prioritized.",
    instruction="""You are the Plan Critic Agent. Your role is to meticulously review the 'planning_document' against the original 'requirements_document' and provide constructive criticism.

    The 'requirements_document' is:
    {{requirements_document}}

    The 'planning_document' to review is:
    {{planning_document}}

    Your critique should focus on:
    1.  **MCP Tool Prioritization:** CRITICAL: Did the planner adequately search for and prioritize MCP (Managed Component Platform) tools before suggesting custom tools? If custom tools are proposed, is there a justification for why an MCP tool couldn't be used?
    2.  **Completeness:** Does the plan address all aspects of the requirements? Are there any missing functionalities or features?
    3.  **Correctness:** Is the proposed architecture suitable for the requirements? Are the ADK components (agent types, tools) chosen appropriately?
    4.  **Feasibility:** Is the plan realistic to implement with ADK? Are there any overly complex or impractical suggestions?
    5.  **Clarity & Ambiguity:** Is the plan clear and unambiguous? Are there parts that could be misinterpreted?
    6.  **Tool Definitions:** If custom tools are proposed, are their descriptions and intended functionalities clear and sufficient for a developer to implement them?
    7.  **Efficiency/Best Practices:** Does the plan follow ADK best practices? Are there more efficient ways to achieve the same goals?
    8.  **Alignment with ADK Capabilities:** Does the plan leverage ADK features effectively?

    Your output must be a 'criticism' document. Be specific in your feedback. If there are no issues and the plan is excellent (especially regarding MCP tool usage), clearly state that no changes are needed.
    Use Google Search if you need to verify ADK best practices or alternative approaches, including the availability of MCP tools.
    """,
    tools=[google_search],
    output_key="criticism",
)

plan_refiner_agent = Agent(
    model="gemini-2.5-pro-preview-05-06",
    name="PlanRefinerAgent",
    description="Refines an agent plan based on provided criticism, aiming to address all identified issues and improve the plan's quality and alignment with requirements, with special attention to MCP tool prioritization. Can decide to exit the refinement loop if the plan is deemed satisfactory.",
    instruction="""You are the Plan Refiner Agent. Your task is to revise and improve the 'planning_document' based on the 'criticism' it received, ensuring it aligns perfectly with the 'requirements_document'. Pay close attention to feedback regarding MCP tool usage.

    The original 'requirements_document' is:
    {{requirements_document}}

    The 'planning_document' to refine is:
    {{planning_document}}

    The 'criticism' received is:
    {{criticism}}

    Your goal is to produce an updated 'planning_document'.
    1.  **Address all points in the 'criticism'**: Systematically go through each piece of feedback and modify the plan accordingly. If the criticism points out a lack of MCP tool consideration, actively use Google Search to find suitable MCP tools before proposing custom ones.
    2.  **Maintain Core Plan Structure**: Unless the criticism points out fundamental flaws, try to refine the existing plan rather than starting from scratch.
    3.  **Ensure Alignment**: Double-check that the refined plan fully meets all specifications in the 'requirements_document'.
    4.  **Clarity and Detail**: Ensure the refined plan is clear, detailed, and actionable for the subsequent coding phases.
    5.  **Decision to Exit**:
        * If the 'criticism' clearly states that 'no changes are needed' or that the plan is excellent (especially regarding MCP tool prioritization and overall quality), and you agree after reviewing, you MUST call the `exit_loop` function as your primary action.
        * Otherwise, after refining the plan, output the new 'planning_document'. Do NOT call `exit_loop` if substantial changes were made or if you believe further review is beneficial.

    Use Google Search extensively to find MCP tools if indicated by the criticism or if you identify opportunities to replace custom tools with MCP alternatives.
    Your output is the refined 'planning_document'. If you call `exit_loop`, that will be your primary action and you should return a message indicating this.
    """,
    tools=[google_search, exit_loop],
    output_key="planning_document",
)


planning_loop_agent = LoopAgent(
    name="PlanningRefinementLoop", sub_agents=[plan_critic_agent, plan_refiner_agent]
)

planning_agent = SequentialAgent(
    name="PlanningAgent",
    description="Orchestrates the overall agent planning process, including initial plan generation and iterative refinement based on criticism (with a focus on MCP tool prioritization), using the requirements provided.",
    sub_agents=[planner_agent, planning_loop_agent],
)
