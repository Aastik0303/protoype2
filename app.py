import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import uuid
from datetime import datetime

st.set_page_config(
    page_title="NeuralNexus · AI Platform",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Space+Grotesk:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  --sky-void:#030d1a; --sky-deep:#06111f; --sky-card:#0a1c35;
  --sky-panel:#0d2040; --sky-border:#1a3a60; --sky-bright:#1e4a78;
  --cyan:#38bdf8; --cyan-dim:#0ea5e9; --cyan-glow:rgba(56,189,248,0.15);
  --violet:#818cf8; --pink:#f472b6; --green:#34d399;
  --yellow:#fbbf24; --red:#f87171;
  --text-1:#e2e8f0; --text-2:#94a3b8; --text-3:#475569;
  --font-hd:'Orbitron',monospace; --font-body:'Space Grotesk',sans-serif;
  --font-mono:'JetBrains Mono',monospace;
}

/* ── Base ── */
.stApp { background:var(--sky-void) !important; font-family:var(--font-body); }

/* ── Sidebar — always visible, collapsible, flexible ── */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #060f1e 0%, #08162b 100%) !important;
  border-right: 1px solid var(--sky-border) !important;
  min-width: 240px !important;
  max-width: 320px !important;
  transition: all 0.3s ease !important;
}
[data-testid="stSidebar"][aria-expanded="false"] {
  min-width: 0px !important;
  max-width: 0px !important;
  overflow: hidden !important;
}
[data-testid="stSidebar"] > div:first-child {
  padding-top: 0 !important;
  overflow-y: auto !important;
  height: 100vh !important;
}

