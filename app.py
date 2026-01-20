import streamlit as st
from fpdf import FPDF

# Professionelles Branding & Mobile-Optimierung
st.set_page_config(page_title="ReturnGuard Pro", layout="wide")

# ERZWUNGENES FARB-DESIGN (CSS)
st.markdown("""
    <style>
    /* Grundgröße der Buttons anpassen */
    div[data-testid="stSegmentedControl"] button {
        height: 60px !important;
        font-weight: bold !important;
        border: 2px solid #d3d3d3 !important;
    }

    /* ERZWINGE FARBEN BEI AUSWAHL */
    /* 1. Button: Mangel -> Rot */
    div[data-testid="stSegmentedControl"] button[aria-checked="true"]:nth-of-type(1) {
        background-color: #FF0000 !important;
        color: white !important;
        border-color: #8B0000 !important;
    }

    /* 2. Button: Gebrauch -> Gelb/Orange */
    div[data-testid="stSegmentedControl"] button[aria-checked="true"]:nth-of-type(2) {
        background-color: #FFCC00 !important;
        color: black !important;
        border-color: #CC9900 !important;
    }

    /* 3. Button: i.O. -> Grün */
    div[data-testid="stSegmentedControl"] button[aria-checked="true"]:nth-of-type(3) {
        background-color: #28A745 !important;
        color: white !important;
        border-color: #1E7E34 !important;
    }

    /* Hover-Effekte deaktivieren, damit Farben stabil bleiben */
    div[data-testid="stSegmentedControl"] button:hover {
        opacity: 0.9;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ ReturnGuard - Experten-Check")

# Reiter-System für den Workflow
tab1, tab2, tab3 = st.tabs(["📋 Zustands-Check", "🚗 Fahrzeugdaten", "📊 Ergebnis"])

with tab1:
    st.info("Bedienung: Tippen Sie auf den Zustand. Bei 'Mangel' erscheint das Kostenfeld.")
    
    # Modularer Aufbau nach Ihren Vorgaben
    sections = {
        "Außenhaut & Karosserie": ["Lackzustand", "Dellen/Beulen", "Kratzer", "Steinschläge"],
        "Fahrwerk & Räder": ["Reifenprofil", "Felgenzustand", "Bremsen"],
        "Verglasung & Optik": ["Windschutzscheibe", "Beleuchtung"],
        "Innenraum & Technik": ["Polster/Leder", "Geruch", "Fehlerspeicher"]
    }

    results = {}
    costs = {}

    for section_name, items in sections.items():
        with st.expander(f"**{section_name}**", expanded=True):
            for item in items:
                # Die Segmented Control zeigt nun die erzwungenen Farben
                choice = st.segmented_control(
                    label=f"**{item}**",
                    options=["Mangel", "Gebrauch", "i.O."],
                    key=f"check_{item}",
                    default="i.O."
                )
                results[item] = choice
                
                if choice == "Mangel":
                    costs[item] = st.number_input(f"Kosten {item} (€)", min_value=0, step=50, key=f"cost_{item}")
                else:
                    costs[item] = 0

with tab2:
    st.subheader("Fahrzeug-Stammdaten")
    col1, col2 = st.columns(2)
    vin = col1.text_input("VIN")
    kz = col2.text_input("Kennzeichen")
    km = col1.number_input("Kilometerstand", value=0, step=1000)
    gutachter = col2.text_input("Name des Prüfers")

with tab3:
    total_minderwert = sum(costs.values())
    st.metric("Gesamt-Minderwert", f"{total_minderwert} €")
    
    if st.button("🏁 Protokoll finalisieren"):
        st.success("Daten wurden für das PDF-Gutachten gespeichert.")
        # Hier kann die PDF-Download-Logik ergänzt werden
