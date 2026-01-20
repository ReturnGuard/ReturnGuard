import streamlit as st
import datetime
import re

# --- 1. KONFIGURATION & ERWEITERTES DESIGN (ReturnGuard CI) ---
st.set_page_config(page_title="ReturnGuard", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* Hintergrund & Reduzierung des oberen Abstands */
    .stApp { background-color: #f3f5f6; }
    
    /* Hero-Balken oben (Dunkelblau) - SCHMALER eingestellt */
    .hero-header {
        background: linear-gradient(135deg, #002b5c 0%, #004080 100%);
        height: 220px; /* Von 320px auf 220px reduziert */
        width: 100%;
        position: absolute;
        top: 0;
        left: 0;
        z-index: 0;
    }

    /* Container für den Inhalt */
    .block-container {
        max-width: 1100px !important;
        padding-top: 25px !important;
        z-index: 1;
    }

    /* Weiße Haupt-Karte */
    .main-card {
        background-color: white;
        padding: 40px;
        border-radius: 12px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        margin-top: 100px; /* Angepasst an schmaleren Balken */
        position: relative;
    }

    .hero-title {
        font-size: 3rem !important;
        font-weight: 800 !important;
        color: #002b5c;
        line-height: 1.1;
        margin-bottom: 20px;
    }

    /* Lead-Box am Ende */
    .lead-container {
        background-color: #f8fafc;
        padding: 25px;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        margin-top: 30px;
        margin-bottom: 20px;
    }

    div.stButton > button {
        border-radius: 6px;
        font-weight: 700;
        background-color: #002b5c;
        color: white;
        height: 3.5rem;
        border: none;
    }

    .usp-item {
        display: flex;
        align-items: center;
        margin-bottom: 10px;
        font-size: 1.1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialisierung Page State
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Kunde"

# --- 2. HEADER & NAVIGATION ---
st.markdown('<div class="hero-header"></div>', unsafe_allow_html=True)

nav_col1, nav_col2 = st.columns([1, 1])
with nav_col1:
    st.markdown('<h2 style="color: white; margin:0; font-weight:800;">🛡️ ReturnGuard</h2>', unsafe_allow_html=True)
with nav_col2:
    # Navigation im blauen Bereich
    nav = st.segmented_control(
        "Nav", ["Privatkunden", "Experten-Login"], 
        default="Privatkunden" if st.session_state.current_page == "Kunde" else "Experten-Login",
        label_visibility="collapsed"
    )
    if nav == "Privatkunden": st.session_state.current_page = "Kunde"
    else: st.session_state.current_page = "Experte"

# --- 3. SEITE: KUNDEN-PORTAL ---
if st.session_state.current_page == "Kunde":
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    
    c1, c2 = st.columns([1.1, 1], gap="large")
    
    with c1:
        st.markdown('<h1 class="hero-title">Leasingrückgabe ohne Überraschungen</h1>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:1.2rem; color:#4a5568;">Schützen Sie sich vor unfairen Nachzahlungen durch unseren unabhängigen Check.</p>', unsafe_allow_html=True)
        
        st.markdown("""
        <div style="margin: 25px 0;">
        <div class="usp-item">✅ <b>Präzise:</b> Detaillierte Schadensmarkierung</div>
        <div class="usp-item">✅ <b>Fair:</b> Bewertung nach offiziellen Standards</div>
        <div class="usp-item">✅ <b>Profitabel:</b> Bis zu 60% Ersparnis durch Tipps</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Jetzt Check anfragen", use_container_width=True):
            st.toast("Bitte scrollen Sie zum E-Mail-Feld.")

    with c2:
        st.image("Analyse.png", 
                 caption="Unsere digitale Experten-Analyse", 
                 use_container_width=True)
        
    st.write("---")
    
    # Prozess
    st.subheader("In 3 Schritten zur Kostensicherheit")
    p1, p2, p3 = st.columns(3)
    p1.info("**1. Aufnahme**\nExperten-Begutachtung vor Ort oder via App.")
    p2.info("**2. Analyse**\nAbgleich mit den Kriterien Ihres Leasinggebers.")
    p3.info("**3. Bericht**\nErhalt des digitalen Rückgabe-Protokolls.")

    # Lead-Sektion (WIEDER EINGEFÜGT)
    st.markdown("""
    <div class="lead-container">
        <h3 style="margin-top:0;">Interesse an einer kostenlosen Erstberatung?</h3>
        <p>Hinterlassen Sie Ihre E-Mail, wir melden uns innerhalb von 24 Stunden.</p>
    </div>
    """, unsafe_allow_html=True)
    
    e1, e2 = st.columns([2, 1])
    with e1:
        email_lp = st.text_input("Ihre E-Mail-Adresse", placeholder="beispiel@firma.de", key="email_footer", label_visibility="collapsed")
    with e2:
        if st.button("Beratung anfordern", use_container_width=True, key="btn_footer"):
            if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email_lp):
                st.success("Anfrage gesendet! Wir kontaktieren Sie.")
            else:
                st.error("E-Mail ungültig.")

    st.markdown('</div>', unsafe_allow_html=True)

# --- 4. SEITE: EXPERTEN-CHECK ---
else:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("🛡️ Experten-System")
    
    tabs = st.tabs(["👤 Halter", "🚗 Technik", "📋 Modularer Check", "📊 Ergebnis"])
    
    with tabs[0]:
        st.subheader("Halterdaten")
        st.text_input("Name des Leasingnehmers")
    with tabs[1]:
        st.subheader("Fahrzeugdaten")
        st.text_input("FIN (17 Zeichen)")
    with tabs[2]:
        st.subheader("Modularer Check")
        # Deine modulare Logik hier...
        st.write("Prüfung der Karosserie, Räder und Innenraum.")
    with tabs[3]:
        st.metric("Gesamt-Minderwert", "0 €")
        st.button("PDF generieren")

    st.markdown('</div>', unsafe_allow_html=True)
