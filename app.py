import streamlit as st
import datetime
import re

# --- 1. KONFIGURATION & DESIGN ---
st.set_page_config(page_title="ReturnGuard", layout="wide", initial_sidebar_state="expanded")

# Erweitertes CSS für Sidebar-Navigation und Layout-Harmonie
st.markdown("""
    <style>
    /* Navigation Buttons in der Sidebar */
    [data-testid="stSidebarNav"] {display: none;} /* Versteckt Standard-Nav */
    
    .nav-button {
        display: block;
        width: 100%;
        padding: 15px;
        margin: 10px 0;
        text-align: left;
        background-color: transparent;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        color: #333;
        font-weight: bold;
        cursor: pointer;
        transition: 0.3s;
    }
    .nav-button:hover {
        background-color: #f0f2f6;
        border-color: #002b5c;
    }
    .nav-active {
        background-color: #002b5c !important;
        color: white !important;
        border: none;
    }

    /* Landingpage Optimierung */
    .main-title {
        font-size: 3.5rem !important;
        font-weight: 800;
        color: #002b5c;
        margin-bottom: 0;
        line-height: 1.2;
    }
    .sub-title {
        font-size: 1.5rem;
        color: #666;
        margin-bottom: 40px;
    }
    .feature-card {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 15px;
        border: 1px solid #eee;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        height: 100%;
    }
    .section-header {
        color: #002b5c;
        font-size: 1.8rem;
        margin-bottom: 20px;
        border-bottom: 2px solid #002b5c;
        display: inline-block;
        padding-bottom: 5px;
    }
    
    /* Experten-Check Buttons */
    div[data-testid="stSegmentedControl"] button { height: 50px !important; flex: 1 !important; }
    div[data-testid="stSegmentedControl"] [data-testid="stBaseButton-secondary"]:nth-of-type(1)[aria-checked="true"] { background-color: #ff4b4b !important; color: white !important; }
    div[data-testid="stSegmentedControl"] [data-testid="stBaseButton-secondary"]:nth-of-type(2)[aria-checked="true"] { background-color: #ffa500 !important; color: white !important; }
    div[data-testid="stSegmentedControl"] [data-testid="stBaseButton-secondary"]:nth-of-type(3)[aria-checked="true"] { background-color: #28a745 !important; color: white !important; }

    /* Hide Spinners */
    input[type=number]::-webkit-inner-spin-button, input[type=number]::-webkit-outer-spin-button { -webkit-appearance: none; margin: 0; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. MANUELLE SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown('<h1 style="color: #002b5c;">🛡️ ReturnGuard</h1>', unsafe_allow_html=True)
    st.write("Professional Leasing Protection")
    st.write("---")
    
    # Session State für Navigation initialisieren
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Kunden-Portal"

    # Buttons als Navigations-Ersatz
    if st.button("🏠 Kunden-Portal", use_container_width=True, type="primary" if st.session_state.current_page == "Kunden-Portal" else "secondary"):
        st.session_state.current_page = "Kunden-Portal"
        st.rerun()
        
    if st.button("🛠️ Experten-Check (Intern)", use_container_width=True, type="primary" if st.session_state.current_page == "Experten-Check" else "secondary"):
        st.session_state.current_page = "Experten-Check"
        st.rerun()

    st.write("---")
    st.caption("© 2026 ReturnGuard System")

# --- 3. SEITE: KUNDEN-PORTAL (LANDINGPAGE) ---
if st.session_state.current_page == "Kunden-Portal":
    # Hero Bereich
    st.markdown('<h1 class="main-title">ReturnGuard</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Schutz vor unerwarteten Kosten bei der Leasingrückgabe.</p>', unsafe_allow_html=True)

    # Layout: Bild links, Text rechts (gleichmäßig verteilt)
    col_img, col_info = st.columns([1, 1], gap="large")

    with col_img:
        st.image("https://raw.githubusercontent.com/Frankyboy1984/ReturnGuard/main/car_top_view_blueprint.png", 
                 use_container_width=True)
        
        st.markdown('<p class="section-header">Der Ablauf</p>', unsafe_allow_html=True)
        st.markdown("""
        <div style="font-size: 1.1rem; line-height: 1.8;">
        1️⃣ <b>Termin vereinbaren:</b> Wir kommen zu Ihnen oder Sie zu uns.<br>
        2️⃣ <b>Digitaler Scan:</b> Präzise Aufnahme aller Fahrzeugbereiche.<br>
        3️⃣ <b>Bericht erhalten:</b> Sofortige Übersicht über Mängel & Kosten.<br>
        4️⃣ <b>Reparatur-Option:</b> Smart-Repair Empfehlungen nutzen & sparen.
        </div>
        """, unsafe_allow_html=True)

    with col_info:
        st.markdown("""
        <div class="feature-card">
            <h3 style="color: #002b5c; margin-top:0;">Warum ReturnGuard?</h3>
            <p style="font-size: 1.1rem;">Leasinggeber berechnen bei der Rückgabe oft überhöhte Pauschalpreise für kleinste Schäden. Wir geben Ihnen die <b>Kontrolle zurück</b>.</p>
            <hr>
            <p>✅ <b>Ersparnis:</b> Bis zu 60% weniger Nachzahlungskosten.</p>
            <p>✅ <b>Sicherheit:</b> Unabhängiges Gutachten als Beweismittel.</p>
            <p>✅ <b>Expertise:</b> Bewertung nach modernsten Standards.</p>
            <p>✅ <b>Schnelligkeit:</b> Digitales Protokoll in Echtzeit.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("---")
        st.markdown('<h3 style="color: #002b5c;">Jetzt Beratung anfordern</h3>', unsafe_allow_html=True)
        email_lp = st.text_input("E-Mail-Adresse für Ihr Angebot:", placeholder="name@firma.de")
        
        c1, c2 = st.columns([1,1])
        if c1.button("📩 Informationen senden", use_container_width=True):
            if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email_lp):
                st.success("Anfrage erfolgreich versendet!")
            else:
                st.error("Ungültige E-Mail.")

