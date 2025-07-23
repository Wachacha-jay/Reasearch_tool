from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, AIMessage
from .state import AgentState
from .llm import create_llm
from .agents import create_research_agent, create_analyst_agent, create_writer_agent, create_supervisor_agent

def create_research_team_graph():
    llm = create_llm()
    members = ["researcher", "analyst", "writer"]
    researcher = create_research_agent(llm)
    analyst = create_analyst_agent(llm)
    writer = create_writer_agent(llm)
    supervisor = create_supervisor_agent(llm, members)
    workflow = StateGraph(AgentState)
    workflow.add_node("researcher", researcher)
    workflow.add_node("analyst", analyst)
    workflow.add_node("writer", writer)
    workflow.add_node("supervisor", supervisor)
    workflow.add_edge("researcher", "supervisor")
    workflow.add_edge("analyst", "supervisor")
    workflow.add_edge("writer", "supervisor")
    workflow.add_conditional_edges(
        "supervisor",
        lambda x: x["next"],
        {
            "researcher": "researcher",
            "analyst": "analyst",
            "writer": "writer",
            "FINISH": END
        }
    )
    workflow.set_entry_point("supervisor")
    return workflow

def compile_research_team():
    workflow = create_research_team_graph()
    memory = MemorySaver()
    app = workflow.compile(checkpointer=memory)
    return app

def run_research_team(topic: str, thread_id: str = "research_session_1"):
    app = compile_research_team()
    initial_state = {
        "messages": [HumanMessage(content=f"Research the topic: {topic}")],
        "research_topic": topic,
        "next": "researcher",
        "current_agent": "start",
        "findings": {},
        "final_report": ""
    }
    config = {"configurable": {"thread_id": thread_id}}
    final_state = None
    for step, state in enumerate(app.stream(initial_state, config=config)):
        current_state = list(state.values())[0]
        final_state = current_state
        if step > 10:
            break
    return final_state 