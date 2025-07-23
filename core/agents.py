from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage
from .state import AgentState
from .llm import create_llm

# Research Agent
def create_research_agent(llm):
    research_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a Research Specialist AI. Your role is to:\n1. Analyze the research topic thoroughly\n2. Identify key areas that need investigation\n3. Provide initial research findings and insights\n4. Suggest specific angles for deeper analysis\n\nFocus on providing comprehensive, accurate information and clear research directions.\nAlways structure your response with clear sections and bullet points.\n"""),
        MessagesPlaceholder(variable_name="messages"),
        ("human", "Research Topic: {research_topic}")
    ])
    research_chain = research_prompt | llm
    def research_agent(state: AgentState) -> AgentState:
        try:
            response = research_chain.invoke({
                "messages": state["messages"],
                "research_topic": state["research_topic"]
            })
            findings = {
                "research_overview": response.content,
                "key_areas": ["area1", "area2", "area3"],
                "initial_insights": response.content[:500] + "..."
            }
            return {
                "messages": state["messages"] + [AIMessage(content=response.content)],
                "next": "analyst",
                "current_agent": "researcher",
                "research_topic": state["research_topic"],
                "findings": {**state.get("findings", {}), "research": findings},
                "final_report": state.get("final_report", "")
            }
        except Exception as e:
            error_msg = f"Research agent error: {str(e)}"
            return {
                "messages": state["messages"] + [AIMessage(content=error_msg)],
                "next": "analyst",
                "current_agent": "researcher",
                "research_topic": state["research_topic"],
                "findings": state.get("findings", {}),
                "final_report": state.get("final_report", "")
            }
    return research_agent

# Analyst Agent
def create_analyst_agent(llm):
    analyst_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a Data Analyst AI. Your role is to:\n1. Analyze data and information provided by the research team\n2. Identify patterns, trends, and correlations\n3. Provide statistical insights and data-driven conclusions\n4. Suggest actionable recommendations based on analysis\n\nFocus on quantitative analysis, data interpretation, and evidence-based insights.\nUse clear metrics and concrete examples in your analysis.\n"""),
        MessagesPlaceholder(variable_name="messages"),
        ("human", "Analyze the research findings for: {research_topic}")
    ])
    analyst_chain = analyst_prompt | llm
    def analyst_agent(state: AgentState) -> AgentState:
        try:
            response = analyst_chain.invoke({
                "messages": state["messages"],
                "research_topic": state["research_topic"]
            })
            analysis_findings = {
                "analysis_summary": response.content,
                "key_metrics": ["metric1", "metric2", "metric3"],
                "recommendations": response.content.split("recommendations:")[-1] if "recommendations:" in response.content.lower() else "No specific recommendations found"
            }
            return {
                "messages": state["messages"] + [AIMessage(content=response.content)],
                "next": "writer",
                "current_agent": "analyst",
                "research_topic": state["research_topic"],
                "findings": {**state.get("findings", {}), "analysis": analysis_findings},
                "final_report": state.get("final_report", "")
            }
        except Exception as e:
            error_msg = f"Analyst agent error: {str(e)}"
            return {
                "messages": state["messages"] + [AIMessage(content=error_msg)],
                "next": "writer",
                "current_agent": "analyst",
                "research_topic": state["research_topic"],
                "findings": state.get("findings", {}),
                "final_report": state.get("final_report", "")
            }
    return analyst_agent

