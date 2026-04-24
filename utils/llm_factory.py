import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Iterator


@st.cache_resource
def get_gemini(temperature: float = 0.7):
    """Cached Gemini instance — created ONCE, reused forever."""
    return ChatGoogleGenerativeAI(
        model=st.secrets.get("GOOGLE_MODEL", "gemini-2.5-flash"),
        google_api_key=st.secrets["GOOGLE_API_KEY"],
        temperature=temperature,
        streaming=True,
        convert_system_message_to_human=True,
    )


def stream_with_fallback(
    messages: list,
    temperature: float = 0.7,
) -> Iterator[str]:
    """
    Stream from Gemini 2.5 Flash.
    On ANY error — immediately yield a status message and retry once.
    No sleep. No buffering. Tokens yielded as fast as they arrive.
    """
    llm = get_gemini(temperature)

    try:
        for chunk in llm.stream(messages):
            if chunk.content:
                yield chunk.content
        return

    except Exception as e:
        err = str(e).lower()
        is_overload = any(x in err for x in [
            "503", "overloaded", "high demand",
            "resource_exhausted", "quota", "429",
            "rate limit", "unavailable"
        ])

        if is_overload:
            # Immediately tell the user — no sleep
            yield "\n\n> ⚡ *System: Gemini is busy, retrying immediately...*\n\n"
            # One immediate retry with a fresh instance
            try:
                fresh_llm = ChatGoogleGenerativeAI(
                    model=st.secrets.get("GOOGLE_MODEL", "gemini-2.5-flash-preview-04-17"),
                    google_api_key=st.secrets["GOOGLE_API_KEY"],
                    temperature=temperature,
                    streaming=True,
                    convert_system_message_to_human=True,
                )
                for chunk in fresh_llm.stream(messages):
                    if chunk.content:
                        yield chunk.content
                return
            except Exception as e2:
                yield f"\n\n❌ Gemini unavailable: {e2}\n\nPlease try again in a moment."
                return
        else:
            yield f"\n\n❌ Error: {e}"
            return


def invoke_with_fallback(messages: list, temperature: float = 0.7) -> str:
    """
    Non-streaming invoke — Gemini only.
    Validates error once and retries immediately on overload.
    """
    llm = get_gemini(temperature)

    try:
        return llm.invoke(messages).content

    except Exception as e:
        err = str(e).lower()
        is_overload = any(x in err for x in [
            "503", "overloaded", "resource_exhausted", "429", "rate limit"
        ])
        if is_overload:
            # One immediate retry with fresh instance
            fresh_llm = ChatGoogleGenerativeAI(
                model=st.secrets.get("GOOGLE_MODEL", "gemini-2.5-flash-preview-04-17"),
                google_api_key=st.secrets["GOOGLE_API_KEY"],
                temperature=temperature,
                streaming=True,
                convert_system_message_to_human=True,
            )
            return fresh_llm.invoke(messages).content
        raise
