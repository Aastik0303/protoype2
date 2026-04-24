import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI


@st.cache_resource
def get_llm():
    """Created once, reused forever."""
    return ChatGoogleGenerativeAI(
        model=st.secrets.get("GOOGLE_MODEL", "gemini-2.5-flash"),
        google_api_key=st.secrets["GOOGLE_API_KEY"],
        streaming=True,
        convert_system_message_to_human=True,
    )


def stream(messages: list, temperature: float = 0.7):
    """Stream tokens. Yields str chunks."""
    try:
        llm = get_llm().bind(temperature=temperature)
        for chunk in llm.stream(messages):
            if chunk.content:
                yield chunk.content
    except Exception as e:
        yield f"\n\n❌ Error: {str(e)}"


def invoke(messages: list, temperature: float = 0.7) -> str:
    """Single call, returns full string."""
    try:
        llm = get_llm().bind(temperature=temperature)
        return llm.invoke(messages).content
    except Exception as e:
        return f"Error: {str(e)}"
