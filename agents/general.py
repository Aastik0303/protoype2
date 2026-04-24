import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain.schema import HumanMessage, AIMessage, SystemMessage
from utils.llm import stream

SYSTEM = """You are a helpful, smart, and friendly AI assistant.
Be clear, concise, and human. Use markdown when helpful."""


def run(message: str, history: list):
    msgs = [SystemMessage(content=SYSTEM)]
    for h in history[-10:]:
        if h["role"] == "user":
            msgs.append(HumanMessage(content=h["content"]))
        else:
            msgs.append(AIMessage(content=h["content"]))
    msgs.append(HumanMessage(content=message))
    yield from stream(msgs, temperature=0.7)
