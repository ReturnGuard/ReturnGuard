import streamlit as st
import datetime
import re

# --- 1. KONFIGURATION (Das mobile.de Card-Layout) ---
st.set_page_config(page_title="ReturnGuard", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #f3f5f6; }
    
    /* Verhindert das Abschneiden der Headline oben */
    .block-container {
        max-width: 1100px !important;
        padding-top: 4rem !important;
    }

    /* Die weiße Haupt-Karte */
    .main-card {
        background-color: white;
        padding: 50px;
        border-radius: 16px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.06);
        margin-top: 20px;
    }

    /* ReturnGuard Headline Design */
    .hero-title {
        font-size: 3.2rem !important;
        font-weight: 800 !important;
        color: #002b5c;
        line-height: 1.1;
        margin-bottom: 25px;
    }

    /* Button-Design wie bei Profi-Portalen */
    div.stButton > button {
        border-radius: 8px;
        font-weight: 600;
        background-color: #002b5c;
        color: white;
        border: none;
        height: 3.2rem;
    }
    
    /* Experten-Check Ampel-Logik */
    div[data-testid="stSegmentedControl"] button { height: 50px !important; flex: 1 !important; }
    div[data-testid="stSegmentedControl"] [data-testid="stBaseButton-secondary"]:nth-of-type(1)[aria-checked="true"] { background-color: #ff4b4b !important; color: white !important; }
    div[data-testid="stSegmentedControl"] [data-testid="stBaseButton-secondary"]:nth-of-type(2)[aria-checked="true"] { background-color: #ffa500 !important; color: white !important; }
    div[data-testid="stSegmentedControl"] [data-testid="stBaseButton-secondary"]:nth-of-type(3)[aria-checked="true"] { background-color: #28a745 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. HEADER NAVIGATION ---
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Kunde"

h_col1, h_col2 = st.columns([1, 1])
with h_col1:
    st.markdown('<h2 style="color: #002b5c; margin:0; font-weight:800;">🛡️ ReturnGuard</h2>', unsafe_allow_html=True)

with h_col2:
    nav_choice = st.segmented_control(
        "Navigation", 
        ["Privatkunden", "Experten-Check"], 
        default="Privatkunden" if st.session_state.current_page == "Kunde" else "Experten-Check",
        label_visibility="collapsed"
    )
    if nav_choice == "Privatkunden": st.session_state.current_page = "Kunde"
    else: st.session_state.current_page = "Experte"

st.write("---")

# --- 3. SEITE: KUNDEN-PORTAL ---
if st.session_state.current_page == "Kunde":
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    
    # Layout wie auf dem Bild: Text links, Fahrzeug rechts
    c1, c2 = st.columns([1.2, 1], gap="large")
    
    with c1:
        st.markdown('<h1 class="hero-title">Leasingrückgabe ohne Risiko</h1>', unsafe_allow_html=True)
        st.write("### Schützen Sie sich vor hohen Nachzahlungen durch unseren unabhängigen Zustands-Check.")
        
        st.markdown("""
        <div style="margin: 30px 0;">
        <p style="font-size: 1.2rem;">🛡️ <b>Unabhängig:</b> Bewertung nach offiziellen Standards.</p>
        <p style="font-size: 1.2rem;">📊 <b>Transparent:</b> Sofort-Bericht mit allen Minderwerten.</p>
        <p style="font-size: 1.2rem;">💰 <b>Ersparnis:</b> Reparaturtipps statt teurer Pauschalen.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Jetzt Check anfragen", use_container_width=True):
            st.toast("E-Mail unten eingeben!")

    with c2:
        # HIER DEIN BILD EINTRAGEN
        # Falls du das Bild auf GitHub hast, ersetze die URL unten:
        st.image("document.querySelector("#primary > div.main > section.postcontent > div > div > div.postcontent-img > img")", 
                 use_container_width=True)

    st.write("---")
    
    # Der ReturnGuard Prozess
    st.subheader("So funktioniert ReturnGuard")
    p1, p2, p3 = st.columns(3)
    p1.info("**1. Aufnahme**\nExperte kommt zu Ihnen.")
    p2.info("**2. Analyse**\nDigitale Zustandsaufnahme.")
    p3.info("**3. Sicherheit**\nKostentransparenz erhalten.")

    st.write("---")
    
    # Lead-Sektion
    st.subheader("Interesse? Jetzt Kontakt aufnehmen.")
    e_col1, e_col2 = st.columns([2, 1])
    email_lp = e_col1.text_input("Ihre E-Mail-Adresse", placeholder="name@beispiel.de", label_visibility="collapsed")
    if e_col2.button("Informationen anfordern", use_container_width=True):
        if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email_lp):
            st.success("Anfrage erhalten! Wir melden uns.")
        else:
            st.error("E-Mail ungültig.")
            
    st.markdown('</div>', unsafe_allow_html=True)

# --- 4. SEITE: EXPERTEN-CHECK ---
else:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("🛡️ Experten-Zustandsbericht")
    
    tabs = st.tabs(["👤 Halter", "🚗 Technik", "📋 Check", "📊 Export"])
    
    # Hier folgen die bereits erstellten Formularfelder für den Experten...
    with tabs[2]:
        st.subheader("Modularer Zustands-Check")
        items = ["Karosserie", "Felgen/Reifen", "Innenraum"]
        costs = {}
        for item in items:
            st.write(f"### {item}")
            choice = st.segmented_control(f"Status {item}", ["Mangel", "Gebrauch", "i.O."], key=f"c_{item}", default="i.O.")
            if choice == "Mangel":
                costs[item] = st.number_input(f"Reparaturkosten {item} (€)", key=f"v_{item}", format="%d")
            else: costs[item] = 0
