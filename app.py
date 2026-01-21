import streamlit as st
import re

# --- 1. KONFIGURATION & ERWEITERTES DESIGN ---
st.set_page_config(page_title="ReturnGuard", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* Hintergrundfarbe */
    .stApp {
        background-color: #f4f4f4;
    }

    /* Hero-Balken */
    .hero-header {
        background: #003366;
        height: 200px;
        position: relative;
        z-index: 0;
        text-align: center;
        color: white;
        padding: 50px 0;
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
        margin-top: 20px;
        position: relative;
    }

    .hero-title {
        font-size: 2.5rem !important;
        font-weight: bold;
        color: #ffffff;
        margin-bottom: 20px;
    }

    .package-container {
        display: flex;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 20px;
    }

    .package-card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 20px;
        flex: 1;
        min-width: 300px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        text-align: center;
    }

    .package-title {
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 10px;
    }

    .package-price {
        font-size: 1.2rem;
        color: #28a745;
        margin: 10px 0;
    }

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
    </style>
    """, unsafe_allow_html=True)

# Initialisierung Page State
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Kunde"

# --- 2. HEADER & NAVIGATION ---
st.markdown('<div class="hero-header"><h1 class="hero-title">Leasingrückgabe für Ihren Audi</h1></div>', unsafe_allow_html=True)

# --- 3. SEITE: KUNDEN-PORTAL ---
if st.session_state.current_page == "Kunde":
    st.markdown('<div class="main-card">', unsafe_allow_html=True)

    st.subheader("Unsere Pakete für Ihre Leasingrückgabe")
    
    st.markdown("""
    <div class="package-container">
        <div class="package-card">
            <h4 class="package-title">Basis Paket</h4>
            <p class="package-price">€199</p>
            <p>Check der Fahrzeugzustände, einfache Beratung.</p>
            <button class="stButton">Jetzt buchen</button>
        </div>
        <div class="package-card">
            <h4 class="package-title">Standard Paket</h4>
            <p class="package-price">€399</p>
            <p>Umfassende Schadensbewertung, Beratung durch Experten.</p>
            <button class="stButton">Jetzt buchen</button>
        </div>
        <div class="package-card">
            <h4 class="package-title">Premium Paket</h4>
            <p class="package-price">€599</p>
            <p>Rechtsberatung, vollständige Dokumentation.</p>
            <button class="stButton">Jetzt buchen</button>
        </div>
        <div class="package-card">
            <h4 class="package-title">VIP Paket</h4>
            <p class="package-price">€999</p>
            <p>Individuelle Betreuung, umfassende Rechtshilfe.</p>
            <button class="stButton">Jetzt buchen</button>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

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
        st.write("Prüfung der Karosserie, Räder und Innenraum.")
    with tabs[3]:
        st.metric("Gesamt-Minderwert", "0 €")
        st.button("PDF generieren")

    st.markdown('</div>', unsafe_allow_html=True)
