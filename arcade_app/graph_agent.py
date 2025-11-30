import os
import operator
from typing import Annotated, TypedDict, List

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_google_vertexai import ChatVertexAI
from langchain_core.messages import BaseMessage, SystemMessage

# Import our new tool
from arcade_app.tools import retrieve_docs

# 1. Define State
class AgentState(TypedDict):
    # 'messages' is a list that grows (append-only)
    messages: Annotated[List[BaseMessage], operator.add]

# 2. Initialize Model with Tools
def _get_model():
    model_name = os.getenv("EVALFORGE_MODEL_VERSION", "gemini-2.0-flash-exp")
    project = os.getenv("GOOGLE_CLOUD_PROJECT")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    
    llm = ChatVertexAI(
        model_name=model_name,
        project=project,
        location=location,
        temperature=0.3
    )
    # Bind tools so the LLM knows it can call them
    return llm.bind_tools([retrieve_docs])

# 3. Define Nodes
async def call_model(state: AgentState):
    llm = _get_model()
    
    # Inject system prompt if this is the first call
    messages = state["messages"]
    if len(messages) == 1:  # Only user message
        system_prompt = SystemMessage(content="""
ROLE: Senior Staff Engineer / Mentor.

IMPORTANT: You have access to the PROJECT CODEBASE via the 'retrieve_docs' tool.

INSTRUCTIONS:
- If asked about "structure" or "files", look for 'PROJECT_MAP' in the search results.
- Use the file tree to explain the architecture (e.g., "The backend logic is in `src/api`...").
- If asked about specific logic, search for the code.
- NEVER say you don't have file access.
- List key directories when explaining structure.
- Answer code-first, but be comprehensive when explaining architecture.
""")
        messages = [system_prompt] + messages
    
    response = await llm.ainvoke(messages)
    return {"messages": [response]}

# 4. Define Router (Should we stop or call a tool?)
def should_continue(state: AgentState) -> str:
    last_message = state["messages"][-1]
    # If the LLM returned a tool_call, go to "tools" node
    if last_message.tool_calls:
        return "tools"
    # Otherwise, we are done
    return END

# 5. Construct Graph
def build_explain_graph():
    workflow = StateGraph(AgentState)
    
    # Nodes
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", ToolNode([retrieve_docs]))
    
    # Edges
    workflow.set_entry_point("agent")
    
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            END: END
        }
    )
    
    # Loop back: After tool execution, go back to agent to read result
    workflow.add_edge("tools", "agent")
    
    return workflow.compile()

# Singleton for reuse
explain_graph = build_explain_graph()
