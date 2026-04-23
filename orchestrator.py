"""
LangGraph-powered orchestrator — auto-routes messages to the best agent.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage
import streamlit as st

ROUTER_PROMPT = """You are an agent router. Reply with EXACTLY ONE of these words — nothing else:
general   → casual chat, general knowledge, opinions, questions
code      → writing code, debugging, programming, algorithms, scripts
document  → questions about uploaded documents, PDFs, files
youtube   → YouTube video analysis, video questions, transcripts
researcher → deep research, current events, fact-finding, news, web search"""

AgentKey = Literal["general", "code", "document", "youtube", "researcher"]

FAST_RULES = {
    "youtube": ["youtube.com", "youtu.be"],
    "code": ["debug", "code", "function", "bug", "error", "script",
             "python", "javascript", "typescript", "sql", "algorithm", "compile", "syntax"],
    "researcher": ["research", "latest", "current news", "what happened",
                   "find information", "analyze", "report on", "search for"],
    "document": ["in the document", "from the pdf", "in the file", "uploaded"],
}


class State(TypedDict):
    message: str
    agent: str


def _fast_route(msg: str) -> str | None:
    lower = msg.lower()
    for agent, keywords in FAST_RULES.items():
        if any(k in lower for k in keywords):
            return agent
    return None


def build_graph():
    llm = ChatGroq(
        model=st.secrets.get("GROQ_MODEL", "llama-3.3-70b-versatile"),
        groq_api_key=st.secrets["GROQ_API_KEY"],
        temperature=0.0,
    )

    def router_node(state: State) -> State:
        fast = _fast_route(state["message"])
        if fast:
            return {**state, "agent": fast}
        try:
            result = llm.invoke([
                SystemMessage(content=ROUTER_PROMPT),
                HumanMessage(content=state["message"]),
            ])
            key = result.content.strip().lower().split()[0]
            if key in ["general", "code", "document", "youtube", "researcher"]:
                return {**state, "agent": key}
        except Exception:
            pass
        return {**state, "agent": "general"}

    g = StateGraph(State)
    g.add_node("router", router_node)
    g.set_entry_point("router")
    g.add_edge("router", END)
    return g.compile()


@st.cache_resource
def get_graph():
    return build_graph()


def route(message: str, override: str = None) -> str:
    if override and override != "auto":
        return override
    graph = get_graph()
    result = graph.invoke({"message": message, "agent": "general"})
    return result["agent"]
