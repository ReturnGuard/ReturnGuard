import streamlit as st
from fpdf import FPDF
import datetime

# Design-Optimierung für Mobile & Große Buttons
st.set_page_config(page_title="ReturnGuard Mobile", layout="wide")

st.markdown("""
    <style>
    /* Große Buttons und Handy-Optimierung */
    .stButton>button {
        height: 60px;
        font-size: 18px !important;
        font-weight: bold;
    }
    /* Hintergrundfarbe für die Sektionen */
    div[data-testid="stVerticalBlock"] > div:has(div.stHeader) {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ ReturnGuard Mobile")

# Tabs für bessere Übersicht am Handy
tab1, tab2, tab3 = st.tabs(["📋 Checkliste", "🚗 Fahrzeug", "📥 Export"])

with tab1:
    st.subheader("Zustandsbewertung")
    st.info("Tippen Sie auf den entsprechenden Zustand:")

    # Definition der Prüfpunkte
    punkte = {
        "Außenhaut": ["Lackzustand", "Dellen/Beulen", "Kratzer"],
        "Räder": ["Reifenprofil", "Felgenzustand"],
        "Glas": ["Windschutzscheibe", "Beleuchtung"]
    }

    check_results = {}
    repair_costs = {}

    for kategorie, items in punkte.items():
        st.markdown(f"### {kategorie}")
        for item in items:
            # Große Auswahl-Buttons statt Schieberegler
            choice = st.segmented_control(
                label=f"**{item}**",
                options=["Mangel", "Gebrauch", "i.O."],
                key=f"btn_{item}",
                default="i.O."
            )
            check_results[item] = choice
            
            # Wenn Mangel gewählt, sofort Kostenfeld zeigen
            if choice == "Mangel":
                repair_costs[item] = st.number_input(f"Kosten für {item} (€)", min_value=0, step=50, key=f"cost_{item}")
            else:
                repair_costs[item] = 0
        st.divider()

with tab2:
    st.subheader("Fahrzeug-Stammdaten")
    vin = st.text_input("VIN (Fahrgestellnummer)")
    kz = st.text_input("Kennzeichen")
    km = st.number_input("Kilometerstand", value=0)
    gutachter = st.text_input("Prüfer Name")

with tab3:
    st.subheader("Zusammenfassung")
    gesamt_minderwert = sum(repair_costs.values())
    
    st.metric("Gesamter Minderwert", f"{gesamt_minderwert} €")
    
    if st.button("🏁 GUTACHTEN ERSTELLEN"):
        # (PDF Logik bleibt wie besprochen erhalten)
        st.success("PDF wird generiert...")
        # Hier käme die PDF-Funktion von oben rein
