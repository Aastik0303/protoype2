import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.llm import invoke
from langchain.schema import HumanMessage, SystemMessage

SYSTEM = """Route the user message to one agent. Reply with EXACTLY one word:
general   - chat, questions, opinions
code      - code, debug, programming, scripts
document  - questions about uploaded files/documents
youtube   - YouTube videos, transcripts
researcher - research, news, web search, current events"""

RULES = {
    "youtube":    ["youtube.com", "youtu.be"],
    "code":       ["debug","def ","class ","function","algorithm","error","bug",
                   "python","javascript","sql","code","script","syntax"],
    "researcher": ["research","latest","news","current","search for","who is",
                   "what happened","find information"],
    "document":   ["document","pdf","uploaded","in the file","from the doc"],
}


def route(message: str, override: str = None) -> str:
    if override and override != "auto":
        return override

    lower = message.lower()

    # Fast keyword check first
    for agent, keywords in RULES.items():
        if any(k in lower for k in keywords):
            return agent

    # LLM fallback for ambiguous
    try:
        result = invoke([
            SystemMessage(content=SYSTEM),
            HumanMessage(content=message),
        ], temperature=0.0)
        key = result.strip().lower().split()[0]
        if key in ["general", "code", "document", "youtube", "researcher"]:
            return key
    except Exception:
        pass

    return "general"
