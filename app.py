import streamlit as st
import datetime
import re

# --- 1. KONFIGURATION & DESIGN ---
st.set_page_config(page_title="ReturnGuard", layout="wide")

st.markdown("""
    <style>
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

    /* Landingpage Styling */
    .hero-section { background-color: #002b5c; padding: 40px; border-radius: 15px; color: white; text-align: center; margin-bottom: 30px; }
    .feature-box { background-color: #ffffff; padding: 20px; border-radius: 10px; border: 1px solid #ddd; height: 100%; box-shadow: 2px 2px 10px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- 2. NAVIGATION ---
with st.sidebar:
    st.title("🛡️ ReturnGuard")
    page = st.selectbox("Menü", ["🏠 Kunden-Portal", "🛠️ Experten-Check (Intern)"])
    st.write("---")
    st.caption("Version 1.2.0 - 2026")

# --- 3. SEITE: KUNDEN-PORTAL (LANDINGPAGE) ---
if page == "🏠 Kunden-Portal":
    st.markdown('<div class="hero-section"><h1>🛡️ ReturnGuard</h1><p style="font-size: 1.5rem;">Sicherheit bei Ihrer Leasingrückgabe</p></div>', unsafe_allow_html=True)

    col_img, col_info = st.columns([0.6, 0.4])

    with col_img:
        st.subheader("Ihre Analyse im Überblick")
        # Platzhalter für die 2D Fahrzeugansicht
        st.image("https://img.freepik.com/vektoren-kostenlos/auto-draufsicht-mit-realistischem-design_23-2147879483.jpg", 
                 caption="Unsere Experten prüfen alle kritischen Zonen Ihres Fahrzeugs.")
        
        st.markdown("""
        **Was wir prüfen:**
        * **Karosserie:** Dellen, Kratzer und Lackmängel.
        * **Räder:** Felgenzustand und Reifenprofiltiefe.
        * **Innenraum:** Polsterzustand und technische Funktionen.
        """)

    with col_info:
        st.markdown('<div class="feature-box"><h3>Ihre Vorteile</h3>'
                    '<ul><li><b>Kostenersparnis:</b> Teure Nachzahlungen vermeiden.</li>'
                    '<li><b>Transparenz:</b> Unabhängiger Zustandsbericht.</li>'
                    '<li><b>Smart-Repair:</b> Gezielte Reparaturempfehlungen.</li></ul></div>', unsafe_allow_html=True)
        
        st.write("---")
        st.write("### Jetzt Kontakt aufnehmen")
        email_lp = st.text_input("E-Mail-Adresse für weitere Informationen:")
        if st.button("Unverbindlich anfragen"):
            if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email_lp):
                st.success(f"Vielen Dank! Wir haben Ihre E-Mail ({email_lp}) erhalten.")
            else:
                st.error("Bitte geben Sie eine gültige E-Mail-Adresse ein.")

# --- 4. SEITE: EXPERTEN-CHECK (INTERN) ---
else:
    st.title("🛠️ Experten-System")
    
    tab_halter, tab_tech, tab_check, tab_export = st.tabs(["👤 Halter", "🚗 Technik", "📋 Check", "📊 Export"])

    with tab_halter:
        st.subheader("Halterinformationen")
        c1, c2 = st.columns(2)
        anrede = c1.selectbox("Anrede", ["Firma", "Herr", "Frau", "keine Angabe"])
        name = c2.text_input("Name / Firma")
        st.text_area("Interne Bemerkung", height=100)

    with tab_tech:
        st.subheader("Fahrzeugdetails")
        t1, t2 = st.columns(2)
        
        if 'vin_clean' not in st.session_state: st.session_state['vin_clean'] = ""
        def format_vin():
            st.session_state.vin_clean = re.sub(r'[^a-zA-Z0-9]', '', st.session_state.vin_input_field).upper()
            st.session_state.vin_input_field = st.session_state.vin_clean

        t1.text_input("FIN (17 Zeichen)", max_chars=17, key="vin_input_field", on_change=format_vin)
        kz = t2.text_input("Amtliches Kennzeichen")
        km = t1.number_input("Kilometerstand", min_value=0, step=1, format="%d")
        ez = t2.date_input("Erstzulassung", value=datetime.date(2020, 1, 1), format="DD.MM.YYYY")
        
        st.divider()
        getriebe = t1.selectbox("Getriebeart", ["Schaltung", "Automatik"])
        euro_norm = t2.selectbox("EURO Norm", ["Euro 6d", "Euro 6", "Euro 5", "Euro 4", "Elektro"])

    with tab_check:
        st.subheader("Zustandsbewertung")
        sections = {
            "Außenhaut & Karosserie": ["Lackzustand", "Dellen/Beulen", "Kratzer", "Steinschläge"],
            "Fahrwerk & Räder": ["Reifenprofil", "Felgenzustand", "Bremsanlage"],
            "Verglasung & Optik": ["Windschutzscheibe", "Beleuchtung", "Spiegel"],
            "Innenraum & Technik": ["Polster/Leder", "Geruch/Raucher", "Armaturen", "Fehlerspeicher"]
        }
        repair_costs = {}
        for sec, items in sections.items():
            with st.expander(f"📦 {sec}", expanded=True):
                for item in items:
                    choice = st.segmented_control(label=f"**{item}**", options=["Mangel", "Gebrauch", "i.O."], key=f"check_{item}", default="i.O.")
                    if choice == "Mangel":
                        repair_costs[item] = st.number_input(f"Minderwert {item} (€)", min_value=0, key=f"cost_{item}", format="%d")
                    else:
                        repair_costs[item] = 0

    with tab_export:
        total = sum(repair_costs.values())
        st.metric("Berechneter Minderwert", f"{total} €")
        if st.button("🏁 Protokoll finalisieren"):
            if len(st.session_state.get('vin_clean', '')) != 17:
                st.error("FIN ungültig!")
            else:
                st.success(f"Zustandsbericht für {st.session_state.vin_clean} erstellt.")
