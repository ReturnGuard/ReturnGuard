import streamlit as st
import datetime
import re

# --- 1. KONFIGURATION & DESIGN ---
st.set_page_config(page_title="ReturnGuard", layout="wide")

# CSS für das Design (Landingpage & Buttons)
st.markdown("""
    <style>
    /* Design für die Landingpage-Cards */
    .feature-card {
        padding: 20px;
        border-radius: 10px;
        background-color: #f0f2f6;
        border-left: 5px solid #002b5c;
        margin-bottom: 10px;
    }
    /* Bekannte Farblogik für Experten-Buttons */
    div[data-testid="stSegmentedControl"] button { height: 55px !important; font-weight: bold !important; flex: 1 !important; }
    div[data-testid="stSegmentedControl"] [data-testid="stBaseButton-secondary"]:nth-of-type(1)[aria-checked="true"] { background-color: #ff4b4b !important; color: white !important; }
    div[data-testid="stSegmentedControl"] [data-testid="stBaseButton-secondary"]:nth-of-type(2)[aria-checked="true"] { background-color: #ffa500 !important; color: white !important; }
    div[data-testid="stSegmentedControl"] [data-testid="stBaseButton-secondary"]:nth-of-type(3)[aria-checked="true"] { background-color: #28a745 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. NAVIGATION LOGIK ---
# Wir nutzen die Seitenleiste, um zwischen Kunde und Experte zu wählen
page = st.sidebar.selectbox("Bereich wählen", ["🏠 Kunden-Portal", "🛠️ Experten-Check (Intern)"])

# --- 3. SEITE: LANDINGPAGE (KUNDE) ---
if page == "🏠 Kunden-Portal":
    st.title("🛡️ ReturnGuard")
    st.subheader("Sorgenfreie Leasingrückgabe durch professionelle Vorab-Prüfung.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h4>Sicherheit vor Nachzahlungen</h4>
            <p>Wir prüfen Ihr Fahrzeug nach offiziellen Standards, bevor es der Leasinggeber tut.</p>
        </div>
        <div class="feature-card">
            <h4>Smart-Repair Empfehlungen</h4>
            <p>Sparen Sie bis zu 60% der Kosten durch gezielte Instandsetzung vor der Rückgabe.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        st.write("### Jetzt Informationen anfordern")
        email = st.text_input("Ihre E-Mail-Adresse für ein unverbindliches Angebot:")
        
        if st.button("Anfrage senden"):
            if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
                st.success(f"Vielen Dank! Ein Experte wird sich unter {email} bei Ihnen melden.")
            else:
                st.error("Bitte geben Sie eine gültige E-Mail-Adresse ein.")

    with col2:
        st.info("**Kontakt**\n\n📞 +49 (0) 123 456 78\n\n📧 info@returnguard.de\n\n📍 Berlin / Hamburg / München")

# --- 4. SEITE: EXPERTEN-CHECK (UNSER GRUNDGERÜST) ---
elif page == "🛠️ Experten-Check (Intern)":
    st.title("🛡️ ReturnGuard - Experten-System")
    
    tab_halter, tab_tech, tab_check, tab_export = st.tabs([
        "👤 Halter", "🚗 Technik", "📋 Expert-Check", "📊 Export"
    ])

    # --- TAB: HALTER ---
    with tab_halter:
        st.subheader("Halterinformationen")
        c1, c2 = st.columns(2)
        anrede = c1.selectbox("Anrede", ["Firma", "Herr", "Frau", "keine Angabe"])
        name = c2.text_input("Name / Firma")
        st.text_area("Interne Bemerkung", height=100)

    # --- TAB: TECHNIK (Ihre optimierten Felder) ---
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

    # --- TAB: CHECK ---
    with tab_check:
        st.subheader("Zustandsbewertung")
        sections = {
            "Außenhaut & Karosserie": ["Lackzustand", "Dellen/Beulen", "Kratzer"],
            "Innenraum & Technik": ["Polster/Leder", "Geruch/Raucher", "Fehlerspeicher"]
        }
        repair_costs = {}
        for sec, items in sections.items():
            with st.expander(f"📦 {sec}", expanded=True):
                for item in items:
                    choice = st.segmented_control(label=f"**{item}**", options=["Mangel", "Gebrauch", "i.O."], key=f"check_{item}", default="i.O.")
                    if choice == "Mangel":
                        repair_costs[item] = st.number_input(f"Kosten {item} (€)", min_value=0, key=f"cost_{item}", format="%d")
                    else:
                        repair_costs[item] = 0

    # --- TAB: EXPORT ---
    with tab_export:
        total = sum(repair_costs.values())
        st.metric("Gesamt-Minderwert", f"{total} €")
        if st.button("🏁 Protokoll abschließen"):
            if len(st.session_state.get('vin_clean', '')) != 17:
                st.error("FIN unvollständig!")
            else:
                st.success("Daten finalisiert.")
