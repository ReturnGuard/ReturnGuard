import streamlit as st
import re
from datetime import datetime
import json

# ==================== KONFIGURATION ====================
st.set_page_config(
    page_title="ReturnGuard - Leasingrückgabe ohne Sorgen",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="🛡️"
)

# ==================== SESSION STATE ====================
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Lazy initialization - only create when needed
def init_calculator_state():
    if 'damages' not in st.session_state:
        st.session_state.damages = {}
    if 'vehicle_class' not in st.session_state:
        st.session_state.vehicle_class = 'Mittelklasse'
    if 'vehicle_year' not in st.session_state:
        st.session_state.vehicle_year = 2020
    if 'calculation_done' not in st.session_state:
        st.session_state.calculation_done = False
    if 'total_cost' not in st.session_state:
        st.session_state.total_cost = 0

# ==================== CACHED DATA ====================
@st.cache_data
def get_damage_costs(vehicle_class):
    """Cached damage costs calculation"""
    multipliers = {
        'Kompaktklasse': 0.7,
        'Mittelklasse': 1.0,
        'Oberklasse': 1.4,
        'Luxusklasse': 2.0
    }
    mult = multipliers.get(vehicle_class, 1.0)

    base_costs = {
        'Frontschürze': [0, 120, 280, 650, 1200],
        'Heckschürze': [0, 110, 260, 620, 1150],
        'Kotflügel vorn links': [0, 130, 320, 720, 1350],
        'Kotflügel vorn rechts': [0, 130, 320, 720, 1350],
        'Kotflügel hinten links': [0, 125, 310, 700, 1300],
        'Kotflügel hinten rechts': [0, 125, 310, 700, 1300],
        'Tür Fahrerseite': [0, 140, 350, 780, 1450],
        'Tür Beifahrerseite': [0, 140, 350, 780, 1450],
        'Tür hinten links': [0, 135, 340, 760, 1420],
        'Tür hinten rechts': [0, 135, 340, 760, 1420],
        'Motorhaube': [0, 150, 380, 850, 1550],
        'Dach': [0, 180, 450, 950, 1800],
        'Heckklappe/Kofferraum': [0, 145, 370, 820, 1500],
        'Felgen (Satz)': [0, 200, 480, 1100, 2200],
        'Windschutzscheibe': [0, 80, 350, 850, 1200],
        'Seitenscheiben': [0, 60, 180, 420, 800],
        'Sitze': [0, 90, 240, 580, 1100],
        'Armaturenbrett': [0, 70, 190, 450, 900],
        'Teppich/Fußmatten': [0, 50, 140, 320, 650],
        'Lackierung gesamt': [0, 250, 650, 1500, 3500],
    }

    adjusted_costs = {}
    for part, costs in base_costs.items():
        adjusted_costs[part] = [int(cost * mult) for cost in costs]

    return adjusted_costs

@st.cache_data
def get_damage_levels():
    """Cached damage level descriptions"""
    return [
        '0 - Keine Beschädigung',
        '1 - Leichte Kratzer/Gebrauchsspuren',
        '2 - Mittlere Kratzer/Dellen',
        '3 - Starke Beschädigungen',
        '4 - Sehr starke Beschädigungen/Austausch'
    ]

