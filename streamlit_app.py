import os
import streamlit as st

from config.config_loader import load_config, save_config
from RAG.rag import RAG


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Enterprise RAG",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

:root {
    --bg:           #0c0e14;
    --bg-card:      #13151f;
    --bg-hover:     #1a1d2a;
    --border:       rgba(255,255,255,0.07);
    --border-focus: rgba(99,179,237,0.45);
    --accent:       #4f9cf9;
    --accent-2:     #a78bfa;
    --accent-glow:  rgba(79,156,249,0.14);
    --text-primary: #e8ecf4;
    --text-muted:   #7a849c;
    --text-dim:     #4a5266;
    --success:      #34d399;
    --warning:      #fbbf24;
    --danger:       #f87171;
    --radius:       12px;
    --radius-lg:    18px;
}

html, body, [class*="css"] { font-family: 'Syne', sans-serif !important; color: var(--text-primary); }
.stApp { background: var(--bg) !important; }
.main .block-container { padding: 2rem 2.5rem 4rem !important; max-width: 1100px !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] { background: var(--bg-card) !important; border-right: 1px solid var(--border) !important; }
[data-testid="stSidebar"] > div:first-child { padding: 1.5rem 1.2rem 2rem !important; }
.sidebar-brand { display: flex; align-items: center; gap: 10px; padding: 0 0 1.4rem; border-bottom: 1px solid var(--border); margin-bottom: 1.4rem; }
.brand-icon { width: 36px; height: 36px; background: linear-gradient(135deg, var(--accent), var(--accent-2)); border-radius: 9px; display: flex; align-items: center; justify-content: center; font-size: 18px; flex-shrink: 0; }
.brand-name { font-size: 0.98rem; font-weight: 700; letter-spacing: 0.03em; color: var(--text-primary); line-height: 1.2; }
.brand-sub  { font-size: 0.66rem; color: var(--text-muted); font-family: 'DM Mono', monospace; letter-spacing: 0.06em; text-transform: uppercase; }
.sb-label   { font-size: 0.63rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: var(--text-dim); margin: 1.4rem 0 0.5rem; padding: 0 0.2rem; }

/* ── Nav radio ── */
[data-testid="stSidebar"] .stRadio > label { display: none; }
[data-testid="stSidebar"] .stRadio [role="radiogroup"] { gap: 4px; display: flex; flex-direction: column; }
[data-testid="stSidebar"] .stRadio label { background: transparent; border: 1px solid transparent; border-radius: var(--radius); padding: 0.55rem 0.85rem; cursor: pointer; transition: all 0.16s ease; color: var(--text-muted) !important; font-size: 0.87rem; font-weight: 500; width: 100%; display: flex; align-items: center; gap: 8px; }
[data-testid="stSidebar"] .stRadio label:hover { background: var(--bg-hover); color: var(--text-primary) !important; border-color: var(--border); }
[data-testid="stSidebar"] .stRadio [role="radio"] { display: none !important; }
[data-testid="stSidebar"] .stRadio div:has(input:checked) label { background: var(--accent-glow) !important; border-color: rgba(79,156,249,0.28) !important; color: var(--accent) !important; }

/* ── Sidebar metrics ── */
.sb-metrics { display: flex; flex-direction: column; gap: 5px; }
.sb-metric  { display: flex; align-items: center; justify-content: space-between; padding: 0.45rem 0.7rem; background: var(--bg-hover); border: 1px solid var(--border); border-radius: 9px; }
.sb-metric-label { font-size: 0.68rem; color: var(--text-dim); font-family: 'DM Mono', monospace; text-transform: uppercase; letter-spacing: 0.08em; }
.sb-metric-value { font-size: 0.81rem; font-weight: 700; color: var(--text-muted); }

