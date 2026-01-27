import streamlit as st
import pandas as pd
import json
from datetime import datetime, timedelta

# ==================== CONFIGURATION & THEME ====================
st.set_page_config(
    page_title="ReturnGuard v0.2 | Professional Leasing Protection",
    page_icon="🛡️",
    layout="wide"
)

# Custom CSS für den Investor-Showcase Look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main { background-color: #f8f9fa; }
    .stButton>button { 
        background: linear-gradient(135deg, #1B365D 0%, #1E3A8A 100%); 
        color: white; border-radius: 8px; border: none; padding: 0.5rem 1rem;
    }
    .veto-card { 
        background-color: #fff1f2; border-left: 5px solid #e11d48; 
        padding: 1.5rem; border-radius: 8px; margin: 1rem 0;
    }
    .savings-badge {
        background-color: #dcfce7; color: #166534;
        padding: 0.5rem 1rem; border-radius: 20px; font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ==================== DATA HEART (SESSION STATE) ====================
if 'rg_data' not in st.session_state:
    st.session_state.rg_data = {
        "vehicle": {"vin": "---", "brand": "---", "model": "---", "year": "---", "mileage": 0},
        "customer": {"name": "---", "address": "---", "email": "---"},
        "assessment": {"damages": [], "vetos": [], "confidence": 0.0},
        "financials": {"dealer_total": 0.0, "rg_total": 0.0, "savings": 0.0},
        "is_ocr_done": False
    }

# ==================== HELPER FUNCTIONS ====================
def simulate_ocr():
    """Simuliert den Deep-Scan des Fahrzeugscheins"""
    st.session_state.rg_data["vehicle"] = {
        "vin": "WVGZZZ1K7FW001234",
        "brand": "Volkswagen",
        "model": "Golf VIII (GTE)",
        "year": "2022",
        "mileage": 42500
    }
    st.session_state.rg_data["customer"] = {
        "name": "Max Mustermann",
        "address": "Musterstraße 1, 80331 München",
        "email": "max.mustermann@email.de"
    }
    st.session_state.rg_data["is_ocr_done"] = True
    st.toast("Fahrzeugschein erfolgreich gescannt!", icon="✅")

# ==================== SIDEBAR NAVIGATION ====================
with st.sidebar:
    st.image("https://via.placeholder.com/150x50?text=ReturnGuard", width=150)
    st.title("Navigation")
    page = st.radio("Bereich wählen:", [
        "🏠 Home", 
        "🔍 Expert-Check", 
        "🛡️ Shadow Expert (Veto)", 
        "🏢 Fleet-Portal", 
        "📊 Investor-Dashboard"
    ])
    
    st.divider()
    if st.button("📄 Fahrzeugschein scannen (OCR)"):
        simulate_ocr()

# ==================== PAGE 1: HOME ====================
if page == "🏠 Home":
    st.title("Willkommen bei ReturnGuard")
    st.subheader("Ihr digitaler Schutzschild bei der Leasingrückgabe.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        ### Warum ReturnGuard?
        * **Unabhängig:** Wir prüfen Händlerforderungen gegen Hersteller-Kataloge.
        * **Rechtssicher:** Inklusive aktueller OLG-Urteile (z.B. OLG Stuttgart 2025).
        * **Kosteneffizient:** Durchschnittliche Ersparnis von **850 € pro Rückgabe**.
        """)
        if st.button("Jetzt Expert-Check starten"):
            st.info("Bitte nutzen Sie die Navigation links, um fortzufahren.")
    
    with col2:
        st.info("**Aktueller Status:** " + 
                ("✅ Dokumente erkannt" if st.session_state.rg_data["is_ocr_done"] else "⚠️ Bitte Fahrzeugschein scannen"))
        if st.session_state.rg_data["is_ocr_done"]:
            st.write(f"**Fahrzeug:** {st.session_state.rg_data['vehicle']['brand']} {st.session_state.rg_data['vehicle']['model']}")
            st.write(f"**Halter:** {st.session_state.rg_data['customer']['name']}")
