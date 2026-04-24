import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import uuid
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(
    page_title="NeuralNexus",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Space+Grotesk:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  --bg:#06111f; --card:#0a1c35; --panel:#0d2040;
  --border:#1a3a60; --cyan:#38bdf8; --violet:#818cf8;
  --pink:#f472b6; --green:#34d399; --yellow:#fbbf24;
  --t1:#e2e8f0; --t2:#94a3b8; --t3:#475569;
  --fh:'Orbitron',monospace; --fb:'Space Grotesk',sans-serif; --fm:'JetBrains Mono',monospace;
}

/* Base */
.stApp { background:var(--bg) !important; font-family:var(--fb) !important; }

/* ── SIDEBAR LOCKED OPEN ── */
section[data-testid="stSidebar"] {
  background:linear-gradient(180deg,#060f1e,#081729) !important;
  border-right:1px solid var(--border) !important;
  width:265px !important; min-width:265px !important; max-width:265px !important;
}
section[data-testid="stSidebar"] > div:first-child {
  width:265px !important; padding:0 !important; overflow-y:auto; height:100vh;
}
[data-testid="collapsedControl"] { display:none !important; }

/* Scrollbar */
::-webkit-scrollbar{width:4px} ::-webkit-scrollbar-track{background:#06111f}
::-webkit-scrollbar-thumb{background:#1e4a78;border-radius:3px}

/* Header */
.hdr{background:linear-gradient(135deg,rgba(3,13,26,.97),rgba(10,28,53,.97));
  border-bottom:1px solid var(--border);padding:11px 20px;
  display:flex;align-items:center;gap:12px;
  margin:-1rem -1rem 1rem -1rem;backdrop-filter:blur(16px);}
.logo{width:36px;height:36px;border-radius:9px;
  background:linear-gradient(135deg,var(--cyan),var(--violet));
  display:flex;align-items:center;justify-content:center;
  font-size:17px;font-weight:900;color:#fff;
  box-shadow:0 0 16px rgba(56,189,248,.45);flex-shrink:0;}
.title{font-family:var(--fh);font-size:14px;font-weight:900;letter-spacing:.1em;
  background:linear-gradient(90deg,var(--cyan),var(--violet));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;}
.sub{font-size:8px;color:var(--t3);font-family:var(--fm);letter-spacing:.18em;margin-top:1px;}
.bdg{padding:2px 8px;border-radius:20px;font-size:8px;font-family:var(--fm);border:1px solid;margin-left:3px;}

/* Messages */
.mu{display:flex;justify-content:flex-end;margin-bottom:12px;animation:fu .2s ease;}
.mb-u{max-width:72%;padding:10px 14px;
  background:linear-gradient(135deg,rgba(129,140,248,.2),rgba(56,189,248,.12));
  border:1px solid rgba(56,189,248,.25);border-radius:16px 16px 4px 16px;
  color:var(--t1);font-size:13px;line-height:1.6;word-break:break-word;}
.ma{display:flex;gap:9px;align-items:flex-start;margin-bottom:12px;animation:fu .2s ease;}
.av{width:30px;height:30px;border-radius:7px;display:flex;align-items:center;
  justify-content:center;font-size:14px;flex-shrink:0;margin-top:2px;}
.lbl{font-family:var(--fm);font-size:8px;letter-spacing:.15em;
  margin-bottom:3px;display:flex;align-items:center;gap:4px;}
.dot{width:4px;height:4px;border-radius:50%;display:inline-block;}
.mb-a{background:var(--card);border:1px solid var(--border);
  border-radius:4px 14px 14px 14px;padding:12px 15px;
  font-size:13px;line-height:1.75;color:var(--t1);flex:1;
  word-break:break-word;overflow-x:auto;}
.mb-a code{background:rgba(56,189,248,.09);padding:2px 5px;border-radius:4px;
  font-family:var(--fm);font-size:11px;color:var(--cyan);}
.mb-a pre{background:#020d1a;border:1px solid var(--border);border-radius:7px;
  padding:11px;overflow-x:auto;margin:8px 0;}
.mb-a pre code{background:none;padding:0;color:var(--t1);}
.mb-a h2{color:var(--cyan);font-size:14px;margin:10px 0 4px;}
.mb-a h3{color:var(--violet);font-size:12px;margin:8px 0 3px;}
.mb-a table{border-collapse:collapse;width:100%;margin:8px 0;font-size:12px;}
.mb-a th{padding:6px 10px;border-bottom:1px solid #1e4a78;color:var(--cyan);
  font-family:var(--fm);font-size:9px;text-align:left;}
.mb-a td{padding:6px 10px;border-bottom:1px solid var(--border);color:var(--t2);}
.mb-a strong{color:#fff;} .mb-a a{color:var(--cyan);}
.mb-a ul,.mb-a ol{padding-left:18px;margin:5px 0;} .mb-a li{margin-bottom:2px;}
.mb-a blockquote{border-left:3px solid var(--violet);padding-left:11px;color:var(--t2);margin:7px 0;}
.cur{display:inline-block;width:2px;height:13px;background:var(--cyan);
  margin-left:2px;vertical-align:middle;animation:bl .7s infinite;}
@keyframes fu{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}
@keyframes bl{0%,100%{opacity:1}50%{opacity:0}}

/* Stat card */
.sc{background:var(--card);border:1px solid var(--border);border-radius:9px;
  padding:11px 13px;border-left-width:3px;border-left-style:solid;}
.sl{font-size:8px;color:var(--t3);letter-spacing:.15em;margin-bottom:4px;}
.sv{font-size:18px;font-weight:700;font-family:var(--fm);}

/* Tabs */
.stTabs [data-baseweb="tab-list"]{background:transparent !important;border-bottom:1px solid var(--border) !important;gap:0 !important;}
.stTabs [data-baseweb="tab"]{background:transparent !important;color:var(--t3) !important;
  font-family:var(--fb) !important;font-size:12px !important;padding:10px 20px !important;
  border:none !important;border-bottom:2px solid transparent !important;transition:all .15s !important;}
.stTabs [aria-selected="true"]{color:var(--cyan) !important;border-bottom-color:var(--cyan) !important;background:transparent !important;}
.stTabs [data-baseweb="tab-panel"]{padding-top:16px !important;}

/* Buttons */
.stButton>button{background:rgba(56,189,248,.07) !important;border:1px solid var(--border) !important;
  color:var(--t1) !important;font-family:var(--fb) !important;border-radius:7px !important;
  transition:all .15s !important;font-size:12px !important;}
.stButton>button:hover{border-color:var(--cyan) !important;color:var(--cyan) !important;}

/* Inputs */
.stSelectbox>div>div,.stTextInput>div>div>input{background:var(--panel) !important;
  border-color:var(--border) !important;color:var(--t1) !important;font-family:var(--fb) !important;}
.stFileUploader>div{background:var(--panel) !important;
  border:2px dashed #1e4a78 !important;border-radius:9px !important;}
.stFileUploader>div:hover{border-color:var(--cyan) !important;}
.stChatInput>div{background:var(--panel) !important;
  border:1px solid var(--border) !important;border-radius:11px !important;}
.stChatInput>div:focus-within{border-color:var(--cyan) !important;}
.stChatInput textarea{color:var(--t1) !important;font-family:var(--fb) !important;}

/* Alerts */
.stSuccess,.stError,.stWarning,.stInfo{border-radius:7px !important;}

hr{border-color:var(--border) !important;}
#MainMenu,footer,header{visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# ── Imports ────────────────────────────────────────────────────────────────────
import agents.general    as ag_general
import agents.code       as ag_code
import agents.document   as ag_document
import agents.youtube    as ag_youtube
import agents.researcher as ag_researcher
import agents.data_analyst as ag_data
import plots
from router import route

# ── Agent config ───────────────────────────────────────────────────────────────
AGENTS = {
    "auto":       {"name":"Auto Route",    "icon":"⚡","color":"#38bdf8","mod":None},
    "general":    {"name":"General Chat",  "icon":"🤖","color":"#38bdf8","mod":ag_general},
    "code":       {"name":"Code Agent",    "icon":"💻","color":"#818cf8","mod":ag_code},
    "document":   {"name":"Document RAG",  "icon":"📄","color":"#34d399","mod":ag_document},
    "youtube":    {"name":"YouTube RAG",   "icon":"▶️","color":"#f472b6","mod":ag_youtube},
    "researcher": {"name":"Deep Research", "icon":"🔬","color":"#fbbf24","mod":ag_researcher},
}

# ── Session state ──────────────────────────────────────────────────────────────
def init():
    if "chats" not in st.session_state:
        cid = str(uuid.uuid4())[:8]
        st.session_state.chats       = {cid:{"title":"New Chat","messages":[]}}
        st.session_state.active      = cid
    if "sel"        not in st.session_state: st.session_state.sel        = "auto"
    if "last"       not in st.session_state: st.session_state.last       = None
    if "df"         not in st.session_state: st.session_state.df         = None
    if "eda"        not in st.session_state: st.session_state.eda        = None
    if "dchat"      not in st.session_state: st.session_state.dchat      = []

init()

def msgs(): return st.session_state.chats[st.session_state.active]["messages"]
def add(role, content, agent=None): msgs().append({"role":role,"content":content,"agent":agent})

def get_eda(df):
    nc = df.select_dtypes(include=np.number).columns.tolist()
    cc = df.select_dtypes(include=["object","category"]).columns.tolist()
    return {"num_cols":nc,"cat_cols":cc,"nulls":df.isnull().sum().to_dict(),
            "duplicates":int(df.duplicated().sum()),
            "memory":f"{df.memory_usage(deep=True).sum()/1024:.1f} KB",
            "corr":df[nc].corr().round(3) if len(nc)>=2 else None}

def render(msg):
    if msg["role"] == "user":
        st.markdown(f'<div class="mu"><div class="mb-u">{msg["content"]}</div></div>',
                    unsafe_allow_html=True)
    else:
        ak = msg.get("agent","general")
        if ak not in AGENTS: ak = "general"
        m = AGENTS[ak]
        st.markdown(f"""
        <div class="ma">
          <div class="av" style="background:{m['color']}18;border:1px solid {m['color']}35;">{m['icon']}</div>
          <div style="flex:1;min-width:0;">
            <div class="lbl" style="color:{m['color']};">
              <span class="dot" style="background:{m['color']};box-shadow:0 0 4px {m['color']};"></span>
              {m['name'].upper()}
            </div>
            <div class="mb-a">{msg["content"]}</div>
          </div>
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:

    # Logo
    st.markdown("""
    <div style="padding:14px 8px 10px;text-align:center;
      border-bottom:1px solid #1a3a60;margin-bottom:10px;">
      <div style="display:inline-flex;align-items:center;gap:9px;">
        <div style="width:32px;height:32px;border-radius:8px;
          background:linear-gradient(135deg,#38bdf8,#818cf8);
          display:flex;align-items:center;justify-content:center;
          font-size:15px;font-weight:900;color:#fff;
          box-shadow:0 0 12px rgba(56,189,248,.45);">N</div>
        <div style="text-align:left;">
          <div style="font-family:'Orbitron',monospace;font-size:11px;font-weight:900;
            background:linear-gradient(90deg,#38bdf8,#818cf8);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;
            letter-spacing:.1em;">NEURALNEXUS</div>
          <div style="font-size:7px;color:#475569;letter-spacing:.15em;
            font-family:'JetBrains Mono',monospace;">AI PLATFORM</div>
        </div>
      </div>
    </div>""", unsafe_allow_html=True)

    # ── Agent Selector ─────────────────────────────────────────────────────────
    st.markdown('<p style="font-family:\'JetBrains Mono\',monospace;font-size:8px;color:#475569;letter-spacing:.2em;text-transform:uppercase;margin-bottom:6px;">🤖 SELECT AGENT</p>', unsafe_allow_html=True)

    for key, meta in AGENTS.items():
        active = st.session_state.sel == key
        label  = f"{'●  ' if active else '    '}{meta['icon']}  {meta['name']}"
        if st.button(label, key=f"ab_{key}", use_container_width=True, help=meta.get("mod",{}) and ""):
            st.session_state.sel = key
            st.rerun()

    # Show current
    am = AGENTS[st.session_state.sel]
    st.markdown(f"""
    <div style="margin:6px 0;padding:5px 9px;
      background:{am['color']}0c;border:1px solid {am['color']}22;
      border-radius:6px;font-size:8px;font-family:'JetBrains Mono',monospace;color:{am['color']};">
      Active: {am['icon']} {am['name']}
    </div>""", unsafe_allow_html=True)

    st.divider()

    # ── Chat Sessions ──────────────────────────────────────────────────────────
    st.markdown('<p style="font-family:\'JetBrains Mono\',monospace;font-size:8px;color:#475569;letter-spacing:.2em;text-transform:uppercase;margin-bottom:6px;">💬 CHAT SESSIONS</p>', unsafe_allow_html=True)

    if st.button("＋  New Chat", use_container_width=True, key="nc"):
        cid = str(uuid.uuid4())[:8]
        n   = len(st.session_state.chats) + 1
        st.session_state.chats[cid] = {"title":f"Chat {n}","messages":[]}
        st.session_state.active = cid
        st.rerun()

    for cid, chat in list(st.session_state.chats.items()):
        is_act = cid == st.session_state.active
        preview = chat["messages"][-1]["content"][:25]+"…" if chat["messages"] else "Empty"
        c1, c2 = st.columns([5,1])
        with c1:
            if st.button(f"{'●' if is_act else '○'}  {chat['title']}",
                         key=f"ch_{cid}", use_container_width=True, help=preview):
                st.session_state.active = cid
                st.rerun()
        with c2:
            if len(st.session_state.chats) > 1:
                if st.button("✕", key=f"d_{cid}"):
                    del st.session_state.chats[cid]
                    if st.session_state.active == cid:
                        st.session_state.active = list(st.session_state.chats.keys())[0]
                    st.rerun()

    st.divider()

    # ── Document Upload ────────────────────────────────────────────────────────
    st.markdown('<p style="font-family:\'JetBrains Mono\',monospace;font-size:8px;color:#475569;letter-spacing:.2em;text-transform:uppercase;margin-bottom:6px;">📎 DOCUMENT RAG</p>', unsafe_allow_html=True)
    doc_f = st.file_uploader("PDF / TXT / DOCX", type=["pdf","txt","docx"],
                              label_visibility="collapsed", key="du")
    if doc_f:
        with st.spinner("Indexing..."):
            try:
                st.success(ag_document.ingest(doc_f))
            except Exception as e:
                st.error(f"❌ {e}")

    st.divider()

    # ── YouTube ────────────────────────────────────────────────────────────────
    st.markdown('<p style="font-family:\'JetBrains Mono\',monospace;font-size:8px;color:#475569;letter-spacing:.2em;text-transform:uppercase;margin-bottom:6px;">▶️ YOUTUBE RAG</p>', unsafe_allow_html=True)
    yt = st.text_input("YouTube URL", placeholder="https://youtube.com/watch?v=...",
                        label_visibility="collapsed", key="yu")
    if st.button("Load Video", use_container_width=True, key="lv"):
        if yt.strip():
            with st.spinner("Fetching transcript..."):
                try:
                    st.success(ag_youtube.ingest(yt.strip()))
                except Exception as e:
                    st.error(f"❌ {e}")
        else:
            st.warning("Enter a YouTube URL.")

    st.divider()
    if st.button("🧹 Clear Chat", use_container_width=True, key="cc"):
        st.session_state.chats[st.session_state.active]["messages"] = []
        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hdr">
  <div class="logo">N</div>
  <div>
    <div class="title">NEURALNEXUS</div>
    <div class="sub">MULTI-AGENT AI PLATFORM · GEMINI 2.5 FLASH</div>
  </div>
  <div style="margin-left:auto;display:flex;gap:4px;flex-wrap:wrap;">
    <span class="bdg" style="border-color:#38bdf8;color:#38bdf8;background:rgba(56,189,248,.07);">Gemini 2.5 Flash</span>
    <span class="bdg" style="border-color:#818cf8;color:#818cf8;background:rgba(129,140,248,.07);">LangChain</span>
    <span class="bdg" style="border-color:#34d399;color:#34d399;background:rgba(52,211,153,.07);">HF Embed</span>
  </div>
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════════════
t1, t2 = st.tabs(["◈  Multi-Agent Chat", "◇  Data Analysis"])

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 — CHAT
# ─────────────────────────────────────────────────────────────────────────────
with t1:
    all_msgs = msgs()

    if not all_msgs:
        st.markdown("""
        <div style="text-align:center;padding:40px 20px;">
          <div style="font-size:44px;margin-bottom:12px;">🌌</div>
          <div style="font-family:'Orbitron',monospace;font-size:17px;font-weight:700;
            background:linear-gradient(90deg,#38bdf8,#818cf8);
            -webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:9px;">
            Welcome to NeuralNexus
          </div>
          <div style="color:#94a3b8;font-size:13px;line-height:1.8;max-width:420px;margin:0 auto;">
            Select an agent in the sidebar or use <strong style="color:#38bdf8;">Auto Route</strong>.
          </div>
          <div style="display:flex;justify-content:center;gap:7px;flex-wrap:wrap;margin-top:18px;">
            <span style="padding:4px 12px;border-radius:20px;font-size:10px;border:1px solid #38bdf828;color:#38bdf8;">🤖 General</span>
            <span style="padding:4px 12px;border-radius:20px;font-size:10px;border:1px solid #818cf828;color:#818cf8;">💻 Code</span>
            <span style="padding:4px 12px;border-radius:20px;font-size:10px;border:1px solid #34d39928;color:#34d399;">📄 Document</span>
            <span style="padding:4px 12px;border-radius:20px;font-size:10px;border:1px solid #f472b628;color:#f472b6;">▶️ YouTube</span>
            <span style="padding:4px 12px;border-radius:20px;font-size:10px;border:1px solid #fbbf2428;color:#fbbf24;">🔬 Research</span>
          </div>
        </div>""", unsafe_allow_html=True)

    for msg in all_msgs:
        render(msg)

    sel = st.session_state.sel
    ph  = (f"Message {AGENTS[sel]['name']}..."
           if sel != "auto" else "Ask anything — I'll route to the best agent...")

    if prompt := st.chat_input(ph, key="ci"):
        add("user", prompt)
        chat = st.session_state.chats[st.session_state.active]
        if len(chat["messages"]) == 1:
            chat["title"] = prompt[:20] + ("…" if len(prompt) > 20 else "")

        # Route
        ak  = route(prompt, sel)
        if ak == "auto": ak = "general"
        mod = AGENTS[ak]["mod"]
        if mod is None: mod = ag_general
        m   = AGENTS[ak]
        hist = [{"role":h["role"],"content":h["content"]} for h in msgs()[:-1]]

        ph_el = st.empty()
        full  = ""
        with st.spinner(f"{m['icon']} {m['name']}..."):
            for chunk in mod.run(prompt, hist):
                full += chunk
                ph_el.markdown(f"""
                <div class="ma">
                  <div class="av" style="background:{m['color']}18;border:1px solid {m['color']}35;">{m['icon']}</div>
                  <div style="flex:1;min-width:0;">
                    <div class="lbl" style="color:{m['color']};">
                      <span class="dot" style="background:{m['color']};box-shadow:0 0 4px {m['color']};"></span>
                      {m['name'].upper()}
                    </div>
                    <div class="mb-a">{full}<span class="cur"></span></div>
                  </div>
                </div>""", unsafe_allow_html=True)
            ph_el.empty()

        st.session_state.last = ak
        add("assistant", full, ak)
        st.rerun()

    if st.session_state.last:
        m = AGENTS[st.session_state.last]
        st.markdown(f"""
        <div style="font-family:'JetBrains Mono',monospace;font-size:8px;
          color:{m['color']};text-align:center;padding:4px;
          border-top:1px solid #1a3a60;margin-top:2px;opacity:.6;">
          {m['icon']} {m['name']} · {len(msgs())} messages
        </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 — DATA ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
with t2:
    st.markdown('<p style="font-family:\'Orbitron\',monospace;font-size:10px;color:#38bdf8;letter-spacing:.1em;margin-bottom:12px;">◇ DATA ANALYSIS · EDA + VISUALIZATION + AI CHAT</p>', unsafe_allow_html=True)

    up = st.file_uploader("Upload CSV / TSV / XLSX", type=["csv","tsv","xlsx"], key="du2")
    if up:
        with st.spinner("Loading..."):
            try:
                name = up.name
                if name.endswith(".xlsx"):
                    df = pd.read_excel(up)
                elif name.endswith(".tsv"):
                    df = pd.read_csv(up, sep="\t")
                else:
                    df = pd.read_csv(up)
                st.session_state.df    = df
                st.session_state.eda   = get_eda(df)
                st.session_state.dchat = []
                st.success(f"✅ **{name}** — {df.shape[0]:,} rows × {df.shape[1]} cols")
            except Exception as e:
                st.error(f"Failed: {e}")

    df  = st.session_state.df
    eda = st.session_state.eda

    if df is None:
        st.markdown("""
        <div style="text-align:center;padding:50px;color:#475569;">
          <div style="font-size:48px;opacity:.2;margin-bottom:12px;">◇</div>
          <div style="font-family:'Orbitron',monospace;font-size:12px;letter-spacing:.1em;">NO DATASET LOADED</div>
          <div style="font-size:11px;margin-top:6px;">Upload a CSV, TSV, or Excel file above</div>
        </div>""", unsafe_allow_html=True)
    else:
        # Stat cards
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

        d1, d2, d3, d4 = st.tabs(["📋 Preview", "📈 EDA", "🎨 Visualize", "🤖 AI Chat"])

        with d1:
            st.caption(f"Showing first 50 rows · {eda['memory']}")
            st.dataframe(df.head(50), use_container_width=True, height=380)

        with d2:
            a, b = st.columns(2)
            with a:
                st.markdown("**Missing Values**")
                nulls = df.isnull().sum().reset_index()
                nulls.columns = ["Column","Nulls"]
                st.dataframe(nulls.sort_values("Nulls",ascending=False), use_container_width=True, height=240)
            with b:
                st.markdown("**Data Types**")
                dt = df.dtypes.reset_index()
                dt.columns = ["Column","Type"]
                dt["Type"] = dt["Type"].astype(str)
                st.dataframe(dt, use_container_width=True, height=240)
            if eda["corr"] is not None:
                st.markdown("**Correlation Matrix**")
                st.dataframe(eda["corr"], use_container_width=True, height=220)
            st.markdown("**Summary Statistics**")
            st.dataframe(df.describe(include="all").fillna(""), use_container_width=True, height=220)

        with d3:
            nc = eda["num_cols"]
            cc = eda["cat_cols"]
            ac = df.columns.tolist()
            PL = ["Histogram","Scatter","Box Plot","Correlation Heatmap",
                  "Bar Chart","Line Chart","Violin","Pairplot"]
            v1,v2,v3,v4 = st.columns([2,2,2,1])
            with v1: pt = st.selectbox("Plot Type", PL, key="pt")
            with v2:
                xc = st.selectbox("X Axis",["—"]+ac,key="xc") if pt not in ["Box Plot","Violin","Correlation Heatmap","Pairplot"] else "—"
            with v3:
                yc = st.selectbox("Y Axis",["—"]+nc,key="yc") if pt in ["Scatter","Bar Chart","Line Chart"] else "—"
            with v4:
                hc = st.selectbox("Color By",["—"]+cc,key="hc") if pt=="Scatter" else "—"

            if st.button("Generate Plot ◇", key="gp"):
                with st.spinner("Rendering..."):
                    try:
                        img = plots.make(df, pt,
                            x=xc if xc!="—" else None,
                            y=yc if yc!="—" else None,
                            hue=hc if hc!="—" else None)
                        st.image(img, use_column_width=True)
                    except Exception as e:
                        st.error(f"Plot error: {e}")

        with d4:
            st.markdown("""
            <div style="background:rgba(56,189,248,.05);border:1px solid rgba(56,189,248,.18);
              border-radius:9px;padding:10px 14px;margin-bottom:12px;font-size:12px;color:#94a3b8;line-height:1.7;">
              💡 <strong style="color:#38bdf8;">AI Data Chat</strong> — Ask anything about your data.<br>
              <em>Examples: "Show histogram of Age" · "Top correlations?" · "Describe the dataset"</em>
            </div>""", unsafe_allow_html=True)

            for dm in st.session_state.dchat:
                if dm["role"] == "user":
                    st.markdown(f'<div class="mu"><div class="mb-u">{dm["content"]}</div></div>',
                                unsafe_allow_html=True)
                elif dm.get("type") == "plot":
                    st.image(dm["content"], use_column_width=True)
                else:
                    st.markdown(f"""
                    <div class="ma">
                      <div class="av" style="background:#34d39918;border:1px solid #34d39935;">📊</div>
                      <div style="flex:1;min-width:0;">
                        <div class="lbl" style="color:#34d399;">
                          <span class="dot" style="background:#34d399;box-shadow:0 0 4px #34d399;"></span>
                          DATA ANALYST
                        </div>
                        <div class="mb-a">{dm["content"]}</div>
                      </div>
                    </div>""", unsafe_allow_html=True)

            if dp := st.chat_input("Ask about your data...", key="dci"):
                st.session_state.dchat.append({"role":"user","content":dp})
                dh = [{"role":x["role"],"content":x["content"] if x.get("type")!="plot" else "[chart]"}
                      for x in st.session_state.dchat[:-1]]

                with st.spinner("Analyzing..."):
                    full_t = ""
                    pdone  = False
                    for chunk in ag_data.run(dp, dh, df, eda):
                        if isinstance(chunk, dict) and chunk.get("tool") == "plot":
                            try:
                                img = plots.make(df,
                                    plot_type=chunk.get("type","histogram"),
                                    x=chunk.get("x"), y=chunk.get("y"),
                                    hue=chunk.get("hue"), title=chunk.get("title"))
                                st.session_state.dchat.append({"role":"assistant","content":img,"type":"plot"})
                                st.image(img, use_column_width=True)
                                pdone = True
                            except Exception as e:
                                full_t = f"❌ Plot error: {e}"
                        else:
                            full_t += chunk
                    if full_t and not pdone:
                        st.session_state.dchat.append({"role":"assistant","content":full_t,"type":"text"})
                st.rerun()
