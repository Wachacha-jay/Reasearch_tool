from typing import Annotated
from typing_extensions import TypedDict
import operator

class AgentState(TypedDict):
    """State shared between all agents in the graph"""
    messages: Annotated[list, operator.add]
    next: str
    current_agent: str
    research_topic: str
    findings: dict
    final_report: str

class AgentResponse(TypedDict):
    """Standard response format for all agents"""
    content: str
    next_agent: str
    findings: dict 