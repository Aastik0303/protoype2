import time
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

# 1. Cache the LLM instances to avoid overhead on every run
@st.cache_resource
def get_llm(provider="gemini", temperature=0.7):
    if provider == "gemini":
        return ChatGoogleGenerativeAI(
            model=st.secrets.get("GOOGLE_MODEL", "gemini-2.5-flash"),
            google_api_key=st.secrets["GOOGLE_API_KEY"],
            temperature=temperature,
            streaming=True
        )
    else:
        return ChatGroq(
            model=st.secrets.get("GROQ_MODEL", "llama-3.3-70b-versatile"),
            groq_api_key=st.secrets["GROQ_API_KEY"],
            temperature=temperature,
            streaming=True
        )

def stream_with_fallback(messages, temperature=0.7):
    # Get pre-initialized models
    gemini = get_llm("gemini", temperature)
    
    try:
        # Attempt Gemini
        for chunk in gemini.stream(messages):
            if chunk.content:
                yield chunk.content
    except Exception as e:
        err = str(e).lower()
        # List of errors that trigger fallback
        overload_triggers = ["503", "overloaded", "quota", "429", "unavailable"]
        
        if any(x in err for x in overload_triggers):
            yield "\n\n> ⚡ *Switching to Llama 3.3 (Gemini overloaded)...*\n\n"
            
            # Immediately try Groq without a long sleep
            try:
                groq = get_llm("groq", temperature)
                for chunk in groq.stream(messages):
                    if chunk.content:
                        yield chunk.content
            except Exception as e2:
                yield f"\n\n❌ Critical Error: {e2}"
        else:
            yield f"\n\n❌ Connection Error: {e}"