# ==================== MINIMAL CORE CSS ====================
st.markdown("""
<style>
* {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    box-sizing: border-box;
}

.stApp {
    background: #F9FAFB;
}

/* NAVIGATION */
.top-nav {
    background: white;
    border-bottom: 1px solid #E5E7EB;
    padding: 15px 0;
    position: sticky;
    top: 0;
    z-index: 999;
}

.nav-brand {
    text-align: center;
    font-size: 1.4rem;
    font-weight: 600;
    color: #1B365D;
    margin-bottom: 12px;
}

div[data-testid="column"] > div.stButton > button {
    background: transparent;
    color: #6B7280;
    border: 1px solid #E5E7EB;
    box-shadow: none;
    font-weight: 500;
    padding: 10px 15px;
    font-size: 0.9rem;
}

div[data-testid="column"] > div.stButton > button:hover {
    background: #F3F4F6;
    color: #1F2937;
    border-color: #1B365D;
}

/* BUTTONS */
div.stButton > button {
    background: linear-gradient(135deg, #1B365D 0%, #1E3A8A 100%);
    color: white;
    border: none;
    padding: 14px 30px;
    border-radius: 8px;
    font-weight: 600;
    width: 100%;
}

div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(27, 54, 93, 0.3);
}

/* RESPONSIVE */
@media (max-width: 768px) {
    .nav-brand { font-size: 1.2rem; }
    div[data-testid="column"] > div.stButton > button {
        padding: 8px 10px;
        font-size: 0.85rem;
    }
}
</style>
""", unsafe_allow_html=True)

# ==================== NAVIGATION ====================
st.markdown('<div class="top-nav">', unsafe_allow_html=True)
st.markdown('<div class="nav-brand">🛡️ ReturnGuard</div>', unsafe_allow_html=True)

nav_cols = st.columns(8)
with nav_cols[0]:
    if st.button("🏠 Home", use_container_width=True):
        st.session_state.page = 'home'
        st.rerun()
with nav_cols[1]:
    if st.button("👥 Über uns", use_container_width=True):
        st.session_state.page = 'about'
        st.rerun()
with nav_cols[2]:
    if st.button("📦 Leistungen", use_container_width=True):
        st.session_state.page = 'services'
        st.rerun()
with nav_cols[3]:
    if st.button("💰 Rechner", use_container_width=True):
        st.session_state.page = 'calculator'
        st.rerun()
with nav_cols[4]:
    if st.button("❓ FAQ", use_container_width=True):
        st.session_state.page = 'faq'
        st.rerun()
with nav_cols[5]:
    if st.button("📝 Blog", use_container_width=True):
        st.session_state.page = 'blog'
        st.rerun()
with nav_cols[6]:
    if st.button("📞 Kontakt", use_container_width=True):
        st.session_state.page = 'contact'
        st.rerun()
with nav_cols[7]:
    if st.button("⚖️ Rechtliches", use_container_width=True):
        st.session_state.page = 'legal'
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# ==================== PAGE-SPECIFIC CSS & CONTENT ====================
# LAZY LOADING: Only load CSS and content for current page

