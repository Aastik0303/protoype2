"""
HuggingFace Embeddings — replaces Google embeddings.
Uses sentence-transformers/all-MiniLM-L6-v2 (free, no API key needed, fast).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from langchain_community.embeddings import HuggingFaceEmbeddings

_embeddings = None


@st.cache_resource(show_spinner=False)
def get_embeddings():
    """Cached HuggingFace embeddings — loads once, reused across sessions."""
    global _embeddings
    if _embeddings is None:
        _embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )
    return _embeddings
