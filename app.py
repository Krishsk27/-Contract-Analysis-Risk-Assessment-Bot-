import streamlit as st
import pandas as pd
import json

# Import Custom Modules
from src.document_processor import DocumentProcessor
from src.llm_engine import ContractAnalyzer
from src.audit_logger import AuditLogger
from src.report_generator import generate_pdf_report
from src.utils import highlight_text 

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="ContractSentinel AI",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# 2. PREMIUM CSS OVERHAUL
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    /* IMPORT FONTS */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    /* GLOBAL RESET */
    * {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    
    .stApp {
        background-color: #f3f4f6;
    }

    /* HIDE STREAMLIT CHROME */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* SIDEBAR STYLING */
    [data-testid="stSidebar"] {
        background-color: #0f172a; /* Midnight Blue */
        border-right: none;
    }
    [data-testid="stSidebar"] * {
        color: #94a3b8;
    }
    [data-testid="stSidebar"] h1 {
        color: white;
        font-size: 1.5rem;
    }

    /* CUSTOM GRADIENT BUTTONS */
    div.stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 12px;
        font-weight: 600;
        box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.3);
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.4);
    }
    
    /* GLASSMORPHISM CARDS */
    .premium-card {
        background: white;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        border: 1px solid rgba(255,255,255,0.5);
        margin-bottom: 24px;
    }
    
    /* METRIC WIDGETS */
    [data-testid="stMetric"] {
        background: white;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        border: 1px solid #e5e7eb;
    }
    [data-testid="stMetricLabel"] {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748b;
    }
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #0f172a;
    }

    /* RISK BADGES */
    .badge-high {
        background: #fee2e2;
        color: #991b1b;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        display: inline-block;
    }
    .badge-medium {
        background: #ffedd5;
        color: #9a3412;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        display: inline-block;
    }

    /* DOCUMENT PREVIEW */
    .doc-paper {
        background: white;
        padding: 40px;
        min-height: 600px;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        border-radius: 4px;
        font-family: 'Georgia', serif;
        line-height: 1.8;
        color: #334155;
    }

    /* HERO GRADIENT TEXT */
    .gradient-text {
        background: linear-gradient(to right, #2563eb, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 3. SESSION STATE
# -----------------------------------------------------------------------------
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None
if "full_text" not in st.session_state:
    st.session_state.full_text = ""
if "current_filename" not in st.session_state:
    st.session_state.current_filename = ""

analyzer = ContractAnalyzer()
logger = AuditLogger()

# -----------------------------------------------------------------------------
# 4. DARK SIDEBAR NAVIGATION
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("<h1 style='color:white; margin-bottom:0;'>Contract<span style='color:#3b82f6'>Sentinel</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.8rem; opacity:0.6; margin-top:0;'>ENTERPRISE EDITION v2.0</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("### ⚙️ **Configuration**")
    target_lang = st.radio("Target Language", ["English", "Hindi"], label_visibility="collapsed")
    
    st.markdown("### 📂 **Upload File**")
    uploaded_file = st.file_uploader("Upload Contract", type=["pdf", "docx", "txt"], label_visibility="collapsed")
    
    if uploaded_file:
        st.success(f" Ready: {uploaded_file.name}")
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("✨ START ANALYSIS", type="primary", use_container_width=True):
            with st.spinner("🤖 AI Consultant is reviewing..."):
                text, error = DocumentProcessor.extract_text(uploaded_file)
                if error:
                    st.error(error)
                else:
                    st.session_state.full_text = text
                    st.session_state.current_filename = uploaded_file.name
                    result = analyzer.analyze_contract(text, language=target_lang)
                    if "error" in result:
                        st.error(result["error"])
                    else:
                        st.session_state.analysis_result = result
                        logger.log_event("ANALYSIS", uploaded_file.name, result.get("risk_score", 0))

    st.markdown("---")
    st.markdown("<div style='background:#1e293b; padding:15px; border-radius:10px; font-size:0.8rem; color:#94a3b8;'>🔒 <b>Secure Enclave</b><br>Your documents are processed locally and never stored.</div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 5. MAIN DASHBOARD
# -----------------------------------------------------------------------------

# HERO SECTION
if not st.session_state.analysis_result:
    st.markdown("""
    <div style="text-align: center; padding: 60px 20px;">
        <h1 style="font-size: 3.5rem; margin-bottom: 20px;">
            AI-Powered Legal <span class="gradient-text">Intelligence</span>
        </h1>
        <p style="font-size: 1.25rem; color: #64748b; max-width: 700px; margin: 0 auto 40px auto;">
            Transform complex contracts into clear, actionable insights in seconds. 
            Upload a document to detect risks, ensure compliance, and draft amendments instantly.
        </p>
        <div style="display: flex; justify-content: center; gap: 20px;">
            <div class="premium-card" style="width: 200px; text-align: center;">
                <div style="font-size: 2rem;">⚡</div>
                <div style="font-weight: 600; margin-top: 10px;">Instant Audit</div>
            </div>
            <div class="premium-card" style="width: 200px; text-align: center;">
                <div style="font-size: 2rem;">🛡️</div>
                <div style="font-weight: 600; margin-top: 10px;">Risk Shield</div>
            </div>
            <div class="premium-card" style="width: 200px; text-align: center;">
                <div style="font-size: 2rem;">📝</div>
                <div style="font-weight: 600; margin-top: 10px;">Smart Draft</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# RESULTS DASHBOARD
else:
    res = st.session_state.analysis_result
    
    # 1. HEADER
    c1, c2 = st.columns([2,1])
    with c1:
        st.markdown(f"## 📊 Audit Report: **{st.session_state.current_filename}**")
    with c2:
        st.markdown(f"<div style='text-align:right; padding-top:10px;'><span class='badge-high'>CONFIDENTIAL</span></div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

    # 2. KEY METRICS
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        score = res.get('risk_score', 0)
        st.metric("Safety Score", f"{score}/100", delta="- Critical" if score > 70 else "+ Secure")
    with m2:
        st.metric("Risk Assessment", res.get('overall_risk_level', 'N/A'))
    with m3:
        st.metric("Document Type", res.get('contract_type', 'General'))
    with m4:
        st.metric("Jurisdiction", "India (ISO)")
    
    st.markdown("<br>", unsafe_allow_html=True)

    # 3. CONTENT TABS
    tab1, tab2, tab3 = st.tabs(["👁️ Visual Analysis", "⚖️ Compliance & Risks", "📤 Export Tools"])

    # TAB 1: VISUAL ANALYSIS
    with tab1:
        col_doc, col_ins = st.columns([1.5, 1])
        
        with col_doc:
            st.markdown("##### 📄 Document Viewer")
            # Apply the "Paper" effect
            highlighted = highlight_text(st.session_state.full_text, res.get('clauses', []))
            st.markdown(f'<div class="doc-paper">{highlighted}</div>', unsafe_allow_html=True)
            
        with col_ins:
            st.markdown("##### 🧠 AI Consultant Insights")
            
            # ADVICE CARD
            advice = res.get('executive_advice', res.get('summary', ''))
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1e3a8a 0%, #172554 100%); color: white; padding: 25px; border-radius: 16px; box-shadow: 0 10px 15px -3px rgba(30, 58, 138, 0.4); margin-bottom: 25px;">
                <div style="font-weight: 700; font-size: 1.1rem; margin-bottom: 10px; display: flex; align-items: center; gap: 10px;">
                    ✨ Executive Summary
                </div>
                <div style="line-height: 1.6; opacity: 0.9;">{advice}</div>
            </div>
            """, unsafe_allow_html=True)

            # RISK FEED
            st.markdown("##### 🚨 Detected Issues")
            clauses = res.get('clauses', [])
            risky = [c for c in clauses if c.get('risk_level') in ['High', 'Medium']]
            
            for c in risky:
                risk_badge = "badge-high" if c['risk_level'] == "High" else "badge-medium"
                icon = "🔥" if c['risk_level'] == "High" else "⚠️"
                
                st.markdown(f"""
                <div class="premium-card" style="padding: 20px; border-left: 4px solid {'#ef4444' if c['risk_level'] == 'High' else '#f97316'};">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 8px;">
                        <span style="font-weight: 700; color: #1e293b;">{c['title']}</span>
                        <span class="{risk_badge}">{c['risk_level']}</span>
                    </div>
                    <p style="font-size: 0.9rem; color: #475569; margin-bottom: 12px;">{c['explanation']}</p>
                    <div style="background: #f8fafc; padding: 10px; border-radius: 8px; font-size: 0.85rem; border: 1px dashed #cbd5e1;">
                        <strong style="color: #059669;">✅ Recommendation:</strong> {c['recommendation']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # TAB 2: COMPLIANCE
    with tab2:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="premium-card">', unsafe_allow_html=True)
            st.subheader("🇮🇳 Indian Law Compliance")
            comp = res.get('compliance_check', {})
            if comp.get('status') == "Fail":
                st.error(f"{comp.get('notes')}")
            else:
                st.success(f"{comp.get('notes')}")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with c2:
            st.markdown('<div class="premium-card">', unsafe_allow_html=True)
            st.subheader("📋 Missing Clauses")
            missing = res.get('missing_clauses', [])
            if missing:
                for m in missing:
                    st.warning(f"⚠️ Missing: {m}")
            else:
                st.info("✅ All standard clauses are present.")
            st.markdown('</div>', unsafe_allow_html=True)

    # TAB 3: EXPORT
    with tab3:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.subheader("📤 Export & Share")
        col_pdf, col_json = st.columns(2)
        
        with col_pdf:
            st.markdown(" **Download PDF Report**")
            st.caption("Professional format for legal review.")
            try:
                pdf_data = generate_pdf_report(res, st.session_state.current_filename)
                st.download_button("📥 Download PDF", pdf_data, "report.pdf", "application/pdf", use_container_width=True)
            except:
                st.error("PDF generation failed.")
                
        with col_json:
            st.markdown("**Download Raw Data**")
            st.caption("JSON format for developers.")
            st.download_button("📥 Download JSON", json.dumps(res, indent=4), "data.json", "application/json", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)