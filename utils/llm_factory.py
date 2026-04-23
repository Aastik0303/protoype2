"""
LLM Factory — creates LLMs with automatic fallback on 503 / overload errors.
Primary: Google Gemini 2.5 Flash
Fallback: Groq Llama 3.3 70B (fast, free, rarely overloaded)
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain.schema import BaseMessage
from typing import Iterator


def _make_gemini(temperature: float = 0.7):
    return ChatGoogleGenerativeAI(
        model=st.secrets.get("GOOGLE_MODEL", "gemini-2.5-flash"),
        google_api_key=st.secrets["GOOGLE_API_KEY"],
        temperature=temperature,
        streaming=True,
        convert_system_message_to_human=True,
    )


def _make_groq(temperature: float = 0.7):
    return ChatGroq(
        model=st.secrets.get("GROQ_MODEL", "llama-3.3-70b-versatile"),
        groq_api_key=st.secrets["GROQ_API_KEY"],
        temperature=temperature,
        streaming=True,
    )


def stream_with_fallback(
    messages: list[BaseMessage],
    temperature: float = 0.7,
    max_retries: int = 2,
) -> Iterator[str]:
    """
    Stream from Gemini; on 503/overload automatically fall back to Groq.
    Yields text chunks.
    """
    # Try Gemini first
    for attempt in range(max_retries):
        try:
            llm = _make_gemini(temperature)
            for chunk in llm.stream(messages):
                if chunk.content:
                    yield chunk.content
            return  # success
        except Exception as e:
            err = str(e).lower()
            is_overload = any(x in err for x in [
                "503", "overloaded", "high demand", "resource_exhausted",
                "quota", "429", "rate limit", "unavailable"
            ])
            if is_overload and attempt < max_retries - 1:
                time.sleep(1.5)
                continue
            elif is_overload:
                # Fall back to Groq
                yield "\n\n> ⚡ *Gemini busy — switching to Groq Llama 3.3...*\n\n"
                try:
                    llm = _make_groq(temperature)
                    for chunk in llm.stream(messages):
                        if chunk.content:
                            yield chunk.content
                    return
                except Exception as e2:
                    yield f"\n\n❌ Both models failed: {e2}"
                    return
            else:
                yield f"\n\n❌ Error: {e}"
                return


def invoke_with_fallback(
    messages: list[BaseMessage],
    temperature: float = 0.7,
) -> str:
    """Non-streaming invoke with Gemini → Groq fallback."""
    try:
        llm = _make_gemini(temperature)
        result = llm.invoke(messages)
        return result.content
    except Exception as e:
        err = str(e).lower()
        is_overload = any(x in err for x in [
            "503", "overloaded", "high demand", "resource_exhausted",
            "quota", "429", "rate limit", "unavailable"
        ])
        if is_overload:
            llm = _make_groq(temperature)
            result = llm.invoke(messages)
            return result.content
        raise
