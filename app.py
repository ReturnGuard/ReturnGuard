import streamlit as st
import datetime
import re

# --- 1. KONFIGURATION & MOBILE-STYLE DESIGN ---
# Wir nutzen layout="centered", um den Look von mobile.de (zentrierter Content, Platz für Banner) zu erzielen
st.set_page_config(page_title="ReturnGuard", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* Hintergrundfarbe wie bei mobile.de (leichtes Grau) */
    .stApp {
        background-color: #f3f5f6;
    }
    
    /* Top Navigation Bar */
    .top-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: white;
        padding: 10px 20px;
        border-bottom: 1px solid #e1e4e8;
        margin-bottom: 30px;
        border-radius: 8px;
    }
    
    .nav-links button {
        border: none;
        background: none;
        color: #002b5c;
        font-weight: bold;
        padding: 10px 15px;
        cursor: pointer;
    }

    /* Card Design für den Content */
    .main-card {
        background-color: white;
        padding: 40px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }

    /* Überschriften Design */
    h1 {
        color: #002b5c;
        font-weight: 800 !important;
    }

    /* Experten-Check Buttons (Ampel-Logik) */
    div[data-testid="stSegmentedControl"] button { height: 50px !important; flex: 1 !important; }
    div[data-testid="stSegmentedControl"] [data-testid="stBaseButton-secondary"]:nth-of-type(1)[aria-checked="true"] { background-color: #ff4b4b !important; color: white !important; }
    div[data-testid="stSegmentedControl"] [data-testid="stBaseButton-secondary"]:nth-of-type(2)[aria-checked="true"] { background-color: #ffa500 !important; color: white !important; }
    div[data-testid="stSegmentedControl"] [data-testid="stBaseButton-secondary"]:nth-of-type(3)[aria-checked="true"] { background-color: #28a745 !important; color: white !important; }
    
    /* KM-Eingabe ohne Pfeile */
    input[type=number]::-webkit-inner-spin-button, input[type=number]::-webkit-outer-spin-button { -webkit-appearance: none; margin: 0; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. TOP NAVIGATION LOGIK ---
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Kunde"

# Container für die obere Leiste (simuliert mobile.de Header)
col_logo, col_nav = st.columns([1, 2])

with col_logo:
    st.markdown('<h2 style="color: #002b5c; margin:0;">🛡️ ReturnGuard</h2>', unsafe_allow_html=True)

with col_nav:
    # Buttons für die Navigation nebeneinander
    c1, c2 = st.columns(2)
    if c1.button("🏠 Privatkunden", use_container_width=True, type="primary" if st.session_state.current_page == "Kunde" else "secondary"):
        st.session_state.current_page = "Kunde"
        st.rerun()
    if c2.button("🛠️ Experten-Check", use_container_width=True, type="primary" if st.session_state.current_page == "Experte" else "secondary"):
        st.session_state.current_page = "Experte"
        st.rerun()

st.write("---")

# --- 3. SEITE: KUNDEN-PORTAL (MOBILE.DE STYLE) ---
if st.session_state.current_page == "Kunde":
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    
    st.title("Was ist Ihr Fahrzeug bei der Rückgabe wert?")
    st.write("Vermeiden Sie Nachzahlungen. Erhalten Sie jetzt eine professionelle Zustandsbewertung.")
    
    # Fahrzeugbild zentral (Draufsicht für Analyse)
    st.image("https://img.freepik.com/free-vector/top-view-of-sedan-car-isolated-on-white-background_1308-72439.jpg", 
             width=400, use_container_width=False)
    
    st.write("---")
    
    # Vorteile im 2-Spalten-Layout
    v1, v2 = st.columns(2)
    with v1:
        st.markdown("### ✅ Kosten-Check\nSofortige Kalkulation potenzieller Minderwerte.")
    with v2:
        st.markdown("### ✅ Smart-Repair\nTipps zur günstigen Instandsetzung.")

    st.write("---")
    
    # Lead-Formular
    st.subheader("Jetzt Bericht anfordern")
    email_lp = st.text_input("Ihre E-Mail-Adresse", placeholder="name@beispiel.de")
    if st.button("Kostenlose Informationen senden", use_container_width=True):
        if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email_lp):
            st.success("Erfolg! Sie erhalten in Kürze Post von uns.")
        else:
            st.error("Bitte E-Mail prüfen.")
            
    st.markdown('</div>', unsafe_allow_html=True)

# --- 4. SEITE: EXPERTEN-CHECK (INTERN) ---
else:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("Experten-Bewertung")
    
    tab_halter, tab_tech, tab_check, tab_export = st.tabs(["👤 Halter", "🚗 Technik", "📋 Check", "📊 Export"])
    
    with tab_halter:
        st.subheader("Halterdaten")
        st.selectbox("Anrede", ["Firma", "Herr", "Frau"])
        st.text_input("Name")
        st.text_area("Bemerkung")

    with tab_tech:
        st.subheader("Fahrzeugdetails")
        if 'vin_clean' not in st.session_state: st.session_state['vin_clean'] = ""
        def format_vin():
            st.session_state.vin_clean = re.sub(r'[^a-zA-Z0-9]', '', st.session_state.vin_input_field).upper()
            st.session_state.vin_input_field = st.session_state.vin_clean
        st.text_input("FIN (17 Zeichen)", max_chars=17, key="vin_input_field", on_change=format_vin)
        st.text_input("Kennzeichen")
        st.number_input("Kilometer", min_value=0, format="%d")
        st.date_input("Erstzulassung", value=datetime.date(2022,1,1), format="DD.MM.YYYY")

    with tab_check:
        st.subheader("Zustandsbewertung")
        # Beispiel-Check
        items = ["Lackzustand", "Reifenprofil", "Felgen", "Innenraum"]
        costs = {}
        for item in items:
            choice = st.segmented_control(f"**{item}**", ["Mangel", "Gebrauch", "i.O."], key=f"c_{item}", default="i.O.")
            if choice == "Mangel":
                costs[item] = st.number_input(f"Kosten {item} (€)", key=f"v_{item}", format="%d")
            else:
                costs[item] = 0

    with tab_export:
        total = sum(costs.values())
        st.metric("Potenzieller Minderwert", f"{total} €")
        if st.button("Protokoll abschließen"):
            st.success("Bericht generiert.")

    st.markdown('</div>', unsafe_allow_html=True)

# Platz für Banner (unten oder seitlich durch layout="centered" automatisch frei)
st.write("")
st.caption("Platz für Partner-Banner & Werbung")
