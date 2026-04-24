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

# ── STYLES ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Space+Grotesk:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  --void:#030d1a; --deep:#06111f; --card:#0a1c35;
  --panel:#0d2040; --border:#1a3a60; --bright:#1e4a78;
  --cyan:#38bdf8; --violet:#818cf8; --pink:#f472b6;
  --green:#34d399; --yellow:#fbbf24; --red:#f87171;
  --t1:#e2e8f0; --t2:#94a3b8; --t3:#475569;
  --fhd:'Orbitron',monospace;
  --fb:'Space Grotesk',sans-serif;
  --fm:'JetBrains Mono',monospace;
}

/* ── Global ── */
.stApp { background:var(--void) !important; font-family:var(--fb) !important; }

/* ═══════════════════════════════════════════════════
   SIDEBAR — LOCKED OPEN, ALWAYS VISIBLE, NO TOGGLE
   ═══════════════════════════════════════════════════ */
section[data-testid="stSidebar"] {
  background: linear-gradient(180deg,#060f1e,#08162b) !important;
  border-right: 1px solid var(--border) !important;
  width: 260px !important;
  min-width: 260px !important;
  max-width: 260px !important;
  flex-shrink: 0 !important;
  transform: translateX(0) !important;
  visibility: visible !important;
  display: block !important;
  position: relative !important;
}
section[data-testid="stSidebar"] > div {
  width: 260px !important;
  min-width: 260px !important;
  overflow-y: auto !important;
  overflow-x: hidden !important;
  height: 100vh !important;
  padding: 0 !important;
}
/* Kill the collapse arrow completely */
[data-testid="collapsedControl"],
button[kind="header"],
.css-1rs6os { display: none !important; visibility: hidden !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar{width:4px;height:4px}
::-webkit-scrollbar-track{background:var(--deep)}
::-webkit-scrollbar-thumb{background:var(--bright);border-radius:3px}
::-webkit-scrollbar-thumb:hover{background:var(--cyan)}

/* ── Header ── */
.nn-hdr {
  background:linear-gradient(135deg,rgba(6,17,31,.98),rgba(10,28,53,.98));
  border-bottom:1px solid var(--border); padding:11px 20px;
  display:flex; align-items:center; gap:12px;
  margin:-1rem -1rem 1.2rem -1rem; backdrop-filter:blur(20px);
}
.nn-logo {
  width:36px; height:36px; border-radius:9px;
  background:linear-gradient(135deg,var(--cyan),var(--violet));
  display:flex; align-items:center; justify-content:center;
  font-size:17px; font-weight:900; color:#fff;
  box-shadow:0 0 16px rgba(56,189,248,.5); flex-shrink:0;
}
.nn-title {
  font-family:var(--fhd); font-size:14px; font-weight:900; letter-spacing:.1em;
  background:linear-gradient(90deg,var(--cyan),var(--violet));
  -webkit-background-clip:text; -webkit-text-fill-color:transparent;
}
.nn-sub { font-size:8px; color:var(--t3); font-family:var(--fm); letter-spacing:.18em; margin-top:1px; }
.badge {
  padding:2px 8px; border-radius:20px; font-size:9px;
  font-family:var(--fm); letter-spacing:.04em; border:1px solid; margin-left:3px;
}
.bc { border-color:var(--cyan);   color:var(--cyan);   background:rgba(56,189,248,.07);}
.bv { border-color:var(--violet); color:var(--violet); background:rgba(129,140,248,.07);}
.bg { border-color:var(--green);  color:var(--green);  background:rgba(52,211,153,.07);}

/* ── Sidebar section labels ── */
.sb-lbl {
  font-family:var(--fm); font-size:8px; color:var(--t3);
  letter-spacing:.2em; text-transform:uppercase;
  margin:0 0 6px; padding-left:2px;
}

/* ── Messages ── */
.mw { animation:fu .22s ease; margin-bottom:12px; }
@keyframes fu{from{opacity:0;transform:translateY(7px)}to{opacity:1;transform:translateY(0)}}
.mu { display:flex; justify-content:flex-end; }
.mub {
  max-width:74%; padding:10px 14px;
  background:linear-gradient(135deg,rgba(129,140,248,.22),rgba(56,189,248,.13));
  border:1px solid rgba(56,189,248,.28); border-radius:16px 16px 4px 16px;
  color:var(--t1); font-size:13px; line-height:1.6; word-break:break-word;
}
.ma { display:flex; gap:9px; align-items:flex-start; }
.mav {
  width:30px; height:30px; border-radius:7px;
  display:flex; align-items:center; justify-content:center;
  font-size:14px; flex-shrink:0; margin-top:2px;
}
.mal { font-family:var(--fm); font-size:8px; letter-spacing:.15em; margin-bottom:4px; display:flex; align-items:center; gap:4px; }
.mdot { width:4px; height:4px; border-radius:50%; display:inline-block; }
.mab {
  background:var(--card); border:1px solid var(--border);
  border-radius:4px 14px 14px 14px; padding:12px 15px;
  font-size:13px; line-height:1.75; color:var(--t1);
  flex:1; word-break:break-word; overflow-x:auto;
}
.mab code{background:rgba(56,189,248,.09);padding:2px 5px;border-radius:4px;font-family:var(--fm);font-size:11px;color:var(--cyan);}
.mab pre{background:#020d1a;border:1px solid var(--border);border-radius:7px;padding:11px;overflow-x:auto;margin:8px 0;}
.mab pre code{background:none;padding:0;color:var(--t1);font-size:11px;}
.mab table{border-collapse:collapse;width:100%;margin:8px 0;font-size:12px;}
.mab th{padding:6px 10px;border-bottom:1px solid var(--bright);color:var(--cyan);font-family:var(--fm);font-size:9px;text-align:left;}
.mab td{padding:6px 10px;border-bottom:1px solid var(--border);color:var(--t2);}
.mab h1{color:#fff;font-size:16px;margin:10px 0 5px;}
.mab h2{color:var(--cyan);font-size:14px;margin:10px 0 4px;}
.mab h3{color:var(--violet);font-size:12px;margin:8px 0 3px;}
.mab a{color:var(--cyan);}
.mab blockquote{border-left:3px solid var(--violet);padding-left:11px;color:var(--t2);margin:7px 0;}
.mab ul,.mab ol{padding-left:18px;margin:5px 0;}
.mab li{margin-bottom:2px;}
.mab strong{color:#fff;}
.cur{display:inline-block;width:2px;height:14px;background:var(--cyan);margin-left:2px;vertical-align:middle;animation:blink .7s infinite;}
@keyframes blink{0%,100%{opacity:1}50%{opacity:0}}

/* ── Stat cards ── */
.sc{background:var(--card);border:1px solid var(--border);border-radius:9px;padding:11px 13px;border-left-width:3px;border-left-style:solid;}
.sl{font-size:8px;color:var(--t3);letter-spacing:.15em;margin-bottom:4px;}
.sv{font-size:19px;font-weight:700;font-family:var(--fm);}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"]{background:transparent !important;border-bottom:1px solid var(--border) !important;gap:0 !important;}
.stTabs [data-baseweb="tab"]{background:transparent !important;color:var(--t3) !important;font-family:var(--fb) !important;font-size:12px !important;padding:10px 20px !important;border:none !important;border-bottom:2px solid transparent !important;transition:all .15s !important;}
.stTabs [aria-selected="true"]{color:var(--cyan) !important;border-bottom-color:var(--cyan) !important;background:transparent !important;}
.stTabs [data-baseweb="tab-panel"]{padding-top:16px !important;}

/* ── Buttons ── */
.stButton>button{background:linear-gradient(135deg,rgba(56,189,248,.09),rgba(129,140,248,.09)) !important;border:1px solid var(--border) !important;color:var(--t1) !important;font-family:var(--fb) !important;border-radius:7px !important;transition:all .15s !important;font-size:12px !important;}
.stButton>button:hover{border-color:var(--cyan) !important;color:var(--cyan) !important;}

/* ── Inputs ── */
.stSelectbox>div>div,.stTextInput>div>div>input,.stTextArea>div>div>textarea{background:var(--panel) !important;border-color:var(--border) !important;color:var(--t1) !important;font-family:var(--fb) !important;}
.stFileUploader>div{background:var(--panel) !important;border:2px dashed var(--bright) !important;border-radius:9px !important;}
.stFileUploader>div:hover{border-color:var(--cyan) !important;}
.stChatInput>div{background:var(--panel) !important;border:1px solid var(--border) !important;border-radius:11px !important;}
.stChatInput>div:focus-within{border-color:var(--cyan) !important;}
.stChatInput input{color:var(--t1) !important;font-family:var(--fb) !important;}

/* ── Alerts ── */
.stSuccess{background:rgba(52,211,153,.07) !important;border:1px solid rgba(52,211,153,.22) !important;border-radius:7px !important;}
.stError{background:rgba(248,113,113,.07) !important;border:1px solid rgba(248,113,113,.22) !important;border-radius:7px !important;}
.stWarning{background:rgba(251,191,36,.07) !important;border:1px solid rgba(251,191,36,.22) !important;border-radius:7px !important;}

hr{border-color:var(--border) !important;}
#MainMenu,footer,header{visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# ── Imports ───────────────────────────────────────────────────────────────────
from agents import (GeneralChatbotAgent, CodeAgent, DocumentRAGAgent,
                    YouTubeRAGAgent, DeepResearcherAgent, DataAnalystAgent)
from orchestrator import route
import data_analysis as da

# ── Agent metadata ─────────────────────────────────────────────────────────────
AGENTS = {
    "auto":       {"name":"Auto Route",      "icon":"⚡","color":"#38bdf8","desc":"LangGraph Router"},
    "general":    {"name":"General Chat",    "icon":"🤖","color":"#38bdf8","desc":"Gemini 2.5 Flash"},
    "code":       {"name":"Code Agent",      "icon":"💻","color":"#818cf8","desc":"Gemini 2.5 Flash"},
    "document":   {"name":"Document RAG",    "icon":"📄","color":"#34d399","desc":"HF Embed + FAISS"},
    "youtube":    {"name":"YouTube RAG",     "icon":"▶️","color":"#f472b6","desc":"Transcript + RAG"},
    "researcher": {"name":"Deep Research",   "icon":"🔬","color":"#fbbf24","desc":"Web + Gemini"},
    "data":       {"name":"Data Analyst",    "icon":"📊","color":"#34d399","desc":"Gemini + Tools"},
}

# ── Session init ───────────────────────────────────────────────────────────────
def init():
    if "chats" not in st.session_state:
        cid = str(uuid.uuid4())[:8]
        st.session_state.chats = {cid:{"title":"New Chat","messages":[],"created":datetime.now()}}
        st.session_state.active_chat = cid
    if "agents_obj" not in st.session_state:
        st.session_state.agents_obj = {
            "general":    GeneralChatbotAgent(),
            "code":       CodeAgent(),
            "document":   DocumentRAGAgent(),
            "youtube":    YouTubeRAGAgent(),
            "researcher": DeepResearcherAgent(),
        }
    if "data_analyst"   not in st.session_state: st.session_state.data_analyst   = DataAnalystAgent()
    if "selected_agent" not in st.session_state: st.session_state.selected_agent = "auto"
    if "data_df"        not in st.session_state: st.session_state.data_df        = None
    if "data_eda"       not in st.session_state: st.session_state.data_eda       = None
    if "data_chat"      not in st.session_state: st.session_state.data_chat      = []
    if "last_agent"     not in st.session_state: st.session_state.last_agent     = None

init()

def active_msgs(): return st.session_state.chats[st.session_state.active_chat]["messages"]
def add_msg(role, content, agent=None): active_msgs().append({"role":role,"content":content,"agent":agent})

def render_msg(msg):
    if msg["role"] == "user":
        st.markdown(f'<div class="mw mu"><div class="mub">{msg["content"]}</div></div>', unsafe_allow_html=True)
    else:
        ak = msg.get("agent") or "general"
        if ak not in AGENTS: ak = "general"
        m = AGENTS[ak]
        st.markdown(f"""
        <div class="mw ma">
          <div class="mav" style="background:{m['color']}18;border:1px solid {m['color']}35;">{m['icon']}</div>
          <div style="flex:1;min-width:0;">
            <div class="mal" style="color:{m['color']};">
              <span class="mdot" style="background:{m['color']};box-shadow:0 0 4px {m['color']};"></span>
              {m['name'].upper()} · {m['desc']}
            </div>
            <div class="mab">{msg["content"]}</div>
          </div>
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR — LOCKED OPEN
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:

    # Logo
    st.markdown("""
    <div style="padding:14px 8px 10px;text-align:center;border-bottom:1px solid #1a3a60;margin-bottom:10px;">
      <div style="display:inline-flex;align-items:center;gap:9px;">
        <div style="width:32px;height:32px;border-radius:8px;
          background:linear-gradient(135deg,#38bdf8,#818cf8);
          display:flex;align-items:center;justify-content:center;
          font-size:15px;font-weight:900;color:white;
          box-shadow:0 0 12px rgba(56,189,248,0.5);">N</div>
        <div style="text-align:left;">
          <div style="font-family:'Orbitron',monospace;font-size:11px;font-weight:900;
            background:linear-gradient(90deg,#38bdf8,#818cf8);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;
            letter-spacing:.1em;">NEURALNEXUS</div>
          <div style="font-size:7px;color:#475569;letter-spacing:.15em;
            font-family:'JetBrains Mono',monospace;">AI PLATFORM v2</div>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

    # ── Agent Selector ─────────────────────────────────────────────────────────
    st.markdown('<div class="sb-lbl">🤖 Select Agent</div>', unsafe_allow_html=True)

    for key, meta in AGENTS.items():
        is_sel = st.session_state.selected_agent == key
        border = meta["color"] if is_sel else "#1a3a60"
        bg     = f"{meta['color']}12" if is_sel else "transparent"
        col    = meta["color"] if is_sel else "#94a3b8"
        dot    = f'● ' if is_sel else ''

        if st.button(
            f"{meta['icon']}  {dot}{meta['name']}",
            key=f"ab_{key}",
            use_container_width=True,
            help=meta["desc"],
        ):
            st.session_state.selected_agent = key
            st.rerun()

    # Active agent pill
    am = AGENTS[st.session_state.selected_agent]
    st.markdown(f"""
    <div style="margin:6px 0 4px;padding:6px 9px;
      background:{am['color']}0d;border:1px solid {am['color']}25;
      border-radius:6px;font-family:'JetBrains Mono',monospace;
      font-size:8px;color:{am['color']};">
      ⚡ {am['icon']} {am['name']} · <span style="color:#475569;">{am['desc']}</span>
    </div>""", unsafe_allow_html=True)

    st.divider()

    # ── Chat Sessions ──────────────────────────────────────────────────────────
    st.markdown('<div class="sb-lbl">💬 Chat Sessions</div>', unsafe_allow_html=True)

    if st.button("＋  New Chat", use_container_width=True, key="nc"):
        cid = str(uuid.uuid4())[:8]
        n   = len(st.session_state.chats) + 1
        st.session_state.chats[cid] = {"title":f"Chat {n}","messages":[],"created":datetime.now()}
        st.session_state.active_chat = cid
        st.rerun()

    for cid, chat in list(st.session_state.chats.items()):
        is_act  = cid == st.session_state.active_chat
        preview = chat["messages"][-1]["content"][:26]+"…" if chat["messages"] else "Empty"
        c1, c2  = st.columns([5,1])
        with c1:
            if st.button(
                f"{'●' if is_act else '○'}  {chat['title']}",
                key=f"ch_{cid}", use_container_width=True, help=preview,
            ):
                st.session_state.active_chat = cid
                st.rerun()
        with c2:
            if len(st.session_state.chats) > 1:
                if st.button("🗑", key=f"d_{cid}"):
                    del st.session_state.chats[cid]
                    if st.session_state.active_chat == cid:
                        st.session_state.active_chat = list(st.session_state.chats.keys())[0]
                    st.rerun()

    st.divider()

    # ── Document Upload ────────────────────────────────────────────────────────
    st.markdown('<div class="sb-lbl">📎 Document RAG</div>', unsafe_allow_html=True)
    doc_f = st.file_uploader("Upload", type=["pdf","txt","docx"],
                              label_visibility="collapsed", key="du")
    if doc_f:
        with st.spinner("Indexing..."):
            try:
                st.success(st.session_state.agents_obj["document"].ingest(doc_f))
            except Exception as e:
                st.error(f"❌ {e}")

    st.divider()

    # ── YouTube Loader ─────────────────────────────────────────────────────────
    st.markdown('<div class="sb-lbl">▶️ YouTube RAG</div>', unsafe_allow_html=True)
    yt = st.text_input("URL", placeholder="https://youtube.com/watch?v=...",
                        label_visibility="collapsed", key="yu")
    if st.button("Load Video", use_container_width=True, key="lv"):
        if yt.strip():
            with st.spinner("Fetching transcript..."):
                try:
                    st.success(st.session_state.agents_obj["youtube"].ingest(yt.strip()))
                except Exception as e:
                    st.error(f"❌ {e}")
        else:
            st.warning("Enter a YouTube URL first.")

    st.divider()

    if st.button("🧹  Clear Chat", use_container_width=True, key="cc"):
        st.session_state.chats[st.session_state.active_chat]["messages"] = []
        st.rerun()

    # Session info footer
    st.markdown(f"""
    <div style="margin-top:10px;padding:7px 9px;
      background:rgba(56,189,248,.03);border:1px solid #1a3a60;
      border-radius:7px;font-family:'JetBrains Mono',monospace;
      font-size:8px;color:#475569;line-height:2;">
      Session · {st.session_state.active_chat}<br>
      Chats · {len(st.session_state.chats)} &nbsp;|&nbsp;
      Msgs · {len(active_msgs())}
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="nn-hdr">
  <div class="nn-logo">N</div>
  <div>
    <div class="nn-title">NEURALNEXUS</div>
    <div class="nn-sub">MULTI-AGENT AI · LANGCHAIN + LANGGRAPH</div>
  </div>
  <div style="margin-left:auto;display:flex;gap:4px;align-items:center;flex-wrap:wrap;">
    <span class="badge bc">Gemini 2.5 Flash</span>
    <span class="badge bv">LangGraph</span>
    <span class="badge bg">HF Embed</span>
  </div>
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════════════
tab_chat, tab_data = st.tabs(["◈  Multi-Agent Chat", "◇  Data Analysis + AI"])

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 — CHAT
# ─────────────────────────────────────────────────────────────────────────────
with tab_chat:
    msgs = active_msgs()

    if not msgs:
        st.markdown("""
        <div style="text-align:center;padding:42px 20px;">
          <div style="font-size:44px;margin-bottom:12px;">🌌</div>
          <div style="font-family:'Orbitron',monospace;font-size:17px;font-weight:700;
            background:linear-gradient(90deg,#38bdf8,#818cf8);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:9px;">
            Welcome to NeuralNexus
          </div>
          <div style="color:#94a3b8;font-size:12px;max-width:460px;margin:0 auto;line-height:1.8;">
            5 specialized agents powered by <strong style="color:#38bdf8;">Gemini 2.5 Flash</strong><br>
            Auto-routed by <strong style="color:#818cf8;">LangGraph Orchestrator</strong>
          </div>
          <div style="display:flex;justify-content:center;gap:7px;flex-wrap:wrap;margin-top:18px;">
            <span style="padding:4px 12px;border-radius:20px;font-size:10px;border:1px solid #38bdf828;color:#38bdf8;background:#38bdf807;">🤖 General</span>
            <span style="padding:4px 12px;border-radius:20px;font-size:10px;border:1px solid #818cf828;color:#818cf8;background:#818cf807;">💻 Code</span>
            <span style="padding:4px 12px;border-radius:20px;font-size:10px;border:1px solid #34d39928;color:#34d399;background:#34d39907;">📄 Doc RAG</span>
            <span style="padding:4px 12px;border-radius:20px;font-size:10px;border:1px solid #f472b628;color:#f472b6;background:#f472b607;">▶️ YouTube</span>
            <span style="padding:4px 12px;border-radius:20px;font-size:10px;border:1px solid #fbbf2428;color:#fbbf24;background:#fbbf2407;">🔬 Research</span>
          </div>
        </div>""", unsafe_allow_html=True)

    for msg in msgs:
        render_msg(msg)

    sel = st.session_state.selected_agent
    ph  = (f"Message {AGENTS[sel]['name']}..." if sel != "auto"
           else "Ask anything — auto-routed to the best agent...")

    if prompt := st.chat_input(ph, key="ci"):
        add_msg("user", prompt)
        chat = st.session_state.chats[st.session_state.active_chat]
        if len(chat["messages"]) == 1:
            chat["title"] = prompt[:20] + ("…" if len(prompt) > 20 else "")

        ak    = route(prompt, sel if sel != "auto" else None)
        st.session_state.last_agent = ak
        agent = st.session_state.agents_obj.get(ak) or st.session_state.agents_obj["general"]
        m     = AGENTS.get(ak, AGENTS["general"])
        hist  = [{"role":h["role"],"content":h["content"]} for h in active_msgs()[:-1]]

        with st.spinner(f"{m['icon']} {m['name']} thinking..."):
            ph_el = st.empty()
            full  = ""
            for chunk in agent.stream(prompt, hist):
                full += chunk
                ph_el.markdown(f"""
                <div class="mw ma">
                  <div class="mav" style="background:{m['color']}18;border:1px solid {m['color']}35;">{m['icon']}</div>
                  <div style="flex:1;min-width:0;">
                    <div class="mal" style="color:{m['color']};">
                      <span class="mdot" style="background:{m['color']};box-shadow:0 0 4px {m['color']};"></span>
                      {m['name'].upper()} · Streaming...
                    </div>
                    <div class="mab">{full}<span class="cur"></span></div>
                  </div>
                </div>""", unsafe_allow_html=True)
            ph_el.empty()

        add_msg("assistant", full, ak)
        st.rerun()

    if st.session_state.last_agent:
        m = AGENTS[st.session_state.last_agent]
        st.markdown(f"""
        <div style="font-family:'JetBrains Mono',monospace;font-size:8px;
          color:{m['color']};text-align:center;padding:4px;
          border-top:1px solid #1a3a60;margin-top:2px;opacity:.65;">
          ⚡ {m['icon']} {m['name']} · {st.session_state.active_chat} · {len(active_msgs())} msgs
        </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 — DATA ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
with tab_data:
    st.markdown('<div style="font-family:\'Orbitron\',monospace;font-size:10px;color:#38bdf8;letter-spacing:.12em;margin-bottom:12px;">◇ DATA ANALYSIS · EDA, VISUALIZATION & AI CHAT</div>', unsafe_allow_html=True)

    df_up = st.file_uploader("Upload CSV / TSV / XLSX", type=["csv","tsv","xlsx"], key="dfu")
    if df_up:
        with st.spinner("Parsing..."):
            try:
                st.session_state.data_df   = da.load_df(df_up)
                st.session_state.data_eda  = da.get_eda(st.session_state.data_df)
                st.session_state.data_chat = []
                st.success(f"✅ **{df_up.name}** — {st.session_state.data_df.shape[0]:,} rows × {st.session_state.data_df.shape[1]} cols")
            except Exception as e:
                st.error(f"Failed: {e}")

    df  = st.session_state.data_df
    eda = st.session_state.data_eda

    if df is None:
        st.markdown("""
        <div style="text-align:center;padding:50px 20px;color:#475569;">
          <div style="font-size:52px;margin-bottom:12px;opacity:.2;">◇</div>
          <div style="font-family:'Orbitron',monospace;font-size:12px;letter-spacing:.1em;">NO DATASET LOADED</div>
          <div style="font-size:11px;margin-top:7px;">Upload a CSV, TSV, or Excel file above</div>
        </div>""", unsafe_allow_html=True)
    else:
        c1,c2,c3,c4,c5 = st.columns(5)
        for col,lbl,val,color in [
            (c1,"ROWS",    f"{df.shape[0]:,}",             "#38bdf8"),
            (c2,"COLS",    str(df.shape[1]),                "#818cf8"),
            (c3,"NUMERIC", str(len(eda["num_cols"])),       "#34d399"),
            (c4,"MISSING", str(sum(eda["nulls"].values())), "#fbbf24"),
            (c5,"DUPES",   str(eda["duplicates"]),          "#f472b6"),
        ]:
            with col:
                st.markdown(f'<div class="sc" style="border-left-color:{color};"><div class="sl">{lbl}</div><div class="sv" style="color:{color};">{val}</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        dt1,dt2,dt3,dt4 = st.tabs(["📋 Preview","📈 EDA","🎨 Visualize","🤖 AI Chat"])

        with dt1:
            st.caption(f"First 50 of {df.shape[0]:,} rows · {eda['memory']}")
            st.dataframe(df.head(50), use_container_width=True, height=400)

        with dt2:
            ca,cb = st.columns(2)
            with ca:
                st.markdown("**Null Values**")
                st.dataframe(df.isnull().sum().reset_index().rename(columns={"index":"Column",0:"Nulls"}).sort_values("Nulls",ascending=False), use_container_width=True, height=250)
            with cb:
                st.markdown("**Data Types**")
                dt = df.dtypes.reset_index().rename(columns={"index":"Column",0:"Type"})
                dt["Type"] = dt["Type"].astype(str)
                st.dataframe(dt, use_container_width=True, height=250)
            if eda["corr"] is not None:
                st.markdown("**Correlation Matrix**")
                st.dataframe(eda["corr"], use_container_width=True, height=230)
            st.markdown("**Descriptive Statistics**")
            st.dataframe(df.describe(include="all").fillna(""), use_container_width=True, height=230)

        with dt3:
            ac = df.columns.tolist()
            nc = eda["num_cols"]
            cc = eda["cat_cols"]
            PL = ["Histogram","Scatter","Box Plot","Correlation Heatmap","Bar Chart","Line Chart","Violin","Pairplot"]
            v1,v2,v3,v4 = st.columns([2,2,2,1])
            with v1: pt = st.selectbox("Plot Type", PL, key="pt")
            with v2: xc = st.selectbox("X Axis",["—"]+ac,key="xc") if pt not in ["Box Plot","Violin","Correlation Heatmap","Pairplot"] else "—"
            with v3: yc = st.selectbox("Y Axis",["—"]+nc,key="yc") if pt in ["Scatter","Bar Chart","Line Chart"] else "—"
            with v4: hc = st.selectbox("Color By",["—"]+cc,key="hc") if pt=="Scatter" else "—"
            if st.button("◇  Generate Plot", key="gp"):
                with st.spinner("Rendering..."):
                    try:
                        st.image(da.make_plot(df,pt,
                            x_col=xc if xc!="—" else None,
                            y_col=yc if yc!="—" else None,
                            hue_col=hc if hc!="—" else None),
                            use_column_width=True)
                    except Exception as e:
                        st.error(f"Plot error: {e}")

        with dt4:
            st.markdown("""
            <div style="background:rgba(56,189,248,.05);border:1px solid rgba(56,189,248,.2);
              border-radius:9px;padding:10px 14px;margin-bottom:12px;font-size:11px;color:#94a3b8;line-height:1.7;">
              💡 <strong style="color:#38bdf8;">AI Data Chat</strong> — Ask anything about your dataset.<br>
              <em>Try: "Show histogram of Age" · "What are the top correlations?" · "Plot salary vs experience"</em>
            </div>""", unsafe_allow_html=True)

            for m2 in st.session_state.data_chat:
                if m2["role"] == "user":
                    st.markdown(f'<div class="mw mu"><div class="mub">{m2["content"]}</div></div>', unsafe_allow_html=True)
                else:
                    if m2.get("type") == "plot":
                        st.image(m2["content"], use_column_width=True)
                    else:
                        st.markdown(f"""
                        <div class="mw ma">
                          <div class="mav" style="background:#34d39918;border:1px solid #34d39935;">📊</div>
                          <div style="flex:1;min-width:0;">
                            <div class="mal" style="color:#34d399;">
                              <span class="mdot" style="background:#34d399;box-shadow:0 0 4px #34d399;"></span>
                              DATA ANALYST · Gemini 2.5 Flash + Tools
                            </div>
                            <div class="mab">{m2["content"]}</div>
                          </div>
                        </div>""", unsafe_allow_html=True)

            if dp := st.chat_input("Ask about your data...", key="dci"):
                st.session_state.data_chat.append({"role":"user","content":dp})
                analyst = st.session_state.data_analyst
                dh = [{"role":x["role"],"content":x["content"] if x.get("type")!="plot" else "[chart]"}
                      for x in st.session_state.data_chat[:-1]]

                with st.spinner("📊 Analyzing..."):
                    full_t = ""
                    pdone  = False
                    phi    = st.empty()
                    for chunk in analyst.stream_with_data(dp, dh, df, eda):
                        if isinstance(chunk, dict) and chunk.get("tool") == "plot":
                            try:
                                img = da.make_plot(df,
                                    plot_type=chunk.get("type","histogram"),
                                    x_col=chunk.get("x"), y_col=chunk.get("y"),
                                    hue_col=chunk.get("hue"), title=chunk.get("title"))
                                st.session_state.data_chat.append({"role":"assistant","content":img,"type":"plot"})
                                phi.image(img, use_column_width=True)
                                pdone = True
                            except Exception as e:
                                full_t = f"❌ Plot error: {e}"
                        else:
                            full_t += chunk
                    if full_t and not pdone:
                        st.session_state.data_chat.append({"role":"assistant","content":full_t,"type":"text"})
                st.rerun()