if st.session_state.page == 'home':
    # Load home page CSS only
    st.markdown("""
    <style>
    .hero-section {
        background: linear-gradient(135deg, rgba(27, 54, 93, 0.95) 0%, rgba(30, 58, 138, 0.92) 100%),
                    url('https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?w=1920') center/cover;
        padding: 80px 20px 60px 20px;
        text-align: center;
        color: white;
        border-radius: 10px;
        margin: 20px 0;
    }
    .hero-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 15px;
    }
    .hero-subtitle {
        font-size: 1.2rem;
        margin-bottom: 25px;
        opacity: 0.95;
    }
    .hero-cta {
        display: inline-block;
        background: #059669;
        color: white;
        padding: 14px 40px;
        border-radius: 8px;
        font-weight: 600;
        text-decoration: none;
    }
    .stat-box {
        text-align: center;
        padding: 30px;
        background: white;
        border-radius: 8px;
        margin: 10px;
    }
    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1B365D;
    }
    .stat-label {
        color: #6B7280;
        margin-top: 5px;
    }
    @media (max-width: 768px) {
        .hero-title { font-size: 1.8rem; }
        .hero-subtitle { font-size: 1rem; }
        .stat-number { font-size: 2rem; }
    }
    </style>
    """, unsafe_allow_html=True)

    # Hero Section
    st.markdown('''
        <div class="hero-section">
            <h1 class="hero-title">Leasingrückgabe ohne böse Überraschungen</h1>
            <p class="hero-subtitle">
                Schützen Sie sich vor unfairen Nachzahlungen. Unsere Experten
                stehen Ihnen von der Prüfung bis zur Verhandlung zur Seite.
            </p>
            <a href="#calculator" class="hero-cta">Jetzt kostenlos berechnen →</a>
        </div>
    ''', unsafe_allow_html=True)

    # Stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="stat-box"><div class="stat-number">1.200+</div><div class="stat-label">Zufriedene Kunden</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="stat-box"><div class="stat-number">2.500€</div><div class="stat-label">Ø Ersparnis</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="stat-box"><div class="stat-number">98%</div><div class="stat-label">Erfolgsquote</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("## 🎯 So einfach funktioniert's")

    s1, s2, s3 = st.columns(3)
    with s1:
        st.markdown("### 1️⃣ Schäden bewerten")
        st.write("Nutzen Sie unseren interaktiven Schadensrechner für eine präzise Kostenschätzung.")
    with s2:
        st.markdown("### 2️⃣ Kostenlose Prüfung")
        st.write("Unsere TÜV-zertifizierten Gutachter prüfen Ihr Fahrzeug professionell.")
    with s3:
        st.markdown("### 3️⃣ Geld sparen")
        st.write("Wir verhandeln für Sie und sparen durchschnittlich 60% der Kosten ein.")

    st.markdown("---")
    st.markdown("## 💬 Kundenstimmen")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.info("⭐⭐⭐⭐⭐\n\n**Michael W.** - Audi A4\n\n'Professionelle Beratung, 3.200€ gespart!'")
    with c2:
        st.info("⭐⭐⭐⭐⭐\n\n**Sarah M.** - BMW 3er\n\n'Absolut empfehlenswert! 2.800€ Ersparnis.'")
    with c3:
        st.info("⭐⭐⭐⭐⭐\n\n**Thomas S.** - Mercedes C\n\n'Von 5.000€ auf 1.200€ reduziert!'")

