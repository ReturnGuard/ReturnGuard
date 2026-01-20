import streamlit as st
import datetime
import re

# --- 1. KONFIGURATION (Centered Layout für mobile.de Look) ---
st.set_page_config(page_title="ReturnGuard", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #f3f5f6; }
    .block-container {
        max-width: 1100px !important;
        padding-top: 2rem !important;
    }
    .main-card {
        background-color: white;
        padding: 50px;
        border-radius: 16px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.06);
        margin-top: 20px;
    }
    .hero-title {
        font-size: 3.2rem !important;
        font-weight: 800 !important;
        color: #002b5c;
        line-height: 1.1;
        margin-bottom: 20px;
    }
    div.stButton > button { border-radius: 8px; font-weight: 600; }
    
    /* Experten-Check Ampel-Logik */
    div[data-testid="stSegmentedControl"] button { height: 50px !important; flex: 1 !important; }
    div[data-testid="stSegmentedControl"] [data-testid="stBaseButton-secondary"]:nth-of-type(1)[aria-checked="true"] { background-color: #ff4b4b !important; color: white !important; }
    div[data-testid="stSegmentedControl"] [data-testid="stBaseButton-secondary"]:nth-of-type(2)[aria-checked="true"] { background-color: #ffa500 !important; color: white !important; }
    div[data-testid="stSegmentedControl"] [data-testid="stBaseButton-secondary"]:nth-of-type(3)[aria-checked="true"] { background-color: #28a745 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. TOP NAVIGATION ---
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Kunde"

t_col1, t_col2, t_col3 = st.columns([1, 0.5, 1.5])
with t_col1:
    st.markdown('<h2 style="color: #002b5c; margin-top:0;">🛡️ ReturnGuard</h2>', unsafe_allow_html=True)

with t_col3:
    nav_choice = st.segmented_control(
        "Bereich", 
        ["Privatkunden-Portal", "Experten-Login"], 
        default="Privatkunden-Portal" if st.session_state.current_page == "Kunde" else "Experten-Login",
        label_visibility="collapsed"
    )
    if nav_choice == "Privatkunden-Portal": st.session_state.current_page = "Kunde"
    else: st.session_state.current_page = "Experte"

# --- 3. SEITE: KUNDEN-PORTAL ---
if st.session_state.current_page == "Kunde":
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    
    c1, c2 = st.columns([1.1, 1], gap="large")
    
    with c1:
        st.markdown('<h1 class="hero-title">Keine Angst vor der Leasing-Rückgabe</h1>', unsafe_allow_html=True)
        st.write("### Schützen Sie sich vor unerwarteten Kosten mit dem ReturnGuard Zustands-Check.")
        
        st.markdown("""
        <div style="margin: 30px 0;">
        <p style="font-size: 1.2rem;">🛡️ <b>Unabhängig:</b> Wir bewerten objektiv und fair.</p>
        <p style="font-size: 1.2rem;">📊 <b>Transparent:</b> Detaillierter Bericht aller Mängel.</p>
        <p style="font-size: 1.2rem;">💰 <b>Sparpotential:</b> Smart-Repair Empfehlungen nutzen.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Jetzt unverbindlich anfragen", use_container_width=True, type="primary"):
            st.toast("Bitte E-Mail unten eingeben!")

    with c2:
        # Einbindung des hyperrealistischen 3D-Renderings
        st.image("https://raw.githubusercontent.com/Frankyboy1984/ReturnGuard/main/hyper_realistic_car_analysis.png", 
                 caption="Präzise Schadensidentifikation an allen Bauteilen", 
                 use_container_width=True)

    st.write("---")
    
    st.subheader("Der ReturnGuard Ablauf")
    a1, a2, a3 = st.columns(3)
    a1.info("**1. Experten-Check**\nAufnahme des Fahrzeugzustands vor Ort.")
    a2.info("**2. Analyse**\nAbgleich mit Rückgabestandards.")
    a3.info("**3. Sicherheit**\nMit Gutachten entspannt zum Leasinggeber.")

    st.write("---")
    
    st.subheader("Interesse? Wir melden uns bei Ihnen.")
    e_col1, e_col2 = st.columns([2, 1])
    email_lp = e_col1.text_input("Ihre E-Mail-Adresse", placeholder="beispiel@firma.de", label_visibility="collapsed")
    if e_col2.button("Absenden", use_container_width=True):
        if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email_lp):
            st.success("Vielen Dank! Ein Experte wird Sie kontaktieren.")
        else:
            st.error("E-Mail ungültig.")
            
    st.markdown('</div>', unsafe_allow_html=True)

# --- 4. SEITE: EXPERTEN-CHECK ---
else:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("🛡️ Experten-System")
    
    tab_halter, tab_tech, tab_check, tab_export = st.tabs(["👤 Halter", "🚗 Technik", "📋 Check", "📊 Export"])
    
    with tab_halter:
        st.subheader("Halterdaten")
        st.selectbox("Anrede", ["Firma", "Herr", "Frau"])
        st.text_input("Name")
        st.text_area("Interne Bemerkungen")

    with tab_tech:
        st.subheader("Fahrzeug-Details")
        if 'vin_clean' not in st.session_state: st.session_state['vin_clean'] = ""
        def format_vin():
            st.session_state.vin_clean = re.sub(r'[^a-zA-Z0-9]', '', st.session_state.vin_input_field).upper()
            st.session_state.vin_input_field = st.session_state.vin_clean
        st.text_input("FIN (17 Zeichen)", max_chars=17, key="vin_input_field", on_change=format_vin)
        st.number_input("Aktueller KM-Stand", min_value=0, format="%d")
        st.date_input("Erstzulassung", value=datetime.date(2023,1,1), format="DD.MM.YYYY")

    with tab_check:
        st.subheader("Modularer Zustands-Check")
        items = ["Außenhaut (Lack/Dellen)", "Räder & Reifen", "Verglasung", "Innenraum"]
        costs = {}
        for item in items:
            st.write(f"### {item}")
            choice = st.segmented_control(f"Status {item}", ["Mangel", "Gebrauch", "i.O."], key=f"c_{item}", default="i.O.")
            if choice == "Mangel":
                costs[item] = st.number_input(f"Reparaturkosten {item} (€)", key=f"v_{item}", format="%d")
            else:
                costs[item] = 0

    with tab_export:
        total = sum(costs.values())
        st.metric("Gesamter Minderwert", f"{total} €")
        if st.button("Bericht finalisieren"):
            st.balloons()
            st.success("Zustandsbericht wurde lokal gespeichert.")

    st.markdown('</div>', unsafe_allow_html=True)
