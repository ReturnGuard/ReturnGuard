import streamlit as st
import datetime
import re

# --- 1. KONFIGURATION & DESIGN ---
st.set_page_config(page_title="ReturnGuard", layout="wide")

st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { height: 50px; background-color: #f0f2f6; border-radius: 5px; }
    .stTabs [aria-selected="true"] { background-color: #002b5c !important; color: white !important; }

    /* Farblogik für Experten-Check Buttons */
    div[data-testid="stSegmentedControl"] button { height: 55px !important; font-weight: bold !important; flex: 1 !important; }
    div[data-testid="stSegmentedControl"] [data-testid="stBaseButton-secondary"]:nth-of-type(1)[aria-checked="true"] { background-color: #ff4b4b !important; color: white !important; }
    div[data-testid="stSegmentedControl"] [data-testid="stBaseButton-secondary"]:nth-of-type(2)[aria-checked="true"] { background-color: #ffa500 !important; color: white !important; }
    div[data-testid="stSegmentedControl"] [data-testid="stBaseButton-secondary"]:nth-of-type(3)[aria-checked="true"] { background-color: #28a745 !important; color: white !important; }
    
    input[type=number]::-webkit-inner-spin-button, input[type=number]::-webkit-outer-spin-button { -webkit-appearance: none; margin: 0; }

    /* Landingpage Styling */
    .hero-section { background-color: #002b5c; padding: 40px; border-radius: 15px; color: white; text-align: center; margin-bottom: 30px; }
    .feature-box { background-color: #ffffff; padding: 25px; border-radius: 12px; border: 1px solid #e0e0e0; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .instruction-text { font-size: 1.05rem; line-height: 1.6; color: #333; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. NAVIGATION ---
with st.sidebar:
    st.title("🛡️ ReturnGuard")
    page = st.selectbox("Menü", ["🏠 Kunden-Portal", "🛠️ Experten-Check (Intern)"])
    st.write("---")
    st.caption("Version 1.2.0 - 2026")

# --- 3. SEITE: KUNDEN-PORTAL ---
if page == "🏠 Kunden-Portal":
    st.markdown('<div class="hero-section"><h1>🛡️ ReturnGuard</h1><p style="font-size: 1.3rem;">Professionelle Zustandsberichte für Ihre Leasingrückgabe</p></div>', unsafe_allow_html=True)

    col_img, col_info = st.columns([0.55, 0.45])

    with col_img:
        st.subheader("Analysebereiche am Fahrzeug")
        # Professionelle 2D Draufsicht (Platzhalter durch ein neutrales Auto-Diagramm ersetzt)
        st.image("https://raw.githubusercontent.com/Frankyboy1984/ReturnGuard/main/car_top_view_blueprint.png", 
                 caption="Präzise Erfassung aller Schadensbereiche.")
        
        st.markdown("""
        <div class="instruction-text">
        <h3>So funktioniert ReturnGuard für Sie:</h3>
        <ol>
            <li><b>Termin vor Rückgabe:</b> Wir prüfen Ihr Fahrzeug ca. 2-4 Wochen vor dem Abgabetermin.</li>
            <li><b>Detaillierte Erfassung:</b> Unsere Experten scannen die markierten Bereiche auf Dellen, Kratzer und Verschleiß.</li>
            <li><b>Kosten-Analyse:</b> Sie erhalten sofort eine Übersicht der potenziellen Minderwerte.</li>
            <li><b>Handlungsempfehlung:</b> Wir zeigen Ihnen, welche Schäden per Smart-Repair günstiger behoben werden können.</li>
        </ol>
        </div>
        """, unsafe_allow_html=True)

    with col_info:
        st.markdown("""
        <div class="feature-box">
            <h3>Ihre Vorteile</h3>
            <p>✅ <b>Hohe Ersparnis:</b> Vermeiden Sie überteuerte pauschale Abrechnungen der Leasinggeber.</p>
            <p>✅ <b>Volle Transparenz:</b> Sie wissen genau, in welchem Zustand Ihr Fahrzeug zurückgeht.</p>
            <p>✅ <b>Keine Überraschungen:</b> Ein unabhängiges Gutachten als Argumentationsgrundlage.</p>
            <p>✅ <b>Zeitgewinn:</b> Schnelle Abwicklung durch digitale Protokollierung.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("---")
        st.subheader("Interesse geweckt?")
        st.write("Geben Sie Ihre E-Mail an. Wir senden Ihnen eine Checkliste für die Rückgabe und melden uns für eine Beratung.")
        email_lp = st.text_input("E-Mail-Adresse:", placeholder="beispiel@mail.de")
        if st.button("Jetzt Informationen anfordern"):
            if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email_lp):
                st.success("Erfolgreich! Wir haben Ihre Anfrage erhalten.")
            else:
                st.error("Bitte eine gültige E-Mail eingeben.")

# --- 4. SEITE: EXPERTEN-CHECK ---
else:
    # (Hier bleibt dein bewährter Experten-Code mit Halter, Technik, Check und Export stehen)
    st.title("🛠️ Interner Experten-Bereich")
    st.info("Bitte nutzen Sie die Tabs für die Fahrzeugaufnahme.")
    
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
        st.divider()
        t1.selectbox("Getriebeart", ["Schaltung", "Automatik"])
        t2.selectbox("EURO Norm", ["Euro 6d", "Euro 6", "Euro 5", "Euro 4", "Elektro"])

    with tab_check:
        st.subheader("Zustandsbewertung")
        sections = {
            "Außenhaut": ["Lack", "Dellen", "Kratzer"],
            "Räder": ["Reifen", "Felgen"],
            "Innenraum": ["Polster", "Geruch"]
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
        if st.button("🏁 Gutachten abschließen"):
            st.success("Bericht wurde generiert.")
            