/* ── Sidebar toggle button — always visible ── */
[data-testid="collapsedControl"] {
  background: var(--sky-card) !important;
  border: 1px solid var(--sky-border) !important;
  border-radius: 0 8px 8px 0 !important;
  color: var(--cyan) !important;
  top: 50% !important;
  transform: translateY(-50%) !important;
  z-index: 999999 !important;
}
[data-testid="collapsedControl"]:hover {
  background: var(--sky-bright) !important;
  border-color: var(--cyan) !important;
}
section[data-testid="stSidebar"] > div > div > div {
  padding-bottom: 40px !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar{width:5px;height:5px}
::-webkit-scrollbar-track{background:var(--sky-deep)}
::-webkit-scrollbar-thumb{background:var(--sky-bright);border-radius:3px}
::-webkit-scrollbar-thumb:hover{background:var(--cyan-dim)}

/* ── Header ── */
.nn-header{
  background:linear-gradient(135deg,rgba(6,17,31,0.97),rgba(10,28,53,0.97));
  border-bottom:1px solid var(--sky-border);
  padding:12px 24px;
  display:flex;align-items:center;gap:14px;
  margin:-1rem -1rem 1.2rem -1rem;
  backdrop-filter:blur(20px);
  position:sticky;top:0;z-index:100;
}
.nn-logo{
  width:40px;height:40px;border-radius:10px;
  background:linear-gradient(135deg,var(--cyan),var(--violet));
  display:flex;align-items:center;justify-content:center;
  font-size:18px;font-weight:900;color:white;
  box-shadow:0 0 20px rgba(56,189,248,0.5);flex-shrink:0;
}
.nn-title{
  font-family:var(--font-hd);font-size:16px;font-weight:900;letter-spacing:.1em;
  background:linear-gradient(90deg,var(--cyan),var(--violet));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
}
.nn-sub{font-size:9px;color:var(--text-3);font-family:var(--font-mono);letter-spacing:.2em;margin-top:2px;}
.nn-badge{
  padding:3px 9px;border-radius:20px;font-size:10px;
  font-family:var(--font-mono);letter-spacing:.04em;border:1px solid;margin-left:4px;
}
.nn-badge-cyan{border-color:var(--cyan);color:var(--cyan);background:rgba(56,189,248,.07);}
.nn-badge-violet{border-color:var(--violet);color:var(--violet);background:rgba(129,140,248,.07);}
.nn-badge-green{border-color:var(--green);color:var(--green);background:rgba(52,211,153,.07);}

/* ── Sidebar inner labels ── */
.sidebar-label{
  font-family:var(--font-mono);font-size:9px;color:var(--text-3);
  letter-spacing:.2em;text-transform:uppercase;margin-bottom:6px;margin-top:2px;
}

/* ── Messages ── */
.msg-wrapper{animation:fadeSlideIn .28s ease;margin-bottom:14px;}
@keyframes fadeSlideIn{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
.msg-user{display:flex;justify-content:flex-end;}
.msg-user-bubble{
  max-width:74%;padding:11px 15px;
  background:linear-gradient(135deg,rgba(129,140,248,.22),rgba(56,189,248,.13));
  border:1px solid rgba(56,189,248,.28);border-radius:18px 18px 4px 18px;
  color:var(--text-1);font-size:14px;line-height:1.6;word-break:break-word;
}
.msg-ai{display:flex;gap:10px;align-items:flex-start;}
.msg-avatar{
  width:32px;height:32px;border-radius:8px;
  display:flex;align-items:center;justify-content:center;
  font-size:15px;flex-shrink:0;margin-top:2px;
}
.msg-agent-label{
  font-family:var(--font-mono);font-size:9px;letter-spacing:.15em;
  margin-bottom:4px;display:flex;align-items:center;gap:5px;
}
.msg-dot{width:5px;height:5px;border-radius:50%;display:inline-block;}
.msg-ai-bubble{
  background:var(--sky-card);border:1px solid var(--sky-border);
  border-radius:4px 16px 16px 16px;
  padding:13px 16px;font-size:14px;line-height:1.75;
  color:var(--text-1);flex:1;word-break:break-word;overflow-x:auto;
}
.msg-ai-bubble code{
  background:rgba(56,189,248,.09);padding:2px 6px;
  border-radius:4px;font-family:var(--font-mono);font-size:12px;color:var(--cyan);
}
.msg-ai-bubble pre{
  background:#020d1a;border:1px solid var(--sky-border);
  border-radius:8px;padding:13px;overflow-x:auto;margin:10px 0;
}
.msg-ai-bubble pre code{background:none;padding:0;color:var(--text-1);font-size:12px;}
.msg-ai-bubble table{border-collapse:collapse;width:100%;margin:10px 0;font-size:13px;}
.msg-ai-bubble th{
  padding:7px 11px;border-bottom:1px solid var(--sky-bright);
  color:var(--cyan);font-family:var(--font-mono);font-size:10px;text-align:left;
}
.msg-ai-bubble td{padding:7px 11px;border-bottom:1px solid var(--sky-border);color:var(--text-2);}
.msg-ai-bubble h1{color:white;font-size:17px;margin:12px 0 6px;}
.msg-ai-bubble h2{color:var(--cyan);font-size:15px;margin:12px 0 5px;}
.msg-ai-bubble h3{color:var(--violet);font-size:13px;margin:9px 0 4px;}
.msg-ai-bubble a{color:var(--cyan);}
.msg-ai-bubble blockquote{border-left:3px solid var(--violet);padding-left:12px;color:var(--text-2);margin:8px 0;}
.msg-ai-bubble ul,
.msg-ai-bubble ol{padding-left:20px;margin:6px 0;}
.msg-ai-bubble li{margin-bottom:3px;}
.msg-ai-bubble strong{color:white;}

.streaming-cursor{
  display:inline-block;width:2px;height:15px;background:var(--cyan);
  margin-left:3px;vertical-align:middle;animation:blink .7s infinite;
}
@keyframes blink{0%,100%{opacity:1}50%{opacity:0}}

/* ── Stat cards ── */
.stat-card{
  background:var(--sky-card);border:1px solid var(--sky-border);
  border-radius:10px;padding:12px 14px;border-left-width:3px;border-left-style:solid;
}
.stat-label{font-size:9px;color:var(--text-3);letter-spacing:.15em;margin-bottom:5px;}
.stat-value{font-size:20px;font-weight:700;font-family:var(--font-mono);}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"]{
  background:transparent !important;
  border-bottom:1px solid var(--sky-border) !important;gap:0 !important;
}
.stTabs [data-baseweb="tab"]{
  background:transparent !important;color:var(--text-3) !important;
  font-family:var(--font-body) !important;font-size:13px !important;
  padding:11px 22px !important;border:none !important;
  border-bottom:2px solid transparent !important;transition:all .15s !important;
}
.stTabs [aria-selected="true"]{
  color:var(--cyan) !important;
  border-bottom-color:var(--cyan) !important;background:transparent !important;
}
.stTabs [data-baseweb="tab-panel"]{padding-top:18px !important;}

/* ── Buttons ── */
.stButton>button{
  background:linear-gradient(135deg,rgba(56,189,248,.12),rgba(129,140,248,.12)) !important;
  border:1px solid var(--sky-border) !important;color:var(--text-1) !important;
  font-family:var(--font-body) !important;border-radius:8px !important;
  transition:all .15s !important;font-size:13px !important;
}
.stButton>button:hover{
  border-color:var(--cyan) !important;color:var(--cyan) !important;
  box-shadow:0 0 12px rgba(56,189,248,.2) !important;
}

/* ── Inputs ── */
.stSelectbox>div>div,
.stTextInput>div>div>input,
.stTextArea>div>div>textarea{
  background:var(--sky-panel) !important;
  border-color:var(--sky-border) !important;
  color:var(--text-1) !important;font-family:var(--font-body) !important;
}
.stFileUploader>div{
  background:var(--sky-panel) !important;
  border:2px dashed var(--sky-bright) !important;border-radius:10px !important;
}
.stFileUploader>div:hover{border-color:var(--cyan) !important;}

/* ── Chat input ── */
.stChatInput>div{
  background:var(--sky-panel) !important;
  border:1px solid var(--sky-border) !important;border-radius:12px !important;
}
.stChatInput>div:focus-within{border-color:var(--cyan) !important;}
.stChatInput input{color:var(--text-1) !important;font-family:var(--font-body) !important;}

/* ── Metric ── */
[data-testid="metric-container"]{
  background:var(--sky-card) !important;
  border:1px solid var(--sky-border) !important;
  border-radius:10px !important;padding:12px !important;
}
[data-testid="metric-container"] label{color:var(--text-3) !important;font-size:11px !important;}
[data-testid="metric-container"] [data-testid="stMetricValue"]{color:var(--cyan) !important;}

/* ── Success / Error / Warning ── */
.stSuccess{background:rgba(52,211,153,.1) !important;border:1px solid rgba(52,211,153,.3) !important;border-radius:8px !important;}
.stError{background:rgba(248,113,113,.1) !important;border:1px solid rgba(248,113,113,.3) !important;border-radius:8px !important;}
.stWarning{background:rgba(251,191,36,.1) !important;border:1px solid rgba(251,191,36,.3) !important;border-radius:8px !important;}
.stInfo{background:rgba(56,189,248,.1) !important;border:1px solid rgba(56,189,248,.3) !important;border-radius:8px !important;}

/* ── Dataframe ── */
[data-testid="stDataFrame"]{border:1px solid var(--sky-border) !important;border-radius:8px !important;}

hr{border-color:var(--sky-border) !important;}
#MainMenu,footer,header{visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# ── Imports ──────────────────────────────────────────────────────────────────
from agents import (GeneralChatbotAgent, CodeAgent, DocumentRAGAgent,
                    YouTubeRAGAgent, DeepResearcherAgent, DataAnalystAgent)
from orchestrator import route
import data_analysis as da

# ── Constants ─────────────────────────────────────────────────────────────────
AGENTS_META = {
    "auto":       {"name":"Auto Route",      "icon":"⚡","color":"#38bdf8","desc":"LangGraph Orchestrator"},
    "general":    {"name":"General Chatbot", "icon":"🤖","color":"#38bdf8","desc":"Gemini 2.5 Flash"},
    "code":       {"name":"Code Agent",      "icon":"💻","color":"#818cf8","desc":"Groq Llama 3.3 70B"},
    "document":   {"name":"Document RAG",    "icon":"📄","color":"#34d399","desc":"HuggingFace + FAISS"},
    "youtube":    {"name":"YouTube RAG",     "icon":"▶️","color":"#f472b6","desc":"Transcript + RAG"},
    "researcher": {"name":"Deep Researcher", "icon":"🔬","color":"#fbbf24","desc":"Web + Synthesis"},
    "data":       {"name":"Data Analyst",    "icon":"📊","color":"#34d399","desc":"Gemini/Groq + Tools"},
}

# ── Session init ──────────────────────────────────────────────────────────────
def init():
    if "chats" not in st.session_state:
        cid = str(uuid.uuid4())[:8]
        st.session_state.chats = {
            cid: {"title":"New Chat", "messages":[], "created":datetime.now()}
        }
        st.session_state.active_chat = cid
    if "agents" not in st.session_state:
        st.session_state.agents = {
            "general":    GeneralChatbotAgent(),
            "code":       CodeAgent(),
            "document":   DocumentRAGAgent(),
            "youtube":    YouTubeRAGAgent(),
            "researcher": DeepResearcherAgent(),
        }
    if "data_analyst" not in st.session_state:
        st.session_state.data_analyst = DataAnalystAgent()
    if "selected_agent" not in st.session_state:
        st.session_state.selected_agent = "auto"
    if "data_df"    not in st.session_state: st.session_state.data_df    = None
    if "data_eda"   not in st.session_state: st.session_state.data_eda   = None
    if "data_chat"  not in st.session_state: st.session_state.data_chat  = []
    if "last_agent" not in st.session_state: st.session_state.last_agent = None

init()

def active_msgs():
    return st.session_state.chats[st.session_state.active_chat]["messages"]

def add_msg(role, content, agent=None):
    active_msgs().append({"role":role,"content":content,"agent":agent})

def render_msg(msg):
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="msg-wrapper msg-user">
          <div class="msg-user-bubble">{msg["content"]}</div>
        </div>""", unsafe_allow_html=True)
    else:
        ak = msg.get("agent") or "general"
        if ak not in AGENTS_META: ak = "general"
        m = AGENTS_META[ak]
        st.markdown(f"""
        <div class="msg-wrapper msg-ai">
          <div class="msg-avatar" style="background:{m['color']}18;border:1px solid {m['color']}35;">
            {m['icon']}
          </div>
          <div style="flex:1;min-width:0;">
            <div class="msg-agent-label" style="color:{m['color']};">
              <span class="msg-dot" style="background:{m['color']};box-shadow:0 0 4px {m['color']};"></span>
              {m['name'].upper()} · {m['desc']}
            </div>
            <div class="msg-ai-bubble">{msg["content"]}</div>
          </div>
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:

    # Logo
    st.markdown("""
    <div style="padding:16px 4px 10px;text-align:center;">
      <div style="display:inline-flex;align-items:center;gap:10px;">
        <div style="width:34px;height:34px;border-radius:9px;
          background:linear-gradient(135deg,#38bdf8,#818cf8);
          display:flex;align-items:center;justify-content:center;
          font-size:17px;font-weight:900;color:white;
          box-shadow:0 0 14px rgba(56,189,248,0.5);">N</div>
        <div>
          <div style="font-family:'Orbitron',monospace;font-size:12px;font-weight:900;
            background:linear-gradient(90deg,#38bdf8,#818cf8);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;
            letter-spacing:.1em;">NEURALNEXUS</div>
          <div style="font-size:8px;color:#475569;letter-spacing:.15em;
            font-family:'JetBrains Mono',monospace;">AI PLATFORM v2</div>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

    st.divider()

    # ── Chat Sessions ─────────────────────────────────────────────────────────
    st.markdown('<div class="sidebar-label">💬 Chat Sessions</div>', unsafe_allow_html=True)

    if st.button("＋  New Chat", use_container_width=True, key="new_chat_btn"):
        cid = str(uuid.uuid4())[:8]
        n = len(st.session_state.chats) + 1
        st.session_state.chats[cid] = {
            "title": f"Chat {n}", "messages": [], "created": datetime.now()
        }
        st.session_state.active_chat = cid
        st.rerun()

    # List existing chats
    for cid, chat in list(st.session_state.chats.items()):
        is_active = cid == st.session_state.active_chat
        msgs      = chat["messages"]
        preview   = msgs[-1]["content"][:28] + "…" if msgs else "Empty chat"
        icon      = "●" if is_active else "○"

        c1, c2 = st.columns([5, 1])
        with c1:
            btn_style = "color:var(--cyan);" if is_active else ""
            if st.button(
                f"{icon}  {chat['title']}",
                key=f"chat_{cid}",
                use_container_width=True,
                help=preview,
            ):
                st.session_state.active_chat = cid
                st.rerun()
        with c2:
            if len(st.session_state.chats) > 1:
                if st.button("🗑", key=f"del_{cid}", help="Delete"):
                    del st.session_state.chats[cid]
                    if st.session_state.active_chat == cid:
                        st.session_state.active_chat = list(st.session_state.chats.keys())[0]
                    st.rerun()

    st.divider()

    # ── Agent Selector ────────────────────────────────────────────────────────
    st.markdown('<div class="sidebar-label">🤖 Agent</div>', unsafe_allow_html=True)

    opts   = list(AGENTS_META.keys())
    labels = [f"{AGENTS_META[a]['icon']} {AGENTS_META[a]['name']}" for a in opts]
    sel    = st.selectbox(
        "Agent",
        labels,
        index=opts.index(st.session_state.selected_agent),
        label_visibility="collapsed",
        key="agent_selector",
    )
    st.session_state.selected_agent = opts[labels.index(sel)]
    m = AGENTS_META[st.session_state.selected_agent]
    st.markdown(f"""
    <div style="font-size:10px;color:{m['color']};font-family:'JetBrains Mono',monospace;
      margin-top:4px;padding:5px 9px;background:{m['color']}0d;
      border-radius:6px;border:1px solid {m['color']}28;">
      {m['icon']} {m['desc']}
    </div>""", unsafe_allow_html=True)

    st.divider()

    # ── Document Upload ───────────────────────────────────────────────────────
    st.markdown('<div class="sidebar-label">📎 Document RAG</div>', unsafe_allow_html=True)
    doc_file = st.file_uploader(
        "Upload file", type=["pdf", "txt", "docx"],
        label_visibility="collapsed", key="doc_uploader"
    )
    if doc_file:
        with st.spinner("Indexing..."):
            try:
                msg = st.session_state.agents["document"].ingest(doc_file)
                st.success(msg)
            except Exception as e:
                st.error(f"❌ {e}")

    st.divider()

    # ── YouTube Loader ────────────────────────────────────────────────────────
    st.markdown('<div class="sidebar-label">▶️ YouTube RAG</div>', unsafe_allow_html=True)
    yt_url = st.text_input(
        "YouTube URL",
        placeholder="https://youtube.com/watch?v=...",
        label_visibility="collapsed",
        key="yt_url_input",
    )
    if st.button("Load Video", use_container_width=True, key="load_yt_btn"):
        if yt_url.strip():
            with st.spinner("Fetching transcript..."):
                try:
                    msg = st.session_state.agents["youtube"].ingest(yt_url.strip())
                    st.success(msg)
                except Exception as e:
                    st.error(f"❌ {e}")
        else:
            st.warning("Please enter a YouTube URL first.")

    st.divider()

    # ── Clear Chat ────────────────────────────────────────────────────────────
    if st.button("🧹  Clear Current Chat", use_container_width=True, key="clear_btn"):
        st.session_state.chats[st.session_state.active_chat]["messages"] = []
        st.rerun()

    # ── Current session info ──────────────────────────────────────────────────
    st.markdown(f"""
    <div style="margin-top:auto;padding:8px;
      background:rgba(56,189,248,.04);border:1px solid var(--sky-border);
      border-radius:8px;font-family:'JetBrains Mono',monospace;font-size:9px;
      color:var(--text-3);line-height:1.8;">
      Session: {st.session_state.active_chat}<br>
      Chats: {len(st.session_state.chats)}<br>
      Messages: {len(active_msgs())}
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="nn-header">
  <div class="nn-logo">N</div>
  <div>
    <div class="nn-title">NEURALNEXUS</div>
    <div class="nn-sub">MULTI-AGENT AI PLATFORM · LANGCHAIN + LANGGRAPH</div>
  </div>
  <div style="margin-left:auto;display:flex;gap:5px;align-items:center;flex-wrap:wrap;">
    <span class="nn-badge nn-badge-cyan">Gemini 2.5</span>
    <span class="nn-badge nn-badge-violet">Groq Llama</span>
    <span class="nn-badge nn-badge-green">HF Embed</span>
  </div>
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════════════
tab_chat, tab_data = st.tabs(["◈  Multi-Agent Chat", "◇  Data Analysis + AI"])

# ──────────────────────────────────────────────────────────────────────────────
# TAB 1 — CHAT
# ──────────────────────────────────────────────────────────────────────────────
with tab_chat:
    messages = active_msgs()

    if not messages:
        st.markdown("""
        <div style="text-align:center;padding:44px 20px;">
          <div style="font-size:46px;margin-bottom:14px;">🌌</div>
          <div style="font-family:'Orbitron',monospace;font-size:18px;font-weight:700;
            background:linear-gradient(90deg,#38bdf8,#818cf8);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:8px;">
            Welcome to NeuralNexus
          </div>
          <div style="color:#94a3b8;font-size:13px;max-width:500px;margin:0 auto;line-height:1.8;">
            5 specialized AI agents auto-routed by <strong style="color:#38bdf8;">LangGraph</strong>.<br>
            Select an agent in the sidebar or let <strong style="color:#38bdf8;">Auto Route</strong> decide.
          </div>
          <div style="display:flex;justify-content:center;gap:8px;flex-wrap:wrap;margin-top:22px;">
            <span style="padding:5px 13px;border-radius:20px;font-size:11px;border:1px solid #38bdf830;color:#38bdf8;background:#38bdf810;">🤖 General</span>
            <span style="padding:5px 13px;border-radius:20px;font-size:11px;border:1px solid #818cf830;color:#818cf8;background:#818cf810;">💻 Code</span>
            <span style="padding:5px 13px;border-radius:20px;font-size:11px;border:1px solid #34d39930;color:#34d399;background:#34d39910;">📄 Document RAG</span>
            <span style="padding:5px 13px;border-radius:20px;font-size:11px;border:1px solid #f472b630;color:#f472b6;background:#f472b610;">▶️ YouTube RAG</span>
            <span style="padding:5px 13px;border-radius:20px;font-size:11px;border:1px solid #fbbf2430;color:#fbbf24;background:#fbbf2410;">🔬 Deep Research</span>
          </div>
        </div>""", unsafe_allow_html=True)

    # Render all messages
    for msg in messages:
        render_msg(msg)

    # Chat input
    sel = st.session_state.selected_agent
    ph  = (
        f"Message {AGENTS_META[sel]['name']}..."
        if sel != "auto"
        else "Ask anything — auto-routed to the best agent..."
    )

    if prompt := st.chat_input(ph, key="main_chat_input"):
        add_msg("user", prompt)

        # Auto-title chat from first message
        chat = st.session_state.chats[st.session_state.active_chat]
        if len(chat["messages"]) == 1:
            chat["title"] = prompt[:22] + ("…" if len(prompt) > 22 else "")

        # Route
        agent_key = route(prompt, sel if sel != "auto" else None)
        st.session_state.last_agent = agent_key
        agent = st.session_state.agents.get(agent_key)

        if agent is None:
            agent = st.session_state.agents["general"]
            agent_key = "general"

        m       = AGENTS_META[agent_key]
        history = [{"role":h["role"],"content":h["content"]} for h in active_msgs()[:-1]]

        # Stream response
        with st.spinner(f"{m['icon']} {m['name']} thinking..."):
            ph_el = st.empty()
            full  = ""
            for chunk in agent.stream(prompt, history):
                full += chunk
                ph_el.markdown(f"""
                <div class="msg-wrapper msg-ai">
                  <div class="msg-avatar" style="background:{m['color']}18;border:1px solid {m['color']}35;">
                    {m['icon']}
                  </div>
                  <div style="flex:1;min-width:0;">
                    <div class="msg-agent-label" style="color:{m['color']};">
                      <span class="msg-dot" style="background:{m['color']};box-shadow:0 0 4px {m['color']};"></span>
                      {m['name'].upper()} · Streaming...
                    </div>
                    <div class="msg-ai-bubble">{full}<span class="streaming-cursor"></span></div>
                  </div>
                </div>""", unsafe_allow_html=True)
            ph_el.empty()

        add_msg("assistant", full, agent_key)
        st.rerun()

    # Status bar
    if st.session_state.last_agent:
        m = AGENTS_META[st.session_state.last_agent]
        st.markdown(f"""
        <div style="font-family:'JetBrains Mono',monospace;font-size:9px;
          color:{m['color']};text-align:center;padding:5px;
          border-top:1px solid #1a3a60;margin-top:2px;opacity:0.8;">
          ⚡ Last agent → {m['icon']} {m['name']} &nbsp;·&nbsp;
          Session: {st.session_state.active_chat} &nbsp;·&nbsp;
          {len(active_msgs())} messages
        </div>""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# TAB 2 — DATA ANALYSIS
# ──────────────────────────────────────────────────────────────────────────────
with tab_data:
    st.markdown("""
    <div style="font-family:'Orbitron',monospace;font-size:10px;color:#38bdf8;
      letter-spacing:.12em;margin-bottom:14px;">
      ◇ DATA ANALYSIS · EDA, VISUALIZATION &amp; AI CHAT
    </div>""", unsafe_allow_html=True)

    data_file = st.file_uploader(
        "Upload CSV / TSV / XLSX", type=["csv","tsv","xlsx"],
        key="data_uploader"
    )
    if data_file:
        with st.spinner("Parsing dataset..."):
            try:
                st.session_state.data_df  = da.load_df(data_file)
                st.session_state.data_eda = da.get_eda(st.session_state.data_df)
                st.session_state.data_chat = []
                st.success(
                    f"✅ **{data_file.name}** — "
                    f"{st.session_state.data_df.shape[0]:,} rows × "
                    f"{st.session_state.data_df.shape[1]} columns"
                )
            except Exception as e:
                st.error(f"Failed to load: {e}")

    df  = st.session_state.data_df
    eda = st.session_state.data_eda

    if df is None:
        st.markdown("""
        <div style="text-align:center;padding:56px 20px;color:#475569;">
          <div style="font-size:56px;margin-bottom:14px;opacity:.25;">◇</div>
          <div style="font-family:'Orbitron',monospace;font-size:13px;letter-spacing:.1em;">
            NO DATASET LOADED
          </div>
          <div style="font-size:12px;margin-top:8px;">
            Upload a CSV, TSV, or Excel file above to begin
          </div>
        </div>""", unsafe_allow_html=True)
    else:
        # Stat cards
        c1,c2,c3,c4,c5 = st.columns(5)
        for col, lbl, val, color in [
            (c1, "ROWS",       f"{df.shape[0]:,}",             "#38bdf8"),
            (c2, "COLUMNS",    str(df.shape[1]),                "#818cf8"),
            (c3, "NUMERIC",    str(len(eda["num_cols"])),       "#34d399"),
            (c4, "MISSING",    str(sum(eda["nulls"].values())), "#fbbf24"),
            (c5, "DUPLICATES", str(eda["duplicates"]),          "#f472b6"),
        ]:
            with col:
                st.markdown(f"""
                <div class="stat-card" style="border-left-color:{color};">
                  <div class="stat-label">{lbl}</div>
                  <div class="stat-value" style="color:{color};">{val}</div>
                </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        dtab1, dtab2, dtab3, dtab4 = st.tabs([
            "📋 Preview", "📈 EDA Stats", "🎨 Visualize", "🤖 AI Data Chat"
        ])

        with dtab1:
            st.caption(f"Showing first 50 of {df.shape[0]:,} rows · Memory: {eda['memory']}")
            st.dataframe(df.head(50), use_container_width=True, height=400)

        with dtab2:
            ca, cb = st.columns(2)
            with ca:
                st.markdown("**Null Values per Column**")
                nulls = (df.isnull().sum().reset_index()
                         .rename(columns={"index":"Column", 0:"Nulls"})
                         .sort_values("Nulls", ascending=False))
                st.dataframe(nulls, use_container_width=True, height=260)
            with cb:
                st.markdown("**Column Data Types**")
                dtypes = df.dtypes.reset_index().rename(columns={"index":"Column", 0:"Type"})
                dtypes["Type"] = dtypes["Type"].astype(str)
                st.dataframe(dtypes, use_container_width=True, height=260)
            if eda["corr"] is not None:
                st.markdown("**Correlation Matrix**")
                st.dataframe(eda["corr"], use_container_width=True, height=240)
            st.markdown("**Descriptive Statistics**")
            st.dataframe(df.describe(include="all").fillna(""), use_container_width=True, height=240)

        with dtab3:
            all_cols = df.columns.tolist()
            num_cols = eda["num_cols"]
            cat_cols = eda["cat_cols"]
            PLOTS = ["Histogram","Scatter","Box Plot","Correlation Heatmap",
                     "Bar Chart","Line Chart","Violin","Pairplot"]
            vc1, vc2, vc3, vc4 = st.columns([2,2,2,1])
            with vc1: pt = st.selectbox("Plot Type", PLOTS, key="plot_type_sel")
            with vc2:
                xc = st.selectbox("X Axis", ["—"]+all_cols, key="x_col_sel") \
                     if pt not in ["Box Plot","Violin","Correlation Heatmap","Pairplot"] else "—"
            with vc3:
                yc = st.selectbox("Y Axis", ["—"]+num_cols, key="y_col_sel") \
                     if pt in ["Scatter","Bar Chart","Line Chart"] else "—"
            with vc4:
                hc = st.selectbox("Color By", ["—"]+cat_cols, key="hue_col_sel") \
                     if pt == "Scatter" else "—"

            if st.button("◇  Generate Plot", key="gen_plot_btn"):
                with st.spinner("Rendering visualization..."):
                    try:
                        img = da.make_plot(
                            df, pt,
                            x_col=xc if xc != "—" else None,
                            y_col=yc if yc != "—" else None,
                            hue_col=hc if hc != "—" else None,
                        )
                        st.image(img, use_column_width=True)
                    except Exception as e:
                        st.error(f"Plot error: {e}")

        with dtab4:
            st.markdown("""
            <div style="background:rgba(56,189,248,.05);border:1px solid rgba(56,189,248,.2);
              border-radius:10px;padding:11px 15px;margin-bottom:14px;font-size:12px;color:#94a3b8;line-height:1.7;">
              💡 <strong style="color:#38bdf8;">AI Data Chat</strong> —
              Ask anything about your dataset. Request visualizations, statistics, or insights.<br>
              <em>Try: "Show histogram of Age" · "What are the top correlations?" · "Plot salary vs experience"</em>
            </div>""", unsafe_allow_html=True)

            # Render data chat history
            for msg in st.session_state.data_chat:
                if msg["role"] == "user":
                    st.markdown(f"""
                    <div class="msg-wrapper msg-user">
                      <div class="msg-user-bubble">{msg["content"]}</div>
                    </div>""", unsafe_allow_html=True)
                else:
                    if msg.get("type") == "plot":
                        st.image(msg["content"], use_column_width=True)
                    else:
                        st.markdown(f"""
                        <div class="msg-wrapper msg-ai">
                          <div class="msg-avatar" style="background:#34d39918;border:1px solid #34d39935;">📊</div>
                          <div style="flex:1;min-width:0;">
                            <div class="msg-agent-label" style="color:#34d399;">
                              <span class="msg-dot" style="background:#34d399;box-shadow:0 0 4px #34d399;"></span>
                              DATA ANALYST · Gemini/Groq + Tools
                            </div>
                            <div class="msg-ai-bubble">{msg["content"]}</div>
                          </div>
                        </div>""", unsafe_allow_html=True)

            if data_prompt := st.chat_input(
                "Ask about your data... e.g. 'show histogram of age'",
                key="data_chat_input"
            ):
                st.session_state.data_chat.append({"role":"user","content":data_prompt})
                analyst = st.session_state.data_analyst
                data_history = [
                    {"role":m["role"], "content":m["content"] if m.get("type") != "plot" else "[chart]"}
                    for m in st.session_state.data_chat[:-1]
                ]

                with st.spinner("📊 Analyzing..."):
                    full_text      = ""
                    plot_generated = False
                    ph_plot        = st.empty()

                    for chunk in analyst.stream_with_data(data_prompt, data_history, df, eda):
                        if isinstance(chunk, dict) and chunk.get("tool") == "plot":
                            try:
                                img_bytes = da.make_plot(
                                    df,
                                    plot_type=chunk.get("type", "histogram"),
                                    x_col=chunk.get("x"),
                                    y_col=chunk.get("y"),
                                    hue_col=chunk.get("hue"),
                                    title=chunk.get("title"),
                                )
                                st.session_state.data_chat.append({
                                    "role":"assistant","content":img_bytes,"type":"plot"
                                })
                                ph_plot.image(img_bytes, use_column_width=True)
                                plot_generated = True
                            except Exception as e:
                                full_text = f"❌ Plot error: {e}"
                        else:
                            full_text += chunk

                    if full_text and not plot_generated:
                        st.session_state.data_chat.append({
                            "role":"assistant","content":full_text,"type":"text"
                        })

                st.rerun()