elif st.session_state.page == 'calculator':
    init_calculator_state()
    damage_costs = get_damage_costs(st.session_state.vehicle_class)
    damage_levels = get_damage_levels()

    st.markdown("""
    <style>
    .calc-header {
        background: linear-gradient(135deg, #1B365D 0%, #1E3A8A 100%);
        color: white;
        padding: 40px 30px;
        border-radius: 10px;
        text-align: center;
        margin: 20px 0;
    }
    .progress-bar {
        height: 25px;
        background: #E5E7EB;
        border-radius: 12px;
        overflow: hidden;
        margin: 20px 0;
    }
    .progress-fill {
        height: 100%;
        background: #059669;
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        font-size: 0.9rem;
    }
    .result-box {
        background: linear-gradient(135deg, #1B365D 0%, #1E3A8A 100%);
        padding: 40px;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin: 30px 0;
    }
    .result-amount {
        font-size: 3rem;
        font-weight: 300;
    }
    .savings-box {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        padding: 35px;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('''
        <div class="calc-header">
            <h1>🔧 Interaktiver Schadensrechner</h1>
            <p>Bewerten Sie die Beschädigungen an Ihrem Fahrzeug basierend auf einem professionellen Leasingrücknahmegutachten</p>
        </div>
    ''', unsafe_allow_html=True)

    # Fahrzeugdaten
    st.markdown("### 🚗 Fahrzeugdaten")
    col_v1, col_v2 = st.columns(2)

    with col_v1:
        st.session_state.vehicle_class = st.selectbox(
            "Fahrzeugklasse",
            ['Kompaktklasse', 'Mittelklasse', 'Oberklasse', 'Luxusklasse'],
            index=1
        )

    with col_v2:
        current_year = datetime.now().year
        st.session_state.vehicle_year = st.selectbox(
            "Baujahr",
            list(range(current_year, current_year-10, -1)),
            index=4
        )

    # Progress
    if not st.session_state.damages or len(st.session_state.damages) != len(damage_costs):
        st.session_state.damages = {part: 0 for part in damage_costs.keys()}

    total_parts = len(damage_costs)
    evaluated_parts = sum(1 for v in st.session_state.damages.values() if v > 0)
    progress_percent = int((evaluated_parts / total_parts) * 100)

    st.markdown(f'''
        <div class="progress-bar">
            <div class="progress-fill" style="width: {progress_percent}%;">
                {progress_percent}% - {evaluated_parts} von {total_parts} bewertet
            </div>
        </div>
    ''', unsafe_allow_html=True)

    if st.button("🔄 Alle Bewertungen zurücksetzen", use_container_width=True):
        st.session_state.damages = {part: 0 for part in damage_costs.keys()}
        st.session_state.calculation_done = False
        st.rerun()

    st.markdown("---")
    st.markdown("### 🚗 Außenbereich")

    exterior_parts = [
        'Frontschürze', 'Heckschürze',
        'Kotflügel vorn links', 'Kotflügel vorn rechts',
        'Kotflügel hinten links', 'Kotflügel hinten rechts',
        'Tür Fahrerseite', 'Tür Beifahrerseite',
        'Tür hinten links', 'Tür hinten rechts',
        'Motorhaube', 'Dach', 'Heckklappe/Kofferraum'
    ]

    col1, col2 = st.columns(2)
    for idx, part in enumerate(exterior_parts):
        with col1 if idx % 2 == 0 else col2:
            current_value = st.slider(
                f"**{part}**",
                min_value=0,
                max_value=4,
                value=st.session_state.damages.get(part, 0),
                key=f"slider_{part}"
            )
            st.session_state.damages[part] = current_value
            if current_value > 0:
                cost = damage_costs[part][current_value]
                st.caption(f"💰 Kosten: {cost:,}€")

    st.markdown("---")
    st.markdown("### 🎨 Lackierung & Scheiben")

    col3, col4 = st.columns(2)
    for part in ['Lackierung gesamt', 'Windschutzscheibe', 'Felgen (Satz)', 'Seitenscheiben']:
        with col3 if ['Lackierung gesamt', 'Windschutzscheibe'].count(part) else col4:
            val = st.slider(f"**{part}**", 0, 4, st.session_state.damages.get(part, 0), key=f"slider_{part}")
            st.session_state.damages[part] = val
            if val > 0:
                st.caption(f"💰 {damage_costs[part][val]:,}€")

    st.markdown("---")
    st.markdown("### 🪑 Innenraum")

    col5, col6 = st.columns(2)
    for idx, part in enumerate(['Sitze', 'Armaturenbrett', 'Teppich/Fußmatten']):
        with col5 if idx % 2 == 0 else col6:
            val = st.slider(f"**{part}**", 0, 4, st.session_state.damages.get(part, 0), key=f"slider_{part}")
            st.session_state.damages[part] = val
            if val > 0:
                st.caption(f"💰 {damage_costs[part][val]:,}€")

    st.markdown("---")

    if st.button("🔍 Beschädigungen schätzen", use_container_width=True, type="primary"):
        total_cost = 0
        damage_breakdown = []

        for part, level in st.session_state.damages.items():
            if level > 0:
                cost = damage_costs[part][level]
                total_cost += cost
                damage_breakdown.append({'part': part, 'level': level, 'cost': cost})

        st.session_state.total_cost = total_cost

        if total_cost > 0:
            st.markdown(f'''
                <div class="result-box">
                    <div>Geschätzte Gesamtkosten</div>
                    <div class="result-amount">{total_cost:,.0f} €</div>
                    <p style="margin-top: 15px;">
                        {st.session_state.vehicle_class} | Baujahr {st.session_state.vehicle_year}
                    </p>
                </div>
            ''', unsafe_allow_html=True)

            st.markdown("### 📋 Aufschlüsselung")
            for item in sorted(damage_breakdown, key=lambda x: x['cost'], reverse=True):
                st.write(f"**{item['part']}** - Stufe {item['level']}: {item['cost']:,}€")

            potential_savings = total_cost * 0.60
            st.markdown(f'''
                <div class="savings-box">
                    <div>💰 Mögliche Ersparnis mit ReturnGuard</div>
                    <div class="result-amount" style="font-size: 2.5rem;">bis zu {potential_savings:,.0f} €</div>
                    <p style="margin-top: 10px;">
                        Durchschnittlich 60% Ersparnis durch Expertenverhandlung
                    </p>
                </div>
            ''', unsafe_allow_html=True)

            st.markdown("---")
            st.markdown("### 📞 Jetzt Kontakt aufnehmen")

            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown("📞 **Telefon**\n\n[+49 89 123 456 78](tel:+498912345678)")
            with c2:
                st.markdown("💬 **WhatsApp**\n\n[Jetzt chatten](https://wa.me/4917698765432)")
            with c3:
                st.markdown("📧 **E-Mail**\n\n[info@returnguard.de](mailto:info@returnguard.de)")
        else:
            st.info("ℹ️ Bitte bewerten Sie mindestens eine Beschädigung.")

elif st.session_state.page == 'faq':
    st.markdown("# ❓ Häufig gestellte Fragen")

    with st.expander("Wie funktioniert der Schadensrechner?"):
        st.write("Unser interaktiver Schadensrechner basiert auf realen Leasingrücknahmegutachten. Sie bewerten 20 verschiedene Fahrzeugbereiche auf einer Skala von 0-4.")

    with st.expander("Wann sollte ich ReturnGuard kontaktieren?"):
        st.write("Idealerweise 2-3 Monate vor der Leasingrückgabe. So haben wir genug Zeit für eine gründliche Prüfung.")

    with st.expander("Was kostet eine Beratung?"):
        st.write("Die Erstberatung ist komplett kostenlos. Pakete liegen zwischen 99€ und 999€ - und sparen durchschnittlich 2.500€!")

    with st.expander("Welche Schäden sind normal?"):
        st.write("Leichte Kratzer (kleiner als Kreditkarte), leichte Steinschläge und normale Abnutzung sind akzeptabel.")

    with st.expander("Wie viel kann ich sparen?"):
        st.write("Durchschnittlich 60% der ursprünglichen Forderung - etwa 2.500€ bei 4.200€ Forderung.")

elif st.session_state.page == 'blog':
    st.markdown("# 📝 Ratgeber & Blog")

    st.info("✅ **Die ultimative Leasingrückgabe-Checkliste**\n\nBereiten Sie Ihre Leasingrückgabe perfekt vor!")

    st.markdown("### 📅 Wichtige Schritte")
    st.write("1. **3 Monate vorher**: Termin vereinbaren")
    st.write("2. **Leasingvertrag prüfen**: Rückgabebedingungen lesen")
    st.write("3. **Fahrzeug reinigen**: Professionelle Aufbereitung lohnt sich")
    st.write("4. **Dokumentieren**: Alle Fotos machen")
    st.write("5. **Professionelle Prüfung**: ReturnGuard kontaktieren")

    st.markdown("---")
    st.markdown("### 📚 Weitere Artikel")

    a1, a2, a3 = st.columns(3)
    with a1:
        st.info("🚗 **Die 10 häufigsten Fehler**\n\nVermeiden Sie teure Fehler bei der Rückgabe.")
    with a2:
        st.info("💡 **Smart Repair Guide**\n\nWann lohnt sich welche Reparatur?")
    with a3:
        st.info("⚖️ **Ihre Rechte**\n\nWas ist rechtlich zulässig?")

elif st.session_state.page == 'about':
    st.markdown("# 👥 Über ReturnGuard")
    st.markdown("### Ihr Partner für faire Leasingrückgaben seit 2008")

    st.write("""
    **Was uns auszeichnet:**
    - ✅ Über 1.200 zufriedene Kunden
    - ✅ Durchschnittlich 2.500€ Ersparnis
    - ✅ 98% Erfolgsquote
    - ✅ TÜV-zertifizierte Gutachter
    - ✅ Rechtsanwälte im Verkehrsrecht

    ### 🏆 Erfolgsgeschichten
    """)

    st.success("**BMW 3er**: Von 5.200€ auf 1.400€ - Ersparnis: 3.800€")
    st.success("**Audi Q5**: Von 4.800€ auf 1.200€ - Ersparnis: 3.600€")
    st.success("**Mercedes C**: Von 6.100€ auf 0€ - Ersparnis: 6.100€")

elif st.session_state.page == 'services':
    st.markdown("# 📦 Unsere Leistungen")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### 🔍 Technische Prüfung
        - Professionelle Fahrzeuginspektion
        - Detaillierte Schadensdokumentation
        - Fotodokumentation
        - TÜV-Gutachten

        ### ⚖️ Rechtliche Beratung
        - Vertragsprüfung
        - Bewertung von Nachforderungen
        - Verhandlung mit Leasinggebern
        """)

    with col2:
        st.markdown("""
        ### 📊 Kostenermittlung
        - Marktgerechte Einschätzung
        - Vergleich mit Leasingvertrag
        - Einsparpotenzial-Analyse

        ### 💼 Zusatzservices
        - Vor-Ort Service bundesweit
        - Express-Bearbeitung
        - 24/7 Hotline (Premium/VIP)
        """)

