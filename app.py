import streamlit as st
import datetime
import re

# --- 1. KONFIGURATION & DESIGN ---
st.set_page_config(page_title="ReturnGuard Pro", layout="wide")

# CSS für professionelles Branding und farbige Buttons
st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { height: 50px; background-color: #f0f2f6; border-radius: 5px; }
    .stTabs [aria-selected="true"] { background-color: #002b5c !important; color: white !important; }

    /* Farblogik für Experten-Check Buttons */
    div[data-testid="stSegmentedControl"] button {
        height: 55px !important;
        font-weight: bold !important;
        flex: 1 !important;
    }
    div[data-testid="stSegmentedControl"] [data-testid="stBaseButton-secondary"]:nth-of-type(1)[aria-checked="true"] {
        background-color: #ff4b4b !important; color: white !important;
    }
    div[data-testid="stSegmentedControl"] [data-testid="stBaseButton-secondary"]:nth-of-type(2)[aria-checked="true"] {
        background-color: #ffa500 !important; color: white !important;
    }
    div[data-testid="stSegmentedControl"] [data-testid="stBaseButton-secondary"]:nth-of-type(3)[aria-checked="true"] {
        background-color: #28a745 !important; color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ ReturnGuard - Alpha Integration")

# --- 2. TABS STRUKTUR ---
tab_halter, tab_tech, tab_check, tab_export = st.tabs([
    "👤 Halter", "🚗 Technik", "📋 Expert-Check", "📊 Export"
])

# --- 3. TAB: FAHRZEUGHALTER ---
with tab_halter:
    st.subheader("Halterinformationen")
    c1, c2 = st.columns(2)
    anrede = c1.selectbox("Anrede", ["Firma", "Herr", "Frau", "keine Angabe"])
    name = c2.text_input("Name / Firma")
    strasse = c1.text_input("Straße & Nr.")
    ort = c2.text_input("PLZ & Ort")
    st.text_area("Interne Bemerkung", height=100)

# --- 4. TAB: TECHNIK & FIN-FIX ---
with tab_tech:
    st.subheader("Fahrzeugdetails")
    t1, t2 = st.columns(2)
    
    # Initialisierung des Session States für die FIN, falls noch nicht vorhanden
    if 'vin_clean' not in st.session_state:
        st.session_state['vin_clean'] = ""

    # Die Eingabe erfolgt in das Feld. 
    # Durch 'on_change' stellen wir sicher, dass die Umwandlung sofort beim Verlassen greift.
    def format_vin():
        raw = st.session_state.vin_input_field
        # Entferne Sonderzeichen und mache alles GROSS
        st.session_state.vin_clean = re.sub(r'[^a-zA-Z0-9]', '', raw).upper()
        # Schreibe den sauberen Wert zurück in das Eingabefeld
        st.session_state.vin_input_field = st.session_state.vin_clean

    vin = t1.text_input(
        "FIN (17 Zeichen)", 
        max_chars=17, 
        key="vin_input_field", 
        on_change=format_vin,
        help="Wird beim Verlassen des Feldes automatisch großgeschrieben."
    )
    
    # Aktueller Stand der bereinigten FIN für die Logik
    final_vin = st.session_state.get('vin_clean', '')

    # Visuelles Feedback
    if final_vin:
        if len(final_vin) < 17:
            t1.warning(f"⚠️ FIN unvollständig: {len(final_vin)}/17 Zeichen")
        elif len(final_vin) == 17:
            t1.success(f"✅ FIN korrekt: {final_vin}")
    
    kz = t2.text_input("Amtliches Kennzeichen")
    km = t1.number_input("Kilometerstand", value=0, step=1)
    ez = t2.text_input("Erstzulassung (MM/JJJJ)")
    
    st.divider()
    t3, t4 = st.columns(2)
    t3.selectbox("Getriebeart", ["Schaltgetriebe", "Automatik", "Doppelkupplung"])
    t4.selectbox("Kraftstoff", ["Benzin", "Diesel", "Elektro", "Hybrid"])
    t3.number_input("CO2 g/km", value=0)
    t4.selectbox("Umweltplakette", ["Grün (4)", "Gelb (3)", "Rot (2)", "Keine"])

# --- 5. TAB: EXPERT-CHECK (MODULAR) ---
with tab_check:
    st.subheader("Zustandsbewertung")
    
    sections = {
        "Außenhaut & Karosserie": ["Lackzustand", "Dellen/Beulen", "Kratzer", "Steinschläge"],
        "Fahrwerk & Räder": ["Reifenprofil", "Felgenzustand", "Bremsanlage"],
        "Verglasung & Optik": ["Windschutzscheibe", "Beleuchtung", "Spiegel"],
        "Innenraum & Technik": ["Polster/Leder", "Geruch/Raucher", "Armaturen", "Fehlerspeicher"]
    }

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
                if choice == "Mangel":
                    repair_costs[item] = st.number_input(f"Minderwert {item} (€)", min_value=0, step=50, key=f"cost_{item}")
                else:
                    repair_costs[item] = 0

# --- 6. TAB: EXPORT ---
with tab_export:
    st.subheader("Zusammenfassung")
    total_minderwert = sum(repair_costs.values())
    st.metric("Gesamt-Minderwert", f"{total_minderwert} €")
    
    if st.button("🏁 GUTACHTEN FINALISIEREN"):
        if len(final_vin) != 17:
            st.error(f"❌ Abbruch: FIN hat nur {len(final_vin)} von 17 Stellen.")
        else:
            st.balloons()
            st.success(f"Bericht für {final_vin} erstellt.")
