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
# ==================== PAGE 2: EXPERT-CHECK ====================
if page == "🔍 Expert-Check":
    st.title("Interaktiver Fahrzeug-Check")
    st.write("Markieren Sie die betroffenen Stellen am Fahrzeug oder nutzen Sie die Kategorien.")

    # Interaktive SVG Skizze (Simuliert als Spalten-Buttons für Stabilität)
    st.subheader("Fahrzeug-Bereich wählen")
    c1, c2, c3, c4 = st.columns(4)
    with c1: 
        if st.button("🚗 Front / Motorhaube"): st.session_state.target_cat = "Außenhaut"
    with c2:
        if st.button("🎡 Räder / Felgen"): st.session_state.target_cat = "Fahrwerk"
    with c3:
        if st.button("🪟 Glas / Optik"): st.session_state.target_cat = "Verglasung"
    with c4:
        if st.button("🛋️ Innenraum"): st.session_state.target_cat = "Innenraum"

    st.divider()

    # Modulares Audit System
    with st.expander("🛡️ Außenhaut & Karosserie", expanded=(st.session_state.get('target_cat') == "Außenhaut")):
        col_a, col_b = st.columns(2)
        with col_a:
            delle = st.checkbox("Delle / Beule (Tür/Haube)")
            kratzer = st.checkbox("Kratzer (Lackbeschädigung)")
        with col_b:
            if delle:
                groesse = st.slider("Größe der Delle (in mm)", 0, 100, 15)
                # Shadow Expert Preview Logik
                if groesse < 20:
                    st.info("💡 **Shadow Expert:** VWFS & BMW akzeptieren Dellen < 20mm oft als Gebrauchsspur.")
                else:
                    st.warning("⚠️ **Shadow Expert:** Über 20mm gilt meist als reparaturpflichtiger Schaden.")

    with st.expander("🎡 Fahrwerk & Räder", expanded=(st.session_state.get('target_cat') == "Fahrwerk")):
        felge = st.checkbox("Bordsteinschaden an Felge")
        if felge:
            tiefe = st.number_input("Tiefe des Kratzers (in mm)", 0.0, 5.0, 0.5)
            if tiefe < 1.0:
                st.info("💡 **Shadow Expert:** Kratzer < 1mm Tiefe sind laut BMW/Mercedes meist zulässiger Verschleiß.")

    with st.expander("🪟 Verglasung & Optik", expanded=(st.session_state.get('target_cat') == "Verglasung")):
        stein = st.checkbox("Steinschlag Windschutzscheibe")
        if stein:
            sichtfeld = st.radio("Lage des Steinschlags:", ["Im Sichtfeld des Fahrers", "Am Rand / Beifahrerseite"])
            if sichtfeld == "Am Rand / Beifahrerseite":
                st.success("💡 **Shadow Expert:** Außerhalb des Sichtfelds ist eine Reparatur (ca. 100€) statt Tausch (ca. 1000€) zulässig.")

# ==================== PAGE 3: SHADOW EXPERT (VETO) ====================
if page == "🛡️ Shadow Expert (Veto)":
    st.title("Shadow Expert: Händler-Protokoll Veto-Check")
    st.write("Laden Sie hier das Rückgabeprotokoll des Händlers hoch, um unberechtigte Forderungen zu finden.")
    
    uploaded_file = st.file_uploader("Protokoll (PDF/JPG) hochladen", type=["pdf", "jpg", "png"])
    
    if uploaded_file:
        with st.status("Analysiere Protokoll gegen Hersteller-Kataloge 2026...", expanded=True):
            st.write("Suche nach Positionen...")
            st.write("Vergleiche mit OLG Stuttgart Az. 6 U 84/24...")
        
        st.subheader("Analyse-Ergebnis")
        
        # Beispiel für ein gefundenes Veto
        st.markdown("""
        <div class="veto-card">
            <h4>❌ VETO: Position 'Alufelge vorne rechts'</h4>
            <p><b>Händler-Forderung:</b> 450,00 € (Austausch)</p>
            <p><b>Shadow Expert Urteil:</b> Unberechtigt. Der Kratzer wird im Protokoll mit 12mm beschrieben. 
            Laut aktuellem BMW-Schadenskatalog sind Kratzer bis 20mm als Gebrauchsspur zu akzeptieren.</p>
            <p><b>Rechtlicher Hebel:</b> OLG Stuttgart (Neu-für-Alt Abzug nicht berücksichtigt).</p>
            <span class="savings-badge">Potenzielle Ersparnis: 450,00 €</span>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Widerspruchs-Schreiben generieren (PDF)"):
            st.success("Widerspruch wurde erstellt. Bitte beim Händler vorlegen.")
            st.download_button("Datei herunterladen", "Hier stünde der Text des Schreibens...", file_name="Widerspruch_ReturnGuard.txt")