elif st.session_state.page == 'contact':
    st.markdown("# 📞 Kontakt")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### 📱 Direkt erreichen
        **Telefon:** [+49 89 123 456 78](tel:+498912345678)

        **WhatsApp:** [+49 176 987 654 32](https://wa.me/4917698765432)

        **E-Mail:** info@returnguard.de

        ### 🕒 Servicezeiten
        Mo-Fr: 8:00 - 18:00 Uhr
        Sa: 9:00 - 14:00 Uhr
        """)

    with col2:
        st.markdown("""
        ### 📍 Standort
        ReturnGuard GmbH
        Musterstraße 123
        80333 München

        ### 🚗 Anfahrt
        Direkt am Hauptbahnhof München
        Parkplätze vorhanden
        U-Bahn, S-Bahn, Tram
        """)

elif st.session_state.page == 'legal':
    st.markdown("# ⚖️ Rechtliches")

    tab1, tab2, tab3 = st.tabs(["Impressum", "Datenschutz", "AGB"])

    with tab1:
        st.markdown("""
        ### Impressum
        **ReturnGuard GmbH**
        Musterstraße 123, 80333 München

        Geschäftsführer: Max Mustermann
        Registergericht: Amtsgericht München
        HRB 123456 | USt-ID: DE123456789
        """)

    with tab2:
        st.markdown("""
        ### Datenschutzerklärung
        Wir verarbeiten Ihre Daten gemäß DSGVO.

        **Verarbeitete Daten:** Kontaktdaten, Fahrzeugdaten, Zahlungsinformationen

        **Ihre Rechte:** Auskunft, Berichtigung, Löschung, Einschränkung, Widerspruch
        """)

    with tab3:
        st.markdown("""
        ### AGB
        1. Geltungsbereich - Diese AGB gelten für alle Leistungen
        2. Leistungsumfang - Richtet sich nach gebuchtem Paket
        3. Preise - Inkl. gesetzlicher MwSt.
        4. Zahlung - Per Rechnung oder Vorkasse
        5. Haftung - Für Vorsatz und grobe Fahrlässigkeit
        6. Widerrufsrecht - 14 Tage ab Vertragsschluss
        """)

# ==================== FOOTER ====================
st.markdown("---")
st.markdown('''
    <div style="text-align: center; color: #6B7280; padding: 30px 20px;">
        <strong style="color: #1B365D;">🛡️ ReturnGuard GmbH</strong><br>
        📞 +49 89 123 456 78 | 💬 +49 176 987 654 32 | 📧 info@returnguard.de<br>
        © 2024 ReturnGuard - Ihr Partner für faire Leasingrückgaben
    </div>
''', unsafe_allow_html=True)
