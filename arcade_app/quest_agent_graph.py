import os
import operator
from typing import Annotated, TypedDict, List
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain_google_vertexai import ChatVertexAI
from langchain_core.messages import BaseMessage

from arcade_app.tools import REGISTRY_TOOLS

class AgentState(TypedDict):
    # Append-only message history
    messages: Annotated[List[BaseMessage], operator.add]

def _get_model():
    model_name = os.getenv("EVALFORGE_MODEL_VERSION", "gemini-2.5-flash-001")
    llm = ChatVertexAI(
        model_name=model_name,
        project=os.getenv("GOOGLE_CLOUD_PROJECT"),
        location=os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1"),
        temperature=0.3
    )
    return llm.bind_tools(REGISTRY_TOOLS)

async def call_model(state: AgentState):
    llm = _get_model()
    response = await llm.ainvoke(state["messages"])
    return {"messages": [response]}

def should_continue(state: AgentState) -> str:
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END

def build_quest_graph():
    workflow = StateGraph(AgentState)
    
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", ToolNode(REGISTRY_TOOLS))
    
    workflow.set_entry_point("agent")
    
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            END: END
        }
    )
    
    # Loop back to agent after tools run so it can summarize the result
    workflow.add_edge("tools", "agent")
    
    return workflow.compile()

# Singleton
quest_graph = build_quest_graph()