# --- 4. SEITE: EXPERTEN-CHECK (INTERN) ---
else:
    st.markdown('<h1 class="main-title">Experten-System</h1>', unsafe_allow_html=True)
    
    tab_halter, tab_tech, tab_check, tab_export = st.tabs(["👤 Halter", "🚗 Technik", "📋 Check", "📊 Export"])
    
    with tab_halter:
        st.subheader("Halterinformationen")
        c1, c2 = st.columns(2)
        c1.selectbox("Anrede", ["Firma", "Herr", "Frau"])
        c2.text_input("Name / Firma")
        st.text_area("Interne Bemerkung (Alpha Controller)")

    with tab_tech:
        st.subheader("Fahrzeugdetails")
        t1, t2 = st.columns(2)
        if 'vin_clean' not in st.session_state: st.session_state['vin_clean'] = ""
        def format_vin():
            st.session_state.vin_clean = re.sub(r'[^a-zA-Z0-9]', '', st.session_state.vin_input_field).upper()
            st.session_state.vin_input_field = st.session_state.vin_clean
        t1.text_input("FIN (17 Zeichen)", max_chars=17, key="vin_input_field", on_change=format_vin)
        t2.text_input("Amtliches Kennzeichen")
        t1.number_input("Kilometerstand", min_value=0, format="%d")
        t2.date_input("Erstzulassung", value=datetime.date(2020,1,1), format="DD.MM.YYYY")
        st.divider()
        t1.selectbox("Getriebeart", ["Schaltung", "Automatik"])
        t2.selectbox("EURO Norm", ["Euro 6d", "Euro 6", "Euro 5", "Euro 4", "Elektro"])

    with tab_check:
        st.subheader("Zustandsbewertung")
        sections = {
            "Außenhaut & Karosserie": ["Lackzustand", "Dellen/Beulen", "Kratzer", "Steinschläge"],
            "Fahrwerk & Räder": ["Reifenprofil", "Felgenzustand", "Bremsanlage"],
            "Innenraum & Technik": ["Polster/Leder", "Geruch/Raucher", "Armaturen", "Fehlerspeicher"]
        }
        costs = {}
        for sec, items in sections.items():
            with st.expander(f"📦 {sec}", expanded=True):
                for item in items:
                    choice = st.segmented_control(f"**{item}**", ["Mangel", "Gebrauch", "i.O."], key=f"c_{item}", default="i.O.")
                    if choice == "Mangel":
                        costs[item] = st.number_input(f"Kosten {item} (€)", key=f"v_{item}", format="%d")
                    else:
                        costs[item] = 0

    with tab_export:
        total = sum(costs.values())
        st.metric("Gesamt-Minderwert", f"{total} €")
        if st.button("🏁 Gutachten finalisieren"):
            if len(st.session_state.get('vin_clean', '')) != 17:
                st.error("FIN ungültig!")
            else:
                st.success("Zustandsbericht erfolgreich generiert.")
