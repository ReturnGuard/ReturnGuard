import streamlit as st
import re
from datetime import datetime
import json

# ==================== FEATURE FLAGS ====================
SHOW_AUTO_DIAGRAM = False  # Safari Mobile zeigt Raw HTML - Fallback für stabile V1

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
if 'show_cookie_banner' not in st.session_state:
    st.session_state.show_cookie_banner = True
if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False
if 'is_mobile' not in st.session_state:
    st.session_state.is_mobile = False  # Default: Desktop

# ==================== GUTACHTERTABELLE ====================
# Preise nach Fahrzeugklasse: [Kompakt, Mittel, Ober, Luxus]
def get_damage_costs(vehicle_class):
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

    # Anpassung der Preise nach Fahrzeugklasse
    adjusted_costs = {}
    for part, costs in base_costs.items():
        adjusted_costs[part] = [int(cost * mult) for cost in costs]

    return adjusted_costs

# ==================== LEAD-FORMULAR VALIDIERUNG ====================
def sanitize_phone(phone: str) -> str:
    """
    Normalisiert Telefonnummer (entfernt Leerzeichen, Bindestriche).

    Args:
        phone: Rohe Telefoneingabe

    Returns:
        str: Bereinigte Telefonnummer (nur Zahlen und +)
    """
    if not phone:
        return ""
    # Entferne Leerzeichen und Bindestriche
    return phone.replace(" ", "").replace("-", "")

def validate_lead_form(name: str, email: str, phone: str, lease_end: str) -> dict:
    """
    Validiert Lead-Formular Eingaben und gibt Validierungsergebnis zurück.

    Args:
        name: Vollständiger Name des Kunden
        email: Email-Adresse des Kunden
        phone: Telefonnummer des Kunden
        lease_end: Wann endet das Leasing (Zeitfenster)

    Returns:
        dict: {'is_valid': bool, 'errors': dict[str, str]}
    """
    errors = {}

    # Name validieren
    if not name or not name.strip():
        errors['name'] = "Name ist erforderlich"
    elif len(name.strip()) < 2:
        errors['name'] = "Name muss mindestens 2 Zeichen haben"
    elif len(name.strip()) > 100:
        errors['name'] = "Name darf maximal 100 Zeichen haben"

    # Email validieren
    if not email or not email.strip():
        errors['email'] = "Email ist erforderlich"
    else:
        # Regex für Email-Validierung
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email.strip()):
            errors['email'] = "Bitte geben Sie eine gültige Email-Adresse ein"

    # Telefon validieren
    phone_clean = sanitize_phone(phone)
    if not phone or not phone.strip():
        errors['phone'] = "Telefonnummer ist erforderlich"
    elif len(phone_clean) < 5:
        errors['phone'] = "Telefonnummer zu kurz"
    elif len(phone_clean) > 20:
        errors['phone'] = "Telefonnummer zu lang"

    # Leasingende validieren
    valid_lease_options = ['Unter 1 Monat', '1-3 Monate', '3-6 Monate', 'Über 6 Monate']
    if not lease_end or lease_end not in valid_lease_options:
        errors['lease_end'] = "Bitte wählen Sie einen Zeitraum"

    return {
        'is_valid': len(errors) == 0,
        'errors': errors
    }

# ==================== AUTO-GRAFIK (SVG) ====================
def generate_auto_svg(selected_damages):
    """
    Generiert SVG-Auto mit Markern basierend auf ausgewählten Schäden.

    Args:
        selected_damages: Liste von Strings wie ['kratzer', 'felgen']

    Returns:
        str: SVG-Code (nur statische Strings, kein User-Input!)
    """
    # SVG mit responsive viewBox
    svg = '''
    <svg viewBox="0 0 400 250"
         preserveAspectRatio="xMidYMid meet"
         style="width:100%; height:auto; max-width:400px; margin:0 auto; display:block;">

        <!-- Hintergrund -->
        <rect width="400" height="250" fill="#f9fafb"/>

        <!-- Auto-Outline (Draufsicht) -->
        <rect x="100" y="30" width="200" height="190"
              fill="none" stroke="#d1d5db" stroke-width="2" rx="15"/>

        <!-- Motorhaube -->
        <rect x="100" y="30" width="200" height="50"
              fill="#f3f4f6" stroke="#9ca3af" stroke-width="1.5" rx="15"/>
        <text x="200" y="60" text-anchor="middle"
              font-size="12" fill="#6b7280" font-family="Arial">Motorhaube</text>

        <!-- Windschutzscheibe -->
        <rect x="120" y="85" width="160" height="15"
              fill="#dbeafe" stroke="#60a5fa" stroke-width="1"/>
        <text x="200" y="96" text-anchor="middle"
              font-size="10" fill="#1e40af" font-family="Arial">Scheibe</text>

        <!-- Türen Links -->
        <rect x="80" y="105" width="18" height="60"
              fill="#f3f4f6" stroke="#9ca3af" stroke-width="1"/>
        <text x="89" y="138" text-anchor="middle"
              font-size="10" fill="#6b7280" font-family="Arial" transform="rotate(-90 89,138)">Tür L</text>

        <!-- Innenraum -->
        <rect x="120" y="110" width="160" height="70"
              fill="#e5e7eb" stroke="#9ca3af" stroke-width="1"/>
        <text x="200" y="150" text-anchor="middle"
              font-size="12" fill="#6b7280" font-family="Arial">Innenraum</text>

        <!-- Türen Rechts -->
        <rect x="302" y="105" width="18" height="60"
              fill="#f3f4f6" stroke="#9ca3af" stroke-width="1"/>
        <text x="311" y="138" text-anchor="middle"
              font-size="10" fill="#6b7280" font-family="Arial" transform="rotate(90 311,138)">Tür R</text>

        <!-- Heckklappe -->
        <rect x="100" y="170" width="200" height="50"
              fill="#f3f4f6" stroke="#9ca3af" stroke-width="1.5" rx="15"/>
        <text x="200" y="200" text-anchor="middle"
              font-size="12" fill="#6b7280" font-family="Arial">Heckklappe</text>

        <!-- Felgen (4 Ecken) -->
        <circle cx="130" cy="50" r="15" fill="#374151" stroke="#1f2937" stroke-width="2"/>
        <circle cx="270" cy="50" r="15" fill="#374151" stroke="#1f2937" stroke-width="2"/>
        <circle cx="130" cy="200" r="15" fill="#374151" stroke="#1f2937" stroke-width="2"/>
        <circle cx="270" cy="200" r="15" fill="#374151" stroke="#1f2937" stroke-width="2"/>
    '''

    # Dynamische Marker basierend auf selected_damages
    # WICHTIG: Nur vordefinierte Keys, kein User-Input!

    if 'kratzer' in selected_damages:
        # Kratzer = Motorhaube + Türen
        svg += '''
        <circle cx="200" cy="55" r="12" fill="red" opacity="0.8"/>
        <text x="200" y="60" text-anchor="middle" font-size="14" fill="white" font-weight="bold">!</text>
        <circle cx="89" cy="135" r="10" fill="red" opacity="0.8"/>
        <text x="89" y="139" text-anchor="middle" font-size="12" fill="white" font-weight="bold">!</text>
        <circle cx="311" cy="135" r="10" fill="red" opacity="0.8"/>
        <text x="311" y="139" text-anchor="middle" font-size="12" fill="white" font-weight="bold">!</text>
        '''

    if 'dellen' in selected_damages:
        # Dellen = Türen + Seitenwand
        svg += '''
        <circle cx="89" cy="120" r="10" fill="orange" opacity="0.8"/>
        <text x="89" y="124" text-anchor="middle" font-size="12" fill="white" font-weight="bold">!</text>
        <circle cx="311" cy="120" r="10" fill="orange" opacity="0.8"/>
        <text x="311" y="124" text-anchor="middle" font-size="12" fill="white" font-weight="bold">!</text>
        '''

    if 'felgen' in selected_damages:
        # Felgen = 4 Räder
        svg += '''
        <circle cx="130" cy="50" r="8" fill="red" opacity="0.9"/>
        <text x="130" y="54" text-anchor="middle" font-size="10" fill="white" font-weight="bold">!</text>
        <circle cx="270" cy="50" r="8" fill="red" opacity="0.9"/>
        <text x="270" y="54" text-anchor="middle" font-size="10" fill="white" font-weight="bold">!</text>
        <circle cx="130" cy="200" r="8" fill="red" opacity="0.9"/>
        <text x="130" y="204" text-anchor="middle" font-size="10" fill="white" font-weight="bold">!</text>
        <circle cx="270" cy="200" r="8" fill="red" opacity="0.9"/>
        <text x="270" y="204" text-anchor="middle" font-size="10" fill="white" font-weight="bold">!</text>
        '''

    if 'scheibe' in selected_damages:
        # Scheibe = Windschutzscheibe
        svg += '''
        <circle cx="200" cy="92" r="10" fill="red" opacity="0.8"/>
        <text x="200" y="96" text-anchor="middle" font-size="12" fill="white" font-weight="bold">!</text>
        '''

    if 'innenraum' in selected_damages:
        # Innenraum = Mitte
        svg += '''
        <circle cx="200" cy="145" r="12" fill="red" opacity="0.8"/>
        <text x="200" y="150" text-anchor="middle" font-size="14" fill="white" font-weight="bold">!</text>
        '''

    if 'unsure' in selected_damages:
        # Nicht sicher = Fragezeichen in Mitte
        svg += '''
        <circle cx="200" cy="125" r="15" fill="#fbbf24" opacity="0.9"/>
        <text x="200" y="132" text-anchor="middle" font-size="18" fill="white" font-weight="bold">?</text>
        '''

    svg += '</svg>'
    return svg

