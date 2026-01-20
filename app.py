import streamlit as st
import datetime
import re

# --- 1. KONFIGURATION & DESIGN (Mobile.de Look) ---
st.set_page_config(page_title="ReturnGuard", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #f3f5f6; }
    
    /* Verhindert das Abschneiden der Headline oben */
    .block-container {
        max-width: 1100px !important;
        padding-top: 5rem !important; 
        padding-bottom: 2rem !important;
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

    /* Button-Design: Professionell & Dunkelblau */
    div.stButton > button {
        border-radius: 8px;
        font-weight: 600;
        background-color: #002b5c;
        color: white;
        border: none;
        height: 3.5rem;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #004080;
        border: none;
    }
    
    /* Experten-Check Ampel-Logik */
    div[data-testid="stSegmentedControl"] button { height: 50px !important; flex: 1 !important; }
    div[data-testid="stSegmentedControl"] [data-testid="stBaseButton-secondary"]:nth-of-type(1)[aria-checked="true"] { background-color: #ff4b4b !important; color: white !important; }
    div[data-testid="stSegmentedControl"] [data-testid="stBaseButton-secondary"]:nth-of-type(2)[aria-checked="true"] { background-color: #ffa500 !important; color: white !important; }
    div[data-testid="stSegmentedControl"] [data-testid="stBaseButton-secondary"]:nth-of-type(3)[aria-checked="true"] { background-color: #28a745 !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. TOP NAVIGATION (Header) ---
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
    
    # Layout: Text links, Fahrzeug-Analyse rechts
    c1, c2 = st.columns([1.1, 1], gap="large")
    
    with c1:
        st.markdown('<h1 class="hero-title">Keine Angst vor der Leasing-Rückgabe</h1>', unsafe_allow_html=True)
        st.write("### Schützen Sie sich vor hohen Nachzahlungen durch unseren unabhängigen Vorab-Check.")
        
        st.markdown("""
        <div style="margin: 30px 0;">
        <p style="font-size: 1.2rem;">🛡️ <b>Unabhängig:</b> Wir bewerten objektiv nach offiziellen Standards.</p>
        <p style="font-size: 1.2rem;">📊 <b>Transparent:</b> Sofort-Bericht mit allen Minderwerten.</p>
        <p style="font-size: 1.2rem;">💰 <b>Ersparnis:</b> Gezielte Reparaturtipps statt teurer Pauschalen.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Jetzt Check anfragen", use_container_width=True):
            st.toast("Geben Sie unten Ihre E-Mail an!")

    with c2:
        # Einbindung des hochgeladenen Bildes (Fahrzeug mit Markierungen)
        st.image("https://raw.githubusercontent.com/Frankyboy1984/ReturnGuard/main/Gemini_Generated_Image_zdbbxqzdbbxqzdbb.jpg", 
                 caption="Digitale Schadensidentifikation an allen Bauteilen", 
                 use_container_width=True)

    st.write("---")
    
    # Prozess-Schritte
    st.subheader("Ihr Weg zur sicheren Rückgabe")
    a1, a2, a3 = st.columns(3)
    a1.info("**1. Termin**\nExperten-Besuch vereinbaren.")
    a2.info("**2. Analyse**\nZustandsaufnahme per App.")
    a3.info("**3. Sicherheit**\nMit Fakten zur Rückgabe.")

    st.write("---")
    
    # Lead-Formular
    st.subheader("Interesse? Wir beraten Sie gerne.")
    e1, e2 = st.columns([2, 1])
    email_lp = e1.text_input("Ihre E-Mail-Adresse", placeholder="beispiel@firma.de", label_visibility="collapsed")
    if e2.button("Absenden", use_container_width=True):
        if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email_lp):
            st.success("Erfolgreich! Wir melden uns in Kürze.")
        else:
            st.error("E-Mail ungültig.")
            
    st.markdown('</div>', unsafe_allow_html=True)

# --- 4. SEITE: EXPERTEN-CHECK (Intern) ---
else:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.title("🛡️ Experten-Zustandsbericht")
    
    tabs = st.tabs(["👤 Halter", "🚗 Technik", "📋 Check", "📊 Export"])
    
    with tabs[0]:
        st.subheader("Stammdaten")
        st.selectbox("Anrede", ["Firma", "Herr", "Frau"])
        st.text_input("Vollständiger Name")

    with tabs[1]:
        st.subheader("Fahrzeugdaten")
        st.text_input("FIN (17 Zeichen)", max_chars=17)
        st.number_input("Aktueller KM-Stand", min_value=0, format="%d")

    with tabs[2]:
        # Modulare Struktur für den Check [cite: 2026-01-20]
        st.subheader("Punktuelle Bewertung")
        items = ["Außenhaut & Karosserie", "Fahrwerk & Räder", "Verglasung & Optik", "Innenraum & Technik"]
        costs = {}
        for item in items:
            st.write(f"### {item}")
            choice = st.segmented_control(f"Status {item}", ["Mangel", "Gebrauch", "i.O."], key=f"c_{item}", default="i.O.")
            if choice == "Mangel":
                costs[item] = st.number_input(f"Reparaturkosten {item} (€)", key=f"v_{item}", format="%d")
            else: costs[item] = 0

    with tabs[3]:
        total = sum(costs.values())
        st.metric("Gesamter Minderwert", f"{total} €")
        if st.button("Protokoll abschließen"):
            st.balloons()
            st.success("Zustandsbericht wurde im System gespeichert.")

    st.markdown('</div>', unsafe_allow_html=True)
    
