import streamlit as st
from fpdf import FPDF
import datetime

# --- KONFIGURATION & DESIGN ---
st.set_page_config(page_title="ReturnGuard Pro", layout="wide")

# CSS für farbige Segmented-Control Buttons & Mobile-Optimierung
st.markdown("""
    <style>
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { height: 50px; background-color: #f0f2f6; border-radius: 5px; }
    .stTabs [aria-selected="true"] { background-color: #002b5c !important; color: white !important; }

    /* Echte Farblogik für die Buttons nebeneinander */
    div[data-testid="stSegmentedControl"] button {
        height: 55px !important;
        font-weight: bold !important;
        flex: 1 !important;
    }
    /* Mangel = Rot */
    div[data-testid="stSegmentedControl"] [data-testid="stBaseButton-secondary"]:nth-of-type(1)[aria-checked="true"] {
        background-color: #ff4b4b !important;
        color: white !important;
    }
    /* Gebrauch = Gelb */
    div[data-testid="stSegmentedControl"] [data-testid="stBaseButton-secondary"]:nth-of-type(2)[aria-checked="true"] {
        background-color: #ffa500 !important;
        color: white !important;
    }
    /* i.O. = Grün */
    div[data-testid="stSegmentedControl"] [data-testid="stBaseButton-secondary"]:nth-of-type(3)[aria-checked="true"] {
        background-color: #28a745 !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ ReturnGuard - Alpha Integration")

# --- STRUKTUR (REITER) ---
tab_halter, tab_tech, tab_check, tab_export = st.tabs([
    "👤 Halter", "🚗 Technik", "📋 Expert-Check", "📊 Export"
])

# 1. TAB: FAHRZEUGHALTER (Alpha Controller Daten)
with tab_halter:
    st.subheader("Halterinformationen")
    c1, c2 = st.columns(2)
    anrede = c1.selectbox("Anrede", ["Firma", "Herr", "Frau", "keine Angabe"])
    name = c2.text_input("Name / Firma")
    strasse = c1.text_input("Straße & Nr.")
    ort = c2.text_input("PLZ & Ort")
    bemerkung = st.text_area("Interne Notiz", height=100)

# 2. TAB: TECHNIK & UMWELT
with tab_tech:
    st.subheader("Fahrzeugdetails")
    t1, t2 = st.columns(2)
    vin = t1.text_input("VIN (Fahrgestellnummer)")
    kz = t2.text_input("Amtliches Kennzeichen")
    km = t1.number_input("Kilometerstand", value=0, step=1)
    ez = t2.text_input("Erstzulassung (MM/JJJJ)")
    
    st.divider()
    t3, t4 = st.columns(2)
    getriebe = t3.selectbox("Getriebeart", ["Schaltgetriebe", "Automatik", "Doppelkupplung"])
    kraftstoff = t4.selectbox("Kraftstoff", ["Benzin", "Diesel", "Elektro", "Hybrid"])
    co2 = t3.number_input("CO2 g/km", value=0)
    plakette = t4.selectbox("Umweltplakette", ["Grün (4)", "Gelb (3)", "Rot (2)", "Keine"])

# 3. TAB: EXPERT-CHECK (Die 14 Punkte Logik)
with tab_check:
    st.subheader("Zustandsbewertung (Vest Standard)")
    
    sections = {
        "Außenhaut & Karosserie": ["Lackzustand", "Dellen/Beulen", "Kratzer", "Steinschläge"],
        "Fahrwerk & Räder": ["Reifenprofil", "Felgenzustand", "Bremsanlage"],
        "Verglasung & Optik": ["Windschutzscheibe", "Beleuchtung", "Spiegel"],
        "Innenraum & Technik": ["Polster/Leder", "Geruch/Raucher", "Armaturen", "Funktionstest"]
    }

    check_results = {}
    repair_costs = {}

    for section_name, items in sections.items():
        with st.expander(f"📦 {section_name}", expanded=True):
            for item in items:
                choice = st.segmented_control(
                    label=f"**{item}**",
                    options=["Mangel", "Gebrauch", "i.O."],
                    key=f"check_{item}",
                    default="i.O."
                )
                check_results[item] = choice
                
                if choice == "Mangel":
                    repair_costs[item] = st.number_input(f"Minderwert {item} (€)", min_value=0, step=50, key=f"cost_{item}")
                else:
                    repair_costs[item] = 0

# 4. TAB: EXPORT & PDF
with tab_export:
    st.subheader("Zusammenfassung")
    total_minderwert = sum(repair_costs.values())
    
    col_a, col_b = st.columns(2)
    col_a.metric("Gesamt-Minderwert", f"{total_minderwert} €")
    col_b.write(f"**Prüfdatum:** {datetime.date.today()}")

    if st.button("🏁 GUTACHTEN FINALISIEREN"):
        if not vin or not kz:
            st.warning("⚠️ Bitte VIN und Kennzeichen in Tab 'Technik' eingeben!")
        else:
            st.balloons()
            st.success("Bericht bereit zum Download.")
            # PDF-Logik hier einbinden...