damage_levels = [
    '0 - Keine Beschädigung',
    '1 - Leichte Kratzer/Gebrauchsspuren',
    '2 - Mittlere Kratzer/Dellen',
    '3 - Starke Beschädigungen',
    '4 - Sehr starke Beschädigungen/Austausch'
]

# ==================== CSS STYLES - MINIMAL (Performance-optimiert) ====================
st.markdown("""
st.markdown("""
<style>
/* ULTRA-MINIMAL CSS - Nur absolute Essentials für Mobile */
* { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; box-sizing: border-box; margin: 0; padding: 0; }
.stApp { background: #F9FAFB; }

/* Hero */
.hero-section { background: linear-gradient(135deg, #1B365D, #1E3A8A); padding: 60px 20px 40px; text-align: center; color: white; }
.hero-content { max-width: 900px; margin: 0 auto; }
.hero-title { font-size: 2rem; font-weight: 700; margin-bottom: 15px; }
.hero-subtitle { font-size: 1rem; margin: 10px auto 25px; opacity: 0.9; }
.hero-cta { display: inline-block; background: #059669; color: white; padding: 12px 35px; border-radius: 8px; font-weight: 600; text-decoration: none; }

/* Social Proof */
.social-proof-banner { background: white; padding: 25px 15px; text-align: center; border-top: 2px solid #1B365D; }
.social-stats { display: flex; justify-content: center; gap: 30px; flex-wrap: wrap; }
.stat-number { font-size: 2rem; font-weight: 700; color: #1B365D; }
.stat-label { font-size: 0.85rem; color: #6B7280; }

/* Floating Buttons */
.floating-cta { position: fixed; bottom: 15px; right: 15px; z-index: 1000; display: flex; flex-direction: column; gap: 8px; }
.floating-btn { width: 52px; height: 52px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.4rem; box-shadow: 0 4px 15px rgba(0,0,0,0.2); text-decoration: none; border: 2px solid white; }
.floating-phone { background: #1B365D; }
.floating-whatsapp { background: #25D366; }
.floating-main { background: #059669; width: 56px; height: 56px; font-size: 1.6rem; }

/* Content */
.content-section { max-width: 1200px; margin: 30px auto; padding: 30px 20px; background: white; border-radius: 8px; border: 1px solid #E5E7EB; }
.section-title { font-size: 1.6rem; font-weight: 600; color: #1F2937; margin-bottom: 15px; }

/* Calculator Results */
.result-box { background: linear-gradient(135deg, #1B365D, #1E3A8A); padding: 25px; border-radius: 8px; text-align: center; color: white; margin-top: 15px; }
.result-amount { font-size: 2.2rem; font-weight: 300; }
.savings-box { background: linear-gradient(135deg, #059669, #047857); padding: 20px; border-radius: 8px; text-align: center; color: white; margin-top: 15px; }

/* Buttons */
div.stButton > button { background: linear-gradient(135deg, #1B365D, #1E3A8A); color: white; border: none; padding: 12px 25px; border-radius: 8px; font-weight: 600; width: 100%; }

/* Navigation */
.top-nav { background: white; border-bottom: 1px solid #E5E7EB; padding: 12px 0; }
.nav-brand { text-align: center; font-size: 1.3rem; font-weight: 600; color: #1B365D; margin-bottom: 8px; }
div[data-testid="column"] > div.stButton > button { background: transparent; color: #6B7280; border: 1px solid #E5E7EB; box-shadow: none; padding: 8px 12px; }
</style>
""", unsafe_allow_html=True)
# Deaktiviert für bessere Performance - für Produktion mit echtem Cookie-Management-Tool ersetzen
# if st.session_state.show_cookie_banner:
#     cookie_col1, cookie_col2 = st.columns([4, 1])
#     with cookie_col1:
#         st.info("🍪 Wir verwenden Cookies zur Verbesserung Ihrer Erfahrung. Details in unserer Datenschutzerklärung.")
#     with cookie_col2:
#         if st.button("OK", key="accept_cookies"):
#             st.session_state.show_cookie_banner = False
#             st.rerun()

# ==================== FLOATING ACTION BUTTONS ====================
st.markdown("""
<div class="floating-cta">
    <a href="tel:+498912345678" class="floating-btn floating-phone" title="Jetzt anrufen">
        📞
    </a>
    <a href="https://wa.me/4917698765432?text=Hallo%20ReturnGuard%2C%20ich%20interessiere%20mich%20f%C3%BCr%20eine%20Leasingr%C3%BCckgabe-Beratung."
       target="_blank" class="floating-btn floating-whatsapp" title="WhatsApp">
        💬
    </a>
    <a href="#calculator" class="floating-btn floating-main" title="Jetzt berechnen">
        🧮
    </a>
</div>
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

# ==================== STARTSEITE ====================
if st.session_state.page == 'home':

    # HERO SECTION
    st.markdown('''
        <div class="hero-section">
            <div class="hero-content">
                <h1 class="hero-title">Leasingrückgabe ohne böse Überraschungen</h1>
                <p class="hero-subtitle">
                    Schützen Sie sich vor unfairen Nachzahlungen. Unsere Experten
                    stehen Ihnen von der Prüfung bis zur Verhandlung zur Seite.
                </p>
                <a href="#calculator" class="hero-cta">Jetzt kostenlos berechnen →</a>
            </div>
        </div>
    ''', unsafe_allow_html=True)

    # SOCIAL PROOF BANNER
    st.markdown('''
        <div class="social-proof-banner">
            <div class="social-stats">
                <div class="stat-item">
                    <div class="stat-number">1.200+</div>
                    <div class="stat-label">Zufriedene Kunden</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">2.500€</div>
                    <div class="stat-label">Ø Ersparnis pro Kunde</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">98%</div>
                    <div class="stat-label">Erfolgsquote</div>
                </div>
            </div>
        </div>
    ''', unsafe_allow_html=True)

    # 3-SCHRITTE PROZESS
    st.markdown('<div class="process-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="process-title">So einfach funktioniert\'s</h2>', unsafe_allow_html=True)
    st.markdown('<p class="process-subtitle">In nur 3 Schritten zu Ihrer fairen Leasingrückgabe</p>', unsafe_allow_html=True)

    step1, step2, step3 = st.columns(3)

    with step1:
        st.markdown('''
            <div class="process-step">
                <div class="step-number">1</div>
                <div class="step-icon">📋</div>
                <h3 class="step-title">Schäden bewerten</h3>
                <p class="step-description">
                    Nutzen Sie unseren interaktiven Schadensrechner mit 20 Fahrzeugbereichen
                    für eine präzise Kostenschätzung.
                </p>
            </div>
        ''', unsafe_allow_html=True)

    with step2:
        st.markdown('''
            <div class="process-step">
                <div class="step-number">2</div>
                <div class="step-icon">🔍</div>
                <h3 class="step-title">Kostenlose Prüfung</h3>
                <p class="step-description">
                    Unsere TÜV-zertifizierten Gutachter prüfen Ihr Fahrzeug und erstellen
                    eine professionelle Bewertung.
                </p>
            </div>
        ''', unsafe_allow_html=True)

    with step3:
        st.markdown('''
            <div class="process-step">
                <div class="step-number">3</div>
                <div class="step-icon">💰</div>
                <h3 class="step-title">Geld sparen</h3>
                <p class="step-description">
                    Unsere Anwälte verhandeln für Sie und sparen durchschnittlich
                    60% der Rückgabekosten ein.
                </p>
            </div>
        ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # KUNDENBEWERTUNGEN
    st.markdown('<div class="testimonial-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Was unsere Kunden sagen</h2>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">Echte Erfahrungen von echten Menschen</p>', unsafe_allow_html=True)

    st.markdown('<div class="testimonial-grid">', unsafe_allow_html=True)

    testimonials = [
        {
            "name": "Michael Weber",
            "role": "Audi A4 Leasing",
            "avatar": "M",
            "text": "Ich hatte große Sorgen wegen mehrerer Kratzer und Dellen. ReturnGuard hat nicht nur alles professionell dokumentiert, sondern auch erfolgreich verhandelt.",
            "savings": "Ersparnis: 3.200€"
        },
        {
            "name": "Sarah Müller",
            "role": "BMW 3er Leasing",
            "avatar": "S",
            "text": "Absolut empfehlenswert! Die Beratung war erstklassig und das Team hat mich durch den gesamten Prozess begleitet. Hätte nie gedacht, dass ich so viel sparen kann.",
            "savings": "Ersparnis: 2.800€"
        },
        {
            "name": "Thomas Schmidt",
            "role": "Mercedes C-Klasse",
            "avatar": "T",
            "text": "Die Leasinggesellschaft wollte über 5.000€ für angebliche Schäden. Dank ReturnGuard musste ich am Ende nur 1.200€ zahlen. Unglaublich!",
            "savings": "Ersparnis: 3.800€"
        },
        {
            "name": "Julia Hoffmann",
            "role": "VW Tiguan Leasing",
            "avatar": "J",
            "text": "Sehr professionell und transparent. Der Schadensrechner hat mir vorab schon eine gute Einschätzung gegeben. Das Ergebnis war sogar noch besser!",
            "savings": "Ersparnis: 2.100€"
        },
        {
            "name": "Daniel Becker",
            "role": "Audi Q5 Leasing",
            "avatar": "D",
            "text": "Ich war skeptisch, aber ReturnGuard hat meine Erwartungen übertroffen. Die Kommunikation war top und das Ergebnis beeindruckend.",
            "savings": "Ersparnis: 4.500€"
        },
        {
            "name": "Anna Fischer",
            "role": "BMW X3 Leasing",
            "avatar": "A",
            "text": "Ohne ReturnGuard hätte ich wahrscheinlich eine hohe Nachzahlung geleistet. Stattdessen wurde alles fair geregelt. Danke!",
            "savings": "Ersparnis: 2.900€"
        }
    ]

    col1, col2, col3 = st.columns(3)
    columns = [col1, col2, col3]

    for idx, testimonial in enumerate(testimonials):
        with columns[idx % 3]:
            st.markdown(f'''
                <div class="testimonial-card">
                    <div class="testimonial-header">
                        <div class="testimonial-avatar">{testimonial["avatar"]}</div>
                        <div class="testimonial-info">
                            <div class="testimonial-name">{testimonial["name"]}</div>
                            <div class="testimonial-role">{testimonial["role"]}</div>
                        </div>
                    </div>
                    <div class="testimonial-stars">⭐⭐⭐⭐⭐</div>
                    <div class="testimonial-text">"{testimonial["text"]}"</div>
                    <div class="testimonial-savings">💰 {testimonial["savings"]}</div>
                </div>
            ''', unsafe_allow_html=True)

    st.markdown('</div></div>', unsafe_allow_html=True)

    # PARTNER LOGOS
    st.markdown('<div class="partner-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Unsere Partner & Zertifizierungen</h2>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">Vertrauen Sie auf geprüfte Qualität</p>', unsafe_allow_html=True)

    st.markdown('''
        <div class="partner-grid">
            <div class="partner-logo">
                <div class="partner-logo-text">TÜV<br/>Süd</div>
            </div>
            <div class="partner-logo">
                <div class="partner-logo-text">DEKRA</div>
            </div>
            <div class="partner-logo">
                <div class="partner-logo-text">DAV<br/>Anwalt</div>
            </div>
            <div class="partner-logo">
                <div class="partner-logo-text">VDA</div>
            </div>
            <div class="partner-logo">
                <div class="partner-logo-text">§<br/>Rechts<br/>Schutz</div>
            </div>
        </div>
    ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # TRUST BADGES
    st.markdown('''
        <div class="trust-section">
            <div class="trust-badges">
                <div class="trust-badge">
                    <div class="trust-icon">⚖️</div>
                    <div class="trust-title">Rechtsanwälte<br/>Verkehrsrecht</div>
                </div>
                <div class="trust-badge">
                    <div class="trust-icon">🔍</div>
                    <div class="trust-title">TÜV-zertifizierte<br/>KFZ-Gutachter</div>
                </div>
                <div class="trust-badge">
                    <div class="trust-icon">🏆</div>
                    <div class="trust-title">15+ Jahre<br/>Erfahrung</div>
                </div>
                <div class="trust-badge">
                    <div class="trust-icon">✅</div>
                    <div class="trust-title">100%<br/>Transparenz</div>
                </div>
            </div>
        </div>
    ''', unsafe_allow_html=True)

    # PAKETE
    st.markdown('<div class="packages-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Unsere Pakete</h2>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">Wählen Sie den Service, der zu Ihnen passt</p>', unsafe_allow_html=True)

    pkg1, pkg2, pkg3, pkg4 = st.columns(4)

    with pkg1:
        st.markdown('''
            <div class="package-card">
                <div class="package-icon">📋</div>
                <h3 class="package-title">Basis</h3>
                <p class="package-subtitle">Für einfache Prüfungen</p>
                <div class="package-price">99<span class="package-price-unit">€</span></div>
                <ul class="package-features">
                    <li>✓ Grundcheck Fahrzeug</li>
                    <li>✓ 20 Dokumentationsfotos</li>
                    <li>✓ PDF-Bericht per Email</li>
                    <li>✓ Bearbeitung in 48h</li>
                </ul>
            </div>
        ''', unsafe_allow_html=True)
        st.button("Jetzt buchen", key="b1", use_container_width=True)

    with pkg2:
        st.markdown('''
            <div class="package-card">
                <div class="package-icon">📊</div>
                <h3 class="package-title">Standard</h3>
                <p class="package-subtitle">Umfassende Beratung</p>
                <div class="package-price">199<span class="package-price-unit">€</span></div>
                <ul class="package-features">
                    <li>✓ Umfassende Prüfung</li>
                    <li>✓ 50 Detailfotos</li>
                    <li>✓ Telefonberatung 1h</li>
                    <li>✓ Bearbeitung in 24h</li>
                </ul>
            </div>
        ''', unsafe_allow_html=True)
        st.button("Jetzt buchen", key="b2", use_container_width=True)

    with pkg3:
        st.markdown('''
            <div class="package-card package-popular" style="position: relative;">
                <div class="popular-badge">⭐ BELIEBT</div>
                <div class="package-icon">🥇</div>
                <h3 class="package-title">Premium</h3>
                <p class="package-subtitle">Mit Rechtsschutz</p>
                <div class="package-price">299<span class="package-price-unit">€</span></div>
                <ul class="package-features">
                    <li>✓ Rechtliche Prüfung</li>
                    <li>✓ Anwaltsberatung 2h</li>
                    <li>✓ 24/7 Support-Hotline</li>
                    <li>✓ Sofort-Bearbeitung</li>
                </ul>
            </div>
        ''', unsafe_allow_html=True)
        st.button("Jetzt buchen", key="b3", use_container_width=True)

    with pkg4:
        st.markdown('''
            <div class="package-card">
                <div class="package-icon">💎</div>
                <h3 class="package-title">VIP</h3>
                <p class="package-subtitle">Rundum-Sorglos</p>
                <div class="package-price">999<span class="package-price-unit">€</span></div>
                <ul class="package-features">
                    <li>✓ Full-Service Paket</li>
                    <li>✓ Vor-Ort bundesweit</li>
                    <li>✓ Rückgabe-Garantie</li>
                    <li>✓ Persönlicher Manager</li>
                </ul>
            </div>
        ''', unsafe_allow_html=True)
        st.button("Jetzt buchen", key="b4", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ==================== SCHADENSRECHNER ====================
elif st.session_state.page == 'calculator':
    st.markdown('<div class="calculator-section">', unsafe_allow_html=True)

    st.markdown('''
        <div class="calculator-box">
            <h1 class="calculator-title">🔧 Interaktiver Schadensrechner</h1>
            <p class="calculator-subtitle">
                Bewerten Sie die Beschädigungen an Ihrem Fahrzeug basierend auf einem professionellen Leasingrücknahmegutachten
            </p>
        </div>
    ''', unsafe_allow_html=True)

    # FAHRZEUGKLASSE UND BAUJAHR
    st.markdown('<div class="calculator-box">', unsafe_allow_html=True)
    st.markdown("### 🚗 Fahrzeugdaten")

    col_v1, col_v2 = st.columns(2)

    with col_v1:
        st.session_state.vehicle_class = st.selectbox(
            "**Fahrzeugklasse**",
            ['Kompaktklasse', 'Mittelklasse', 'Oberklasse', 'Luxusklasse'],
            index=1,
            help="Die Fahrzeugklasse beeinflusst die Reparaturkosten"
        )

    with col_v2:
        current_year = datetime.now().year
        st.session_state.vehicle_year = st.selectbox(
            "**Baujahr**",
            list(range(current_year, current_year-10, -1)),
            index=4,
            help="Neuere Fahrzeuge haben oft höhere Reparaturkosten"
        )

    st.markdown('</div>', unsafe_allow_html=True)

    # Gutachtertabelle laden
    damage_costs = get_damage_costs(st.session_state.vehicle_class)

    # Initialisiere Session State
    if not st.session_state.damages or len(st.session_state.damages) != len(damage_costs):
        st.session_state.damages = {part: 0 for part in damage_costs.keys()}

    # FORTSCHRITTSANZEIGE
    total_parts = len(damage_costs)
    evaluated_parts = sum(1 for v in st.session_state.damages.values() if v > 0)
    progress_percent = int((evaluated_parts / total_parts) * 100)

    st.markdown(f'''
        <div class="progress-container">
            <div class="progress-bar">
                <div class="progress-fill" style="width: {progress_percent}%;">
                    {progress_percent}%
                </div>
            </div>
            <div class="progress-text">
                {evaluated_parts} von {total_parts} Fahrzeugbereichen bewertet
            </div>
        </div>
    ''', unsafe_allow_html=True)

    # RESET BUTTON
    if st.button("🔄 Alle Bewertungen zurücksetzen", use_container_width=True):
        st.session_state.damages = {part: 0 for part in damage_costs.keys()}
        st.session_state.calculation_done = False
        st.rerun()

    st.markdown("---")

    # AUSSENBERE ICH
    st.markdown("### 🚗 Außenbereich")
    st.markdown("Bewerten Sie den Zustand der Karosserieteile:")

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
                format="%d",
                help=f"Kosten: 0€ - {damage_costs[part][4]:,}€ | 0 = Keine Schäden | 4 = Sehr starke Schäden",
                key=f"slider_{part}"
            )
            st.session_state.damages[part] = current_value
            level_desc = damage_levels[current_value].split(' - ')[1]
            cost = damage_costs[part][current_value]
            st.caption(f"📊 Stufe {current_value}: {level_desc} | 💰 Kosten: {cost:,}€")

    st.markdown("---")
    st.markdown("### 🎨 Lackierung & Scheiben")

    col3, col4 = st.columns(2)

    with col3:
        lackierung_value = st.slider(
            "**Lackierung gesamt**",
            min_value=0,
            max_value=4,
            value=st.session_state.damages.get('Lackierung gesamt', 0),
            format="%d",
            help=f"Kosten: 0€ - {damage_costs['Lackierung gesamt'][4]:,}€",
            key="slider_Lackierung gesamt"
        )
        st.session_state.damages['Lackierung gesamt'] = lackierung_value
        cost = damage_costs['Lackierung gesamt'][lackierung_value]
        st.caption(f"📊 Stufe {lackierung_value}: {damage_levels[lackierung_value].split(' - ')[1]} | 💰 {cost:,}€")

        windschutz_value = st.slider(
            "**Windschutzscheibe**",
            min_value=0,
            max_value=4,
            value=st.session_state.damages.get('Windschutzscheibe', 0),
            format="%d",
            help=f"Kosten: 0€ - {damage_costs['Windschutzscheibe'][4]:,}€",
            key="slider_Windschutzscheibe"
        )
        st.session_state.damages['Windschutzscheibe'] = windschutz_value
        cost = damage_costs['Windschutzscheibe'][windschutz_value]
        st.caption(f"📊 Stufe {windschutz_value}: {damage_levels[windschutz_value].split(' - ')[1]} | 💰 {cost:,}€")

    with col4:
        felgen_value = st.slider(
            "**Felgen (Satz)**",
            min_value=0,
            max_value=4,
            value=st.session_state.damages.get('Felgen (Satz)', 0),
            format="%d",
            help=f"Kosten: 0€ - {damage_costs['Felgen (Satz)'][4]:,}€",
            key="slider_Felgen (Satz)"
        )
        st.session_state.damages['Felgen (Satz)'] = felgen_value
        cost = damage_costs['Felgen (Satz)'][felgen_value]
        st.caption(f"📊 Stufe {felgen_value}: {damage_levels[felgen_value].split(' - ')[1]} | 💰 {cost:,}€")

        seiten_value = st.slider(
            "**Seitenscheiben**",
            min_value=0,
            max_value=4,
            value=st.session_state.damages.get('Seitenscheiben', 0),
            format="%d",
            help=f"Kosten: 0€ - {damage_costs['Seitenscheiben'][4]:,}€",
            key="slider_Seitenscheiben"
        )
        st.session_state.damages['Seitenscheiben'] = seiten_value
        cost = damage_costs['Seitenscheiben'][seiten_value]
        st.caption(f"📊 Stufe {seiten_value}: {damage_levels[seiten_value].split(' - ')[1]} | 💰 {cost:,}€")

    st.markdown("---")
    st.markdown("### 🪑 Innenraum")

    col5, col6 = st.columns(2)

    with col5:
        sitze_value = st.slider(
            "**Sitze**",
            min_value=0,
            max_value=4,
            value=st.session_state.damages.get('Sitze', 0),
            format="%d",
            help=f"Kosten: 0€ - {damage_costs['Sitze'][4]:,}€",
            key="slider_Sitze"
        )
        st.session_state.damages['Sitze'] = sitze_value
        cost = damage_costs['Sitze'][sitze_value]
        st.caption(f"📊 Stufe {sitze_value}: {damage_levels[sitze_value].split(' - ')[1]} | 💰 {cost:,}€")

        armatur_value = st.slider(
            "**Armaturenbrett**",
            min_value=0,
            max_value=4,
            value=st.session_state.damages.get('Armaturenbrett', 0),
            format="%d",
            help=f"Kosten: 0€ - {damage_costs['Armaturenbrett'][4]:,}€",
            key="slider_Armaturenbrett"
        )
        st.session_state.damages['Armaturenbrett'] = armatur_value
        cost = damage_costs['Armaturenbrett'][armatur_value]
        st.caption(f"📊 Stufe {armatur_value}: {damage_levels[armatur_value].split(' - ')[1]} | 💰 {cost:,}€")

    with col6:
        teppich_value = st.slider(
            "**Teppich/Fußmatten**",
            min_value=0,
            max_value=4,
            value=st.session_state.damages.get('Teppich/Fußmatten', 0),
            format="%d",
            help=f"Kosten: 0€ - {damage_costs['Teppich/Fußmatten'][4]:,}€",
            key="slider_Teppich/Fußmatten"
        )
        st.session_state.damages['Teppich/Fußmatten'] = teppich_value
        cost = damage_costs['Teppich/Fußmatten'][teppich_value]
        st.caption(f"📊 Stufe {teppich_value}: {damage_levels[teppich_value].split(' - ')[1]} | 💰 {cost:,}€")

    st.markdown("---")

    # BERECHNUNG
    if st.button("🔍 Beschädigungen schätzen", use_container_width=True, type="primary"):
        total_cost = 0
        damage_breakdown = []

        for part, level in st.session_state.damages.items():
            if level > 0:
                cost = damage_costs[part][level]
                total_cost += cost
                damage_breakdown.append({
                    'part': part,
                    'level': level,
                    'level_desc': damage_levels[level],
                    'cost': cost
                })

        st.session_state.total_cost = total_cost
        st.session_state.calculation_done = True

        if total_cost > 0:
            # WhatsApp Text vorbereiten
            whatsapp_text = f"Hallo ReturnGuard, ich habe den Schadensrechner genutzt.\n\n"
            whatsapp_text += f"Fahrzeug: {st.session_state.vehicle_class}, Baujahr {st.session_state.vehicle_year}\n"
            whatsapp_text += f"Geschätzte Kosten: {total_cost:,.0f}€\n"
            whatsapp_text += f"Anzahl Schäden: {len(damage_breakdown)}\n\n"
            whatsapp_text += "Ich interessiere mich für eine Beratung!"

            import urllib.parse
            whatsapp_url = f"https://wa.me/4917698765432?text={urllib.parse.quote(whatsapp_text)}"

            st.markdown(f'''
                <div class="result-box">
                    <div class="result-label">Geschätzte Gesamtkosten der Beschädigungen</div>
                    <div class="result-amount">{total_cost:,.0f} €</div>
                    <p style="margin-top: 15px; opacity: 0.9;">
                        Fahrzeugklasse: {st.session_state.vehicle_class} | Baujahr: {st.session_state.vehicle_year}
                    </p>
                </div>
            ''', unsafe_allow_html=True)

            # Detaillierte Aufschlüsselung
            st.markdown("---")
            st.markdown("### 📋 Detaillierte Aufschlüsselung")

            for item in sorted(damage_breakdown, key=lambda x: x['cost'], reverse=True):
                st.markdown(f"""
                <div style="background: white; padding: 15px; border-radius: 8px; margin: 10px 0; border-left: 4px solid #1B365D;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong style="color: #1F2937;">{item['part']}</strong>
                            <div style="color: #6B7280; font-size: 0.9rem;">{item['level_desc']}</div>
                        </div>
                        <div style="font-size: 1.3rem; font-weight: 600; color: #1B365D;">
                            {item['cost']:,.0f} €
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Ersparnis
            potential_savings = total_cost * 0.60
            st.markdown(f'''
                <div class="savings-box">
                    <div class="result-label">💰 Mögliche Ersparnis mit ReturnGuard</div>
                    <div class="result-amount" style="font-size: 3rem;">bis zu {potential_savings:,.0f} €</div>
                    <p style="margin-top: 15px; font-size: 0.95rem; opacity: 0.9;">
                        Unsere Experten verhandeln mit der Leasinggesellschaft und können durchschnittlich 60% der Kosten einsparen.
                    </p>
                </div>
            ''', unsafe_allow_html=True)

            st.markdown("---")

            # KONTAKTFORMULAR
            st.markdown("### 📝 Jetzt kostenlose Beratung anfordern")
            st.markdown("Lassen Sie sich von unseren Experten beraten und sparen Sie bares Geld!")

            with st.form("contact_form"):
                form_col1, form_col2 = st.columns(2)

                with form_col1:
                    name = st.text_input("Ihr Name *", placeholder="Max Mustermann")
                    email = st.text_input("E-Mail *", placeholder="max@example.com")

                with form_col2:
                    phone = st.text_input("Telefon", placeholder="+49 123 456789")
                    vehicle = st.text_input("Fahrzeug", placeholder=f"{st.session_state.vehicle_class}")

                message = st.text_area(
                    "Nachricht (optional)",
                    placeholder=f"Ich interessiere mich für eine Beratung. Geschätzte Kosten: {total_cost:,.0f}€",
                    height=100
                )

                submitted = st.form_submit_button("📧 Anfrage senden", use_container_width=True)

                if submitted:
                    if name and email:
                        st.success("✅ Vielen Dank! Wir melden uns innerhalb von 24 Stunden bei Ihnen.")
                        st.balloons()
                    else:
                        st.error("❌ Bitte füllen Sie alle Pflichtfelder aus (Name & E-Mail)")

            st.markdown("---")
            st.markdown("### 📞 Oder kontaktieren Sie uns direkt")

            col_a, col_b, col_c = st.columns(3)

            with col_a:
                st.markdown("""
                <div style="text-align: center; padding: 20px; background: white; border-radius: 8px; border: 2px solid #E5E7EB;">
                    <div style="font-size: 2.5rem; margin-bottom: 10px;">📞</div>
                    <strong>Kostenlose Beratung</strong>
                    <div style="margin-top: 10px;">
                        <a href="tel:+498912345678" style="color: #1B365D; font-weight: 600; text-decoration: none;">
                            +49 89 123 456 78
                        </a>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col_b:
                st.markdown(f"""
                <div style="text-align: center; padding: 20px; background: white; border-radius: 8px; border: 2px solid #E5E7EB;">
                    <div style="font-size: 2.5rem; margin-bottom: 10px;">💬</div>
                    <strong>WhatsApp Kontakt</strong>
                    <div style="margin-top: 10px;">
                        <a href="{whatsapp_url}" target="_blank" style="color: #25D366; font-weight: 600; text-decoration: none;">
                            Jetzt chatten
                        </a>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col_c:
                st.markdown("""
                <div style="text-align: center; padding: 20px; background: white; border-radius: 8px; border: 2px solid #E5E7EB;">
                    <div style="font-size: 2.5rem; margin-bottom: 10px;">📧</div>
                    <strong>E-Mail Anfrage</strong>
                    <div style="margin-top: 10px;">
                        <a href="mailto:info@returnguard.de" style="color: #1B365D; font-weight: 600; text-decoration: none;">
                            info@returnguard.de
                        </a>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("ℹ️ Bitte bewerten Sie mindestens eine Beschädigung, um eine Schätzung zu erhalten.")

    st.markdown('</div>', unsafe_allow_html=True)

# ==================== FAQ ====================
elif st.session_state.page == 'faq':
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.markdown('<h1 class="section-title">❓ Häufig gestellte Fragen</h1>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">Alles was Sie über Leasingrückgaben wissen müssen</p>', unsafe_allow_html=True)

    faqs = [
        {
            "question": "Wie funktioniert der Schadensrechner?",
            "answer": "Unser interaktiver Schadensrechner basiert auf realen Leasingrücknahmegutachten. Sie bewerten 20 verschiedene Fahrzeugbereiche auf einer Skala von 0-4. Die Preise sind nach Fahrzeugklasse und Baujahr angepasst und geben Ihnen eine realistische Einschätzung der zu erwartenden Kosten."
        },
        {
            "question": "Wann sollte ich ReturnGuard kontaktieren?",
            "answer": "Idealerweise 2-3 Monate vor der Leasingrückgabe. So haben wir genug Zeit für eine gründliche Prüfung und können bei Bedarf noch kleinere Reparaturen empfehlen, die sich lohnen. Aber auch kurzfristig können wir oft noch helfen!"
        },
        {
            "question": "Was kostet eine Beratung?",
            "answer": "Die Erstberatung und Kostenschätzung ist komplett kostenlos. Erst wenn Sie sich für eines unserer Pakete entscheiden, fallen Kosten an. Diese liegen je nach Umfang zwischen 99€ und 999€ - und sparen Ihnen durchschnittlich 2.500€ an Rückgabekosten!"
        },
        {
            "question": "Welche Schäden sind bei Leasingrückgabe normal?",
            "answer": "Normale Gebrauchsspuren wie leichte Kratzer im Lack (kleiner als eine Kreditkarte), leichte Steinschläge auf der Windschutzscheibe (nicht im Sichtfeld) und leichte Abnutzung im Innenraum sind in der Regel akzeptabel. Alles darüber hinaus kann zu Nachzahlungen führen."
        },
        {
            "question": "Wie viel kann ich wirklich sparen?",
            "answer": "Unsere Kunden sparen durchschnittlich 60% der ursprünglich geforderten Rückgabekosten. Bei einem Durchschnitt von 4.200€ Forderung bedeutet das eine Ersparnis von etwa 2.500€ - abzüglich unserer Servicegebühr bleibt ein Plus von über 2.000€!"
        },
        {
            "question": "Was passiert, wenn die Leasinggesellschaft nicht verhandelt?",
            "answer": "In über 98% der Fälle kommen wir zu einer fairen Einigung. Sollte dies nicht der Fall sein, haben unsere Anwälte (Premium/VIP-Paket) die Möglichkeit, rechtliche Schritte einzuleiten. Dank unserer Erfahrung wissen wir genau, welche Forderungen rechtlich haltbar sind."
        },
        {
            "question": "Kann ich das Fahrzeug selbst reparieren lassen?",
            "answer": "Ja, aber Vorsicht! Laienhaft durchgeführte Reparaturen können zu höheren Nachforderungen führen. Wir prüfen zunächst, welche Schäden überhaupt relevant sind und welche Reparaturen sich wirtschaftlich lohnen. Oft ist es günstiger, zu verhandeln als zu reparieren!"
        },
        {
            "question": "Arbeitet ReturnGuard deutschlandweit?",
            "answer": "Ja! Unsere Vor-Ort-Services (VIP-Paket) sind bundesweit verfügbar. Für Basis- und Standard-Pakete arbeiten wir mit Fotos und Dokumenten, die Sie uns digital zusenden. Premium-Kunden können Termine in unseren Standorten oder via Video-Call wahrnehmen."
        },
        {
            "question": "Was ist, wenn ich mehr Kilometer gefahren bin?",
            "answer": "Mehrkilometer werden meist separat abgerechnet und sind vertraglich geregelt. Wir konzentrieren uns auf die Schadensbewertung. Aber: Auch hier lohnt es sich oft, zu verhandeln - manchmal können Mehrkilometer und Schäden gegeneinander aufgerechnet werden."
        },
        {
            "question": "Wie lange dauert der gesamte Prozess?",
            "answer": "Von der ersten Kontaktaufnahme bis zur finalen Einigung dauert es durchschnittlich 2-4 Wochen. Die Prüfung selbst nimmt 1-3 Tage in Anspruch (je nach Paket). Die anschließende Verhandlung mit der Leasinggesellschaft kann 1-3 Wochen dauern."
        }
    ]

    for faq in faqs:
        st.markdown(f'''
            <div class="faq-item">
                <div class="faq-question">❓ {faq["question"]}</div>
                <div class="faq-answer">{faq["answer"]}</div>
            </div>
        ''', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 💬 Ihre Frage war nicht dabei?")
    st.markdown("Kontaktieren Sie uns gerne direkt - wir beantworten alle Ihre Fragen!")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("📞 **Telefon:** +49 89 123 456 78")
    with col2:
        st.markdown("💬 **WhatsApp:** +49 176 987 654 32")
    with col3:
        st.markdown("📧 **E-Mail:** info@returnguard.de")

    st.markdown('</div>', unsafe_allow_html=True)

# ==================== BLOG ====================
elif st.session_state.page == 'blog':
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.markdown('<h1 class="section-title">📝 Ratgeber & Blog</h1>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">Expertenwissen rund um Leasingrückgaben</p>', unsafe_allow_html=True)

    # CHECKLISTE als Featured Article
    st.markdown('''
        <div style="background: linear-gradient(135deg, #1B365D 0%, #1E3A8A 100%); padding: 40px; border-radius: 12px; color: white; margin-bottom: 40px;">
            <h2 style="font-size: 2rem; margin-bottom: 15px;">✅ Die ultimative Leasingrückgabe-Checkliste</h2>
            <p style="font-size: 1.1rem; opacity: 0.9;">
                Bereiten Sie Ihre Leasingrückgabe perfekt vor! Folgen Sie unserer Schritt-für-Schritt-Anleitung
                und vermeiden Sie teure Fehler.
            </p>
        </div>
    ''', unsafe_allow_html=True)

    # Checkliste Items
    checklist_items = [
        {
            "icon": "📅",
            "title": "3 Monate vorher: Termin vereinbaren",
            "description": "Kontaktieren Sie ReturnGuard oder einen Gutachter Ihrer Wahl. Frühe Planung gibt Ihnen mehr Handlungsspielraum für eventuelle Reparaturen."
        },
        {
            "icon": "📄",
            "title": "Leasingvertrag prüfen",
            "description": "Lesen Sie die Rückgabebedingungen genau durch. Achten Sie auf: erlaubte Kilometerleistung, Definition von 'normalem Verschleiß', Rückgabemodalitäten."
        },
        {
            "icon": "🧽",
            "title": "Fahrzeug gründlich reinigen",
            "description": "Innen- und Außenreinigung inkl. professioneller Aufbereitung. Saubere Fahrzeuge werden wohlwollender bewertet. Kosten: 150-300€ - lohnt sich!"
        },
        {
            "icon": "🔧",
            "title": "Kleine Schäden selbst beheben",
            "description": "Smart Repair für Kratzer (50-150€) und Dellendrücker für kleine Beulen (80-200€) können sich lohnen. Aber: Lassen Sie sich vorher von Experten beraten!"
        },
        {
            "icon": "📸",
            "title": "Alles dokumentieren",
            "description": "Fotografieren Sie das Fahrzeug von allen Seiten, Innenraum, Kofferraum, Motorraum. Datum und Kilometerstand festhalten. Diese Fotos sind Ihr Beweis!"
        },
        {
            "icon": "🔑",
            "title": "Schlüssel und Zubehör prüfen",
            "description": "Alle Schlüssel, Fernbedienungen, Ladekabel (E-Auto), Warndreieck, Verbandskasten, Wagenheber, Bordmappe vorhanden? Fehlende Teile können teuer werden!"
        },
        {
            "icon": "🔍",
            "title": "Professionelle Begutachtung",
            "description": "Lassen Sie das Fahrzeug von ReturnGuard oder einem unabhängigen Gutachter prüfen. Kostet 99-299€, spart aber durchschnittlich 2.500€!"
        },
        {
            "icon": "📋",
            "title": "Rückgabeprotokoll genau lesen",
            "description": "Bei der Rückgabe: Lesen Sie das Protokoll gründlich! Unterschreiben Sie nichts, womit Sie nicht einverstanden sind. Sie haben das Recht auf Nachverhandlung."
        },
        {
            "icon": "⏰",
            "title": "Nach Rückgabe: Fristen beachten",
            "description": "Die Leasinggesellschaft hat oft 4-6 Wochen Zeit für die Endabrechnung. Prüfen Sie jede Forderung kritisch. ReturnGuard hilft auch nach der Rückgabe!"
        },
        {
            "icon": "💰",
            "title": "Forderungen anfechten",
            "description": "Nicht jede Forderung ist berechtigt! Lassen Sie überhöhte oder ungerechtfertigte Kosten von Experten prüfen. In 60% der Fälle können wir deutlich reduzieren."
        }
    ]

    for item in checklist_items:
        st.markdown(f'''
            <div class="checklist-item">
                <div class="checklist-icon">{item["icon"]}</div>
                <div class="checklist-content">
                    <div class="checklist-title">{item["title"]}</div>
                    <div class="checklist-description">{item["description"]}</div>
                </div>
            </div>
        ''', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("## 📚 Weitere Ratgeber-Artikel")

    st.markdown('<div class="blog-grid">', unsafe_allow_html=True)

    blog_posts = [
        {
            "icon": "🚗",
            "category": "Ratgeber",
            "title": "Die 10 häufigsten Fehler bei der Leasingrückgabe",
            "excerpt": "Diese Fehler können Sie tausende Euro kosten. Erfahren Sie, wie Sie sie vermeiden.",
            "date": "15. Januar 2024"
        },
        {
            "icon": "💡",
            "category": "Tipps",
            "title": "Smart Repair vs. Vollreparatur: Was lohnt sich?",
            "excerpt": "Nicht jeder Schaden muss teuer repariert werden. Wir zeigen Ihnen die besten Alternativen.",
            "date": "08. Januar 2024"
        },
        {
            "icon": "⚖️",
            "category": "Recht",
            "title": "Ihre Rechte bei der Leasingrückgabe",
            "excerpt": "Welche Forderungen sind rechtlich zulässig? Ein Anwalt klärt auf.",
            "date": "22. Dezember 2023"
        },
        {
            "icon": "🔍",
            "category": "Guide",
            "title": "So lesen Sie ein Rückgabeprotokoll richtig",
            "excerpt": "Verstehen Sie, was die Gutachter wirklich meinen und wie Sie reagieren sollten.",
            "date": "10. Dezember 2023"
        },
        {
            "icon": "💰",
            "category": "Kostenübersicht",
            "title": "Was kostet welcher Schaden wirklich?",
            "excerpt": "Realistische Preise für Reparaturen und was Leasinggesellschaften typischerweise fordern.",
            "date": "01. Dezember 2023"
        },
        {
            "icon": "📊",
            "category": "Vergleich",
            "title": "Leasingrückgabe mit vs. ohne Expertenunterstützung",
            "excerpt": "Ein detaillierter Vergleich mit echten Zahlen aus über 1000 Fällen.",
            "date": "18. November 2023"
        }
    ]

    col1, col2, col3 = st.columns(3)
    columns = [col1, col2, col3]

    for idx, post in enumerate(blog_posts):
        with columns[idx % 3]:
            st.markdown(f'''
                <div class="blog-card">
                    <div class="blog-image">{post["icon"]}</div>
                    <div class="blog-content">
                        <div class="blog-category">{post["category"]}</div>
                        <div class="blog-title">{post["title"]}</div>
                        <div class="blog-excerpt">{post["excerpt"]}</div>
                        <div class="blog-meta">📅 {post["date"]}</div>
                    </div>
                </div>
            ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ==================== ERFOLGSGESCHICHTEN ====================
elif st.session_state.page == 'about':
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.markdown('<h1 class="section-title">👥 Über ReturnGuard</h1>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">Ihr Partner für faire Leasingrückgaben seit 2008</p>', unsafe_allow_html=True)

    st.write("""
    ### Unsere Mission

    ReturnGuard wurde 2008 mit einer klaren Mission gegründet: Leasingnehmern zu helfen,
    unfaire Nachzahlungen zu vermeiden und faire Leasingrückgaben sicherzustellen.

    **Was uns auszeichnet:**
    - **Erfahrenes Team:** Rechtsanwälte im Verkehrsrecht & TÜV-zertifizierte KFZ-Gutachter
    - **Über 1.200 zufriedene Kunden** mit durchschnittlich 2.500€ Ersparnis
    - **98% Erfolgsquote** bei Verhandlungen mit Leasinggesellschaften
    - **Transparente Preise** ohne versteckte Kosten

    ### Unsere Werte

    - ✅ **Transparenz:** Keine versteckten Kosten, klare Kommunikation
    - ⚖️ **Fairness:** Wir kämpfen für Ihre Rechte
    - 🎯 **Professionalität:** Höchste Qualitätsstandards
    - 💙 **Persönliche Betreuung:** Jeder Kunde ist einzigartig
    """)

    st.markdown("---")
    st.markdown("### 🏆 Erfolgsgeschichten")
    st.markdown("Echte Fälle, echte Ergebnisse")

    success_stories = [
        {
            "title": "Fall 1: BMW 3er - Von 5.200€ auf 1.400€",
            "description": """
            **Ausgangssituation:** Kunde sollte 5.200€ für Lackschäden und Felgenkratzer zahlen.

            **Unsere Lösung:** Professionelle Gutachten zeigten: 60% der Schäden waren normale Gebrauchsspuren.

            **Ergebnis:** Verhandlung auf 1.400€ - **Ersparnis: 3.800€**
            """
        },
        {
            "title": "Fall 2: Audi Q5 - Von 4.800€ auf 1.200€",
            "description": """
            **Ausgangssituation:** Leasinggesellschaft forderte 4.800€ für Innenraumschäden und Steinschläge.

            **Unsere Lösung:** Rechtliche Prüfung ergab: Viele Forderungen waren überhöht.

            **Ergebnis:** Reduktion auf 1.200€ - **Ersparnis: 3.600€**
            """
        },
        {
            "title": "Fall 3: Mercedes C-Klasse - Von 6.100€ auf 0€",
            "description": """
            **Ausgangssituation:** Kundin sollte 6.100€ für angebliche Unfallschäden zahlen.

            **Unsere Lösung:** Detailprüfung zeigte: Schäden waren bereits vor Leasingbeginn vorhanden!

            **Ergebnis:** Vollständiger Erlass - **Ersparnis: 6.100€**
            """
        }
    ]

    for story in success_stories:
        st.markdown(f'''
            <div style="background: #F9FAFB; padding: 25px; border-radius: 10px; border-left: 4px solid #059669; margin: 20px 0;">
                <h3 style="color: #1F2937; margin-bottom: 15px;">{story["title"]}</h3>
                <div style="color: #6B7280; line-height: 1.8; white-space: pre-line;">{story["description"]}</div>
            </div>
        ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ==================== WEITERE SEITEN ====================
elif st.session_state.page == 'services':
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.markdown('<h1 class="section-title">📦 Unsere Leistungen</h1>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">Umfassender Service für Ihre Leasingrückgabe</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### 🔍 Technische Prüfung
        - Professionelle Fahrzeuginspektion
        - Detaillierte Schadensdokumentation
        - Fotodokumentation nach Standards
        - Gutachten nach Leasingkriterien

        ### ⚖️ Rechtliche Beratung
        - Vertragsprüfung durch Anwälte
        - Bewertung von Nachforderungen
        - Verhandlung mit Leasinggebern
        - Rechtliche Vertretung
        """)

    with col2:
        st.markdown("""
        ### 📊 Kostenermittlung
        - Marktgerechte Schadenseinschätzung
        - Vergleich mit Leasingvertrag
        - Kostentransparenz
        - Einsparpotenzial-Analyse

        ### 💼 Zusatzservices
        - Vor-Ort Service bundesweit
        - Express-Bearbeitung möglich
        - 24/7 Hotline (Premium/VIP)
        - Persönlicher Ansprechpartner
        """)

    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == 'contact':
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.markdown('<h1 class="section-title">📞 Kontakt</h1>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">Wir sind für Sie da</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### 📱 Direkt erreichen
        **Telefon:** [+49 89 123 456 78](tel:+498912345678)
        **WhatsApp:** [+49 176 987 654 32](https://wa.me/4917698765432)
        **E-Mail:** info@returnguard.de

        ### 🕒 Servicezeiten
        **Mo-Fr:** 8:00 - 18:00 Uhr
        **Sa:** 9:00 - 14:00 Uhr
        **So:** Geschlossen
        """)

    with col2:
        st.markdown("""
        ### 📍 Unser Standort
        ReturnGuard GmbH
        Musterstraße 123
        80333 München

        ### 🚗 Anfahrt
        Direkt am Hauptbahnhof München
        Parkplätze vorhanden
        U-Bahn, S-Bahn, Tram
        """)

    # LEAD-FORMULAR
    st.markdown("---")
    st.markdown('<div id="rg-contact-form">', unsafe_allow_html=True)

    # CSS für Mobile/Desktop Split - SICHERER ANSATZ (Page-Level, nicht im iframe)
    st.markdown("""
    <style>
    /* Desktop: Beide Columns sichtbar */
    [data-testid="column"] {
        display: block;
    }

    /* Mobile: Auto-Diagram Column verstecken */
    @media (max-width: 768px) {
        /* Verstecke die zweite Column (Auto-Diagram) auf Mobile */
        [data-testid="stHorizontalBlock"] > div:nth-child(2) {
            display: none !important;
        }
    }

    /* Auto-Diagram Styling */
    #rg-contact-form .auto-diagram-container {
        position: sticky;
        top: 20px;
        padding: 15px;
        background: #f9fafb;
        border-radius: 8px;
        border: 1px solid #e5e7eb;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("### 📝 Kostenlose Erstberatung")
    st.markdown("Beschreiben Sie kurz Ihre Situation - wir melden uns innerhalb von 24h bei Ihnen.")

    # Success State
    if st.session_state.form_submitted:
        st.success("✅ Vielen Dank! Wir melden uns innerhalb von 24h bei Ihnen.")
        if st.button("Neue Anfrage"):
            st.session_state.form_submitted = False
            st.rerun()
    else:
        # Formular nur zeigen wenn nicht gerade submitted
        with st.form("lead_form"):
            # Kontaktdaten
            st.markdown("**Ihre Kontaktdaten**")
            col_form1, col_form2 = st.columns(2)

            with col_form1:
                name = st.text_input("Name *", placeholder="Max Mustermann")
                email = st.text_input("Email *", placeholder="max@beispiel.de")

            with col_form2:
                phone = st.text_input("Telefon *", placeholder="+49 176 12345678")
                lease_end = st.selectbox(
                    "Wann endet Ihr Leasing? *",
                    ['Unter 1 Monat', '1-3 Monate', '3-6 Monate', 'Über 6 Monate'],
                    index=1
                )

            # Schäden erfassen (optional) - NEUES LAYOUT: Form + Diagram Side-by-Side
            st.markdown("---")
            st.markdown("**Welche Schäden sind vorhanden? (optional)**")

            # Zwei Columns: Links = Checkboxen, Rechts = Auto-Diagram (versteckt auf Mobile)
            col_form_main, col_diagram = st.columns([1, 1])

            with col_form_main:
                # Checkboxen in 2 Sub-Columns
                col_damage1, col_damage2 = st.columns(2)

                with col_damage1:
                    damage_kratzer = st.checkbox("Kratzer / Lackschäden")
                    damage_dellen = st.checkbox("Dellen / Beulen")
                    damage_felgen = st.checkbox("Felgen")

                with col_damage2:
                    damage_scheibe = st.checkbox("Scheibe")
                    damage_innenraum = st.checkbox("Innenraum")
                    damage_unsure = st.checkbox("Nicht sicher")

            # Auto-Grafik in rechter Column (nur Desktop, Mobile versteckt via CSS)
            with col_diagram:
                if SHOW_AUTO_DIAGRAM:
                    # Sammle selected damages (nur vordefinierte Keys!)
                    selected_damages = []
                    if damage_kratzer:
                        selected_damages.append('kratzer')
                    if damage_dellen:
                        selected_damages.append('dellen')
                    if damage_felgen:
                        selected_damages.append('felgen')
                    if damage_scheibe:
                        selected_damages.append('scheibe')
                    if damage_innenraum:
                        selected_damages.append('innenraum')
                    if damage_unsure:
                        selected_damages.append('unsure')

                    # SVG generieren und rendern - OHNE CSS im iframe (sicherer!)
                    try:
                        svg_code = generate_auto_svg(selected_damages)

                        # Nur iframe mit SVG - KEINE CSS Media Queries im iframe!
                        import streamlit.components.v1 as components

                        html_content = f"""
                        <!DOCTYPE html>
                        <html>
                        <head>
                            <meta charset="UTF-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        </head>
                        <body style="margin:0; padding:10px; display:flex; justify-content:center; align-items:center; background:#f9fafb;">
                            <div id="svg-container">
                                {svg_code}
                            </div>
                            <script>
                                // Mobile Detection: Verstecke SVG auf Mobile (Viewport < 768px)
                                if (window.innerWidth <= 768) {{
                                    document.body.style.display = 'none';
                                    document.body.style.height = '0';
                                    document.body.style.overflow = 'hidden';
                                }}
                            </script>
                        </body>
                        </html>
                        """

                        components.html(html_content, height=280, scrolling=False)

                    except Exception as e:
                        # Fallback: Silent fail, Checkboxen funktionieren weiter
                        pass

            # Freitext für Schaden-Details
            damage_details = st.text_area(
                "Weitere Details zu den Schäden (optional)",
                placeholder="z.B. Kratzer ca. 10cm an Tür links, Delle in Heckklappe...",
                height=80
            )

            # Foto-Upload (optional)
            st.markdown("---")
            st.markdown("**Fotos der Schäden (optional, aber hilfreich)**")
            uploaded_files = st.file_uploader(
                "Laden Sie Fotos hoch",
                type=["jpg", "jpeg", "png"],
                accept_multiple_files=True,
                help="Maximal 5 Bilder",
                label_visibility="collapsed"
            )

            # Validierung: Max 5 Bilder
            if uploaded_files and len(uploaded_files) > 5:
                st.error("❌ Maximal 5 Bilder erlaubt")
            elif uploaded_files:
                st.success(f"✅ {len(uploaded_files)} Foto(s) hochgeladen")

            st.caption("💡 Tipp: Machen Sie Nahaufnahmen der Schäden + eine Gesamtansicht des Fahrzeugs")

            # Nachricht (optional)
            st.markdown("---")
            message = st.text_area(
                "Ihre Nachricht (optional)",
                placeholder="Erzählen Sie uns mehr über Ihre Situation...",
                height=100
            )

            submitted = st.form_submit_button("💬 Kostenlose Beratung anfordern", use_container_width=True)

            if submitted:
                with st.spinner("Anfrage wird gesendet..."):
                    # Validierung (nur Pflichtfelder)
                    result = validate_lead_form(name, email, phone, lease_end)

                    if result['is_valid']:
                        # Erfolg - hier könnte später Email-Versand implementiert werden
                        st.session_state.form_submitted = True
                        st.rerun()
                    else:
                        # Fehler anzeigen
                        for field, error_msg in result['errors'].items():
                            st.error(f"❌ {error_msg}")

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == 'legal':
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.markdown('<h1 class="section-title">⚖️ Rechtliches</h1>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Impressum", "Datenschutz", "AGB"])

    with tab1:
        st.markdown("""
        ### Impressum
        **ReturnGuard GmbH**
        Musterstraße 123
        80333 München

        **Geschäftsführer:** Max Mustermann
        **Registergericht:** Amtsgericht München
        **Registernummer:** HRB 123456
        **USt-ID:** DE123456789
        """)

    with tab2:
        st.markdown("""
        ### Datenschutzerklärung
        Wir nehmen den Schutz Ihrer persönlichen Daten ernst und verarbeiten
        diese gemäß DSGVO und TKG 2003.

        **Verarbeitete Daten:**
        - Kontaktdaten (Name, E-Mail, Telefon)
        - Fahrzeugdaten für Gutachten
        - Zahlungsinformationen

        **Ihre Rechte:** Auskunft, Berichtigung, Löschung, Einschränkung,
        Widerspruch, Datenübertragbarkeit
        """)

    with tab3:
        st.markdown("""
        ### Allgemeine Geschäftsbedingungen
        **1. Geltungsbereich** - Diese AGB gelten für alle Leistungen.
        **2. Leistungsumfang** - Richtet sich nach gebuchtem Paket.
        **3. Preise** - Inkl. gesetzlicher MwSt.
        **4. Zahlung** - Per Rechnung oder Vorkasse.
        **5. Haftung** - Für Vorsatz und grobe Fahrlässigkeit.
        **6. Widerrufsrecht** - 14 Tage ab Vertragsschluss.
        """)

    st.markdown('</div>', unsafe_allow_html=True)

# ==================== FOOTER ====================
st.markdown("---")
st.markdown('''
    <div style="text-align: center; color: #6B7280; padding: 40px 20px; font-size: 0.95rem;">
        <div style="margin-bottom: 20px;">
            <strong style="color: #1B365D; font-size: 1.1rem;">🛡️ ReturnGuard GmbH</strong>
        </div>
        <div style="margin-bottom: 15px;">
            📞 +49 89 123 456 78 | 💬 +49 176 987 654 32 | 📧 info@returnguard.de
        </div>
        <div>
            © 2024 ReturnGuard - Ihr Partner für faire Leasingrückgaben
        </div>
    </div>
''', unsafe_allow_html=True)
