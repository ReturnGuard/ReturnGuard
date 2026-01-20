import streamlit as st
import datetime
import re

# --- 1. KONFIGURATION & DESIGN ---
st.set_page_config(page_title="ReturnGuard", layout="wide", initial_sidebar_state="expanded")

# CSS für professionelles Branding und Navigation
st.markdown("""
    <style>
    /* Sidebar Navigation Fix */
    [data-testid="stSidebarNav"] {display: none;} /* Standard-Nav ausblenden */
    
    /* Hauptüberschrift Design */
    .main-title {
        font-size: 4rem !important;
        font-weight: 800;
        color: #002b5c;
        margin-bottom: 0px;
    }
    .sub-title {
        font-size: 1.4rem;
        color: #555;
        margin-bottom: 30px;
    }

    /* Feature Box Design */
    .feature-card {
        background-color: #f8f9fa;
        padding: 35px;
        border-radius: 15px;
        border-left: 8px solid #002b5c;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }

    /* Experten-Check Ampel-Logik */
    div[data-testid="stSegmentedControl"] button { height: 50px !important; flex: 1 !important; }
    div[data-testid="stSegmentedControl"] [data-testid="stBaseButton-secondary"]:nth-of-type(1)[aria-checked="true"] { background-color: #ff4b4b !important; color: white !important; }
    div[data-testid="stSegmentedControl"] [data-testid="stBaseButton-secondary"]:nth-of-type(2)[aria-checked="true"] { background-color: #ffa500 !important; color: white !important; }
    div[data-testid="stSegmentedControl"] [data-testid="stBaseButton-secondary"]:nth-of-type(3)[aria-checked="true"] { background-color: #28a745 !important; color: white !important; }
    
    /* KM-Eingabe ohne Pfeile */
    input[type=number]::-webkit-inner-spin-button, input[type=number]::-webkit-outer-spin-button { -webkit-appearance: none; margin: 0; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown('<h2 style="color: #002b5c; margin-bottom: 0;">🛡️ ReturnGuard</h2>', unsafe_allow_html=True)
    st.write("Professional Leasing Protection")
    st.write("---")
    
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Kunden-Portal"

    # Navigation Buttons mit Farblogik
    if st.button("🏠 Kunden-Portal", use_container_width=True, type="primary" if st.session_state.current_page == "Kunden-Portal" else "secondary"):
        st.session_state.current_page = "Kunden-Portal"
        st.rerun()
        
    if st.button("🛠️ Experten-Check (Intern)", use_container_width=True, type="primary" if st.session_state.current_page == "Experten-Check" else "secondary"):
        st.session_state.current_page = "Experten-Check"
        st.rerun()

    st.write("---")
    st.caption("© 2026 ReturnGuard System")

# --- 3. SEITE: KUNDEN-PORTAL ---
if st.session_state.current_page == "Kunden-Portal":
    st.markdown('<h1 class="main-title">ReturnGuard</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Schutz vor unerwarteten Kosten bei der Leasingrückgabe.</p>', unsafe_allow_html=True)

    col_img, col_info = st.columns([1.1, 1], gap="large")

    with col_img:
        # Bild-Fix: Wir nutzen ein hochauflösendes Blueprint-Beispiel
        st.image("https://img.freepik.com/free-vector/modern-car-top-view-design_23-2147915571.jpg", 
                 use_container_width=True, caption="Analyse der kritischen Rückgabebereiche")
        
        st.markdown('<h3 style="color: #002b5c; border-bottom: 2px solid #002b5c; display: inline-block;">Der Ablauf</h3>', unsafe_allow_html=True)
        st.markdown("""
        <div style="font-size: 1.15rem; line-height: 1.9; margin-top: 15px;">
        1️⃣ <b>Termin vereinbaren:</b> Flexibel bei Ihnen vor Ort.<br>
        2️⃣ <b>Zustands-Scan:</b> Aufnahme aller Details per ReturnGuard-App.<br>
        3️⃣ <b>Kosten-Check:</b> Sofortige Auswertung potenzieller Minderwerte.<br>
        4️⃣ <b>Reparatur:</b> Gezielte Empfehlungen zur Kostenminimierung.
        </div>
        """, unsafe_allow_html=True)

    with col_info:
        st.markdown("""
        <div class="feature-card">
            <h2 style="color: #002b5c; margin-top:0;">Warum ReturnGuard?</h2>
            <p style="font-size: 1.1rem; color: #444;">Leasinggeber berechnen oft hohe Pauschalen. Wir geben Ihnen die <b>Fakten</b> für eine faire Rückgabe.</p>
            <hr style="margin: 20px 0; border: 0; border-top: 1px solid #ddd;">
            <p style="font-size: 1.1rem;">✅ <b>Ersparnis:</b> Bis zu 60% geringere Nachzahlungen.</p>
            <p style="font-size: 1.1rem;">✅ <b>Sicherheit:</b> Unabhängiger Bericht als Beweismittel.</p>
            <p style="font-size: 1.1rem;">✅ <b>Expertise:</b> Bewertung nach modernsten Standards.</p>
            <p style="font-size: 1.1rem;">✅ <b>Echtzeit:</b> Digitales Protokoll sofort verfügbar.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("---")
        st.markdown('<h3 style="color: #002b5c;">Jetzt Beratung anfordern</h3>', unsafe_allow_html=True)
        email_lp = st.text_input("Ihre E-Mail-Adresse für ein Angebot:", placeholder="name@firma.de")
        
        if st.button("📩 Informationen jetzt senden", use_container_width=True):
            if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email_lp):
                st.success("Erfolgreich! Wir melden uns in Kürze bei Ihnen.")
            else:
                st.error("Bitte prüfen Sie Ihre E-Mail-Adresse.")

# --- 4. SEITE: EXPERTEN-CHECK ---
else:
    st.markdown('<h1 class="main-title">Experten-System</h1>', unsafe_allow_html=True)
    
    tab_halter, tab_tech, tab_check, tab_export = st.tabs(["👤 Halter", "🚗 Technik", "📋 Check", "📊 Export"])
    
    with tab_halter:
        st.subheader("Halterinformationen")
        c1, c2 = st.columns(2)
        c1.selectbox("Anrede", ["Firma", "Herr", "Frau"])
        c2.text_input("Name / Firma")
        st.text_area("Interne Bemerkung")

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
        if st.button("🏁 Bericht abschließen"):
            st.success("Zustandsbericht wurde generiert.")
