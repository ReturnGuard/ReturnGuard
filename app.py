import streamlit as st
import datetime
import re

# --- 1. KONFIGURATION & ERWEITERTES DESIGN (ReturnGuard CI) ---
st.set_page_config(page_title="ReturnGuard", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* Hintergrund & Reduzierung des oberen Abstands */
    .stApp { background-color: #f3f5f6; }
    
    /* Hero-Balken oben (Dunkelblau) */
    .hero-header {
        background: linear-gradient(135deg, #002b5c 0%, #004080 100%);
        height: 320px;
        width: 100%;
        position: absolute;
        top: 0;
        left: 0;
        z-index: 0;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        color: white;
        text-align: center;
        padding-bottom: 50px;
    }

    /* Container für den Inhalt, damit er über dem Blau schwebt */
    .block-container {
        max-width: 1100px !important;
        padding-top: 40px !important;
        z-index: 1;
    }

    /* Weiße Haupt-Karte mit weichem Schatten */
    .main-card {
        background-color: white;
        padding: 45px;
        border-radius: 12px;
        box-shadow: 0 12px 40px rgba(0,0,0,0.12);
        margin-top: 160px; /* Platz für den Hero-Balken */
        position: relative;
    }

    .hero-title {
        font-size: 3.2rem !important;
        font-weight: 800 !important;
        color: #002b5c;
        line-height: 1.1;
        margin-bottom: 20px;
    }

    div.stButton > button {
        border-radius: 6px;
        font-weight: 700;
        background-color: #002b5c;
        color: white;
        height: 3.8rem;
        border: none;
    }

    .usp-item {
        display: flex;
        align-items: center;
        margin-bottom: 12px;
        font-size: 1.15rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialisierung Page State
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Kunde"

# --- 2. HEADER & NAVIGATION ---
# Wir platzieren die Navigation über den Hero-Balken
st.markdown('<div class="hero-header"></div>', unsafe_allow_html=True)

nav_col1, nav_col2 = st.columns([1, 1])
with nav_col1:
    st.markdown('<h2 style="color: white; margin:0; font-weight:800;">🛡️ ReturnGuard</h2>', unsafe_allow_html=True)
with nav_col2:
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
        st.markdown('<p style="font-size:1.3rem; color:#4a5568;">Schützen Sie sich vor unfairen Nachzahlungen durch unseren unabhängigen Check.</p>', unsafe_allow_html=True)
        
        st.markdown("""
        <div style="margin: 30px 0;">
        <div class="usp-item">✅ <b>Präzise:</b> Detaillierte Schadensmarkierung</div>
        <div class="usp-item">✅ <b>Fair:</b> Bewertung nach offiziellen Standards</div>
        <div class="usp-item">✅ <b>Profitabel:</b> Bis zu 60% Ersparnis durch Tipps</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Jetzt Check anfragen", use_container_width=True):
            st.toast("E-Mail Feld wird fokussiert...")

    with c2:
        # Hier wird nun dein Bild geladen (Achte auf Analyse.png vs analyse.png)
        st.image("Analyse.png", 
                 caption="Unsere digitale Experten-Analyse", 
                 use_container_width=True)
        
    st.write("---")
    st.subheader("In 3 Schritten zur Kostensicherheit")
    p1, p2, p3 = st.columns(3)
    p1.info("**1. Aufnahme**\nExperten-Begutachtung vor Ort oder via App.")
    p2.info("**2. Analyse**\nAbgleich mit den Kriterien Ihres Leasinggebers.")
    p3.info("**3. Bericht**\nErhalt des digitalen Rückgabe-Protokolls.")

    st.markdown('</div>', unsafe_allow_html=True)

# --- 4. SEITE: EXPERTEN-CHECK ---
else:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("🛡️ Experten-System")
    # ... Rest deines Experten-Codes bleibt gleich ...
    st.markdown('</div>', unsafe_allow_html=True)