/* ── PDF chips ── */
[data-testid="stSidebar"] [data-testid="stFileUploader"] { border: 1.5px dashed rgba(79,156,249,0.22) !important; border-radius: var(--radius) !important; background: rgba(79,156,249,0.03) !important; transition: all 0.18s !important; }
[data-testid="stSidebar"] [data-testid="stFileUploader"]:hover { border-color: rgba(79,156,249,0.45) !important; background: rgba(79,156,249,0.07) !important; }
.pdf-chip { display: flex; align-items: center; gap: 7px; padding: 0.38rem 0.65rem; background: var(--bg-hover); border: 1px solid var(--border); border-radius: 8px; margin-bottom: 4px; font-size: 0.74rem; }
.chip-name { flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; color: var(--text-primary); }
.chip-size { color: var(--text-dim); font-family: 'DM Mono', monospace; flex-shrink: 0; }
.chip-ok   { color: var(--success); flex-shrink: 0; }

/* ── Page header ── */
.page-header  { margin-bottom: 1.75rem; }
.page-title   { font-size: 1.7rem; font-weight: 800; letter-spacing: -0.025em; color: var(--text-primary); margin: 0 0 0.25rem; line-height: 1.2; }
.page-title span { color: var(--accent); }
.page-subtitle{ font-size: 0.82rem; color: var(--text-muted); font-family: 'DM Mono', monospace; letter-spacing: 0.03em; }

/* ── Stat row ── */
.stat-row  { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 1.6rem; }
.stat-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius); padding: 0.9rem 1.1rem; position: relative; overflow: hidden; transition: border-color 0.18s; }
.stat-card:hover { border-color: rgba(255,255,255,0.12); }
.stat-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, var(--accent), var(--accent-2)); opacity: 0.55; }
.stat-lbl  { font-size: 0.63rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: var(--text-dim); margin-bottom: 0.35rem; font-family: 'DM Mono', monospace; }
.stat-val  { font-size: 1.05rem; font-weight: 700; color: var(--text-primary); }
.badge     { display: inline-flex; align-items: center; gap: 5px; font-size: 0.76rem; font-weight: 600; padding: 2px 9px; border-radius: 20px; }
.badge-on  { background: rgba(52,211,153,0.1);  color: var(--success); border: 1px solid rgba(52,211,153,0.22); }
.badge-off { background: rgba(248,113,113,0.1); color: var(--danger);  border: 1px solid rgba(248,113,113,0.2);  }
.badge-dot { width: 6px; height: 6px; border-radius: 50%; background: currentColor; display: inline-block; }

/* ── No-docs warning ── */
.no-docs-card { background: rgba(251,191,36,0.06); border: 1px solid rgba(251,191,36,0.2); border-radius: var(--radius); padding: 1.1rem 1.3rem; display: flex; align-items: flex-start; gap: 10px; margin-bottom: 1.5rem; }
.nd-icon { font-size: 1.1rem; flex-shrink: 0; }
.nd-text  { font-size: 0.84rem; color: var(--warning); line-height: 1.55; }
.nd-text strong { font-weight: 700; }

/* ── Empty state ── */
.empty-state    { text-align: center; padding: 3.5rem 2rem; color: var(--text-dim); }
.es-icon        { font-size: 2.5rem; margin-bottom: 1rem; opacity: 0.35; }
.es-title       { font-size: 0.98rem; font-weight: 700; color: var(--text-muted); margin-bottom: 0.35rem; }
.es-desc        { font-size: 0.8rem; line-height: 1.65; }

/* ── Chat messages ── */
[data-testid="stChatMessage"] { background: transparent !important; padding: 0.85rem 1.1rem !important; border-bottom: 1px solid var(--border) !important; }
[data-testid="stChatMessage"]:last-child { border-bottom: none !important; }
[data-testid="stChatMessageContent"] p { font-size: 0.88rem !important; line-height: 1.68 !important; color: var(--text-primary) !important; margin: 0 !important; }
[data-testid="stChatInput"] { background: var(--bg-card) !important; border: 1px solid var(--border) !important; border-radius: var(--radius-lg) !important; transition: border-color 0.18s !important; }
[data-testid="stChatInput"]:focus-within { border-color: var(--border-focus) !important; box-shadow: 0 0 0 3px rgba(79,156,249,0.07) !important; }
[data-testid="stChatInput"] textarea { background: transparent !important; color: var(--text-primary) !important; font-family: 'Syne', sans-serif !important; font-size: 0.87rem !important; }
[data-testid="stChatInput"] textarea::placeholder { color: var(--text-dim) !important; }

