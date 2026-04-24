import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain.schema import HumanMessage, AIMessage, SystemMessage
from utils.llm import stream

SYSTEM = """You are an expert software engineer.
Write clean, efficient code with proper markdown code blocks.
Always explain your code clearly. Debug step by step."""


def run(message: str, history: list):
    msgs = [SystemMessage(content=SYSTEM)]
    for h in history[-10:]:
        if h["role"] == "user":
            msgs.append(HumanMessage(content=h["content"]))
        else:
            msgs.append(AIMessage(content=h["content"]))
    msgs.append(HumanMessage(content=message))
    yield from stream(msgs, temperature=0.1)
