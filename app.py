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

# ── Sky Theme CSS ───────────────────────────────────────────────────────────────
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
.stApp { background:var(--sky-void) !important; font-family:var(--font-body); }
[data-testid="stSidebar"] {
  background:linear-gradient(180deg,#060f1e 0%,#08162b 100%) !important;
  border-right:1px solid var(--sky-border) !important;
}
[data-testid="stSidebar"]>div { padding-top:0 !important; }
::-webkit-scrollbar{width:5px;height:5px}
::-webkit-scrollbar-track{background:var(--sky-deep)}
::-webkit-scrollbar-thumb{background:var(--sky-bright);border-radius:3px}

.nn-header{background:linear-gradient(135deg,rgba(6,17,31,0.95),rgba(10,28,53,0.95));
  border-bottom:1px solid var(--sky-border);padding:14px 24px;
  display:flex;align-items:center;gap:14px;
  margin:-1rem -1rem 1.5rem -1rem;backdrop-filter:blur(20px);}
.nn-logo{width:42px;height:42px;border-radius:10px;
  background:linear-gradient(135deg,var(--cyan),var(--violet));
  display:flex;align-items:center;justify-content:center;
  font-size:20px;font-weight:900;color:white;
  box-shadow:0 0 20px rgba(56,189,248,0.5);flex-shrink:0;}
.nn-title{font-family:var(--font-hd);font-size:18px;font-weight:900;letter-spacing:.1em;
  background:linear-gradient(90deg,var(--cyan),var(--violet));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;}
.nn-sub{font-size:10px;color:var(--text-3);font-family:var(--font-mono);
  letter-spacing:.2em;margin-top:2px;}
.nn-badge{padding:3px 10px;border-radius:20px;font-size:10px;
  font-family:var(--font-mono);letter-spacing:.05em;border:1px solid;margin-left:4px;}
.nn-badge-cyan{border-color:var(--cyan);color:var(--cyan);background:rgba(56,189,248,.07);}
.nn-badge-violet{border-color:var(--violet);color:var(--violet);background:rgba(129,140,248,.07);}

.sidebar-label{font-family:var(--font-mono);font-size:9px;color:var(--text-3);
  letter-spacing:.2em;text-transform:uppercase;margin-bottom:8px;}

.msg-wrapper{animation:fadeSlideIn .3s ease;margin-bottom:16px;}
@keyframes fadeSlideIn{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}
.msg-user{display:flex;justify-content:flex-end;}
.msg-user-bubble{max-width:72%;padding:12px 16px;
  background:linear-gradient(135deg,rgba(129,140,248,.2),rgba(56,189,248,.12));
  border:1px solid rgba(56,189,248,.25);border-radius:18px 18px 4px 18px;
  color:var(--text-1);font-size:14px;line-height:1.6;}
.msg-ai{display:flex;gap:12px;align-items:flex-start;}
.msg-avatar{width:34px;height:34px;border-radius:9px;display:flex;
  align-items:center;justify-content:center;font-size:16px;flex-shrink:0;margin-top:2px;}
.msg-agent-label{font-family:var(--font-mono);font-size:9px;letter-spacing:.15em;
  margin-bottom:5px;display:flex;align-items:center;gap:5px;}
.msg-dot{width:5px;height:5px;border-radius:50%;display:inline-block;}
.msg-ai-bubble{background:var(--sky-card);border:1px solid var(--sky-border);
  border-radius:4px 18px 18px 18px;padding:14px 18px;font-size:14px;
  line-height:1.75;color:var(--text-1);flex:1;}
.msg-ai-bubble code{background:rgba(56,189,248,.08);padding:2px 6px;
  border-radius:4px;font-family:var(--font-mono);font-size:12px;color:var(--cyan);}
.msg-ai-bubble pre{background:#020d1a;border:1px solid var(--sky-border);
  border-radius:8px;padding:14px;overflow-x:auto;margin:10px 0;}
.msg-ai-bubble pre code{background:none;padding:0;color:var(--text-1);}
.msg-ai-bubble table{border-collapse:collapse;width:100%;margin:10px 0;}
.msg-ai-bubble th{padding:8px 12px;border-bottom:1px solid var(--sky-bright);
  color:var(--cyan);font-family:var(--font-mono);font-size:11px;text-align:left;}
.msg-ai-bubble td{padding:8px 12px;border-bottom:1px solid var(--sky-border);color:var(--text-2);}
.msg-ai-bubble h2{color:var(--cyan);font-size:15px;margin:14px 0 6px;}
.msg-ai-bubble h3{color:var(--violet);font-size:13px;margin:10px 0 4px;}
.msg-ai-bubble a{color:var(--cyan);}
.msg-ai-bubble blockquote{border-left:3px solid var(--violet);
  padding-left:12px;color:var(--text-2);margin:8px 0;}
.streaming-cursor{display:inline-block;width:2px;height:16px;background:var(--cyan);
  margin-left:3px;vertical-align:middle;animation:blink .7s infinite;}
@keyframes blink{0%,100%{opacity:1}50%{opacity:0}}

.stat-card{background:var(--sky-card);border:1px solid var(--sky-border);
  border-radius:10px;padding:14px 16px;border-left-width:3px;border-left-style:solid;}
.stat-label{font-size:9px;color:var(--text-3);letter-spacing:.15em;margin-bottom:6px;}
.stat-value{font-size:22px;font-weight:700;font-family:var(--font-mono);}

.stTabs [data-baseweb="tab-list"]{background:transparent !important;
  border-bottom:1px solid var(--sky-border) !important;gap:0 !important;}
.stTabs [data-baseweb="tab"]{background:transparent !important;color:var(--text-3) !important;
  font-family:var(--font-body) !important;font-size:13px !important;
  padding:12px 24px !important;border:none !important;
  border-bottom:2px solid transparent !important;}
.stTabs [aria-selected="true"]{color:var(--cyan) !important;
  border-bottom-color:var(--cyan) !important;background:transparent !important;}
.stTabs [data-baseweb="tab-panel"]{padding-top:20px !important;}

.stButton>button{background:linear-gradient(135deg,rgba(56,189,248,.15),rgba(129,140,248,.15)) !important;
  border:1px solid var(--sky-border) !important;color:var(--text-1) !important;
  font-family:var(--font-body) !important;border-radius:8px !important;transition:all .15s !important;}
.stButton>button:hover{border-color:var(--cyan) !important;color:var(--cyan) !important;
  box-shadow:0 0 12px rgba(56,189,248,.2) !important;}

.stSelectbox>div>div,.stTextInput>div>div>input,.stTextArea>div>div>textarea{
  background:var(--sky-panel) !important;border-color:var(--sky-border) !important;
  color:var(--text-1) !important;font-family:var(--font-body) !important;}
.stFileUploader>div{background:var(--sky-panel) !important;
  border:2px dashed var(--sky-bright) !important;border-radius:10px !important;}
.stChatInput>div{background:var(--sky-panel) !important;
  border:1px solid var(--sky-border) !important;border-radius:12px !important;}
.stChatInput input{color:var(--text-1) !important;}
[data-testid="metric-container"]{background:var(--sky-card) !important;
  border:1px solid var(--sky-border) !important;border-radius:10px !important;padding:14px !important;}
[data-testid="metric-container"] label{color:var(--text-3) !important;font-size:11px !important;}
[data-testid="metric-container"] [data-testid="stMetricValue"]{color:var(--cyan) !important;}
hr{border-color:var(--sky-border) !important;}
#MainMenu,footer,header{visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# ── Imports ────────────────────────────────────────────────────────────────────
from agents import (GeneralChatbotAgent, CodeAgent, DocumentRAGAgent,
                    YouTubeRAGAgent, DeepResearcherAgent, DataAnalystAgent)
from orchestrator import route
import data_analysis as da

# ── Constants ───────────────────────────────────────────────────────────────────
AGENTS_META = {
    "auto":       {"name":"Auto Route",      "icon":"⚡","color":"#38bdf8","desc":"LangGraph Orchestrator"},
    "general":    {"name":"General Chatbot", "icon":"🤖","color":"#38bdf8","desc":"Gemini 2.5 Flash"},
    "code":       {"name":"Code Agent",      "icon":"💻","color":"#818cf8","desc":"Groq Llama 3.3 70B"},
    "document":   {"name":"Document RAG",    "icon":"📄","color":"#34d399","desc":"HuggingFace + FAISS"},
    "youtube":    {"name":"YouTube RAG",     "icon":"▶️","color":"#f472b6","desc":"Transcript + RAG"},
    "researcher": {"name":"Deep Researcher", "icon":"🔬","color":"#fbbf24","desc":"Web + Synthesis"},
}

# ── Session init ────────────────────────────────────────────────────────────────
def init():
    if "chats" not in st.session_state:
        cid = str(uuid.uuid4())[:8]
        st.session_state.chats = {
            cid: {"title": "Chat 1", "messages": [], "created": datetime.now()}
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
    if "data_df" not in st.session_state:
        st.session_state.data_df = None
    if "data_eda" not in st.session_state:
        st.session_state.data_eda = None
    if "data_chat" not in st.session_state:
        st.session_state.data_chat = []
    if "last_agent" not in st.session_state:
        st.session_state.last_agent = None

init()

def active_msgs():
    return st.session_state.chats[st.session_state.active_chat]["messages"]

def add_msg(role, content, agent=None):
    active_msgs().append({"role": role, "content": content, "agent": agent})

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

# ── Sidebar ─────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:18px 4px 12px;text-align:center;">
      <div style="display:inline-flex;align-items:center;gap:10px;">
        <div style="width:36px;height:36px;border-radius:9px;
          background:linear-gradient(135deg,#38bdf8,#818cf8);
          display:flex;align-items:center;justify-content:center;
          font-size:18px;font-weight:900;color:white;
          box-shadow:0 0 16px rgba(56,189,248,0.5);">N</div>
        <div>
          <div style="font-family:'Orbitron',monospace;font-size:13px;font-weight:900;
            background:linear-gradient(90deg,#38bdf8,#818cf8);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;
            letter-spacing:.1em;">NEURALNEXUS</div>
          <div style="font-size:9px;color:#475569;letter-spacing:.15em;
            font-family:'JetBrains Mono',monospace;">AI PLATFORM</div>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

    st.divider()

    # Chat sessions
    st.markdown('<div class="sidebar-label">💬 CHAT SESSIONS</div>', unsafe_allow_html=True)
    if st.button("＋  New Chat", use_container_width=True):
        cid = str(uuid.uuid4())[:8]
        n = len(st.session_state.chats) + 1
        st.session_state.chats[cid] = {"title": f"Chat {n}", "messages": [], "created": datetime.now()}
        st.session_state.active_chat = cid
        st.rerun()

    for cid, chat in list(st.session_state.chats.items()):
        is_active = cid == st.session_state.active_chat
        msgs = chat["messages"]
        preview = msgs[-1]["content"][:30] + "…" if msgs else "Empty"
        c1, c2 = st.columns([5, 1])
        with c1:
            label = f"{'●' if is_active else '○'}  {chat['title']}"
            if st.button(label, key=f"chat_{cid}", use_container_width=True, help=preview):
                st.session_state.active_chat = cid
                st.rerun()
        with c2:
            if len(st.session_state.chats) > 1:
                if st.button("🗑", key=f"del_{cid}"):
                    del st.session_state.chats[cid]
                    if st.session_state.active_chat == cid:
                        st.session_state.active_chat = list(st.session_state.chats.keys())[0]
                    st.rerun()

    st.divider()

    # Agent selector
    st.markdown('<div class="sidebar-label">🤖 AGENT</div>', unsafe_allow_html=True)
    opts   = list(AGENTS_META.keys())
    labels = [f"{AGENTS_META[a]['icon']} {AGENTS_META[a]['name']}" for a in opts]
    sel    = st.selectbox("Agent", labels,
                           index=opts.index(st.session_state.selected_agent),
                           label_visibility="collapsed")
    st.session_state.selected_agent = opts[labels.index(sel)]
    m = AGENTS_META[st.session_state.selected_agent]
    st.markdown(f"""
    <div style="font-size:10px;color:{m['color']};font-family:'JetBrains Mono',monospace;
      margin-top:4px;padding:4px 8px;background:rgba(56,189,248,.05);
      border-radius:6px;border:1px solid {m['color']}30;">
      {m['icon']} {m['desc']}
    </div>""", unsafe_allow_html=True)

    st.divider()

    # Document upload
    st.markdown('<div class="sidebar-label">📎 DOCUMENT RAG</div>', unsafe_allow_html=True)
    doc_file = st.file_uploader("Upload PDF / TXT / DOCX", type=["pdf","txt","docx"],
                                 label_visibility="collapsed")
    if doc_file:
        with st.spinner("Indexing..."):
            msg = st.session_state.agents["document"].ingest(doc_file)
        st.success(msg)

    st.divider()

    # YouTube loader
    st.markdown('<div class="sidebar-label">▶️ YOUTUBE RAG</div>', unsafe_allow_html=True)
    yt_url = st.text_input("YouTube URL", placeholder="https://youtube.com/watch?v=...",
                            label_visibility="collapsed")
    if st.button("Load Video", use_container_width=True) and yt_url.strip():
        with st.spinner("Fetching transcript (trying 3 methods)..."):
            try:
                msg = st.session_state.agents["youtube"].ingest(yt_url.strip())
                st.success(msg)
            except Exception as e:
                st.error(f"❌ All transcript methods failed:\n{e}")

    st.divider()
    if st.button("🧹  Clear Chat", use_container_width=True):
        st.session_state.chats[st.session_state.active_chat]["messages"] = []
        st.rerun()

# ── Header ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="nn-header">
  <div class="nn-logo">N</div>
  <div>
    <div class="nn-title">NEURALNEXUS</div>
    <div class="nn-sub">MULTI-AGENT AI PLATFORM · LANGCHAIN + LANGGRAPH</div>
  </div>
  <div style="margin-left:auto;display:flex;gap:6px;align-items:center;">
    <span class="nn-badge nn-badge-cyan">Gemini 2.5 Flash</span>
    <span class="nn-badge nn-badge-violet">Groq Llama 3.3</span>
    <span class="nn-badge" style="border-color:#34d399;color:#34d399;background:rgba(52,211,153,.07);">HF Embeddings</span>
  </div>
</div>""", unsafe_allow_html=True)

# ── Tabs ─────────────────────────────────────────────────────────────────────────
tab_chat, tab_data = st.tabs(["◈  Multi-Agent Chat", "◇  Data Analysis + AI Chat"])

# ══════════════════════════════════════
# TAB 1 — MULTI-AGENT CHAT
# ══════════════════════════════════════
with tab_chat:
    messages = active_msgs()

    if not messages:
        st.markdown("""
        <div style="text-align:center;padding:48px 20px;">
          <div style="font-size:48px;margin-bottom:16px;">🌌</div>
          <div style="font-family:'Orbitron',monospace;font-size:20px;font-weight:700;
            background:linear-gradient(90deg,#38bdf8,#818cf8);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:8px;">
            Welcome to NeuralNexus
          </div>
          <div style="color:#94a3b8;font-size:13px;max-width:480px;margin:0 auto;line-height:1.7;">
            5 specialized AI agents, auto-routed by LangGraph.<br>
            Select an agent in the sidebar or let <strong style="color:#38bdf8;">Auto Route</strong> decide.
          </div>
        </div>""", unsafe_allow_html=True)

    for msg in messages:
        render_msg(msg)

    sel = st.session_state.selected_agent
    ph  = (f"Message {AGENTS_META[sel]['name']}..."
           if sel != "auto" else "Message NeuralNexus... (auto-routes to best agent)")

    if prompt := st.chat_input(ph):
        add_msg("user", prompt)
        chat = st.session_state.chats[st.session_state.active_chat]
        if len(chat["messages"]) == 1:
            chat["title"] = prompt[:22] + ("…" if len(prompt) > 22 else "")

        agent_key = route(prompt, sel if sel != "auto" else None)
        st.session_state.last_agent = agent_key
        agent = st.session_state.agents[agent_key]
        m     = AGENTS_META[agent_key]
        history = [{"role":h["role"],"content":h["content"]} for h in active_msgs()[:-1]]

        with st.spinner(f"{m['icon']} {m['name']} is thinking..."):
            placeholder = st.empty()
            full = ""
            for chunk in agent.stream(prompt, history):
                full += chunk
                placeholder.markdown(f"""
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
            placeholder.empty()

        add_msg("assistant", full, agent_key)
        st.rerun()

    if st.session_state.last_agent:
        m = AGENTS_META[st.session_state.last_agent]
        st.markdown(f"""
        <div style="font-family:'JetBrains Mono',monospace;font-size:10px;color:{m['color']};
          text-align:center;padding:6px;border-top:1px solid #1a3a60;margin-top:4px;">
          ENTER to send · Last agent → {m['icon']} {m['name']} · Session: {st.session_state.active_chat}
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════
# TAB 2 — DATA ANALYSIS + AI CHAT
# ══════════════════════════════════════
with tab_data:
    st.markdown("""
    <div style="font-family:'Orbitron',monospace;font-size:11px;color:#38bdf8;
      letter-spacing:.12em;margin-bottom:16px;">
      ◇ DATA ANALYSIS · EDA, VISUALIZATION &amp; AI CHAT
    </div>""", unsafe_allow_html=True)

    # Upload
    data_file = st.file_uploader("Upload CSV / TSV / XLSX", type=["csv","tsv","xlsx"], key="du")
    if data_file:
        with st.spinner("Parsing dataset..."):
            try:
                st.session_state.data_df  = da.load_df(data_file)
                st.session_state.data_eda = da.get_eda(st.session_state.data_df)
                st.session_state.data_chat = []
                st.success(f"✅ **{data_file.name}** — "
                           f"{st.session_state.data_df.shape[0]:,} rows × "
                           f"{st.session_state.data_df.shape[1]} columns")
            except Exception as e:
                st.error(f"Failed: {e}")

    df  = st.session_state.data_df
    eda = st.session_state.data_eda

    if df is None:
        st.markdown("""
        <div style="text-align:center;padding:60px 20px;color:#475569;">
          <div style="font-size:60px;margin-bottom:16px;opacity:.3;">◇</div>
          <div style="font-family:'Orbitron',monospace;font-size:14px;letter-spacing:.1em;">
            NO DATASET LOADED
          </div>
          <div style="font-size:12px;margin-top:8px;">Upload a CSV, TSV, or Excel file above</div>
        </div>""", unsafe_allow_html=True)
    else:
        # Stat cards
        c1,c2,c3,c4,c5 = st.columns(5)
        for col, lbl, val, color in [
            (c1,"ROWS",       f"{df.shape[0]:,}",              "#38bdf8"),
            (c2,"COLUMNS",    str(df.shape[1]),                 "#818cf8"),
            (c3,"NUMERIC",    str(len(eda["num_cols"])),        "#34d399"),
            (c4,"MISSING",    str(sum(eda["nulls"].values())),  "#fbbf24"),
            (c5,"DUPLICATES", str(eda["duplicates"]),           "#f472b6"),
        ]:
            with col:
                st.markdown(f"""
                <div class="stat-card" style="border-left-color:{color};">
                  <div class="stat-label">{lbl}</div>
                  <div class="stat-value" style="color:{color};">{val}</div>
                </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Sub-tabs
        dtab1, dtab2, dtab3, dtab4 = st.tabs([
            "📋 Preview", "📈 EDA Stats", "🎨 Visualize", "🤖 AI Data Chat"
        ])

        with dtab1:
            st.caption(f"First 50 of {df.shape[0]:,} rows · Memory: {eda['memory']}")
            st.dataframe(df.head(50), use_container_width=True, height=400)

        with dtab2:
            ca, cb = st.columns(2)
            with ca:
                st.markdown("**Null Values**")
                nulls = (df.isnull().sum().reset_index()
                         .rename(columns={"index":"Column",0:"Nulls"})
                         .sort_values("Nulls", ascending=False))
                st.dataframe(nulls, use_container_width=True, height=260)
            with cb:
                st.markdown("**Data Types**")
                dtypes = df.dtypes.reset_index().rename(columns={"index":"Column",0:"Type"})
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
            vc1,vc2,vc3,vc4 = st.columns([2,2,2,1])
            with vc1: pt = st.selectbox("Plot Type", PLOTS)
            with vc2:
                xc = st.selectbox("X Axis", ["—"]+all_cols) if pt not in ["Box Plot","Violin","Correlation Heatmap","Pairplot"] else "—"
            with vc3:
                yc = st.selectbox("Y Axis", ["—"]+num_cols) if pt in ["Scatter","Bar Chart","Line Chart"] else "—"
            with vc4:
                hc = st.selectbox("Color By", ["—"]+cat_cols) if pt=="Scatter" else "—"
            if st.button("◇  Generate Plot"):
                with st.spinner("Rendering..."):
                    try:
                        img = da.make_plot(df, pt,
                                           x_col=xc if xc!="—" else None,
                                           y_col=yc if yc!="—" else None,
                                           hue_col=hc if hc!="—" else None)
                        st.image(img, use_column_width=True)
                    except Exception as e:
                        st.error(f"Plot error: {e}")

        # ── AI DATA CHAT ────────────────────────────────────────────────────────
        with dtab4:
            st.markdown("""
            <div style="background:rgba(56,189,248,.05);border:1px solid rgba(56,189,248,.2);
              border-radius:10px;padding:12px 16px;margin-bottom:16px;font-size:13px;color:#94a3b8;">
              💡 <strong style="color:#38bdf8;">AI Data Chat</strong> — Ask anything about your dataset.
              Request visualizations, statistics, correlations, or insights. The AI will auto-generate plots when needed.
              <br><br>
              Examples: <em>"Show me a histogram of Age"</em> · <em>"What are the top correlations?"</em> ·
              <em>"Plot salary vs experience"</em> · <em>"Which columns have the most missing values?"</em>
            </div>""", unsafe_allow_html=True)

            # Render data chat history
            for msg in st.session_state.data_chat:
                if msg["role"] == "user":
                    st.markdown(f"""
                    <div class="msg-wrapper msg-user">
                      <div class="msg-user-bubble">{msg["content"]}</div>
                    </div>""", unsafe_allow_html=True)
                else:
                    content = msg["content"]
                    if msg.get("type") == "plot":
                        st.image(content, use_column_width=True)
                    else:
                        st.markdown(f"""
                        <div class="msg-wrapper msg-ai">
                          <div class="msg-avatar" style="background:#34d39918;border:1px solid #34d39935;">📊</div>
                          <div style="flex:1;min-width:0;">
                            <div class="msg-agent-label" style="color:#34d399;">
                              <span class="msg-dot" style="background:#34d399;box-shadow:0 0 4px #34d399;"></span>
                              DATA ANALYST · HuggingFace + Gemini/Groq
                            </div>
                            <div class="msg-ai-bubble">{content}</div>
                          </div>
                        </div>""", unsafe_allow_html=True)

            # Chat input
            if data_prompt := st.chat_input("Ask about your data... e.g. 'show histogram of age'", key="data_chat_input"):
                st.session_state.data_chat.append({"role":"user","content":data_prompt})

                analyst = st.session_state.data_analyst
                data_history = [{"role":m["role"],"content":m["content"]
                                  if m.get("type")!="plot" else "[chart]"}
                                 for m in st.session_state.data_chat[:-1]]

                with st.spinner("📊 Analyzing data..."):
                    plot_generated = False
                    full_text = ""
                    plot_placeholder = st.empty()

                    for chunk in analyst.stream_with_data(data_prompt, data_history, df, eda):
                        if isinstance(chunk, dict) and chunk.get("tool") == "plot":
                            # Generate the plot
                            try:
                                img_bytes = da.make_plot(
                                    df,
                                    plot_type=chunk.get("type","histogram"),
                                    x_col=chunk.get("x"),
                                    y_col=chunk.get("y"),
                                    hue_col=chunk.get("hue"),
                                    title=chunk.get("title"),
                                )
                                st.session_state.data_chat.append({
                                    "role":"assistant","content":img_bytes,"type":"plot"
                                })
                                plot_placeholder.image(img_bytes, use_column_width=True)
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