# Writer Agent
def create_writer_agent(llm):
    writer_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a Report Writer AI. Your role is to:\n1. Synthesize all research and analysis into a comprehensive report\n2. Create clear, professional documentation\n3. Ensure proper structure with executive summary, findings, and conclusions\n4. Make complex information accessible to various audiences\n\nFocus on clarity, completeness, and professional presentation.\nInclude specific examples and actionable insights.\n"""),
        MessagesPlaceholder(variable_name="messages"),
        ("human", "Create a comprehensive report for: {research_topic}")
    ])
    writer_chain = writer_prompt | llm
    def writer_agent(state: AgentState) -> AgentState:
        try:
            response = writer_chain.invoke({
                "messages": state["messages"],
                "research_topic": state["research_topic"]
            })
            return {
                "messages": state["messages"] + [AIMessage(content=response.content)],
                "next": "supervisor",
                "current_agent": "writer",
                "research_topic": state["research_topic"],
                "findings": state.get("findings", {}),
                "final_report": response.content
            }
        except Exception as e:
            error_msg = f"Writer agent error: {str(e)}"
            return {
                "messages": state["messages"] + [AIMessage(content=error_msg)],
                "next": "supervisor",
                "current_agent": "writer",
                "research_topic": state["research_topic"],
                "findings": state.get("findings", {}),
                "final_report": f"Error generating report: {str(e)}"
            }
    return writer_agent

# Additional agents (archivist, translator, custom, supervisor) would be implemented similarly, following the same pattern.

# Arsiv Agent (for research papers)
def create_arsiv_agent(llm):
    arsiv_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an Arsiv Research Paper Agent. Your role is to:\n1. Search for relevant research papers on the given topic using Arsiv or similar sources.\n2. Return a list of relevant papers with titles, authors, and abstracts.\n3. Provide a brief summary of the most relevant findings.\n"""),
        MessagesPlaceholder(variable_name="messages"),
        ("human", "Search for research papers on: {research_topic}")
    ])
    arsiv_chain = arsiv_prompt | llm
    def arsiv_agent(state: AgentState) -> AgentState:
        try:
            response = arsiv_chain.invoke({
                "messages": state["messages"],
                "research_topic": state["research_topic"]
            })
            arsiv_findings = {
                "arsiv_summary": response.content,
                "arsiv_papers": response.content[:500] + "..." if len(response.content) > 500 else response.content
            }
            return {
                "messages": state["messages"] + [AIMessage(content=response.content)],
                "next": "translator",
                "current_agent": "arsiv",
                "research_topic": state["research_topic"],
                "findings": {**state.get("findings", {}), "arsiv": arsiv_findings},
                "final_report": state.get("final_report", "")
            }
        except Exception as e:
            error_msg = f"Arsiv agent error: {str(e)}"
            return {
                "messages": state["messages"] + [AIMessage(content=error_msg)],
                "next": "translator",
                "current_agent": "arsiv",
                "research_topic": state["research_topic"],
                "findings": state.get("findings", {}),
                "final_report": state.get("final_report", "")
            }
    return arsiv_agent

