import streamlit as st
import datetime
import re

# --- 1. KONFIGURATION (Layout-Fix für mobile.de Look) ---
st.set_page_config(page_title="ReturnGuard", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #f3f5f6; }
    
    /* Container-Breite fixieren, damit nichts zerschießt */
    .block-container {
        max-width: 1100px !important;
        padding-top: 2rem !important;
    }

    /* Die weiße Karte */
    .main-card {
        background-color: white;
        padding: 40px;
        border-radius: 16px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.06);
        margin-top: 10px;
    }

    /* Typografie */
    .hero-title {
        font-size: 3rem !important;
        font-weight: 800 !important;
        color: #002b5c;
        line-height: 1.1;
        margin-bottom: 20px;
    }

    /* Button-Design */
    div.stButton > button {
        border-radius: 8px;
        font-weight: 600;
        height: 3rem;
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

# Zentrierter Header
h_col1, h_col2 = st.columns([1, 1])
with h_col1:
    st.markdown('<h2 style="color: #002b5c; margin:0; font-weight:800;">🛡️ ReturnGuard</h2>', unsafe_allow_html=True)

with h_col2:
    nav = st.segmented_control(
        "Navigation", ["Privatkunden", "Experten-Login"], 
        default="Privatkunden" if st.session_state.current_page == "Kunde" else "Experten-Login",
        label_visibility="collapsed"
    )
    if nav == "Privatkunden": st.session_state.current_page = "Kunde"
    else: st.session_state.current_page = "Experte"

st.write("---")

# --- 3. SEITE: KUNDEN-PORTAL ---
if st.session_state.current_page == "Kunde":
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    
    # Hero Sektion mit Bild-Fix
    c1, c2 = st.columns([1.2, 1], gap="medium")
    
    with c1:
        st.markdown('<h1 class="hero-title">Keine Angst vor der Leasing-Rückgabe</h1>', unsafe_allow_html=True)
        st.write("### Schützen Sie sich vor hohen Nachzahlungen durch unseren unabhängigen Vorab-Check.")
        
        st.markdown("""
        <div style="margin: 25px 0;">
        <p style="font-size: 1.1rem;">🛡️ <b>Unabhängig:</b> Wir bewerten objektiv nach offiziellen Standards.</p>
        <p style="font-size: 1.1rem;">📊 <b>Transparent:</b> Sofort-Bericht mit allen Minderwerten.</p>
        <p style="font-size: 1.1rem;">💰 <b>Ersparnis:</b> Gezielte Reparaturtipps statt teurer Pauschalen.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Jetzt Check anfragen", use_container_width=True, type="primary"):
            st.toast("Geben Sie unten Ihre E-Mail an!")

    with c2:
        # Stabiler Bild-Link für das hyperrealistische Auto
        st.image("https://img.freepik.com/free-photo/view-3d-car-with-high-detail_23-2150796914.jpg", 
                 caption="Digitale Schadensanalyse", use_container_width=True)

    st.write("---")
    
    # Prozess-Schritte
    st.subheader("Der ReturnGuard Ablauf")
    a1, a2, a3 = st.columns(3)
    a1.info("**1. Termin**\nExperte kommt zu Ihnen.")
    a2.info("**2. Scan**\nZustandsaufnahme per App.")
    a3.info("**3. Bericht**\nKostensicherheit erhalten.")

    st.write("---")
    
    # Lead-Formular
    st.subheader("Interesse? Wir beraten Sie gerne.")
    e1, e2 = st.columns([2, 1])
    email_lp = e1.text_input("Ihre E-Mail-Adresse", placeholder="ihre@mail.de", label_visibility="collapsed")
    if e2.button("Absenden", use_container_width=True):
        if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email_lp):
            st.success("Erfolg! Wir melden uns bei Ihnen.")
        else:
            st.error("E-Mail ungültig.")
            
    st.markdown('</div>', unsafe_allow_html=True)

# --- 4. SEITE: EXPERTEN-CHECK ---
else:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("🛡️ Experten-System")
    
    tabs = st.tabs(["👤 Halter", "🚗 Technik", "📋 Check", "📊 Export"])
    
    with tabs[0]:
        st.subheader("Halterdaten")
        st.text_input("Vollständiger Name")
        st.text_area("Interne Notizen")

    with tabs[1]:
        st.subheader("Fahrzeug-Identifikation")
        st.text_input("FIN (17 Zeichen)", max_chars=17)
        st.number_input("Aktueller KM-Stand", min_value=0, format="%d")
        st.date_input("Erstzulassung", value=datetime.date(2023,1,1))

    with tabs[2]:
        st.subheader("Modularer Check")
        items = ["Außenhaut", "Räder", "Innenraum"]
        costs = {}
        for item in items:
            st.write(f"### {item}")
            choice = st.segmented_control(f"Status {item}", ["Mangel", "Gebrauch", "i.O."], key=f"c_{item}", default="i.O.")
            if choice == "Mangel":
                costs[item] = st.number_input(f"Kosten {item} (€)", key=f"v_{item}", format="%d")
            else: costs[item] = 0

    with tabs[3]:
        total = sum(costs.values())
        st.metric("Gesamter Minderwert", f"{total} €")
        if st.button("Protokoll abschließen"):
            st.balloons()
            st.success("Zustandsbericht finalisiert.")

    st.markdown('</div>', unsafe_allow_html=True)
