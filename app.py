import streamlit as st
import datetime
import re

# --- 1. KONFIGURATION & ERWEITERTES DESIGN (ReturnGuard CI) ---
st.set_page_config(page_title="ReturnGuard", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* Der ehemals weiße Balken wird nun zum Hero-Banner */
    .hero-banner {
        background: linear-gradient(135deg, #002b5c 0%, #004080 100%);
        padding: 60px;
        border-radius: 12px 12px 0 0; /* Oben abgerundet */
        color: white;
        text-align: center;
        margin-bottom: -20px; /* Zieht die weiße Karte optisch heran */
    }
    
    .main-card {
        background-color: white;
        padding: 40px;
        border-radius: 0 0 12px 12px; /* Unten abgerundet */
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. HEADER NAVIGATION ---
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Kunde"

h_col1, h_col2 = st.columns([1, 1])
with h_col1:
    st.markdown('<h2 style="color: #002b5c; margin:0; font-weight:800; cursor:default;">🛡️ ReturnGuard</h2>', unsafe_allow_html=True)

with h_col2:
    nav = st.segmented_control(
        "Nav", ["Privatkunden", "Experten-Login"], 
        default="Privatkunden" if st.session_state.current_page == "Kunde" else "Experten-Login",
        label_visibility="collapsed"
    )
    if nav == "Privatkunden": st.session_state.current_page = "Kunde"
    else: st.session_state.current_page = "Experte"

st.write("---")

# --- 3. SEITE: KUNDEN-PORTAL ---
if st.session_state.current_page == "Kunde":
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    
  # --- Hero Sektion: Fokus auf das Analyse-Bild ---
    c1, c2 = st.columns([1.1, 1], gap="large")
    
    with c1:
        st.markdown('<h1 class="hero-title">Leasingrückgabe ohne Überraschungen</h1>', unsafe_allow_html=True)
        st.markdown('<p class="sub-title">Schützen Sie sich vor unfairen Nachzahlungen durch unseren unabhängigen Check.</p>', unsafe_allow_html=True)
        
        st.markdown("""
        <div style="margin-bottom: 35px;">
        <div class="usp-item">✅ <b>Präzise:</b> Detaillierte Schadensmarkierung</div>
        <div class="usp-item">✅ <b>Fair:</b> Bewertung nach offiziellen Standards</div>
        <div class="usp-item">✅ <b>Profitabel:</b> Bis zu 60% Ersparnis durch Tipps</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Jetzt Check anfragen", use_container_width=True):
            st.toast("E-Mail Feld wird fokussiert...")

    with c2:
        # Achte darauf, dass dieses Bild 'analyse.png' nun korrekt hochgeladen ist!
        st.image("analyse.png", 
                 caption="Unsere digitale Experten-Analyse", 
                 use_container_width=True)
       
    # Der ReturnGuard Prozess (Horizontaler Fokus)
    st.subheader("In 3 Schritten zur Kostensicherheit")
    p1, p2, p3 = st.columns(3)
    p1.info("**1. Aufnahme**\nExperten-Begutachtung vor Ort oder via App.")
    p2.info("**2. Analyse**\nAbgleich mit den Kriterien Ihres Leasinggebers.")
    p3.info("**3. Bericht**\nErhalt des digitalen Rückgabe-Protokolls.")

    # Lead-Sektion (Optimierte Conversion-Box)
    st.markdown("""
    <div class="lead-container">
        <h3>Interesse an einer kostenlosen Erstberatung?</h3>
        <p>Hinterlassen Sie Ihre E-Mail, wir melden uns innerhalb von 24 Stunden.</p>
    </div>
    """, unsafe_allow_html=True)
    
    e1, e2 = st.columns([2, 1])
    with e1:
        email_lp = st.text_input("Ihre E-Mail-Adresse", placeholder="beispiel@firma.de", label_visibility="collapsed")
    with e2:
        if st.button("Beratung anfordern", use_container_width=True):
            if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email_lp):
                st.success("Anfrage gesendet!")
            else:
                st.error("E-Mail ungültig.")
            
    st.markdown('</div>', unsafe_allow_html=True)

# --- 4. SEITE: EXPERTEN-CHECK (Modulare Struktur) ---
else:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("🛡️ Experten-System")
    
    tabs = st.tabs(["👤 Halter", "🚗 Technik", "📋 Modularer Check", "📊 Ergebnis"])
    
    with tabs[0]:
        st.subheader("Halter- & Kundendaten")
        st.text_input("Vollständiger Name des Leasingnehmers")
        st.text_area("Besondere Vereinbarungen (z.B. Wartungsvertrag)")

    with tabs[1]:
        st.subheader("Fahrzeug-Identifikation")
        st.text_input("FIN (17 Zeichen)", max_chars=17)
        st.number_input("Aktueller Kilometerstand", min_value=0, format="%d")
        st.date_input("Tag der Erstzulassung")

    with tabs[2]:
        # Hier greift die neue modulare Logik [cite: 2026-01-20]
        st.subheader("Detaillierte Prüfung")
        sections = {
            "Außenhaut & Karosserie": ["Lackzustand", "Dellen/Beulen", "Hagelschäden"],
            "Fahrwerk & Räder": ["Felgenzustand", "Reifenprofil", "Bremsanlage"],
            "Innenraum & Technik": ["Polsterung", "Elektronik-Check", "Geruchsprobe"]
        }
        
        costs = {}
        for sec, items in sections.items():
            with st.expander(f"📦 {sec}", expanded=True):
                for item in items:
                    c1, c2 = st.columns([2, 1])
                    with c1:
                        res = st.segmented_control(f"{item}", ["Mangel", "i.O."], key=f"c_{item}", default="i.O.")
                    with c2:
                        if res == "Mangel":
                            costs[item] = st.number_input(f"Kosten (€)", key=f"v_{item}", min_value=0, format="%d")
                        else:
                            costs[item] = 0

    with tabs[3]:
        total = sum(costs.values())
        st.metric("Berechneter Minderwert (Gesamt)", f"{total} €")
        st.markdown("> **Smart-Repair Tipp:** Durch professionelle Aufbereitung der Mängel lässt sich die Nachzahlung oft um bis zu 50% reduzieren.")
        if st.button("Zustandsbericht finalisieren & PDF senden"):
            st.balloons()
            st.success("Bericht erfolgreich an den Kunden versandt.")

    st.markdown('</div>', unsafe_allow_html=True)