# Tavily Agent (for web search)
def create_tavily_agent(llm):
    tavily_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a Tavily Web Search Agent. Your role is to:\n1. Search the web for the latest and most relevant information on the research topic.\n2. Return a summary of key findings and important web sources.\n3. Provide URLs or references where possible.\n"""),
        MessagesPlaceholder(variable_name="messages"),
        ("human", "Search the web for: {research_topic}")
    ])
    tavily_chain = tavily_prompt | llm
    def tavily_agent(state: AgentState) -> AgentState:
        try:
            response = tavily_chain.invoke({
                "messages": state["messages"],
                "research_topic": state["research_topic"]
            })
            tavily_findings = {
                "tavily_summary": response.content,
                "tavily_web_results": response.content[:500] + "..." if len(response.content) > 500 else response.content
            }
            return {
                "messages": state["messages"] + [AIMessage(content=response.content)],
                "next": "translator",
                "current_agent": "tavily",
                "research_topic": state["research_topic"],
                "findings": {**state.get("findings", {}), "tavily": tavily_findings},
                "final_report": state.get("final_report", "")
            }
        except Exception as e:
            error_msg = f"Tavily agent error: {str(e)}"
            return {
                "messages": state["messages"] + [AIMessage(content=error_msg)],
                "next": "translator",
                "current_agent": "tavily",
                "research_topic": state["research_topic"],
                "findings": state.get("findings", {}),
                "final_report": state.get("final_report", "")
            }
    return tavily_agent

# Translator Agent (for translation and summarization)
def create_translator_agent(llm):
    translator_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a Translator and Summarizer AI. Your role is to:\n1. Translate non-English content to English if needed.\n2. Summarize the provided content clearly and concisely.\n3. Highlight key insights from translated material.\n"""),
        MessagesPlaceholder(variable_name="messages"),
        ("human", "Translate and summarize the latest findings for: {research_topic}")
    ])
    translator_chain = translator_prompt | llm
    def translator_agent(state: AgentState) -> AgentState:
        try:
            response = translator_chain.invoke({
                "messages": state["messages"],
                "research_topic": state["research_topic"]
            })
            translation_findings = {
                "translator_summary": response.content,
                "key_translated_insights": response.content[:500] + "..." if len(response.content) > 500 else response.content
            }
            return {
                "messages": state["messages"] + [AIMessage(content=response.content)],
                "next": "supervisor",
                "current_agent": "translator",
                "research_topic": state["research_topic"],
                "findings": {**state.get("findings", {}), "translator": translation_findings},
                "final_report": state.get("final_report", "")
            }
        except Exception as e:
            error_msg = f"Translator agent error: {str(e)}"
            return {
                "messages": state["messages"] + [AIMessage(content=error_msg)],
                "next": "supervisor",
                "current_agent": "translator",
                "research_topic": state["research_topic"],
                "findings": state.get("findings", {}),
                "final_report": state.get("final_report", "")
            }
    return translator_agent

def create_supervisor_agent(llm, members):
    options = ["FINISH"] + members
    supervisor_prompt = ChatPromptTemplate.from_messages([
        ("system", f"""You are a Supervisor AI managing a research team. Your team members are:
        {', '.join(members)}

        Your responsibilities:
        1. Coordinate the workflow between team members
        2. Ensure each agent completes their specialized tasks
        3. Determine when the research is complete
        4. Maintain quality standards throughout the process

        Given the conversation, determine the next step:
        - If research is needed: route to \"researcher\"
        - If analysis is needed: route to \"analyst\"
        - If report writing is needed: route to \"writer\"
        - If work is complete: route to \"FINISH\"

        Available options: {options}

        Respond with just the name of the next agent or \"FINISH\".
        """),
        MessagesPlaceholder(variable_name="messages"),
        ("human", "Current status: {current_agent} just completed their task for topic: {research_topic}")
    ])
    supervisor_chain = supervisor_prompt | llm

    def supervisor_agent(state: AgentState) -> AgentState:
        try:
            response = supervisor_chain.invoke({
                "messages": state["messages"],
                "current_agent": state.get("current_agent", "none"),
                "research_topic": state["research_topic"]
            })
            next_agent = response.content.strip().lower()
            if "finish" in next_agent or "complete" in next_agent:
                next_step = "FINISH"
            elif "research" in next_agent:
                next_step = "researcher"
            elif "analy" in next_agent:
                next_step = "analyst"
            elif "writ" in next_agent:
                next_step = "writer"
            else:
                current = state.get("current_agent", "")
                if current == "researcher":
                    next_step = "analyst"
                elif current == "analyst":
                    next_step = "writer"
                elif current == "writer":
                    next_step = "FINISH"
                else:
                    next_step = "researcher"
            return {
                "messages": state["messages"] + [AIMessage(content=f"Supervisor decision: Next agent is {next_step}")],
                "next": next_step,
                "current_agent": "supervisor",
                "research_topic": state["research_topic"],
                "findings": state.get("findings", {}),
                "final_report": state.get("final_report", "")
            }
        except Exception as e:
            error_msg = f"Supervisor error: {str(e)}"
            return {
                "messages": state["messages"] + [AIMessage(content=error_msg)],
                "next": "FINISH",
                "current_agent": "supervisor",
                "research_topic": state["research_topic"],
                "findings": state.get("findings", {}),
                "final_report": state.get("final_report", "")
            }
    return supervisor_agent 