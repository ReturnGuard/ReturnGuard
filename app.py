import streamlit as st
import datetime
import re

# --- 1. KONFIGURATION & ERWEITERTES DESIGN (ReturnGuard CI) ---
st.set_page_config(page_title="ReturnGuard", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* Hintergrundfarbe */
    .stApp {
        background-color: #f4f4f4;
    }

    /* Hero-Balken */
    .hero-header {
        background: #004080;
        height: 200px;
        position: relative;
        z-index: 0;
    }

    /* Container für den Inhalt */
    .block-container {
        max-width: 1200px !important;
        padding-top: 20px !important;
        z-index: 1;
    }

    /* Hauptkarte */
    .main-card {
        background-color: white;
        padding: 30px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.15);
        margin-top: 80px;
        position: relative;
    }

    .hero-title {
        font-size: 2.5rem !important;
        font-weight: bold;
        color: #002b5c;
        line-height: 1.2;
        margin-bottom: 15px;
    }

    /* Leadbox */
    .lead-container {
        background-color: #e9ecef;
        padding: 20px;
        border-radius: 6px;
        border: 1px solid #ced4da;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    div.stButton > button {
        border-radius: 5px;
        font-weight: 600;
        background-color: #007bff;
        color: white;
        height: 40px;
        border: none;
    }

    .usp-item {
        display: flex;
        align-items: center;
        margin-bottom: 8px;
        font-size: 1rem;
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
    
    c1, c2 = st.columns([1.5, 1], gap="large")
    
    with c1:
        st.markdown('<h1 class="hero-title">Leasingrückgabe ohne Überraschungen</h1>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:1.1rem; color:#4a5568;">Schützen Sie sich vor unfairen Nachzahlungen durch unseren unabhängigen Check.</p>', unsafe_allow_html=True)
        
        st.markdown("""
        <div style="margin: 20px 0;">
        <div class="usp-item">✅ <b>Präzise:</b> Detaillierte Schadensmarkierung</div>
        <div class="usp-item">✅ <b>Fair:</b> Bewertung nach offiziellen Standards</div>
        <div class="usp-item">✅ <b>Profitabel:</b> Bis zu 60% Ersparnis durch Tipps</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Jetzt Check anfragen", use_container_width=True):
            st.toast("Bitte scrollen Sie zum E-Mail-Feld.")

    with c2:
        st.image("Analyse.png", caption="Unsere digitale Experten-Analyse", use_container_width=True)

    st.write("---")

    # Prozess
    st.subheader("In 3 Schritten zur Kostensicherheit")
    p1, p2, p3 = st.columns(3)
    p1.info("**1. Aufnahme**\nExperten-Begutachtung vor Ort oder via App.")
    p2.info("**2. Analyse**\nAbgleich mit den Kriterien Ihres Leasinggebers.")
    p3.info("**3. Bericht**\nErhalt des digitalen Rückgabe-Protokolls.")

    # Lead-Sektion
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
