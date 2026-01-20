import streamlit as st
import datetime
import re

# --- 1. KONFIGURATION & DESIGN ---
st.set_page_config(page_title="ReturnGuard", layout="wide")

st.markdown("""
    <style>
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { height: 50px; background-color: #f0f2f6; border-radius: 5px; }
    .stTabs [aria-selected="true"] { background-color: #002b5c !important; color: white !important; }

    /* Farblogik für Experten-Check Buttons nebeneinander */
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
    
    /* KM-Stand & Kosten: Entfernt die Pfeile (+/-) im Nummernfeld */
    input[type=number]::-webkit-inner-spin-button, 
    input[type=number]::-webkit-outer-spin-button { 
        -webkit-appearance: none; margin: 0; 
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ ReturnGuard")

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

# --- 4. TAB: TECHNIK (Optimiert für DAT-Vorbereitung) ---
with tab_tech:
    st.subheader("Fahrzeugdetails")
    t1, t2 = st.columns(2)
    
    # FIN-Logik mit automatischer Großschreibung beim Verlassen des Feldes
    if 'vin_clean' not in st.session_state: st.session_state['vin_clean'] = ""
    def format_vin():
        st.session_state.vin_clean = re.sub(r'[^a-zA-Z0-9]', '', st.session_state.vin_input_field).upper()
        st.session_state.vin_input_field = st.session_state.vin_clean

    final_vin = t1.text_input("FIN (17 Zeichen)", max_chars=17, key="vin_input_field", on_change=format_vin)
    kz = t2.text_input("Amtliches Kennzeichen")
    
    # KM-Stand als sauberes Eingabefeld ohne +/-
    km = t1.number_input("Kilometerstand", min_value=0, step=1, format="%d")
    
    # EZ als echtes Datum (Tag Monat Jahr)
    ez = t2.date_input("Erstzulassung", value=datetime.date(2020, 1, 1), format="DD.MM.YYYY")
    
    st.divider()
    t3, t4 = st.columns(2)
    getriebe = t3.selectbox("Getriebeart", ["Schaltung", "Automatik"])
    euro_norm = t4.selectbox("EURO Norm", ["Euro 6d", "Euro 6", "Euro 5", "Euro 4", "Elektro/Null Emission"])

# --- 5. TAB: EXPERT-CHECK (MODULAR) ---
with tab_check:
    st.subheader("Zustandsbewertung (Vest Standard)")
    
    # Modulare Sektionen wie gewünscht
    sections = {
        "Außenhaut & Karosserie": ["Lackzustand", "Dellen/Beulen", "Kratzer", "Steinschläge"],
        "Fahrwerk & Räder": ["Reifenprofil", "Felgenzustand", "Bremsanlage"],
        "Verglasung & Optik": ["Windschutzscheibe", "Beleuchtung", "Spiegel"],
        "Innenraum & Technik": ["Polster/Leder", "Geruch/Raucher", "Armaturen", "Fehlerspeicher"]
    }

    check_results = {}
    repair_costs = {}

    for section_name, items in sections.items():
        with st.expander(f"📦 {section_name}", expanded=True):
            for item in items:
                # Große Buttons mit Ampel-Logik
                choice = st.segmented_control(
                    label=f"**{item}**",
                    options=["Mangel", "Gebrauch", "i.O."],
                    key=f"check_{item}",
                    default="i.O."
                )
                check_results[item] = choice
                
                # Smart-Repair Kostenfeld erscheint nur bei Mangel (ohne +/-)
                if choice == "Mangel":
                    repair_costs[item] = st.number_input(f"Minderwert {item} (€)", min_value=0, step=50, key=f"cost_{item}", format="%d")
                else:
                    repair_costs[item] = 0

# --- 6. TAB: EXPORT ---
with tab_export:
    st.subheader("Zusammenfassung")
    total = sum(repair_costs.values())
    st.metric("Gesamt-Minderwert", f"{total} €")
    
    if st.button("🏁 GUTACHTEN FINALISIEREN"):
        current_vin = st.session_state.get('vin_clean', '')
        if len(current_vin) != 17:
            st.error(f"❌ Die FIN ist unvollständig ({len(current_vin)}/17 Zeichen).")
        elif not kz:
            st.error("❌ Bitte geben Sie ein Kennzeichen an.")
        else:
            st.balloons()
            st.success(f"Gutachten für {kz} erfolgreich erstellt. Dokumentation für FIN {current_vin} ist bereit.")