/* ── Sources expander ── */
[data-testid="stExpander"] { background: var(--bg-card) !important; border: 1px solid var(--border) !important; border-radius: var(--radius) !important; margin-bottom: 0.6rem !important; overflow: hidden !important; }
[data-testid="stExpander"] summary { padding: 0.7rem 1rem !important; font-size: 0.8rem !important; font-weight: 600 !important; color: var(--text-muted) !important; }
[data-testid="stExpander"] summary:hover { color: var(--text-primary) !important; }
[data-testid="stExpander"] > div > div { padding: 0 1rem 0.9rem !important; }
.src-card  { display: flex; align-items: flex-start; gap: 10px; background: var(--bg-hover); border: 1px solid var(--border); border-radius: 9px; padding: 0.7rem 0.9rem; margin-bottom: 6px; }
.src-name  { font-size: 0.8rem; font-weight: 600; color: var(--text-primary); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin-bottom: 3px; }
.src-pages { display: inline-flex; align-items: center; gap: 4px; background: rgba(79,156,249,0.1); color: var(--accent); border: 1px solid rgba(79,156,249,0.2); border-radius: 20px; padding: 1px 8px; font-size: 0.68rem; font-family: 'DM Mono', monospace; font-weight: 500; }

/* ── Config sections ── */
.cfg-section { background: var(--bg-card); border: 1px solid var(--border); border-radius: var(--radius-lg); padding: 1.4rem 1.6rem; margin-bottom: 1.1rem; position: relative; overflow: hidden; }
.cfg-section::after { content: ''; position: absolute; top: 0; right: 0; width: 100px; height: 100px; border-radius: 50%; background: radial-gradient(circle, var(--accent-glow), transparent 70%); transform: translate(35px, -35px); pointer-events: none; }
.cfg-title { font-size: 0.72rem; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: var(--text-muted); margin-bottom: 1.1rem; display: flex; align-items: center; gap: 8px; }
.cfg-icon  { width: 24px; height: 24px; border-radius: 6px; background: var(--accent-glow); border: 1px solid rgba(79,156,249,0.22); display: flex; align-items: center; justify-content: center; font-size: 0.82rem; }

