import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import Generator
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from utils.llm_factory import stream_with_fallback


class GeneralChatbotAgent:
    NAME = "General Chatbot"
    ICON = "🤖"
    MODEL_TAG = "Gemini 2.5 Flash / Groq Fallback"

    SYSTEM = (
        "You are a brilliant, warm, and knowledgeable AI assistant. "
        "Respond thoughtfully and clearly. Use markdown formatting when helpful. "
        "Be concise yet thorough."
    )

    def stream(self, message: str, history: list) -> Generator[str, None, None]:
        msgs = [SystemMessage(content=self.SYSTEM)]
        for h in history[-12:]:
            if h["role"] == "user":
                msgs.append(HumanMessage(content=h["content"]))
            else:
                msgs.append(AIMessage(content=h["content"]))
        msgs.append(HumanMessage(content=message))
        yield from stream_with_fallback(msgs, temperature=0.7)
