import streamlit as st
import pandas as pd
import json
import plotly.express as px
from datetime import datetime

# =================================================================
# RETURN GUARD v0.2 - FULL PROTOTYPE FOR INVESTORS (CLEANED)
# =================================================================

# Konfiguration
st.set_page_config(
    page_title="ReturnGuard | Ihr Leasing-Schutzschild",
    page_icon="🛡️",
    layout="wide"
)

# Professionelles Styling (ReturnGuard Brand)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #f9fafb; }
    
    /* Hero Section */
    .hero { background: linear-gradient(135deg, #1B365D 0%, #1E3A8A 100%); color: white; padding: 3rem; border-radius: 15px; margin-bottom: 2rem; }
    
    /* Veto & Status Cards */
    .veto-card { background: #fff1f2; border-left: 5px solid #e11d48; padding: 1.5rem; border-radius: 8px; margin: 10px 0; }
    .info-card { background: #f0fdf4; border-left: 5px solid #16a34a; padding: 1rem; border-radius: 8px; }
    
    /* Sidebar */
    .css-1d391kg { background-color: #ffffff !important; }
</style>
""", unsafe_allow_html=True)

# ==================== LOGIK & DATEN-HUB ====================
if 'rg_data' not in st.session_state:
    st.session_state.rg_data = {
        "vehicle": {"brand": "---", "model": "---", "vin": "---", "ez": "---"},
        "analysis": {"vetos": [], "savings": 0, "status": "Green"},
        "is_scanned": False
    }

def run_ocr_simulation():
    st.session_state.rg_data["vehicle"] = {
        "brand": "Volkswagen", "model": "Golf VIII GTE",
        "vin": "WVGZZZ1K7FW00XXXX", "ez": "03/2022"
    }
    st.session_state.rg_data["is_scanned"] = True
    st.toast("Fahrzeugschein-Daten extrahiert!", icon="📄")

# ==================== SIDEBAR ====================
with st.sidebar:
    st.title("🛡️ ReturnGuard")
    st.caption("Version 0.2 | Investor Showcase")
    st.divider()
    
    # Menü ohne Emojis in den Strings für maximale Stabilität
    menu_options = ["Home", "Expert-Check", "Shadow Expert", "Partner-Portal", "Fleet-Portal", "Investor Dashboard"]
    page = st.radio("Menü wählen:", menu_options)
    
    st.divider()
    if st.button("📸 Fahrzeugschein scannen"):
        run_ocr_simulation()
    
    if st.session_state.rg_data["is_scanned"]:
        st.success(f"Aktiv: {st.session_state.rg_data['vehicle']['model']}")

# ==================== PAGE 1: HOME ====================
if page == "Home":
    st.markdown("""
    <div class="hero">
        <h1>Die Zukunft der Leasingrückgabe.</h1>
        <p>ReturnGuard schützt Leasingnehmer vor unberechtigten Nachforderungen durch herstellerunabhängige Prüfung & Rechts-KI.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("🏠 1. Vor-Check")
        st.write("Prüfen Sie Ihr Fahrzeug modular nach den 14 Vest-Punkten.")
    with col2:
        st.subheader("⚖️ 2. Shadow Expert")
        st.write("Wir prüfen Händler-Gutachten gegen offizielle Hersteller-Kataloge.")
    with col3:
        st.subheader("💰 3. Geld sparen")
        st.write("Ersparnis durch Veto-Logik und Partner-Netzwerk.")

# ==================== PAGE 2: EXPERT-CHECK ====================
elif page == "Expert-Check":
    st.title("🔍 Modularer Expert-Check")
    st.info("Klicken Sie auf die Bereiche, um Schäden zu dokumentieren.")

    with st.expander("🚗 Außenhaut & Karosserie", expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            delle = st.checkbox("Delle / Beule vorhanden")
            kratzer = st.checkbox("Kratzer (Lackbeschädigung)")
        with c2:
            if delle:
                size = st.slider("Größe der Delle (mm)", 5, 50, 15)
                if size <= 20:
                    st.markdown('<div class="info-card">💡 <b>Shadow Expert:</b> Dellen < 20mm gelten bei VWFS/Audi als akzeptierter Verschleiß. 0€ Kosten.</div>', unsafe_allow_html=True)
                else:
                    st.warning("⚠️ Reparaturpflichtiger Schaden (> 20mm).")

    with st.expander("🎡 Fahrwerk & Räder"):
        felge = st.checkbox("Bordsteinschaden")
        if felge:
            tiefe = st.number_input("Tiefe (mm)", 0.1, 5.0, 0.5)
            if tiefe < 1.0:
                st.info("💡 **Shadow Expert:** Kratzer < 1mm Tiefe sind laut BMW meist zulässig.")

# ==================== PAGE 3: SHADOW EXPERT ====================
elif page == "Shadow Expert":
    st.title("⚖️ Shadow Expert: Veto-Analyse")
    st.write("Laden Sie das Gutachten des Händlers hoch.")
    
    up = st.file_uploader("Gutachten hochladen", type=["pdf", "jpg"])
    
    if up or st.button("Beispiel-Analyse starten"):
        st.markdown("""
        <div class="veto-card">
            <h3>❌ VETO GEFUNDEN</h3>
            <p><b>Position:</b> Stoßfänger vorne (Lackierung)<br>
            <b>Händler-Forderung:</b> 480,00 €</p>
            <p><b>Begründung:</b> Kratzer ist polierbar. Laut OLG Stuttgart (Az. 6 U 84/24) normale Gebrauchsspur.</p>
            <h4 style="color: #e11d48;">Ersparnis-Potenzial: 480,00 €</h4>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Anwaltliche Hilfe anfordern (Referral)"):
            st.success("Anfrage an Partner-Fachanwalt übermittelt!")

# ==================== PAGE 4: PARTNER-PORTAL ====================
elif page == "Partner-Portal":
    st.title("🛠️ Partner-Portal: Lead-Marktplatz")
    st.write("Exklusive Reparatur-Aufträge für Werkstätten.")

    tab_leads, tab_stats = st.tabs(["🎯 Offene Leads", "📈 Performance"])
    with tab_leads:
        with st.container():
            c_l1, c_l2 = st.columns([3, 1])
            with c_l1:
                st.markdown("**Anfrage #8821 - VW Golf VIII** | Delle Tür | Potenzial: ~180€")
            with c_l2:
                if st.button("Lead kaufen (15€)", key="lead1"):
                    st.success("Gekauft!")
        st.divider()

# ==================== PAGE 5: FLEET-PORTAL ====================
elif page == "Fleet-Portal":
    st.title("🏢 Fleet Manager Cockpit")
    st.metric("Veto-Ersparnis (YTD)", "5.420 €")
    data = {"Kennzeichen": ["M-RG 101", "M-RG 102"], "Status": ["🔴 Risiko", "🟢 OK"]}
    st.table(pd.DataFrame(data))

# ==================== PAGE 6: INVESTOR DASHBOARD ====================
elif page == "Investor Dashboard":
    st.title("📊 Investor Relations")
    fig = px.bar(x=["TAM", "SAM", "SOM"], y=[1750, 200, 5], title="Markt (Mio. €)")
    st.plotly_chart(fig, use_container_width=True)
    st.write("**Revenue Streams:** B2C Check-Fees, B2B Lead-Fees, Legal Referrals.")
