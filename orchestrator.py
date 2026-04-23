import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from typing import Literal
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage
from typing import TypedDict
import streamlit as st

ROUTER_PROMPT = """You are an Advanced AI Orchestrator responsible for managing multiple specialized agents.

AGENT SELECTION LOGIC — Choose ONLY ONE:
- general    → normal conversation, general questions, simple facts
- code       → writing code, debugging, programming, algorithms
- document   → questions about uploaded documents, PDFs, files
- youtube    → YouTube links or questions about a video
- researcher → complex research, unknown topics, multi-step analysis
- data       → CSV, datasets, numbers, statistics, data analysis

SPEED RULES:
- Do NOT overthink
- Maximum 2 steps of reasoning
- If obvious → answer immediately

Reply with EXACTLY ONE word — nothing else:
general / code / document / youtube / researcher / data"""

FAST_RULES = {
    "youtube":    ["youtube.com", "youtu.be"],
    "code":       ["debug", "code", "function", "bug", "error", "script",
                   "python", "javascript", "typescript", "sql", "algorithm",
                   "compile", "syntax", "class", "import", "def "],
    "researcher": ["research", "latest", "current news", "what happened",
                   "find information", "analyze", "report on", "search for",
                   "who is", "what is the history", "explain in detail"],
    "document":   ["in the document", "from the pdf", "in the file",
                   "uploaded", "from the doc"],
    "data":       ["dataset", "csv", "dataframe", "statistics", "correlation",
                   "regression", "machine learning", "ml model", "plot",
                   "chart", "graph", "analyze data", "data analysis"],
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
        # Fast path first — no LLM call needed
        fast = _fast_route(state["message"])
        if fast:
            return {**state, "agent": fast}

        # LLM fallback for ambiguous queries
        try:
            result = llm.invoke([
                SystemMessage(content=ROUTER_PROMPT),
                HumanMessage(content=state["message"]),
            ])
            key = result.content.strip().lower().split()[0]
            if key in ["general", "code", "document", "youtube", "researcher", "data"]:
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