/* ── Doc list in config ── */
.doc-item  { display: flex; align-items: center; gap: 9px; padding: 0.5rem 0.8rem; background: var(--bg-hover); border: 1px solid var(--border); border-radius: 9px; margin-bottom: 5px; }
.di-icon   { color: var(--danger); font-size: 0.9rem; flex-shrink: 0; }
.di-name   { flex: 1; font-size: 0.8rem; color: var(--text-primary); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.doc-empty { font-size: 0.8rem; color: var(--text-dim); padding: 0.5rem 0; }

/* ── Form elements ── */
.stNumberInput input, .stTextInput input { background: var(--bg-hover) !important; border: 1px solid var(--border) !important; border-radius: 9px !important; color: var(--text-primary) !important; font-family: 'Syne', sans-serif !important; font-size: 0.84rem !important; transition: border-color 0.16s, box-shadow 0.16s !important; }
.stNumberInput input:focus, .stTextInput input:focus { border-color: var(--border-focus) !important; box-shadow: 0 0 0 3px rgba(79,156,249,0.07) !important; outline: none !important; }
[data-baseweb="select"] > div { background: var(--bg-hover) !important; border: 1px solid var(--border) !important; border-radius: 9px !important; color: var(--text-primary) !important; font-size: 0.84rem !important; }
[data-baseweb="select"] > div:focus-within { border-color: var(--border-focus) !important; box-shadow: 0 0 0 3px rgba(79,156,249,0.07) !important; }
[data-baseweb="popover"] [role="listbox"] { background: var(--bg-card) !important; border: 1px solid var(--border) !important; border-radius: 9px !important; }
[data-baseweb="popover"] [role="option"] { background: transparent !important; color: var(--text-muted) !important; font-size: 0.83rem !important; }
[data-baseweb="popover"] [role="option"]:hover, [data-baseweb="popover"] [aria-selected="true"] { background: var(--bg-hover) !important; color: var(--text-primary) !important; }
label[data-testid="stWidgetLabel"], .stSlider label, .stToggle label { font-size: 0.78rem !important; font-weight: 600 !important; color: var(--text-muted) !important; letter-spacing: 0.025em !important; }
[data-testid="stToggle"] [role="checkbox"]                      { background: var(--bg-hover) !important; border: 1px solid var(--border) !important; }
[data-testid="stToggle"] [aria-checked="true"][role="checkbox"] { background: var(--accent) !important; border-color: var(--accent) !important; }
[data-baseweb="slider"] [role="slider"] { background: var(--accent) !important; border-color: var(--accent) !important; }

/* ── Buttons ── */
.stButton button { background: var(--bg-hover) !important; border: 1px solid var(--border) !important; border-radius: var(--radius) !important; color: var(--text-muted) !important; font-family: 'Syne', sans-serif !important; font-size: 0.82rem !important; font-weight: 600 !important; letter-spacing: 0.03em !important; transition: all 0.16s ease !important; }
.stButton button:hover { background: rgba(255,255,255,0.05) !important; border-color: rgba(255,255,255,0.14) !important; color: var(--text-primary) !important; transform: translateY(-1px) !important; box-shadow: 0 4px 12px rgba(0,0,0,0.25) !important; }
.btn-primary button { background: linear-gradient(135deg, var(--accent), #3b82f6) !important; border: none !important; color: #fff !important; font-weight: 700 !important; }
.btn-primary button:hover { opacity: 0.9 !important; color: #fff !important; box-shadow: 0 6px 18px rgba(79,156,249,0.3) !important; }
.btn-success button { background: rgba(52,211,153,0.1) !important; border-color: rgba(52,211,153,0.25) !important; color: var(--success) !important; }
.btn-success button:hover { background: rgba(52,211,153,0.17) !important; color: var(--success) !important; box-shadow: 0 4px 12px rgba(52,211,153,0.15) !important; }
.btn-danger  button { background: rgba(248,113,113,0.08) !important; border-color: rgba(248,113,113,0.22) !important; color: var(--danger) !important; }
.btn-danger  button:hover { background: rgba(248,113,113,0.15) !important; color: var(--danger) !important; }

/* ── Alerts ── */
[data-testid="stInfo"]    { background: rgba(79,156,249,0.07)  !important; border: 1px solid rgba(79,156,249,0.18)  !important; border-radius: var(--radius) !important; color: var(--text-muted) !important; font-size: 0.81rem !important; }
[data-testid="stSuccess"] { background: rgba(52,211,153,0.07)  !important; border: 1px solid rgba(52,211,153,0.2)   !important; border-radius: var(--radius) !important; color: var(--success)    !important; font-size: 0.81rem !important; }
[data-testid="stWarning"] { background: rgba(251,191,36,0.07)  !important; border: 1px solid rgba(251,191,36,0.2)   !important; border-radius: var(--radius) !important; color: var(--warning)    !important; font-size: 0.81rem !important; }
[data-testid="stError"]   { background: rgba(248,113,113,0.07) !important; border: 1px solid rgba(248,113,113,0.2)  !important; border-radius: var(--radius) !important; color: var(--danger)     !important; font-size: 0.81rem !important; }

/* ── Misc ── */
[data-testid="stSpinner"] p { color: var(--text-muted) !important; font-size: 0.81rem !important; }
hr { border-color: var(--border) !important; margin: 0.6rem 0 !important; }
[data-testid="stMetric"] { display: none !important; }
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--bg-hover); border-radius: 10px; }
</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

if "rag" not in st.session_state:
    st.session_state.rag = None

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# CONSTANTS
# ============================================================

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ============================================================
# HELPERS
# ============================================================

def get_uploaded_pdfs():
    if not os.path.exists(UPLOAD_DIR):
        return []
    return sorted([
        f for f in os.listdir(UPLOAD_DIR)
        if f.lower().endswith(".pdf")
    ])


def build_knowledge_base():
    config = load_config()
    pdf_files = get_uploaded_pdfs()
    config["documents"] = [os.path.join(UPLOAD_DIR, p) for p in pdf_files]
    config["use_existing_data"] = False
    save_config(config)
    with st.spinner("Building knowledge base… this may take a moment."):
        RAG(config)
    config["use_existing_data"] = True
    save_config(config)
    st.session_state.rag = None


def fmt_size(n):
    kb = n / 1024
    return f"{kb/1024:.1f} MB" if kb >= 1024 else f"{kb:.0f} KB"


def on_badge(on):
    cls   = "badge-on"  if on else "badge-off"
    label = "ON"        if on else "OFF"
    return f'<span class="badge {cls}"><span class="badge-dot"></span>{label}</span>'


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("""
    <div class="sidebar-brand">
        <div class="brand-icon">🔮</div>
        <div>
            <div class="brand-name">Enterprise RAG</div>
            <div class="brand-sub">AI Platform · v2.0</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Navigation ──
    st.markdown('<div class="sb-label">Navigate</div>', unsafe_allow_html=True)
    page = st.radio(
        "Navigation",
        ["💬  Chat", "⚙️  Configuration"],
        label_visibility="collapsed",
    )

    # ── Live system status ──
    config = load_config()
    pdf_count = len(get_uploaded_pdfs())

    st.markdown('<div class="sb-label">System Status</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="sb-metrics">
        <div class="sb-metric">
            <span class="sb-metric-label">Retriever</span>
            <span class="sb-metric-value">{config["retriever_type"].upper()}</span>
        </div>
        <div class="sb-metric">
            <span class="sb-metric-label">Top K</span>
            <span class="sb-metric-value">{config["top_k"]}</span>
        </div>
        <div class="sb-metric">
            <span class="sb-metric-label">History</span>
            <span class="sb-metric-value">{config["conversation_max_history"]}</span>
        </div>
        <div class="sb-metric">
            <span class="sb-metric-label">Documents</span>
            <span class="sb-metric-value">{pdf_count}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# CHAT PAGE
# ============================================================

def show_chat():
    config = load_config()

    st.markdown("""
    <div class="page-header">
        <div class="page-title">RAG <span>Assistant</span></div>
        <div class="page-subtitle">Semantic Search · Query Rewriting · Reranking</div>
    </div>
    """, unsafe_allow_html=True)

    # Status bar
    st.markdown(f"""
    <div class="stat-row">
        <div class="stat-card">
            <div class="stat-lbl">Retriever</div>
            <div class="stat-val">{config["retriever_type"].upper()}</div>
        </div>
        <div class="stat-card">
            <div class="stat-lbl">Query Rewrite</div>
            <div class="stat-val">{on_badge(config["enable_query_rewriting"])}</div>
        </div>
        <div class="stat-card">
            <div class="stat-lbl">Reranking</div>
            <div class="stat-val">{on_badge(config["enable_reranking"])}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Guard: no documents uploaded yet
    pdf_files = get_uploaded_pdfs()
    if not pdf_files:
        st.markdown("""
        <div class="no-docs-card">
            <span class="nd-icon">⚠️</span>
            <div class="nd-text">
                <strong>No documents in the knowledge base.</strong><br>
                Upload PDFs from the sidebar or the Configuration page, then rebuild the knowledge base.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.stop()

    # Init RAG
    if st.session_state.rag is None:
        with st.spinner("Loading RAG system…"):
            st.session_state.rag = RAG(config=config)

    # Message history
    if not st.session_state.messages:
        st.markdown("""
        <div class="empty-state">
            <div class="es-icon">🔮</div>
            <div class="es-title">Ready to answer</div>
            <div class="es-desc">Ask anything about your documents.<br>I'll retrieve the most relevant context.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # Chat input
    query = st.chat_input("Ask anything about your documents…")

    if query:
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)

        with st.spinner("Searching knowledge base…"):
            response = st.session_state.rag.ask(
                query, hide_auto_regressive_output=True
            )

        answer  = response["answer"]
        sources = response["sources"]

        with st.chat_message("assistant"):
            st.markdown(answer)

            if sources:
                with st.expander(
                    f"📄 {len(sources)} source{'s' if len(sources) != 1 else ''} referenced"
                ):
                    for src in sources:
                        p0, p1 = src["pages"][0], src["pages"][1]
                        st.markdown(f"""
                        <div class="src-card">
                            <span style="font-size:0.95rem;flex-shrink:0;margin-top:1px;">📄</span>
                            <div style="flex:1;min-width:0;">
                                <div class="src-name">{src["source_file"]}</div>
                                <span class="src-pages">pp.&nbsp;{p0}&nbsp;–&nbsp;{p1}</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

        st.session_state.messages.append({"role": "assistant", "content": answer})

    # Clear button — only shown when there are messages
    if st.session_state.messages:
        st.markdown('<div class="btn-danger" style="margin-top:0.5rem;">', unsafe_allow_html=True)
        if st.button("🗑️ Clear conversation"):
            st.session_state.messages = []
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# CONFIGURATION PAGE
# ============================================================

def show_configuration():
    config = load_config()

    st.markdown("""
    <div class="page-header">
        <div class="page-title">System <span>Configuration</span></div>
        <div class="page-subtitle">Manage documents · Tune retrieval &amp; generation</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Knowledge Base ──────────────────────────────────────
    st.markdown("""
    <div class="cfg-section">
        <div class="cfg-title"><div class="cfg-icon">📚</div>Knowledge Base</div>
    """, unsafe_allow_html=True)

    pdf_files = get_uploaded_pdfs()
    col_docs, col_stats = st.columns([2, 1], gap="medium")

    with col_docs:
        st.markdown(
            "<div style='font-size:0.78rem;font-weight:600;color:var(--text-muted);margin-bottom:0.55rem;'>Current documents</div>",
            unsafe_allow_html=True,
        )
        if pdf_files:
            for pdf in pdf_files:
                st.markdown(f"""
                <div class="doc-item">
                    <span class="di-icon">📄</span>
                    <span class="di-name">{pdf}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(
                '<div class="doc-empty">No PDFs found in the knowledge base.</div>',
                unsafe_allow_html=True,
            )

    with col_stats:
        st.markdown(
            "<div style='font-size:0.78rem;font-weight:600;color:var(--text-muted);margin-bottom:0.55rem;'>Stats</div>",
            unsafe_allow_html=True,
        )
        st.markdown(f"""
        <div class="sb-metrics">
            <div class="sb-metric">
                <span class="sb-metric-label">Documents</span>
                <span class="sb-metric-value">{len(pdf_files)}</span>
            </div>
            <div class="sb-metric">
                <span class="sb-metric-label">Chunk size</span>
                <span class="sb-metric-value">{config["chunk_size"]}</span>
            </div>
            <div class="sb-metric">
                <span class="sb-metric-label">Overlap</span>
                <span class="sb-metric-value">{config["overlap"]}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)

    # Upload widget
    uploaded_files = st.file_uploader(
        "Upload new PDF documents",
        type=["pdf"],
        accept_multiple_files=True,
        help="Upload one or more PDFs, then choose to add them or replace the entire knowledge base.",
    )

    if uploaded_files:
        for f in uploaded_files:
            st.markdown(f"""
            <div class="pdf-chip">
                <span>📄</span>
                <span class="chip-name">{f.name}</span>
                <span class="chip-size">{fmt_size(f.size)}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='margin-top:0.7rem;'></div>", unsafe_allow_html=True)
        col_add, col_replace = st.columns(2, gap="small")

        with col_add:
            st.markdown('<div class="btn-success">', unsafe_allow_html=True)
            if st.button("➕ Add to KB", use_container_width=True,
                         help="Append uploaded PDFs to the existing knowledge base"):
                for pdf in uploaded_files:
                    with open(os.path.join(UPLOAD_DIR, pdf.name), "wb") as fh:
                        fh.write(pdf.getbuffer())
                build_knowledge_base()
                st.success(f"✓ Added {len(uploaded_files)} document(s) and rebuilt KB.")
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        with col_replace:
            st.markdown('<div class="btn-danger">', unsafe_allow_html=True)
            if st.button("🔄 Replace & Rebuild", use_container_width=True,
                         help="Remove all existing PDFs, save these, and rebuild"):
                for fname in os.listdir(UPLOAD_DIR):
                    if fname.lower().endswith(".pdf"):
                        os.remove(os.path.join(UPLOAD_DIR, fname))
                for pdf in uploaded_files:
                    with open(os.path.join(UPLOAD_DIR, pdf.name), "wb") as fh:
                        fh.write(pdf.getbuffer())
                build_knowledge_base()
                st.success("✓ Knowledge base replaced and rebuilt.")
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    elif pdf_files:
        st.markdown("<div style='margin-top:0.65rem;'></div>", unsafe_allow_html=True)
        st.markdown('<div class="btn-success">', unsafe_allow_html=True)
        if st.button("🔁 Rebuild Knowledge Base", use_container_width=True,
                     help="Re-index current documents with updated chunk settings"):
            build_knowledge_base()
            st.success("✓ Knowledge base rebuilt.")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)  # end cfg-section

    # ── Chunking ────────────────────────────────────────────
    st.markdown("""
    <div class="cfg-section">
        <div class="cfg-title"><div class="cfg-icon">✂️</div>Chunking</div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        chunk_size = st.number_input(
            "Chunk Size",
            min_value=100, max_value=2000,
            value=config["chunk_size"], step=50,
            help="Number of tokens per document chunk"
        )
    with col2:
        overlap = st.number_input(
            "Chunk Overlap",
            min_value=0, max_value=500,
            value=config["overlap"], step=10,
            help="Token overlap between adjacent chunks"
        )

    st.info("⚠️  Chunk settings only take effect after rebuilding the knowledge base.")
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Retrieval ───────────────────────────────────────────
    st.markdown("""
    <div class="cfg-section">
        <div class="cfg-title"><div class="cfg-icon">🔍</div>Retrieval</div>
    """, unsafe_allow_html=True)

    retriever_options = ["faiss", "bm25", "hybrid"]
    col1, col2 = st.columns(2, gap="medium")
    with col1:
        retriever_type = st.selectbox(
            "Retriever Type",
            retriever_options,
            index=retriever_options.index(config["retriever_type"]),
            help="Vector (FAISS), lexical (BM25), or combined (Hybrid)"
        )
    with col2:
        top_k = st.slider(
            "Top K Documents",
            min_value=1, max_value=20, value=config["top_k"],
            help="Number of chunks retrieved per query"
        )

    enable_query_rewriting = st.toggle(
        "Enable Query Rewriting",
        value=config["enable_query_rewriting"],
        help="LLM rewrites the query using conversation history before retrieval"
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Reranking ───────────────────────────────────────────
    st.markdown("""
    <div class="cfg-section">
        <div class="cfg-title"><div class="cfg-icon">🎯</div>Reranking</div>
    """, unsafe_allow_html=True)

    enable_reranking = st.toggle(
        "Enable Reranking",
        value=config["enable_reranking"],
        help="Cross-encoder re-scores retrieved chunks for higher precision"
    )
    reranking_top_k = st.slider(
        "Reranking Top K",
        min_value=1, max_value=20, value=config["reranking_top_k"],
        disabled=not enable_reranking,
        help="Final number of chunks kept after reranking"
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # ── LLM ────────────────────────────────────────────────
    st.markdown("""
    <div class="cfg-section">
        <div class="cfg-title"><div class="cfg-icon">🤖</div>Language Model</div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        llm_model = st.text_input(
            "Model Name",
            value=config["llm_model"],
            placeholder="e.g. qwen2.5:3b, llama3.2",
            help="Ollama model identifier"
        )
    with col2:
        conversation_max_history = st.slider(
            "Conversation History",
            min_value=1, max_value=20,
            value=config["conversation_max_history"],
            help="Number of prior turns included in the prompt context"
        )
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Save ───────────────────────────────────────────────
    st.markdown('<div class="btn-primary">', unsafe_allow_html=True)
    if st.button("💾 Save Configuration", use_container_width=True):
        config.update({
            "chunk_size":               chunk_size,
            "overlap":                  overlap,
            "retriever_type":           retriever_type,
            "top_k":                    top_k,
            "enable_query_rewriting":   enable_query_rewriting,
            "enable_reranking":         enable_reranking,
            "reranking_top_k":          reranking_top_k,
            "llm_model":                llm_model,
            "conversation_max_history": conversation_max_history,
        })
        save_config(config)
        st.success("✓ Configuration saved. The next query will use the updated settings.")
        st.session_state.rag = None   # Force RAG reload on next query
    st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# ROUTING
# ============================================================

if "Chat" in page:
    show_chat()
else:
    show_configuration()