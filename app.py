import streamlit as st
import datetime
import re

# --- 1. KONFIGURATION & CSS-FIX ---
st.set_page_config(page_title="ReturnGuard", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #f3f5f6; }
    
    /* Fix für abgeschnittene Headline: Mehr Abstand oben */
    .block-container {
        max-width: 1100px !important;
        padding-top: 5rem !important; /* Erhöht, damit Headline nicht klebt */
        padding-bottom: 2rem !important;
    }

    /* Die weiße Haupt-Karte */
    .main-card {
        background-color: white;
        padding: 40px;
        border-radius: 16px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.06);
        margin-top: 20px;
    }

    /* Headline Design */
    .hero-title {
        font-size: 2.8rem !important;
        font-weight: 800 !important;
        color: #002b5c;
        line-height: 1.2;
        margin-bottom: 20px;
    }

    /* Button-Styling */
    div.stButton > button {
        border-radius: 8px;
        font-weight: 600;
        background-color: #002b5c;
        color: white;
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

# Header-Leiste
t_col1, t_col2 = st.columns([1, 1])
with t_col1:
    st.markdown('<h2 style="color: #002b5c; margin:0; font-weight:800;">🛡️ ReturnGuard</h2>', unsafe_allow_html=True)

with t_col2:
    nav_choice = st.segmented_control(
        "Navigation", 
        ["Privatkunden", "Experten-Login"], 
        default="Privatkunden" if st.session_state.current_page == "Kunde" else "Experten-Login",
        label_visibility="collapsed"
    )
    if nav_choice == "Privatkunden": st.session_state.current_page = "Kunde"
    else: st.session_state.current_page = "Experte"

st.write("---")

# --- 3. SEITE: KUNDEN-PORTAL ---
if st.session_state.current_page == "Kunde":
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    
    c1, c2 = st.columns([1.2, 1], gap="large")
    
    with c1:
        st.markdown('<h1 class="hero-title">Keine Angst vor der Leasing-Rückgabe</h1>', unsafe_allow_html=True)
        st.write("### Schützen Sie sich vor hohen Nachzahlungen durch unseren unabhängigen Vorab-Check.")
        
        st.markdown("""
        <div style="margin: 25px 0;">
        <p style="font-size: 1.1rem;">🛡️ <b>Unabhängig:</b> Bewertung nach offiziellen Standards.</p>
        <p style="font-size: 1.1rem;">📊 <b>Transparent:</b> Sofort-Bericht mit allen Minderwerten.</p>
        <p style="font-size: 1.1rem;">💰 <b>Ersparnis:</b> Gezielte Reparaturtipps statt teurer Pauschalen.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Jetzt Check anfragen", use_container_width=True):
            st.toast("Bitte nutzen Sie das Kontaktfeld unten.")

    with c2:
        # Hier ist das von uns kreierte Bild (Hyperrealistische Analyse) integriert
        st.image("https://img.freepik.com/premium-photo/modern-luxury-car-with-high-detail-finish-3d-render_634443-11.jpg", 
                 caption="Digitale Schadensanalyse durch unsere Experten", 
                 use_container_width=True)

    st.write("---")
    
    # Prozess-Übersicht
    st.subheader("Ihr Weg zur sicheren Rückgabe")
    a1, a2, a3 = st.columns(3)
    a1.info("**1. Termin**\nExperten-Besuch vereinbaren.")
    a2.info("**2. Analyse**\nZustandsaufnahme per App.")
    a3.info("**3. Sicherheit**\nMit Fakten zur Rückgabe.")

    st.write("---")
    
    # Lead-Formular
    st.subheader("Interesse? Wir beraten Sie gerne.")
    e_col1, e_col2 = st.columns([2, 1])
    email_lp = e_col1.text_input("Ihre E-Mail-Adresse", placeholder="name@beispiel.de", label_visibility="collapsed")
    if e_col2.button("Absenden", use_container_width=True):
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
        st.text_area("Interne Bemerkungen")

    with tabs[1]:
        st.subheader("Fahrzeugdaten")
        if 'vin_clean' not in st.session_state: st.session_state['vin_clean'] = ""
        def format_vin():
            st.session_state.vin_clean = re.sub(r'[^a-zA-Z0-9]', '', st.session_state.vin_input_field).upper()
            st.session_state.vin_input_field = st.session_state.vin_clean
        st.text_input("FIN (17 Zeichen)", max_chars=17, key="vin_input_field", on_change=format_vin)
        st.number_input("Aktueller KM-Stand", min_value=0, format="%d")
        st.date_input("Erstzulassung", value=datetime.date(2023,1,1))

    with tabs[2]:
        st.subheader("Zustands-Check")
        items = ["Karosserie", "Räder", "Innenraum", "Verglasung"]
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
        if st.button("Bericht finalisieren"):
            st.balloons()
            st.success("Daten wurden im System gespeichert.")

    st.markdown('</div>', unsafe_allow_html=True)
