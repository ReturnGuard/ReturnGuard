import streamlit as st
from fpdf import FPDF
import datetime

# Design-Optimierung: Farben für die Buttons
st.set_page_config(page_title="ReturnGuard Mobile", layout="wide")

st.markdown("""
    <style>
    /* Grunddesign für die Buttons */
    div[data-baseweb="segmented-control"] button {
        height: 50px !important;
        font-weight: bold !important;
    }
    /* Farbe wenn 'Mangel' ausgewählt ist (Rot) */
    div[data-testid="stSegmentedControl"] button[aria-checked="true"]:nth-child(1) {
        background-color: #ff4b4b !important;
        color: white !important;
    }
    /* Farbe wenn 'Gebrauch' ausgewählt ist (Gelb/Orange) */
    div[data-testid="stSegmentedControl"] button[aria-checked="true"]:nth-child(2) {
        background-color: #ffa500 !important;
        color: white !important;
    }
    /* Farbe wenn 'i.O.' ausgewählt ist (Grün) */
    div[data-testid="stSegmentedControl"] button[aria-checked="true"]:nth-child(3) {
        background-color: #28a745 !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ ReturnGuard - Mobile Check")

# Tabs für die Übersicht
tab1, tab2, tab3 = st.tabs(["📋 Checkliste", "🚗 Fahrzeug", "📥 Export"])

with tab1:
    st.subheader("Zustandsbewertung")
    
    # Modulare Struktur basierend auf Ihren Alpha-Controller Daten
    sections = {
        "Außenhaut": ["Lackzustand", "Dellen/Beulen", "Kratzer", "Steinschläge"],
        "Fahrwerk": ["Reifenprofil", "Felgenzustand", "Bremsen"],
        "Innenraum": ["Polster/Leder", "Geruch", "Armaturen"]
    }

    check_results = {}
    repair_costs = {}

    for section, points in sections.items():
        with st.expander(f"**{section}**", expanded=True):
            for p in points:
                # Große Buttons mit Ampel-Logik
                choice = st.segmented_control(
                    label=f"{p}:",
                    options=["Mangel", "Gebrauch", "i.O."],
                    key=f"btn_{p}",
                    default="i.O."
                )
                check_results[p] = choice
                
                if choice == "Mangel":
                    repair_costs[p] = st.number_input(f"Smart-Repair Kosten für {p} (€)", min_value=0, step=50, key=f"cost_{p}")
                else:
                    repair_costs[p] = 0

with tab2:
    st.subheader("Stammdaten aus Alpha Controller")
    # Felder passend zu Ihren Screenshots
    c1, c2 = st.columns(2)
    vin = c1.text_input("VIN")
    kz = c2.text_input("Kennzeichen")
    ez = c1.text_input("Erstzulassung")
    km = c2.number_input("Aktueller KM-Stand", value=0)

with tab3:
    st.subheader("Zusammenfassung & PDF")
    total = sum(repair_costs.values())
    st.metric("Voraussichtlicher Minderwert", f"{total} €")
    
    if st.button("🏁 GUTACHTEN FINALISIEREN"):
        st.success("PDF wird generiert...")
        # Hier folgt die PDF-Download-Logik
