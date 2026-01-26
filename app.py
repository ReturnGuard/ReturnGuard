import streamlit as st
import streamlit.components.v1 as components
import re
from datetime import datetime
import json

# ==================== FEATURE FLAGS ====================
SHOW_AUTO_DIAGRAM = False  # Safari Mobile zeigt Raw HTML - Fallback für stabile V1

# ==================== SCREENING KATALOG ====================
# 14-Punkte Checkliste für Investor-Präsentation
SCREENING_KATALOG = [
    "✓ Vertragsprüfung: Leasingbedingungen analysiert",
    "✓ Schadenserfassung: 20 Fahrzeugbereiche dokumentiert",
    "✓ Kostenermittlung: Marktpreise vs. Leasingforderung",
    "✓ Rechtliche Bewertung: Zulässigkeit der Nachforderungen",
    "✓ Fotodokumentation: Professionelle Beweissicherung",
    "✓ Gutachten: TÜV-zertifizierte Sachverständige",
    "✓ Vergleichsangebot: Alternative Reparaturoptionen",
    "✓ Verhandlungsstrategie: Optimale Argumentation",
    "✓ Kommunikation: Schriftverkehr mit Leasinggeber",
    "✓ Nachverhandlung: Reduzierung der Forderungen",
    "✓ Rechtliche Vertretung: Fachanwälte bei Bedarf",
    "✓ Dokumentation: Vollständige Fallakte",
    "✓ Erfolgsabrechnung: Ersparnis dokumentiert",
    "✓ Nachbetreuung: Follow-up nach Rückgabe"
]

# ==================== REVENUE STREAMS ====================
# Einnahmequellen für Investor-Dashboard
REVENUE_STREAMS = [
    {
        "icon": "🔧",
        "title": "Werkstatt-Leads",
        "description": "Vermittlung von Reparaturaufträgen an Partner-Werkstätten",
        "provision": "50-150€ pro Lead",
        "volume": "~40% der Kunden",
        "potential": "480.000€/Jahr bei 1.000 Leads"
    },
    {
        "icon": "✨",
        "title": "Aufbereiter-Leads",
        "description": "Vermittlung von Fahrzeugaufbereitungen (Innen/Außen)",
        "provision": "30-80€ pro Lead",
        "volume": "~60% der Kunden",
        "potential": "360.000€/Jahr bei 1.000 Leads"
    },
    {
        "icon": "📋",
        "title": "Gutachter-Provision",
        "description": "Anteil an Gutachter-Honoraren aus unserem Netzwerk",
        "provision": "15-25% vom Honorar",
        "volume": "~80% der Kunden",
        "potential": "200.000€/Jahr bei 1.000 Gutachten"
    },
    {
        "icon": "⚖️",
        "title": "Anwalts-Vermittlung",
        "description": "Streitfälle an Fachanwälte für Verkehrsrecht vermitteln",
        "provision": "150-300€ pro Fall",
        "volume": "~15% der Kunden (Streitfälle)",
        "potential": "225.000€/Jahr bei 1.000 Kunden"
    }
]

# ==================== ZUSÄTZLICHE USE CASES ====================
ADDITIONAL_USE_CASES = [
    {
        "icon": "🔮",
        "title": "Vorsorge-Check",
        "description": "Kunden 6 Monate vor Rückgabe prüfen lassen",
        "benefit": "Frühzeitige Lead-Generierung, höhere Conversion",
        "revenue": "Zusatz-Leads + Planungssicherheit"
    },
    {
        "icon": "🚗",
        "title": "Gebrauchtwagen-Vermittlung",
        "description": "Wenn Rückkauf günstiger als Reparatur ist",
        "benefit": "Alternative zum Leasing-Ende, neue Einnahmequelle",
        "revenue": "Vermittlungsprovision 1-3% vom Verkaufspreis"
    },
    {
        "icon": "🛡️",
        "title": "Versicherungs-Affiliate",
        "description": "GAP-Versicherung, Leasingschutzbrief vermitteln",
        "benefit": "Passives Einkommen, Cross-Selling",
        "revenue": "Affiliate-Provision pro Abschluss"
    },
    {
        "icon": "📊",
        "title": "B2B Flotten-Flatrate",
        "description": "Monatliche Aufbereitungspauschale für Firmenkunden",
        "benefit": "Recurring Revenue, langfristige Kundenbindung",
        "revenue": "50-200€/Fahrzeug/Monat"
    },
    {
        "icon": "📍",
        "title": "Mehrkilometer-Optimierung",
        "description": "Beratung zur km-Reduzierung vor Rückgabe",
        "benefit": "Zusätzlicher Touchpoint, Expertise zeigen",
        "revenue": "Service-Fee 49-99€"
    }
]

# ==================== UNIT ECONOMICS ====================
UNIT_ECONOMICS = {
    "cac": "25-40€",  # Customer Acquisition Cost
    "ltv": "180-350€",  # Lifetime Value (alle Revenue Streams)
    "ltv_cac_ratio": "4.5-8.8x",
    "avg_provision_per_customer": "~220€",
    "market_size_germany": "3.5 Mio. Leasingrückgaben/Jahr",
    "target_market_share_y1": "0.1%",
    "target_market_share_y3": "1.0%"
}

# ==================== KONFIGURATION ====================
st.set_page_config(
    page_title="ReturnGuard - Leasingrückgabe ohne Sorgen",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🛡️"
)

# ==================== SESSION STATE ====================
# Page wird jetzt aus query_params gelesen für echte Browser-Navigation
if 'page' not in st.session_state:
    # Initialisiere aus query_params oder default zu 'home'
    st.session_state.page = st.query_params.get('page', 'home')
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
if 'view' not in st.session_state:
    st.session_state.view = 'B2C'  # Default: B2C für Endkunden

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

# ==================== CSS STYLES ====================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
* {
    font-family: 'Inter', sans-serif;
    box-sizing: border-box;
}

/* PROFESSIONELLE SERIOESE OPTIK */
.stApp {
    background: #F9FAFB;
}

/* EMOTIONALER HERO */
.hero-section {
    background: linear-gradient(135deg, rgba(27, 54, 93, 0.95) 0%, rgba(30, 58, 138, 0.92) 100%),
                url('https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?w=1920') center/cover;
    padding: 120px 20px 80px 20px;
    text-align: center;
    color: white;
    position: relative;
    overflow: hidden;
}

.hero-section::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(180deg, transparent 0%, rgba(26, 35, 50, 0.3) 100%);
}

.hero-content {
    position: relative;
    z-index: 2;
    max-width: 900px;
    margin: 0 auto;
}

.hero-title {
    font-size: 3.8rem;
    font-weight: 700;
    line-height: 1.1;
    margin-bottom: 25px;
    text-shadow: 0 2px 20px rgba(0,0,0,0.3);
    animation: fadeInUp 0.8s ease-out;
}

.hero-subtitle {
    font-size: 1.4rem;
    font-weight: 400;
    margin: 20px auto 40px auto;
    max-width: 700px;
    opacity: 0.95;
    line-height: 1.6;
    animation: fadeInUp 0.8s ease-out 0.2s backwards;
}

.hero-cta {
    display: inline-block;
    background: #059669;
    color: white;
    padding: 18px 50px;
    border-radius: 8px;
    font-size: 1.2rem;
    font-weight: 600;
    text-decoration: none;
    box-shadow: 0 8px 25px rgba(5, 150, 105, 0.4);
    transition: all 0.3s ease;
    animation: fadeInUp 0.8s ease-out 0.4s backwards;
}

.hero-cta:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 35px rgba(5, 150, 105, 0.5);
    background: #047857;
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* SCROLL TO TOP BUTTON */
.scroll-to-top {
    position: fixed;
    bottom: 30px;
    left: 30px;
    width: 50px;
    height: 50px;
    background: #1B365D;
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    box-shadow: 0 4px 15px rgba(27, 54, 93, 0.3);
    cursor: pointer;
    transition: all 0.3s ease;
    z-index: 999;
}

.scroll-to-top:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(27, 54, 93, 0.4);
}

/* COOKIE BANNER */
.cookie-banner {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: #1F2937;
    color: white;
    padding: 20px;
    box-shadow: 0 -4px 20px rgba(0,0,0,0.2);
    z-index: 1001;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 20px;
}

.cookie-text {
    flex: 1;
    font-size: 0.95rem;
}

.cookie-buttons {
    display: flex;
    gap: 10px;
}

/* PROGRESS BAR */
.progress-container {
    background: white;
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 30px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

.progress-bar {
    height: 25px;
    background: #E5E7EB;
    border-radius: 12px;
    overflow: hidden;
    position: relative;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #059669 0%, #047857 100%);
    transition: width 0.5s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 0.85rem;
    font-weight: 600;
}

.progress-text {
    margin-top: 10px;
    text-align: center;
    color: #6B7280;
    font-size: 0.95rem;
}

/* SOCIAL PROOF */
.social-proof-banner {
    background: white;
    border-top: 3px solid #1B365D;
    border-bottom: 1px solid #E5E7EB;
    padding: 35px 20px;
    text-align: center;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
}

.social-stats {
    display: flex;
    justify-content: center;
    gap: 60px;
    flex-wrap: wrap;
    max-width: 1000px;
    margin: 0 auto;
}

.stat-item {
    text-align: center;
}

.stat-number {
    font-size: 3rem;
    font-weight: 700;
    color: #1B365D;
    line-height: 1;
    margin-bottom: 8px;
}

.stat-label {
    font-size: 0.95rem;
    color: #6B7280;
    font-weight: 500;
}

/* TESTIMONIALS */
.testimonial-section {
    padding: 80px 20px;
    background: white;
}

.testimonial-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 30px;
    max-width: 1200px;
    margin: 0 auto;
}

.testimonial-card {
    background: #F9FAFB;
    padding: 30px;
    border-radius: 12px;
    border: 2px solid #E5E7EB;
    transition: all 0.3s ease;
}

.testimonial-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    border-color: #1B365D;
}

.testimonial-header {
    display: flex;
    align-items: center;
    gap: 15px;
    margin-bottom: 20px;
}

.testimonial-avatar {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background: linear-gradient(135deg, #1B365D 0%, #1E3A8A 100%);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    font-weight: 600;
}

.testimonial-info {
    flex: 1;
}

.testimonial-name {
    font-weight: 600;
    color: #1F2937;
    margin-bottom: 5px;
}

.testimonial-role {
    font-size: 0.85rem;
    color: #6B7280;
}

.testimonial-stars {
    color: #FFB800;
    font-size: 1.1rem;
    margin-bottom: 15px;
}

.testimonial-text {
    color: #4B5563;
    line-height: 1.7;
    font-style: italic;
}

.testimonial-savings {
    margin-top: 15px;
    padding-top: 15px;
    border-top: 1px solid #E5E7EB;
    color: #059669;
    font-weight: 600;
    font-size: 1.1rem;
}

/* PARTNER LOGOS */
.partner-section {
    padding: 60px 20px;
    background: #F9FAFB;
}

.partner-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 30px;
    max-width: 1000px;
    margin: 0 auto;
    align-items: center;
}

.partner-logo {
    background: white;
    padding: 30px;
    border-radius: 10px;
    text-align: center;
    border: 2px solid #E5E7EB;
    transition: all 0.3s ease;
}

.partner-logo:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.08);
    border-color: #1B365D;
}

.partner-logo-text {
    font-size: 1.5rem;
    font-weight: 700;
    color: #1B365D;
}

/* FLOATING CTA */
.floating-cta {
    position: fixed;
    bottom: 30px;
    right: 30px;
    z-index: 1000;
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.floating-btn {
    width: 64px;
    height: 64px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.8rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    cursor: pointer;
    transition: all 0.3s ease;
    text-decoration: none;
    border: 3px solid white;
}

.floating-btn:hover {
    transform: scale(1.1) translateY(-3px);
    box-shadow: 0 8px 30px rgba(0,0,0,0.3);
}

.floating-phone {
    background: linear-gradient(135deg, #1B365D 0%, #1E3A8A 100%);
}

.floating-whatsapp {
    background: #25D366;
}

.floating-main {
    background: linear-gradient(135deg, #059669 0%, #047857 100%);
    width: 70px;
    height: 70px;
    font-size: 2rem;
}

/* PROZESS */
.process-section {
    padding: 80px 20px;
    background: white;
}

.process-title {
    text-align: center;
    font-size: 2.5rem;
    font-weight: 600;
    color: #1F2937;
    margin-bottom: 15px;
}

.process-subtitle {
    text-align: center;
    font-size: 1.2rem;
    color: #6B7280;
    margin-bottom: 60px;
}

.process-step {
    text-align: center;
    padding: 40px 30px;
    background: white;
    border-radius: 12px;
    border: 2px solid #E5E7EB;
    transition: all 0.3s ease;
}

.process-step:hover {
    transform: translateY(-8px);
    box-shadow: 0 12px 30px rgba(27, 54, 93, 0.15);
    border-color: #1B365D;
}

.step-number {
    width: 70px;
    height: 70px;
    background: linear-gradient(135deg, #1B365D 0%, #1E3A8A 100%);
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
    font-weight: 700;
    margin: 0 auto 25px auto;
    box-shadow: 0 8px 20px rgba(27, 54, 93, 0.3);
}

.step-icon {
    font-size: 3.5rem;
    margin-bottom: 20px;
}

.step-title {
    font-size: 1.5rem;
    font-weight: 600;
    color: #1F2937;
    margin-bottom: 15px;
}

.step-description {
    font-size: 1rem;
    color: #6B7280;
    line-height: 1.6;
}

/* TRUST BADGES */
.trust-section {
    background: #F5F7FA;
    padding: 60px 20px;
}

.trust-badges {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 25px;
    max-width: 1100px;
    margin: 0 auto;
}

.trust-badge {
    background: white;
    padding: 35px 25px;
    border-radius: 10px;
    text-align: center;
    box-shadow: 0 2px 10px rgba(31, 41, 55, 0.06);
    border: 2px solid #E5E7EB;
    transition: all 0.3s ease;
}

.trust-badge:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(31, 41, 55, 0.12);
    border-color: #1B365D;
}

.trust-icon {
    font-size: 3.5rem;
    margin-bottom: 18px;
}

.trust-title {
    font-size: 1rem;
    color: #1F2937;
    font-weight: 600;
    line-height: 1.5;
}

/* PAKETE */
.packages-section {
    padding: 80px 20px;
    background: white;
}

.section-title {
    font-size: 2.5rem;
    font-weight: 600;
    color: #1F2937;
    margin-bottom: 15px;
    text-align: center;
}

.section-subtitle {
    font-size: 1.2rem;
    color: #6B7280;
    text-align: center;
    margin-bottom: 60px;
}

.package-card {
    background: white;
    border-radius: 12px;
    padding: 40px 30px;
    border: 2px solid #E5E7EB;
    transition: all 0.4s ease;
    text-align: center;
}

.package-card:hover {
    transform: translateY(-10px) scale(1.02);
    box-shadow: 0 15px 40px rgba(31, 41, 55, 0.15);
    border-color: #1B365D;
}

.package-popular {
    border: 3px solid #059669;
    background: linear-gradient(180deg, #F0FDF4 0%, white 100%);
    transform: scale(1.05);
}

.package-popular:hover {
    transform: translateY(-10px) scale(1.07);
}

.popular-badge {
    position: absolute;
    top: -15px;
    left: 50%;
    transform: translateX(-50%);
    background: linear-gradient(135deg, #059669 0%, #047857 100%);
    color: white;
    padding: 6px 20px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 700;
}

.package-icon {
    font-size: 3rem;
    margin-bottom: 20px;
}

.package-title {
    font-size: 1.8rem;
    font-weight: 700;
    color: #1F2937;
    margin-bottom: 8px;
}

.package-subtitle {
    font-size: 0.95rem;
    color: #6B7280;
    margin-bottom: 25px;
}

.package-price {
    font-size: 3.5rem;
    font-weight: 300;
    color: #1B365D;
    margin: 25px 0;
}

.package-price-unit {
    font-size: 1.2rem;
    color: #6B7280;
}

.package-features {
    text-align: left;
    list-style: none;
    padding: 0;
    margin: 30px 0;
}

.package-features li {
    padding: 14px 0;
    color: #1F2937;
    border-bottom: 1px solid #F3F4F6;
    font-size: 0.95rem;
}

/* CALCULATOR */
.calculator-section {
    background: linear-gradient(135deg, #F3F4F6 0%, #E5E7EB 100%);
    padding: 60px 20px;
}

.calculator-box {
    background: white;
    padding: 40px;
    border-radius: 12px;
    max-width: 900px;
    margin: 0 auto 30px auto;
    box-shadow: 0 10px 40px rgba(31, 41, 55, 0.1);
    border: 2px solid #E5E7EB;
}

.calculator-title {
    font-size: 2rem;
    font-weight: 600;
    color: #1F2937;
    text-align: center;
    margin-bottom: 15px;
}

.calculator-subtitle {
    font-size: 1.1rem;
    color: #6B7280;
    text-align: center;
    margin-bottom: 30px;
}

/* RESULT BOXES */
.result-box {
    background: linear-gradient(135deg, #1B365D 0%, #1E3A8A 100%);
    padding: 40px;
    border-radius: 10px;
    text-align: center;
    color: white;
    margin-top: 30px;
}

.result-label {
    font-size: 1rem;
    font-weight: 500;
    opacity: 0.9;
    margin-bottom: 10px;
}

.result-amount {
    font-size: 3.5rem;
    font-weight: 300;
}

.savings-box {
    background: linear-gradient(135deg, #059669 0%, #047857 100%);
    padding: 35px;
    border-radius: 10px;
    text-align: center;
    color: white;
    margin-top: 20px;
}

/* CONTENT SECTIONS */
.content-section {
    max-width: 1200px;
    margin: 60px auto;
    padding: 60px 40px;
    background: white;
    border-radius: 12px;
    box-shadow: 0 2px 15px rgba(31, 41, 55, 0.06);
    border: 1px solid #E5E7EB;
}

/* FAQ */
.faq-item {
    background: white;
    padding: 25px;
    border-radius: 10px;
    border: 2px solid #E5E7EB;
    margin-bottom: 20px;
    transition: all 0.3s ease;
}

.faq-item:hover {
    border-color: #1B365D;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
}

.faq-question {
    font-size: 1.1rem;
    font-weight: 600;
    color: #1F2937;
    margin-bottom: 10px;
}

.faq-answer {
    color: #6B7280;
    line-height: 1.7;
}

/* CHECKLIST */
.checklist-item {
    display: flex;
    align-items: start;
    gap: 15px;
    padding: 20px;
    background: white;
    border-radius: 10px;
    border-left: 4px solid #059669;
    margin-bottom: 15px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.checklist-icon {
    font-size: 1.5rem;
    flex-shrink: 0;
}

.checklist-content {
    flex: 1;
}

.checklist-title {
    font-weight: 600;
    color: #1F2937;
    margin-bottom: 5px;
}

.checklist-description {
    color: #6B7280;
    font-size: 0.95rem;
}

/* BLOG */
.blog-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 30px;
}

.blog-card {
    background: white;
    border-radius: 12px;
    overflow: hidden;
    border: 2px solid #E5E7EB;
    transition: all 0.3s ease;
}

.blog-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    border-color: #1B365D;
}

.blog-image {
    width: 100%;
    height: 200px;
    background: linear-gradient(135deg, #1B365D 0%, #1E3A8A 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 4rem;
}

.blog-content {
    padding: 25px;
}

.blog-category {
    display: inline-block;
    background: #E0F2FE;
    color: #1B365D;
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    margin-bottom: 15px;
}

.blog-title {
    font-size: 1.3rem;
    font-weight: 600;
    color: #1F2937;
    margin-bottom: 10px;
}

.blog-excerpt {
    color: #6B7280;
    font-size: 0.95rem;
    line-height: 1.6;
    margin-bottom: 15px;
}

.blog-meta {
    color: #9CA3AF;
    font-size: 0.85rem;
}

/* BUTTONS */
div.stButton > button {
    background: linear-gradient(135deg, #1B365D 0%, #1E3A8A 100%);
    color: white;
    border: none;
    padding: 16px 35px;
    border-radius: 8px;
    font-weight: 600;
    font-size: 1rem;
    width: 100%;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(27, 54, 93, 0.3);
}

div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(27, 54, 93, 0.4);
}

/* NAVIGATION */
.top-nav {
    background: white;
    border-bottom: 1px solid #E5E7EB;
    padding: 20px 0;
    position: sticky;
    top: 0;
    z-index: 999;
    box-shadow: 0 2px 10px rgba(0,0,0,0.03);
}

.nav-brand {
    text-align: center;
    font-size: 1.6rem;
    font-weight: 600;
    color: #1B365D;
    margin-bottom: 15px;
}

/* Navigation Links als Buttons */
.nav-link {
    display: inline-block;
    width: 100%;
    background: transparent;
    color: #6B7280;
    border: 1px solid #E5E7EB;
    border-radius: 8px;
    box-shadow: none;
    font-weight: 500;
    padding: 12px 20px;
    text-align: center;
    text-decoration: none;
    transition: all 0.3s ease;
    font-size: 1rem;
}

.nav-link:hover {
    background: #F3F4F6;
    color: #1F2937;
    border-color: #1B365D;
    text-decoration: none;
}

div[data-testid="column"] > div.stButton > button {
    background: transparent;
    color: #6B7280;
    border: 1px solid #E5E7EB;
    box-shadow: none;
    font-weight: 500;
    padding: 12px 20px;
}

div[data-testid="column"] > div.stButton > button:hover {
    background: #F3F4F6;
    color: #1F2937;
    border-color: #1B365D;
    transform: none;
}

/* RESPONSIVE */
@media (max-width: 768px) {
    .hero-title { font-size: 2.2rem; }
    .hero-subtitle { font-size: 1.1rem; }
    .social-stats { gap: 30px; }
    .stat-number { font-size: 2.2rem; }
    .process-title, .section-title { font-size: 1.8rem; }
    .floating-cta { bottom: 15px; right: 15px; }
    .floating-btn { width: 56px; height: 56px; font-size: 1.5rem; }
    .floating-main { width: 60px; height: 60px; font-size: 1.7rem; }
    .scroll-to-top { bottom: 15px; left: 15px; width: 45px; height: 45px; }
}
</style>
""", unsafe_allow_html=True)

# ==================== SIDEBAR VIEW SELECTOR ====================
with st.sidebar:
    st.markdown("### 🛡️ ReturnGuard")
    st.markdown("**View auswählen:**")

    selected_view = st.radio(
        "Navigation",
        ["Investor", "B2C (Endkunden)", "B2B (Firmenkunden)"],
        index=["Investor", "B2C (Endkunden)", "B2B (Firmenkunden)"].index(
            st.session_state.view if st.session_state.view in ["Investor", "B2C (Endkunden)", "B2B (Firmenkunden)"]
            else "B2C (Endkunden)"
        ),
        label_visibility="collapsed"
    )

    # Update Session State
    if selected_view == "Investor":
        st.session_state.view = "Investor"
    elif selected_view == "B2C (Endkunden)":
        st.session_state.view = "B2C"
    else:
        st.session_state.view = "B2B"

    st.markdown("---")

    # Seiten-Navigation je nach View
    st.markdown("**📄 Seiten**")

    if st.session_state.view == "Investor":
        # Investor-Seiten
        if st.button("👁️ Vision", key="nav_about", use_container_width=True):
            st.session_state.page = "about"
            st.query_params["page"] = "about"
            st.rerun()
        if st.button("📦 Leistungen", key="nav_services", use_container_width=True):
            st.session_state.page = "services"
            st.query_params["page"] = "services"
            st.rerun()
        if st.button("⚖️ Rechtliches", key="nav_legal", use_container_width=True):
            st.session_state.page = "legal"
            st.query_params["page"] = "legal"
            st.rerun()
    elif st.session_state.view == "B2C":
        # B2C-Seiten
        if st.button("🏠 Home", key="nav_home", use_container_width=True):
            st.session_state.page = "home"
            st.query_params["page"] = "home"
            st.rerun()
        if st.button("📱 Quick-Check", key="nav_calculator", use_container_width=True):
            st.session_state.page = "calculator"
            st.query_params["page"] = "calculator"
            st.rerun()
        if st.button("❓ FAQ", key="nav_faq", use_container_width=True):
            st.session_state.page = "faq"
            st.query_params["page"] = "faq"
            st.rerun()
        if st.button("📝 Blog", key="nav_blog", use_container_width=True):
            st.session_state.page = "blog"
            st.query_params["page"] = "blog"
            st.rerun()
        if st.button("📞 Kontakt", key="nav_contact", use_container_width=True):
            st.session_state.page = "contact"
            st.query_params["page"] = "contact"
            st.rerun()
    else:  # B2B
        # B2B-Seiten
        if st.button("📦 Leistungen", key="nav_services_b2b", use_container_width=True):
            st.session_state.page = "services"
            st.query_params["page"] = "services"
            st.rerun()
        if st.button("📞 Kontakt", key="nav_contact_b2b", use_container_width=True):
            st.session_state.page = "contact"
            st.query_params["page"] = "contact"
            st.rerun()
        if st.button("⚖️ Rechtliches", key="nav_legal_b2b", use_container_width=True):
            st.session_state.page = "legal"
            st.query_params["page"] = "legal"
            st.rerun()

    st.markdown("---")

    # View-spezifische Sidebar-Inhalte
    if st.session_state.view == "Investor":
        st.markdown("**📊 Kennzahlen-Dashboard**")
        st.caption("Geschäftsmetriken und Erfolgsnachweise")
    elif st.session_state.view == "B2C":
        st.markdown("**💡 Schnellzugriff**")
        st.caption("Kostenrechner • FAQ • Kontakt")
    else:  # B2B
        st.markdown("**🏢 Enterprise**")
        st.caption("Flottenmanagement • Verträge")

    st.markdown("---")
    st.caption("ReturnGuard 2026 | Vertrauliche Investor-Vorschau")

# ==================== SCROLL TO TOP ====================
# Hinweis: Scroll-to-Top funktioniert in Streamlit nur begrenzt wegen iFrame
# Für bessere UX: Nutzer können mit Tastatur (Pos1) oder Browser-Scroll nach oben
# Alternative: Streamlit's st.rerun() nutzt automatisch Scroll-to-Top

# ==================== RENDER FUNCTIONS ====================
def render_investor():
    """
    Investor View: Scrollbares Pitchdeck
    Struktur nach Master-Briefing:
    1. Zentrales Fundament (Problem + Marktplatz)
    2. Warum jetzt? (Timing)
    3. Drei Perspektiven (A: Investor, B: B2C, C: B2B)
    4. Monetarisierung (implizit + explizit)
    5. Haftung & Compliance
    6. Warum investierbar
    """
    st.markdown('<div id="content-start-investor"></div>', unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════════════════
    # EBENE 1: ZENTRALES FUNDAMENT (für ALLE sichtbar)
    # ═══════════════════════════════════════════════════════════════════════════

    # HERO: Markt-Zahl + Positionierung
    st.markdown('''
        <div class="hero-section">
            <div class="hero-content">
                <p style="color: #86efac; font-size: 1.1rem; margin: 0 0 15px 0; font-weight: 600; letter-spacing: 1px;">
                    4,8 MIO. LEASINGRÜCKGABEN PRO JAHR IN DEUTSCHLAND
                </p>
                <h1 class="hero-title" style="font-size: 2.4rem; line-height: 1.3;">
                    Keine neutrale Instanz dazwischen.<br>
                    <span style="color: #86efac;">Bis jetzt.</span>
                </h1>
                <p class="hero-subtitle" style="max-width: 800px; margin: 25px auto; font-size: 1.1rem; line-height: 1.8;">
                    Wir reparieren nicht. Wir begutachten nicht. Wir klagen nicht.<br>
                    <strong>Wir orchestrieren.</strong><br><br>
                    ReturnGuard verbindet Leasingkunden mit zertifizierten Gutachtern,<br>
                    spezialisierten Werkstätten und Fachanwälten.
                </p>
                <div style="display: flex; justify-content: center; gap: 30px; margin-top: 30px; flex-wrap: wrap;">
                    <span style="color: #86efac; font-weight: 600; font-size: 1.1rem;">✓ Transparent</span>
                    <span style="color: #86efac; font-weight: 600; font-size: 1.1rem;">✓ Skalierbar</span>
                    <span style="color: #86efac; font-weight: 600; font-size: 1.1rem;">✓ Haftungsfrei</span>
                </div>
            </div>
        </div>
    ''', unsafe_allow_html=True)

    # Kernbotschaft-Banner - kompakter
    st.markdown('''
        <div style="background: linear-gradient(135deg, #1B365D 0%, #2d4a7c 100%);
                    padding: 25px 30px; border-radius: 12px; margin: 30px 0;">
            <div style="display: flex; justify-content: space-around; flex-wrap: wrap; gap: 20px; text-align: center;">
                <div>
                    <div style="color: #fde047; font-size: 1.8rem; font-weight: 700;">~2.500€</div>
                    <div style="color: #94a3b8; font-size: 0.85rem;">Ø Nachzahlung bei Rückgabe</div>
                </div>
                <div>
                    <div style="color: #86efac; font-size: 1.8rem; font-weight: 700;">73%</div>
                    <div style="color: #94a3b8; font-size: 0.85rem;">fühlen sich schlecht informiert</div>
                </div>
                <div>
                    <div style="color: #60a5fa; font-size: 1.8rem; font-weight: 700;">0</div>
                    <div style="color: #94a3b8; font-size: 0.85rem;">neutrale Plattformen bisher</div>
                </div>
            </div>
        </div>
    ''', unsafe_allow_html=True)

    # Das Problem (marktweit)
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Das Kernproblem</h2>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">Ein strukturelles Stressereignis – für alle Beteiligten</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('''
            <div style="background: #fef2f2; padding: 25px; border-radius: 12px; border-left: 4px solid #dc2626;">
                <h3 style="color: #991b1b; margin: 0 0 15px 0;">👤 Für Privatkunden</h3>
                <ul style="color: #7f1d1d; margin: 0; padding-left: 20px; line-height: 1.8;">
                    <li>Intransparente Bewertung durch Leasinggesellschaft</li>
                    <li>Informationsasymmetrie – der Kunde ist im Nachteil</li>
                    <li>Angst vor unkalkulierbaren Kosten</li>
                    <li>Keine Zeit, keine Vergleichsangebote, kein Überblick</li>
                </ul>
            </div>
        ''', unsafe_allow_html=True)

    with col2:
        st.markdown('''
            <div style="background: #fef2f2; padding: 25px; border-radius: 12px; border-left: 4px solid #dc2626;">
                <h3 style="color: #991b1b; margin: 0 0 15px 0;">🏢 Für Gewerbekunden & Dienstleister</h3>
                <ul style="color: #7f1d1d; margin: 0; padding-left: 20px; line-height: 1.8;">
                    <li>Werkstätten bekommen unqualifizierte Anfragen</li>
                    <li>Gutachter werden zu spät eingeschaltet</li>
                    <li>Anwälte kommen erst, wenn der Schaden entstanden ist</li>
                    <li>Hoher Akquiseaufwand, niedrige Trefferquote</li>
                </ul>
            </div>
        ''', unsafe_allow_html=True)

    # Marktversagen
    st.markdown('''
        <div style="background: #fef3c7; padding: 20px 30px; border-radius: 12px; margin: 25px 0;
                    border: 2px solid #f59e0b; text-align: center;">
            <p style="color: #92400e; font-size: 1.15rem; margin: 0; font-weight: 600;">
                ⚠️ Marktversagen: Alle Beteiligten existieren – aber sie sind nicht orchestriert.
            </p>
        </div>
    ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════════════════
    # DIE LÖSUNG: ReturnGuard als Orchestrator
    # ═══════════════════════════════════════════════════════════════════════════

    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Die Lösung: ReturnGuard</h2>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">Marktplatz & Orchestrator – nicht Dienstleister</p>', unsafe_allow_html=True)

    # Was ReturnGuard NICHT ist
    st.markdown('''
        <div style="background: #F9FAFB; padding: 25px; border-radius: 12px; margin: 20px 0;">
            <h4 style="color: #6B7280; margin: 0 0 15px 0;">ReturnGuard ist <span style="color: #dc2626;">keine</span>:</h4>
            <div style="display: flex; flex-wrap: wrap; gap: 10px;">
                <span style="background: #fee2e2; color: #991b1b; padding: 8px 16px; border-radius: 20px;">❌ Werkstatt</span>
                <span style="background: #fee2e2; color: #991b1b; padding: 8px 16px; border-radius: 20px;">❌ Aufbereitung</span>
                <span style="background: #fee2e2; color: #991b1b; padding: 8px 16px; border-radius: 20px;">❌ Gutachterfirma</span>
                <span style="background: #fee2e2; color: #991b1b; padding: 8px 16px; border-radius: 20px;">❌ Rechtsberatung</span>
                <span style="background: #fee2e2; color: #991b1b; padding: 8px 16px; border-radius: 20px;">❌ Leasinggesellschaft</span>
            </div>
        </div>
    ''', unsafe_allow_html=True)

    # Was ReturnGuard IST
    st.markdown('''
        <div style="background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
                    padding: 25px; border-radius: 12px; margin: 20px 0; border: 2px solid #059669;">
            <h4 style="color: #166534; margin: 0 0 15px 0;">ReturnGuard <span style="color: #059669;">ist</span> eine neutrale Vermittlungs- und Vorqualifizierungsplattform:</h4>
            <div style="display: flex; flex-wrap: wrap; gap: 10px;">
                <span style="background: #059669; color: white; padding: 8px 16px; border-radius: 20px;">✓ Bündelt Informationen</span>
                <span style="background: #059669; color: white; padding: 8px 16px; border-radius: 20px;">✓ Zieht Entscheidungen vor</span>
                <span style="background: #059669; color: white; padding: 8px 16px; border-radius: 20px;">✓ Macht Angebote vergleichbar</span>
                <span style="background: #059669; color: white; padding: 8px 16px; border-radius: 20px;">✓ Belässt Haftung wo sie hingehört</span>
            </div>
        </div>
    ''', unsafe_allow_html=True)

    # Analogie für Investoren
    st.markdown('''
        <div style="background: #eff6ff; padding: 25px; border-radius: 12px; margin: 20px 0; border-left: 4px solid #3b82f6;">
            <h4 style="color: #1e40af; margin: 0 0 15px 0;">💡 Vergleich für Investoren:</h4>
            <div style="display: flex; flex-wrap: wrap; gap: 20px; color: #1e3a8a;">
                <div><strong>Airbnb</strong> besitzt keine Wohnungen</div>
                <div><strong>Check24</strong> verkauft keine Versicherungen</div>
                <div><strong>MyHammer</strong> repariert nichts</div>
            </div>
            <p style="color: #1e40af; margin: 15px 0 0 0; font-weight: 600; font-size: 1.1rem;">
                → ReturnGuard koordiniert.
            </p>
        </div>
    ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════════════════
    # LEAD-GENERIERUNG: Der "Digitale Quick-Check"
    # ═══════════════════════════════════════════════════════════════════════════

    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">🎯 Lead-Generierung: Der "Digitale Quick-Check"</h2>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">Selbst-qualifizierte Leads ohne Akquisekosten</p>', unsafe_allow_html=True)

    col_flow, col_why = st.columns([3, 2])

    with col_flow:
        st.markdown('''
            <div style="background: #F9FAFB; padding: 25px; border-radius: 12px;">
                <h4 style="color: #1F2937; margin: 0 0 20px 0;">So funktioniert's:</h4>

                <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 15px;">
                    <div style="background: #3b82f6; color: white; width: 35px; height: 35px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; flex-shrink: 0;">1</div>
                    <div style="flex: 1; background: white; padding: 12px 15px; border-radius: 8px;">
                        <strong style="color: #1F2937;">Kunde klickt sich durch</strong>
                        <p style="color: #6B7280; margin: 5px 0 0 0; font-size: 0.85rem;">Karosserie • Glas • Innenraum • Reifen (5 Klicks, 2 Min.)</p>
                    </div>
                </div>

                <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 15px;">
                    <div style="background: #8b5cf6; color: white; width: 35px; height: 35px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; flex-shrink: 0;">2</div>
                    <div style="flex: 1; background: white; padding: 12px 15px; border-radius: 8px;">
                        <strong style="color: #1F2937;">Output: "Potenzielle Ersparnis"</strong>
                        <p style="color: #6B7280; margin: 5px 0 0 0; font-size: 0.85rem;">Kein Gutachten, keine Haftung – nur eine Orientierung</p>
                    </div>
                </div>

                <div style="display: flex; align-items: center; gap: 15px;">
                    <div style="background: #059669; color: white; width: 35px; height: 35px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; flex-shrink: 0;">3</div>
                    <div style="flex: 1; background: #dcfce7; padding: 12px 15px; border-radius: 8px; border: 2px solid #059669;">
                        <strong style="color: #166534;">CTA: "Angebote von Partnerwerkstätten sichern"</strong>
                        <p style="color: #15803d; margin: 5px 0 0 0; font-size: 0.85rem;">→ Lead generiert (20-40€)</p>
                    </div>
                </div>
            </div>
        ''', unsafe_allow_html=True)

    with col_why:
        st.markdown('''
            <div style="background: #1B365D; padding: 25px; border-radius: 12px; height: 100%;">
                <h4 style="color: #86efac; margin: 0 0 20px 0;">💡 Warum das funktioniert:</h4>
                <ul style="color: white; margin: 0; padding-left: 20px; line-height: 2;">
                    <li><strong>CAC → ~0€</strong><br><span style="color: #94a3b8; font-size: 0.85rem;">Kunde kommt organisch oder via SEO</span></li>
                    <li><strong>Selbst-Qualifizierung</strong><br><span style="color: #94a3b8; font-size: 0.85rem;">Klicks zeigen Lead-Potenzial</span></li>
                    <li><strong>Keine Haftung</strong><br><span style="color: #94a3b8; font-size: 0.85rem;">"Ersparnis-Potenzial" ≠ Gutachten</span></li>
                    <li><strong>Emotional Hook</strong><br><span style="color: #94a3b8; font-size: 0.85rem;">"1.850€ sparen" triggert Action</span></li>
                </ul>
            </div>
        ''', unsafe_allow_html=True)

    # Investor-Statement
    st.markdown('''
        <div style="background: linear-gradient(135deg, #059669 0%, #047857 100%); padding: 20px 30px; border-radius: 12px; margin-top: 25px; text-align: center;">
            <p style="color: white; font-size: 1.1rem; margin: 0;">
                📊 <strong>Für Investoren:</strong> Jeder Quick-Check ist ein selbst-qualifizierter, kaufbereiter Lead.
                Skaliert ohne Personal, konvertiert ohne Haftung.
            </p>
        </div>
    ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════════════════
    # WARUM JETZT? (Timing & Rückenwind)
    # ═══════════════════════════════════════════════════════════════════════════

    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Warum jetzt?</h2>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">Timing & Markt-Rückenwind</p>', unsafe_allow_html=True)

    st.markdown('''
        <div style="background: #F9FAFB; padding: 30px; border-radius: 12px;">
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px;">
                <div style="background: white; padding: 20px; border-radius: 8px; border-left: 4px solid #059669;">
                    <div style="font-size: 1.5rem; margin-bottom: 10px;">📈</div>
                    <strong style="color: #1F2937;">Leasingquoten historisch hoch</strong>
                    <p style="color: #6B7280; margin: 10px 0 0 0; font-size: 0.9rem;">
                        Immer mehr Fahrzeuge werden geleast – der Markt wächst kontinuierlich.
                    </p>
                </div>
                <div style="background: white; padding: 20px; border-radius: 8px; border-left: 4px solid #f59e0b;">
                    <div style="font-size: 1.5rem; margin-bottom: 10px;">💹</div>
                    <strong style="color: #1F2937;">Gebrauchtwagenpreise volatil</strong>
                    <p style="color: #6B7280; margin: 10px 0 0 0; font-size: 0.9rem;">
                        Höhere Bewertungssensibilität bei Leasinggesellschaften.
                    </p>
                </div>
                <div style="background: white; padding: 20px; border-radius: 8px; border-left: 4px solid #3b82f6;">
                    <div style="font-size: 1.5rem; margin-bottom: 10px;">🧠</div>
                    <strong style="color: #1F2937;">Kunden sind informierter, aber überfordert</strong>
                    <p style="color: #6B7280; margin: 10px 0 0 0; font-size: 0.9rem;">
                        Sie wissen, dass es Optionen gibt – aber nicht welche.
                    </p>
                </div>
                <div style="background: white; padding: 20px; border-radius: 8px; border-left: 4px solid #8b5cf6;">
                    <div style="font-size: 1.5rem; margin-bottom: 10px;">🔧</div>
                    <strong style="color: #1F2937;">Dienstleister kämpfen mit Akquise & Marge</strong>
                    <p style="color: #6B7280; margin: 10px 0 0 0; font-size: 0.9rem;">
                        Werkstätten und Gutachter suchen qualifizierte Leads.
                    </p>
                </div>
            </div>
        </div>
        <p style="text-align: center; color: #059669; font-weight: 600; margin-top: 20px; font-size: 1.1rem;">
            → Das ist kein nettes Tool, sondern eine Antwort auf Marktveränderungen.
        </p>
    ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════════════════
    # KLAMMER: Eine Plattform – drei Lesarten
    # ═══════════════════════════════════════════════════════════════════════════

    st.markdown('''
        <div style="background: linear-gradient(135deg, #1B365D 0%, #2d4a7c 100%);
                    padding: 40px; border-radius: 12px; margin: 40px 0; text-align: center;">
            <h2 style="color: white; margin: 0 0 15px 0; font-size: 1.8rem;">
                Eine Plattform – drei Lesarten derselben Wahrheit
            </h2>
            <p style="color: #94a3b8; font-size: 1.05rem; margin: 0; max-width: 700px; margin: 0 auto;">
                Alle drei Perspektiven beschreiben dasselbe Geschäftsmodell.<br>
                Sie unterscheiden sich nur in Blickwinkel & Tonalität.
            </p>
        </div>
    ''', unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════════════════
    # DIE DREI EBENEN DES MARKTPLATZES
    # ═══════════════════════════════════════════════════════════════════════════

    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Die drei Ebenen des Marktplatzes</h2>', unsafe_allow_html=True)

    # Ebene A: B2C = Lead Engine
    st.markdown('''
        <div style="background: #eff6ff; padding: 30px; border-radius: 12px; margin: 25px 0; border: 2px solid #3b82f6;">
            <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 20px;">
                <div style="background: #3b82f6; color: white; width: 50px; height: 50px; border-radius: 50%;
                            display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 1.2rem;">A</div>
                <div>
                    <h3 style="color: #1e40af; margin: 0;">Privatkunden-Plattform (B2C)</h3>
                    <span style="color: #3b82f6; font-weight: 600;">= Lead Engine</span>
                </div>
            </div>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
                <div style="background: white; padding: 15px; border-radius: 8px;">
                    <strong style="color: #1e3a8a;">Funktion:</strong>
                    <ul style="color: #1e40af; margin: 10px 0 0 0; padding-left: 20px; font-size: 0.9rem;">
                        <li>Wissensaufbau</li>
                        <li>Erwartungsmanagement</li>
                        <li>Vertrauensaufbau</li>
                        <li>Vorqualifizierung</li>
                    </ul>
                </div>
                <div style="background: white; padding: 15px; border-radius: 8px;">
                    <strong style="color: #1e3a8a;">Kunden kommen, um:</strong>
                    <ul style="color: #1e40af; margin: 10px 0 0 0; padding-left: 20px; font-size: 0.9rem;">
                        <li>Sich schlau zu machen</li>
                        <li>Risiken einzuschätzen</li>
                        <li>Optionen zu verstehen</li>
                        <li>Nicht über den Tisch gezogen zu werden</li>
                    </ul>
                </div>
                <div style="background: white; padding: 15px; border-radius: 8px;">
                    <strong style="color: #1e3a8a;">Investorensicht:</strong>
                    <ul style="color: #1e40af; margin: 10px 0 0 0; padding-left: 20px; font-size: 0.9rem;">
                        <li>Kostengünstiger Acquisition Channel</li>
                        <li>Datenquelle</li>
                        <li>Nachfrage-Seite des Marktplatzes</li>
                    </ul>
                </div>
            </div>
            <p style="color: #1e40af; margin: 20px 0 0 0; font-style: italic;">
                💡 B2C ist kein Selbstzweck – Monetarisierung hier optional, aber strategisch stark.
            </p>
        </div>
    ''', unsafe_allow_html=True)

    # Ebene B: Marktplatz-Kern = Revenue Engine
    st.markdown('''
        <div style="background: #f0fdf4; padding: 30px; border-radius: 12px; margin: 25px 0; border: 2px solid #059669;">
            <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 20px;">
                <div style="background: #059669; color: white; width: 50px; height: 50px; border-radius: 50%;
                            display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 1.2rem;">B</div>
                <div>
                    <h3 style="color: #166534; margin: 0;">Marktplatz-Kern</h3>
                    <span style="color: #059669; font-weight: 600;">= Revenue Engine (hier entsteht Marge)</span>
                </div>
            </div>
            <p style="color: #166534; margin: 0 0 20px 0;">Transaktionen zwischen:</p>
            <div style="display: flex; flex-wrap: wrap; gap: 15px; margin-bottom: 20px;">
                <span style="background: #059669; color: white; padding: 10px 20px; border-radius: 8px;">
                    Kunden ↔ Werkstätten / Aufbereiter
                </span>
                <span style="background: #059669; color: white; padding: 10px 20px; border-radius: 8px;">
                    Kunden ↔ Gutachter
                </span>
                <span style="background: #059669; color: white; padding: 10px 20px; border-radius: 8px;">
                    Kunden ↔ Anwälte
                </span>
            </div>
            <div style="background: white; padding: 15px; border-radius: 8px; margin-top: 15px;">
                <strong style="color: #166534;">ReturnGuard:</strong>
                <span style="color: #15803d;"> strukturiert • verteilt • dokumentiert • vermittelt</span>
            </div>
            <div style="background: #dcfce7; padding: 15px; border-radius: 8px; margin-top: 15px; text-align: center;">
                <strong style="color: #166534; font-size: 1.1rem;">
                    👉 Jeder Kontakt ist potenziell monetarisierbar, aber keiner haftungspflichtig.
                </strong>
            </div>
        </div>
    ''', unsafe_allow_html=True)

    # Ebene C: B2B/Flotten = Stabilitäts-Engine
    st.markdown('''
        <div style="background: #faf5ff; padding: 30px; border-radius: 12px; margin: 25px 0; border: 2px solid #8b5cf6;">
            <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 20px;">
                <div style="background: #8b5cf6; color: white; width: 50px; height: 50px; border-radius: 50%;
                            display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 1.2rem;">C</div>
                <div>
                    <h3 style="color: #6b21a8; margin: 0;">Firmen- & Flottenkunden (B2B)</h3>
                    <span style="color: #8b5cf6; font-weight: 600;">= Stabilitäts-Engine (Fixkosten-Deckel)</span>
                </div>
            </div>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
                <div style="background: white; padding: 15px; border-radius: 8px;">
                    <strong style="color: #6b21a8;">Flottenpakete leisten:</strong>
                    <ul style="color: #7c3aed; margin: 10px 0 0 0; padding-left: 20px; font-size: 0.9rem;">
                        <li>Planbare Einnahmen</li>
                        <li>Grundauslastung der Plattform</li>
                        <li>Geringere Abhängigkeit vom Endkundengeschäft</li>
                    </ul>
                </div>
                <div style="background: white; padding: 15px; border-radius: 8px;">
                    <strong style="color: #6b21a8;">Typische Kunden:</strong>
                    <ul style="color: #7c3aed; margin: 10px 0 0 0; padding-left: 20px; font-size: 0.9rem;">
                        <li>KMU-Flotten</li>
                        <li>Fuhrparkmanager</li>
                        <li>Autohäuser mit Leasingrückläufern</li>
                    </ul>
                </div>
                <div style="background: white; padding: 15px; border-radius: 8px;">
                    <strong style="color: #6b21a8;">Warum Flotten bleiben:</strong>
                    <ul style="color: #7c3aed; margin: 10px 0 0 0; padding-left: 20px; font-size: 0.9rem;">
                        <li>Wiederkehrende Rückgaben</li>
                        <li>Standardisierte Prozesse</li>
                        <li>Historischer Vergleich je Flotte</li>
                        <li>Geringerer interner Aufwand</li>
                    </ul>
                </div>
            </div>
            <div style="background: #ede9fe; padding: 15px; border-radius: 8px; margin-top: 15px; text-align: center;">
                <strong style="color: #6b21a8; font-size: 1.1rem;">
                    👉 Investorensicht: Das senkt Risiko, erhöht Runway und macht das Modell robuster.
                </strong>
            </div>
        </div>
    ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════════════════
    # DATEN ALS PLATTFORMKAPITAL
    # ═══════════════════════════════════════════════════════════════════════════

    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">📊 Daten als strategisches Plattformkapital</h2>', unsafe_allow_html=True)

    st.markdown('''
        <div style="background: #F9FAFB; padding: 30px; border-radius: 12px;">
            <p style="color: #1F2937; font-size: 1.05rem; margin: 0 0 20px 0;">
                ReturnGuard aggregiert mit jeder Rückgabe strukturierte Marktintelligenz:
            </p>
            <div style="display: flex; flex-wrap: wrap; gap: 15px; margin-bottom: 20px;">
                <span style="background: #1B365D; color: white; padding: 12px 20px; border-radius: 8px;">📋 Schäden & Häufigkeiten</span>
                <span style="background: #1B365D; color: white; padding: 12px 20px; border-radius: 8px;">💰 Bewertungen & Differenzen</span>
                <span style="background: #1B365D; color: white; padding: 12px 20px; border-radius: 8px;">📊 Angebotsbandbreiten</span>
                <span style="background: #1B365D; color: white; padding: 12px 20px; border-radius: 8px;">✅ Rückgabe-Ergebnisse</span>
            </div>
            <div style="background: #dbeafe; padding: 15px; border-radius: 8px; border-left: 4px solid #3b82f6;">
                <strong style="color: #1e40af;">Investoren sehen hier:</strong>
                <span style="color: #1e3a8a;"> Pricing Power • Benchmarks • Grundlage für Zusatzprodukte</span>
            </div>
            <div style="background: #fef3c7; padding: 15px; border-radius: 8px; margin-top: 15px; border-left: 4px solid #f59e0b;">
                <strong style="color: #92400e;">Wichtig:</strong>
                <span style="color: #78350f;"> Die aggregierten Daten dienen der Transparenz und Vergleichbarkeit – nicht der individuellen Bewertung einzelner Fahrzeuge. Keine Einzelbewertung, keine Entscheidungshoheit.</span>
            </div>
            <p style="color: #059669; margin: 20px 0 0 0; font-weight: 600; text-align: center;">
                → Wert hoch, Risiko niedrig. Ohne selbst zu bewerten oder zu haften.
            </p>
        </div>
    ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════════════════
    # MONETARISIERUNG (implizit + explizit)
    # ═══════════════════════════════════════════════════════════════════════════

    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">💰 Erlöslogik</h2>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">Wie aus einem ängstlichen Kunden Umsatz wird</p>', unsafe_allow_html=True)

    # Funnel-Visualisierung
    st.markdown('''
        <div style="background: #F9FAFB; padding: 30px; border-radius: 12px; margin-bottom: 30px;">
            <div style="display: flex; flex-direction: column; align-items: center; gap: 5px;">
                <div style="background: #fee2e2; color: #991b1b; padding: 15px 60px; border-radius: 8px; font-weight: 600; text-align: center;">
                    😰 Kunde mit Angst vor Rückgabe
                </div>
                <div style="color: #9CA3AF; font-size: 1.5rem;">↓</div>
                <div style="background: #dbeafe; color: #1e40af; padding: 12px 50px; border-radius: 8px; font-weight: 500; text-align: center;">
                    📱 Digitaler Quick-Check (2 Min.)
                </div>
                <div style="color: #9CA3AF; font-size: 1.5rem;">↓</div>
                <div style="background: #dcfce7; color: #166534; padding: 12px 40px; border-radius: 8px; font-weight: 500; text-align: center;">
                    💰 "Potenzielle Ersparnis: 1.850€"
                </div>
                <div style="color: #9CA3AF; font-size: 1.5rem;">↓</div>
                <div style="background: #059669; color: white; padding: 15px 30px; border-radius: 8px; font-weight: 600; text-align: center;">
                    ✅ LEAD GENERIERT
                </div>
            </div>
        </div>
    ''', unsafe_allow_html=True)

    # Revenue Trigger-Tabelle
    st.markdown('''
        <div style="background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
            <table style="width: 100%; border-collapse: collapse;">
                <thead>
                    <tr style="background: #1B365D;">
                        <th style="padding: 15px; text-align: left; color: white; font-weight: 600;">Layer</th>
                        <th style="padding: 15px; text-align: left; color: white; font-weight: 600;">Trigger (Ereignis)</th>
                        <th style="padding: 15px; text-align: left; color: white; font-weight: 600;">Einnahme</th>
                        <th style="padding: 15px; text-align: left; color: white; font-weight: 600;">Typ</th>
                    </tr>
                </thead>
                <tbody>
                    <tr style="border-bottom: 1px solid #E5E7EB;">
                        <td style="padding: 15px;"><span style="background: #059669; color: white; padding: 4px 12px; border-radius: 20px; font-weight: 600;">1</span> Lead-Sales</td>
                        <td style="padding: 15px; color: #4B5563;">Schaden erkannt (Delle/Kratzer)</td>
                        <td style="padding: 15px;"><strong style="color: #059669;">20-40€</strong> Fixgebühr/Lead</td>
                        <td style="padding: 15px;"><span style="background: #dcfce7; color: #166534; padding: 4px 10px; border-radius: 4px; font-size: 0.85rem;">Kernumsatz, skalierbar</span></td>
                    </tr>
                    <tr style="border-bottom: 1px solid #E5E7EB; background: #F9FAFB;">
                        <td style="padding: 15px;"><span style="background: #0ea5e9; color: white; padding: 4px 12px; border-radius: 20px; font-weight: 600;">2</span> B2B-SaaS</td>
                        <td style="padding: 15px; color: #4B5563;">Flottenmanagement</td>
                        <td style="padding: 15px;"><strong style="color: #0ea5e9;">59-79€</strong> /Fahrzeug/Monat</td>
                        <td style="padding: 15px;"><span style="background: #e0f2fe; color: #0369a1; padding: 4px 10px; border-radius: 4px; font-size: 0.85rem;">Recurring, planbar</span></td>
                    </tr>
                    <tr style="border-bottom: 1px solid #E5E7EB;">
                        <td style="padding: 15px;"><span style="background: #8b5cf6; color: white; padding: 4px 12px; border-radius: 20px; font-weight: 600;">3</span> Expert-Fee</td>
                        <td style="padding: 15px; color: #4B5563;">Kunde will Sicherheit (Gutachten)</td>
                        <td style="padding: 15px;"><strong style="color: #8b5cf6;">15-20%</strong> Provision</td>
                        <td style="padding: 15px;"><span style="background: #ede9fe; color: #6b21a8; padding: 4px 10px; border-radius: 4px; font-size: 0.85rem;">High-Value, episodisch</span></td>
                    </tr>
                    <tr style="background: #F9FAFB;">
                        <td style="padding: 15px;"><span style="background: #f59e0b; color: white; padding: 4px 12px; border-radius: 20px; font-weight: 600;">4</span> Legal-Kickback</td>
                        <td style="padding: 15px; color: #4B5563;">Unberechtigte Forderung (Streitfall)</td>
                        <td style="padding: 15px;"><strong style="color: #f59e0b;">Provision</strong> an Kanzlei</td>
                        <td style="padding: 15px;"><span style="background: #fef3c7; color: #92400e; padding: 4px 10px; border-radius: 4px; font-size: 0.85rem;">Sehr hoher Value/Case</span></td>
                    </tr>
                </tbody>
            </table>
        </div>
    ''', unsafe_allow_html=True)

    # ARPU Summary
    st.markdown('''
        <div style="background: linear-gradient(135deg, #059669 0%, #047857 100%); padding: 25px; border-radius: 12px; margin-top: 25px;">
            <div style="display: flex; justify-content: space-around; flex-wrap: wrap; gap: 20px; text-align: center;">
                <div>
                    <div style="color: white; font-size: 0.85rem; opacity: 0.9;">Ø Revenue pro B2C-Kunde</div>
                    <div style="color: white; font-size: 2rem; font-weight: 700;">85-180€</div>
                </div>
                <div style="border-left: 1px solid rgba(255,255,255,0.3); padding-left: 30px;">
                    <div style="color: white; font-size: 0.85rem; opacity: 0.9;">Ø Revenue pro B2B-Fahrzeug/Jahr</div>
                    <div style="color: white; font-size: 2rem; font-weight: 700;">708-948€</div>
                </div>
                <div style="border-left: 1px solid rgba(255,255,255,0.3); padding-left: 30px;">
                    <div style="color: white; font-size: 0.85rem; opacity: 0.9;">Conversion Lead → Expert</div>
                    <div style="color: white; font-size: 2rem; font-weight: 700;">~30%</div>
                </div>
            </div>
        </div>
    ''', unsafe_allow_html=True)

    # Ausbaustufen
    st.markdown('''
        <div style="background: #F9FAFB; padding: 20px; border-radius: 10px; margin-top: 25px;">
            <h4 style="color: #6B7280; margin: 0 0 15px 0;">🚀 Zusätzliche Revenue-Optionen (später):</h4>
            <div style="display: flex; flex-wrap: wrap; gap: 10px;">
                <span style="background: white; color: #6B7280; padding: 8px 16px; border-radius: 20px; border: 1px solid #E5E7EB;">White-Label für Autohäuser</span>
                <span style="background: white; color: #6B7280; padding: 8px 16px; border-radius: 20px; border: 1px solid #E5E7EB;">Versicherungs-Affiliate</span>
                <span style="background: white; color: #6B7280; padding: 8px 16px; border-radius: 20px; border: 1px solid #E5E7EB;">Gebrauchtwagen-Vermittlung</span>
                <span style="background: white; color: #6B7280; padding: 8px 16px; border-radius: 20px; border: 1px solid #E5E7EB;">Premium-Pakete (Express, Sorgenfrei)</span>
            </div>
        </div>
    ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════════════════
    # HAFTUNG & COMPLIANCE
    # ═══════════════════════════════════════════════════════════════════════════

    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">⚖️ Haftung & Rolle</h2>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">Souverän kommuniziert – nicht versteckt</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('''
            <div style="background: #fef3c7; padding: 25px; border-radius: 12px; height: 100%;">
                <h4 style="color: #92400e; margin: 0 0 15px 0;">ReturnGuard macht:</h4>
                <ul style="color: #78350f; margin: 0; padding-left: 20px; line-height: 2;">
                    <li>Vermitteln</li>
                    <li>Koordinieren</li>
                    <li>Dokumentieren</li>
                    <li>Vorqualifizieren</li>
                </ul>
            </div>
        ''', unsafe_allow_html=True)

    with col2:
        st.markdown('''
            <div style="background: #fee2e2; padding: 25px; border-radius: 12px; height: 100%;">
                <h4 style="color: #991b1b; margin: 0 0 15px 0;">ReturnGuard macht <u>nicht</u>:</h4>
                <ul style="color: #7f1d1d; margin: 0; padding-left: 20px; line-height: 2;">
                    <li>Gutachten erstellen</li>
                    <li>Reparaturen durchführen</li>
                    <li>Rechtsfragen entscheiden</li>
                    <li>Für Leasinggesellschaften bewerten</li>
                </ul>
            </div>
        ''', unsafe_allow_html=True)

    # Compliance
    st.markdown('''
        <div style="background: #f0fdf4; padding: 25px; border-radius: 12px; margin-top: 25px; border: 2px solid #059669;">
            <h4 style="color: #166534; margin: 0 0 15px 0;">✅ Regulatorische Einfachheit:</h4>
            <div style="display: flex; flex-wrap: wrap; gap: 10px;">
                <span style="background: #dcfce7; color: #166534; padding: 8px 16px; border-radius: 20px;">Keine Finanzvermittlung</span>
                <span style="background: #dcfce7; color: #166534; padding: 8px 16px; border-radius: 20px;">Keine Versicherungsberatung</span>
                <span style="background: #dcfce7; color: #166534; padding: 8px 16px; border-radius: 20px;">Keine Rechtsberatung</span>
                <span style="background: #dcfce7; color: #166534; padding: 8px 16px; border-radius: 20px;">Keine Sachverständigentätigkeit</span>
            </div>
            <p style="color: #15803d; margin: 15px 0 0 0; font-weight: 600;">
                → Kein regulatorisches Minenfeld. Das reduziert rechtliches Risiko, operative Komplexität und Skalierungshürden.
            </p>
        </div>
    ''', unsafe_allow_html=True)

    # Investor-Statement
    st.markdown('''
        <div style="background: #1B365D; padding: 20px 30px; border-radius: 12px; margin-top: 25px; text-align: center;">
            <p style="color: white; font-size: 1.1rem; margin: 0;">
                💼 <strong>Für Investoren:</strong> Das ist kein Nachteil – das ist ein Schutzschild.
            </p>
        </div>
    ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════════════════
    # WARUM INVESTIERBAR
    # ═══════════════════════════════════════════════════════════════════════════

    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">🎯 Warum ReturnGuard investierbar ist</h2>', unsafe_allow_html=True)

    st.markdown('''
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px;">
            <div style="background: #F9FAFB; padding: 25px; border-radius: 12px; text-align: center;">
                <div style="font-size: 2.5rem; margin-bottom: 10px;">🪶</div>
                <h4 style="color: #1F2937; margin: 0 0 10px 0;">Asset-light</h4>
                <p style="color: #6B7280; margin: 0; font-size: 0.9rem;">Kein CapEx, keine Lager, keine Angestellten pro Stadt</p>
            </div>
            <div style="background: #F9FAFB; padding: 25px; border-radius: 12px; text-align: center;">
                <div style="font-size: 2.5rem; margin-bottom: 10px;">📈</div>
                <h4 style="color: #1F2937; margin: 0 0 10px 0;">Skalierbar</h4>
                <p style="color: #6B7280; margin: 0; font-size: 0.9rem;">Skalierung über Netzwerk & Software, nicht über Personal</p>
            </div>
            <div style="background: #F9FAFB; padding: 25px; border-radius: 12px; text-align: center;">
                <div style="font-size: 2.5rem; margin-bottom: 10px;">💰</div>
                <h4 style="color: #1F2937; margin: 0 0 10px 0;">Mehrere Erlösströme</h4>
                <p style="color: #6B7280; margin: 0; font-size: 0.9rem;">4+ Revenue Layers, modular erweiterbar</p>
            </div>
            <div style="background: #F9FAFB; padding: 25px; border-radius: 12px; text-align: center;">
                <div style="font-size: 2.5rem; margin-bottom: 10px;">🛡️</div>
                <h4 style="color: #1F2937; margin: 0 0 10px 0;">Geringes Haftungsrisiko</h4>
                <p style="color: #6B7280; margin: 0; font-size: 0.9rem;">Reine Vermittlung, keine operative Ausführung</p>
            </div>
        </div>
    ''', unsafe_allow_html=True)

    # Abschluss-Statement
    st.markdown('''
        <div style="background: linear-gradient(135deg, #059669 0%, #047857 100%);
                    padding: 40px; border-radius: 12px; margin-top: 30px; text-align: center;">
            <p style="color: white; font-size: 1.4rem; margin: 0; font-weight: 600;">
                „Das ist kein Feature, das ist eine Infrastruktur."
            </p>
            <p style="color: #a7f3d0; font-size: 1rem; margin: 15px 0 0 0;">
                ReturnGuard fühlt sich an wie etwas, das es eigentlich schon längst geben müsste.
            </p>
        </div>
    ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


def render_b2c():
    """B2C View: Home, Calculator, FAQ, Blog, Contact"""
    # Floating CTAs nur für B2C
    st.markdown("""
    <div class="floating-cta">
        <a href="tel:+498912345678" class="floating-btn floating-phone" title="Jetzt anrufen">
            📞
        </a>
        <a href="https://wa.me/4917698765432?text=Hallo%20ReturnGuard%2C%20ich%20interessiere%20mich%20f%C3%BCr%20eine%20Leasingr%C3%BCckgabe-Beratung."
           target="_blank" class="floating-btn floating-whatsapp" title="WhatsApp">
            💬
        </a>
        <a href="?page=calculator#content-start-calculator" target="_self" class="floating-btn floating-main" title="Quick-Check starten">
            🧮
        </a>
    </div>
    """, unsafe_allow_html=True)

    # Navigation für B2C
    st.markdown('<div class="top-nav">', unsafe_allow_html=True)
    st.markdown('<div class="nav-brand">🛡️ ReturnGuard</div>', unsafe_allow_html=True)

    nav_cols = st.columns(7)
    with nav_cols[0]:
        st.markdown('<a href="?page=home#content-start-home" target="_self" class="nav-link">🏠 Home</a>', unsafe_allow_html=True)
    with nav_cols[1]:
        st.markdown('<a href="?page=calculator#content-start-calculator" target="_self" class="nav-link">📱 Quick-Check</a>', unsafe_allow_html=True)
    with nav_cols[2]:
        st.markdown('<a href="?page=faq#content-start-faq" target="_self" class="nav-link">❓ FAQ</a>', unsafe_allow_html=True)
    with nav_cols[3]:
        st.markdown('<a href="?page=blog#content-start-blog" target="_self" class="nav-link">📝 Blog</a>', unsafe_allow_html=True)
    with nav_cols[4]:
        st.markdown('<a href="?page=contact#content-start-contact" target="_self" class="nav-link">📞 Kontakt</a>', unsafe_allow_html=True)
    with nav_cols[5]:
        st.markdown('<a href="?page=about#content-start-about" target="_self" class="nav-link">👥 Über uns</a>', unsafe_allow_html=True)
    with nav_cols[6]:
        st.markdown('<a href="?page=legal#content-start-legal" target="_self" class="nav-link">⚖️ Rechtliches</a>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ==================== B2C PAGES ====================
    # Die Page-spezifischen Inhalte werden nach diesem Block gerendert
    # durch den globalen Page-Router (mit View-Checks)


def render_b2b():
    """B2B View: Services, Contact (B2B-Fokus), Legal"""

    # B2B HERO - Fokus auf Effizienz & Planbarkeit
    st.markdown('''
        <div class="hero-section" style="background: linear-gradient(135deg, #1e3a5f 0%, #0f172a 100%);">
            <div class="hero-content">
                <p style="color: #60a5fa; font-size: 0.9rem; font-weight: 600; margin-bottom: 10px; letter-spacing: 1px;">FÜR FLOTTENMANAGER & FUHRPARKLEITER</p>
                <h1 class="hero-title" style="font-size: 2.5rem;">Weniger Verwaltung.<br>Mehr Planbarkeit.</h1>
                <p class="hero-subtitle" style="text-align: center; max-width: 650px; margin: 0 auto 25px auto; font-size: 1.15rem;">
                    Standardisieren Sie Ihre Leasingrückgaben – mit festen Konditionen,<br>
                    einem Netzwerk und einem Ansprechpartner.
                </p>
                <div style="display: flex; justify-content: center; gap: 15px; flex-wrap: wrap;">
                    <a href="?page=contact#content-start-contact" target="_self" class="hero-cta">Angebot anfordern →</a>
                    <a href="tel:+498912345678" class="hero-cta" style="background: transparent; border: 2px solid white;">📞 Direkt sprechen</a>
                </div>
            </div>
        </div>
    ''', unsafe_allow_html=True)

    # PROBLEM-SECTION - Pain Points für Flottenmanager
    st.markdown('''
        <div style="background: #f8fafc; padding: 50px 20px;">
            <div style="max-width: 900px; margin: 0 auto;">
                <h2 style="text-align: center; color: #1F2937; margin-bottom: 30px;">Das Problem bei Flotten-Rückgaben</h2>

                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px;">
                    <div style="background: white; padding: 25px; border-radius: 12px; border-left: 4px solid #ef4444;">
                        <div style="font-size: 2rem; margin-bottom: 10px;">🔄</div>
                        <h4 style="color: #1F2937; margin: 0 0 10px 0;">Jedes Mal neu verhandeln</h4>
                        <p style="color: #6B7280; margin: 0; font-size: 0.9rem;">Für jedes Fahrzeug einzeln Werkstätten suchen, Angebote einholen, vergleichen – bei 50+ Fahrzeugen pro Jahr.</p>
                    </div>
                    <div style="background: white; padding: 25px; border-radius: 12px; border-left: 4px solid #ef4444;">
                        <div style="font-size: 2rem; margin-bottom: 10px;">📊</div>
                        <h4 style="color: #1F2937; margin: 0 0 10px 0;">Unplanbare Kosten</h4>
                        <p style="color: #6B7280; margin: 0; font-size: 0.9rem;">Jede Rückgabe ist eine Blackbox. Budget-Planung für Nachzahlungen? Fast unmöglich.</p>
                    </div>
                    <div style="background: white; padding: 25px; border-radius: 12px; border-left: 4px solid #ef4444;">
                        <div style="font-size: 2rem; margin-bottom: 10px;">👥</div>
                        <h4 style="color: #1F2937; margin: 0 0 10px 0;">Wechselnde Ansprechpartner</h4>
                        <p style="color: #6B7280; margin: 0; font-size: 0.9rem;">Bei jeder Leasinggesellschaft andere Prozesse, andere Kontakte, andere Maßstäbe.</p>
                    </div>
                </div>
            </div>
        </div>
    ''', unsafe_allow_html=True)

    # LÖSUNG - Was ReturnGuard Business bietet
    st.markdown('''
        <div style="background: white; padding: 50px 20px;">
            <div style="max-width: 1000px; margin: 0 auto;">
                <h2 style="text-align: center; color: #1F2937; margin-bottom: 10px;">Die ReturnGuard Business Lösung</h2>
                <p style="text-align: center; color: #6B7280; margin-bottom: 40px;">Ein Partner, ein Preis, ein Prozess – für Ihre gesamte Flotte</p>

                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 25px;">
                    <div style="text-align: center; padding: 30px;">
                        <div style="background: #ecfdf5; width: 70px; height: 70px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 20px auto; font-size: 2rem;">📋</div>
                        <h4 style="color: #1F2937; margin: 0 0 10px 0;">Standardisierter Prozess</h4>
                        <p style="color: #6B7280; margin: 0; font-size: 0.95rem;">Gleicher Ablauf für jedes Fahrzeug. Dokumentation, Aufbereitung, Rückgabe – immer nach dem gleichen Schema.</p>
                    </div>
                    <div style="text-align: center; padding: 30px;">
                        <div style="background: #ecfdf5; width: 70px; height: 70px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 20px auto; font-size: 2rem;">💶</div>
                        <h4 style="color: #1F2937; margin: 0 0 10px 0;">Fixe Konditionen</h4>
                        <p style="color: #6B7280; margin: 0; font-size: 0.95rem;">Flatrate pro Fahrzeug oder Kontingent-Pakete. Sie wissen im Voraus, was Sie zahlen.</p>
                    </div>
                    <div style="text-align: center; padding: 30px;">
                        <div style="background: #ecfdf5; width: 70px; height: 70px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 20px auto; font-size: 2rem;">🤝</div>
                        <h4 style="color: #1F2937; margin: 0 0 10px 0;">Ihr Account Manager</h4>
                        <p style="color: #6B7280; margin: 0; font-size: 0.95rem;">Ein Ansprechpartner für alle Ihre Fahrzeuge. Kennt Ihre Flotte, Ihre Prozesse, Ihre Anforderungen.</p>
                    </div>
                </div>
            </div>
        </div>
    ''', unsafe_allow_html=True)

    # PAKETE - Fixpreis-Modelle
    st.markdown('''
        <div style="background: #f8fafc; padding: 50px 20px;">
            <div style="max-width: 1100px; margin: 0 auto;">
                <h2 style="text-align: center; color: #1F2937; margin-bottom: 10px;">Unsere B2B-Pakete</h2>
                <p style="text-align: center; color: #6B7280; margin-bottom: 40px;">Wählen Sie das Modell, das zu Ihrer Flottengröße passt</p>

                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 25px;">
                    <!-- Starter -->
                    <div style="background: white; padding: 35px; border-radius: 16px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                        <p style="color: #6B7280; font-size: 0.85rem; margin: 0 0 5px 0; font-weight: 600;">STARTER</p>
                        <h3 style="color: #1F2937; margin: 0 0 5px 0;">10-25 Fahrzeuge</h3>
                        <div style="margin: 20px 0;">
                            <span style="font-size: 2.5rem; font-weight: 700; color: #059669;">79€</span>
                            <span style="color: #6B7280;">/Fahrzeug/Monat</span>
                        </div>
                        <ul style="list-style: none; padding: 0; margin: 0 0 25px 0;">
                            <li style="color: #4B5563; padding: 8px 0; border-bottom: 1px solid #f3f4f6;">✓ Standardisierter Rückgabe-Prozess</li>
                            <li style="color: #4B5563; padding: 8px 0; border-bottom: 1px solid #f3f4f6;">✓ Aufbereiter aus unserem Netzwerk</li>
                            <li style="color: #4B5563; padding: 8px 0; border-bottom: 1px solid #f3f4f6;">✓ Dokumentation & Fotobericht</li>
                            <li style="color: #4B5563; padding: 8px 0;">✓ E-Mail Support</li>
                        </ul>
                        <a href="?page=contact#content-start-contact" style="display: block; text-align: center; background: #f3f4f6; color: #1F2937; padding: 12px; border-radius: 8px; text-decoration: none; font-weight: 600;">Angebot anfordern</a>
                    </div>

                    <!-- Business -->
                    <div style="background: white; padding: 35px; border-radius: 16px; box-shadow: 0 4px 15px rgba(5,150,105,0.15); border: 2px solid #059669; position: relative;">
                        <div style="position: absolute; top: -12px; left: 50%; transform: translateX(-50%); background: #059669; color: white; padding: 5px 20px; border-radius: 20px; font-size: 0.8rem; font-weight: 600;">MEISTGEWÄHLT</div>
                        <p style="color: #059669; font-size: 0.85rem; margin: 0 0 5px 0; font-weight: 600;">BUSINESS</p>
                        <h3 style="color: #1F2937; margin: 0 0 5px 0;">25-100 Fahrzeuge</h3>
                        <div style="margin: 20px 0;">
                            <span style="font-size: 2.5rem; font-weight: 700; color: #059669;">59€</span>
                            <span style="color: #6B7280;">/Fahrzeug/Monat</span>
                        </div>
                        <ul style="list-style: none; padding: 0; margin: 0 0 25px 0;">
                            <li style="color: #4B5563; padding: 8px 0; border-bottom: 1px solid #f3f4f6;">✓ Alles aus Starter, plus:</li>
                            <li style="color: #4B5563; padding: 8px 0; border-bottom: 1px solid #f3f4f6;">✓ <strong>Dedizierter Account Manager</strong></li>
                            <li style="color: #4B5563; padding: 8px 0; border-bottom: 1px solid #f3f4f6;">✓ Quartalsberichte & Analysen</li>
                            <li style="color: #4B5563; padding: 8px 0;">✓ Prioritäts-Support (Tel. & E-Mail)</li>
                        </ul>
                        <a href="?page=contact#content-start-contact" style="display: block; text-align: center; background: #059669; color: white; padding: 12px; border-radius: 8px; text-decoration: none; font-weight: 600;">Angebot anfordern</a>
                    </div>

                    <!-- Enterprise -->
                    <div style="background: white; padding: 35px; border-radius: 16px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                        <p style="color: #6B7280; font-size: 0.85rem; margin: 0 0 5px 0; font-weight: 600;">ENTERPRISE</p>
                        <h3 style="color: #1F2937; margin: 0 0 5px 0;">100+ Fahrzeuge</h3>
                        <div style="margin: 20px 0;">
                            <span style="font-size: 2.5rem; font-weight: 700; color: #059669;">Individuell</span>
                        </div>
                        <ul style="list-style: none; padding: 0; margin: 0 0 25px 0;">
                            <li style="color: #4B5563; padding: 8px 0; border-bottom: 1px solid #f3f4f6;">✓ Alles aus Business, plus:</li>
                            <li style="color: #4B5563; padding: 8px 0; border-bottom: 1px solid #f3f4f6;">✓ <strong>Individuelle Konditionen</strong></li>
                            <li style="color: #4B5563; padding: 8px 0; border-bottom: 1px solid #f3f4f6;">✓ API-Anbindung an Ihre Systeme</li>
                            <li style="color: #4B5563; padding: 8px 0;">✓ SLA-Vereinbarungen</li>
                        </ul>
                        <a href="?page=contact#content-start-contact" style="display: block; text-align: center; background: #f3f4f6; color: #1F2937; padding: 12px; border-radius: 8px; text-decoration: none; font-weight: 600;">Gespräch vereinbaren</a>
                    </div>
                </div>
            </div>
        </div>
    ''', unsafe_allow_html=True)

    # VORTEILE - Warum Flottenmanager wechseln
    st.markdown('''
        <div style="background: white; padding: 50px 20px;">
            <div style="max-width: 900px; margin: 0 auto;">
                <h2 style="text-align: center; color: #1F2937; margin-bottom: 40px;">Warum Flottenmanager zu uns wechseln</h2>

                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px;">
                    <div style="display: flex; gap: 15px; align-items: flex-start;">
                        <div style="background: #ecfdf5; padding: 10px; border-radius: 8px; font-size: 1.5rem;">⏱️</div>
                        <div>
                            <h4 style="color: #1F2937; margin: 0 0 5px 0;">70% weniger Verwaltungsaufwand</h4>
                            <p style="color: #6B7280; margin: 0; font-size: 0.9rem;">Keine Einzelverhandlungen mehr. Ein Prozess für alle Fahrzeuge.</p>
                        </div>
                    </div>
                    <div style="display: flex; gap: 15px; align-items: flex-start;">
                        <div style="background: #ecfdf5; padding: 10px; border-radius: 8px; font-size: 1.5rem;">📈</div>
                        <div>
                            <h4 style="color: #1F2937; margin: 0 0 5px 0;">Planbare Budgets</h4>
                            <p style="color: #6B7280; margin: 0; font-size: 0.9rem;">Fixkosten pro Fahrzeug. Keine Überraschungen am Jahresende.</p>
                        </div>
                    </div>
                    <div style="display: flex; gap: 15px; align-items: flex-start;">
                        <div style="background: #ecfdf5; padding: 10px; border-radius: 8px; font-size: 1.5rem;">🔧</div>
                        <div>
                            <h4 style="color: #1F2937; margin: 0 0 5px 0;">Bundesweites Netzwerk</h4>
                            <p style="color: #6B7280; margin: 0; font-size: 0.9rem;">Über 200 Werkstätten und Aufbereiter. Egal wo Ihre Fahrzeuge stehen.</p>
                        </div>
                    </div>
                    <div style="display: flex; gap: 15px; align-items: flex-start;">
                        <div style="background: #ecfdf5; padding: 10px; border-radius: 8px; font-size: 1.5rem;">📋</div>
                        <div>
                            <h4 style="color: #1F2937; margin: 0 0 5px 0;">Revisionssichere Dokumentation</h4>
                            <p style="color: #6B7280; margin: 0; font-size: 0.9rem;">Jede Rückgabe vollständig dokumentiert. Für Ihre Buchhaltung und Revision.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    ''', unsafe_allow_html=True)

    # ONBOARDING - So starten Sie
    st.markdown('''
        <div style="background: #f8fafc; padding: 50px 20px;">
            <div style="max-width: 900px; margin: 0 auto;">
                <h2 style="text-align: center; color: #1F2937; margin-bottom: 10px;">So starten wir zusammen</h2>
                <p style="text-align: center; color: #6B7280; margin-bottom: 40px;">In 4 Wochen einsatzbereit</p>

                <div style="display: flex; justify-content: space-between; flex-wrap: wrap; gap: 20px;">
                    <div style="flex: 1; min-width: 180px; text-align: center;">
                        <div style="background: #059669; color: white; width: 50px; height: 50px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 15px auto; font-weight: bold; font-size: 1.2rem;">1</div>
                        <h4 style="color: #1F2937; margin: 0 0 5px 0;">Bedarfsanalyse</h4>
                        <p style="color: #6B7280; margin: 0; font-size: 0.85rem;">Wir analysieren Ihre Flotte und Prozesse</p>
                    </div>
                    <div style="flex: 1; min-width: 180px; text-align: center;">
                        <div style="background: #059669; color: white; width: 50px; height: 50px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 15px auto; font-weight: bold; font-size: 1.2rem;">2</div>
                        <h4 style="color: #1F2937; margin: 0 0 5px 0;">Individuelles Angebot</h4>
                        <p style="color: #6B7280; margin: 0; font-size: 0.85rem;">Maßgeschneidert auf Ihre Flottengröße</p>
                    </div>
                    <div style="flex: 1; min-width: 180px; text-align: center;">
                        <div style="background: #059669; color: white; width: 50px; height: 50px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 15px auto; font-weight: bold; font-size: 1.2rem;">3</div>
                        <h4 style="color: #1F2937; margin: 0 0 5px 0;">Pilotphase</h4>
                        <p style="color: #6B7280; margin: 0; font-size: 0.85rem;">5 Fahrzeuge testen – risikofrei</p>
                    </div>
                    <div style="flex: 1; min-width: 180px; text-align: center;">
                        <div style="background: #059669; color: white; width: 50px; height: 50px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 15px auto; font-weight: bold; font-size: 1.2rem;">4</div>
                        <h4 style="color: #1F2937; margin: 0 0 5px 0;">Rollout</h4>
                        <p style="color: #6B7280; margin: 0; font-size: 0.85rem;">Vollständige Integration Ihrer Flotte</p>
                    </div>
                </div>
            </div>
        </div>
    ''', unsafe_allow_html=True)

    # ABSCHLUSS CTA
    st.markdown('''
        <div style="background: linear-gradient(135deg, #1e3a5f 0%, #0f172a 100%); padding: 60px 30px; text-align: center;">
            <h2 style="color: white; margin: 0 0 15px 0; font-size: 1.8rem;">Bereit für planbare Leasingrückgaben?</h2>
            <p style="color: rgba(255,255,255,0.8); margin: 0 0 30px 0; font-size: 1.1rem;">
                Lassen Sie uns in 15 Minuten besprechen, wie ReturnGuard Business zu Ihrer Flotte passt.
            </p>
            <div style="display: flex; justify-content: center; gap: 15px; flex-wrap: wrap;">
                <a href="?page=contact#content-start-contact" style="background: #059669; color: white; padding: 15px 35px; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 1.1rem;">Angebot anfordern →</a>
                <a href="tel:+498912345678" style="background: transparent; color: white; padding: 15px 35px; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 1.1rem; border: 2px solid rgba(255,255,255,0.5);">📞 +49 89 123 456 78</a>
            </div>
        </div>
    ''', unsafe_allow_html=True)

    # ==================== B2B PAGES ====================
    # Die Page-spezifischen Inhalte werden nach diesem Block gerendert
    # durch den globalen Page-Router (mit View-Checks)


# ==================== COOKIE BANNER ====================
# Deaktiviert für bessere Performance - für Produktion mit echtem Cookie-Management-Tool ersetzen
# if st.session_state.show_cookie_banner:
#     cookie_col1, cookie_col2 = st.columns([4, 1])
#     with cookie_col1:
#         st.info("🍪 Wir verwenden Cookies zur Verbesserung Ihrer Erfahrung. Details in unserer Datenschutzerklärung.")
#     with cookie_col2:
#         if st.button("OK", key="accept_cookies"):
#             st.session_state.show_cookie_banner = False
#             st.rerun()

# ==================== VIEW ROUTER ====================
# Router entscheidet basierend auf Session State View, welche Render-Funktion aufgerufen wird
if st.session_state.view == "Investor":
    render_investor()
elif st.session_state.view == "B2C":
    render_b2c()
elif st.session_state.view == "B2B":
    render_b2b()

# Bestehende Page-basierte Navigation wird hier integriert (nach Router-Logik)
# Seiten werden nur angezeigt, wenn die passende View aktiv ist
# ==================== STARTSEITE ====================
if st.session_state.view == "B2C" and st.session_state.page == 'home':
    st.markdown('<div id="content-start-home"></div>', unsafe_allow_html=True)

    # HERO SECTION - Fokus auf Sicherheit & Orientierung
    st.markdown('''
        <div class="hero-section">
            <div class="hero-content">
                <h1 class="hero-title">Leasingrückgabe ohne böse Überraschungen</h1>
                <p class="hero-subtitle" style="text-align: center; max-width: 650px; margin: 0 auto 25px auto; font-size: 1.2rem;">
                    Kein Stress. Keine versteckten Kosten. Keine Unsicherheit.<br>
                    <strong style="color: #059669;">Wir begleiten Sie Schritt für Schritt – von der Vorbereitung bis zur Rückgabe.</strong>
                </p>
                <div style="display: flex; justify-content: center; gap: 15px; flex-wrap: wrap;">
                    <a href="?page=calculator#content-start-calculator" target="_self" class="hero-cta">Jetzt Kosten einschätzen →</a>
                    <a href="?page=contact#content-start-contact" target="_self" class="hero-cta" style="background: white; color: #059669; border: 2px solid #059669;">Kostenlos beraten lassen</a>
                </div>
            </div>
        </div>
    ''', unsafe_allow_html=True)

    # Vertrauens-Banner direkt nach Hero
    st.markdown('''
        <div style="background: #ecfdf5; padding: 20px; border-radius: 12px; margin: -30px auto 30px auto; max-width: 800px; text-align: center; border: 1px solid #a7f3d0;">
            <span style="color: #059669; font-size: 1.1rem;">
                ✓ Unverbindlich &nbsp;&nbsp; ✓ Kostenlose Erstberatung &nbsp;&nbsp; ✓ Keine versteckten Gebühren
            </span>
        </div>
    ''', unsafe_allow_html=True)

    # SOCIAL PROOF BANNER
    st.markdown('''
        <div class="social-proof-banner">
            <div class="social-stats">
                <div class="stat-item">
                    <div class="stat-number">1.200+</div>
                    <div class="stat-label">Betreute Fälle</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">2.500€</div>
                    <div class="stat-label">Durchschn. Einsparung</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">98%</div>
                    <div class="stat-label">Erfolgreiche Einigungen</div>
                </div>
            </div>
        </div>
    ''', unsafe_allow_html=True)

    # 3-SCHRITTE PROZESS - Kundenorientiert
    st.markdown('<div class="process-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="process-title">In 3 Schritten sicher zurückgeben</h2>', unsafe_allow_html=True)
    st.markdown('<p class="process-subtitle">Keine Vorkenntnisse nötig – wir führen Sie durch</p>', unsafe_allow_html=True)

    step1, step2, step3 = st.columns(3)

    with step1:
        st.markdown('''
            <div class="process-step">
                <div class="step-number">1</div>
                <div class="step-icon">📱</div>
                <h3 class="step-title">Situation erfassen</h3>
                <p class="step-description">
                    Unser kostenloser Schnellcheck zeigt Ihnen in 2 Minuten,
                    wo Sie stehen und was zu erwarten ist.
                </p>
            </div>
        ''', unsafe_allow_html=True)

    with step2:
        st.markdown('''
            <div class="process-step">
                <div class="step-number">2</div>
                <div class="step-icon">🛡️</div>
                <h3 class="step-title">Vorbereitung</h3>
                <p class="step-description">
                    Wir zeigen Ihnen, was vor der Rückgabe noch zu tun ist –
                    und was sich lohnt, reparieren zu lassen.
                </p>
            </div>
        ''', unsafe_allow_html=True)

    with step3:
        st.markdown('''
            <div class="process-step">
                <div class="step-number">3</div>
                <div class="step-icon">✅</div>
                <h3 class="step-title">Entspannt zurückgeben</h3>
                <p class="step-description">
                    Gut vorbereitet, fair bewertet, ohne Nachzahlungs-Stress.
                    Im Schnitt sparen unsere Kunden 2.500€.
                </p>
            </div>
        ''', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # HÄUFIGE SORGEN - Direkte Ansprache der Pain Points
    st.markdown('''
        <div style="background: white; padding: 40px 20px; margin: 30px 0;">
            <h2 style="text-align: center; color: #1F2937; margin-bottom: 10px;">Kennen Sie das?</h2>
            <p style="text-align: center; color: #6B7280; margin-bottom: 30px;">Diese Sorgen haben die meisten Leasingnehmer vor der Rückgabe</p>

            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; max-width: 1000px; margin: 0 auto;">
                <div style="background: #FEF2F2; padding: 20px; border-radius: 12px; border-left: 4px solid #EF4444;">
                    <div style="font-size: 1.5rem; margin-bottom: 10px;">😰</div>
                    <h4 style="color: #991B1B; margin: 0 0 8px 0;">"Was wird mir die Leasingfirma berechnen?"</h4>
                    <p style="color: #7F1D1D; margin: 0; font-size: 0.9rem;">→ Unser Quick-Check zeigt Ihnen vorab eine realistische Einschätzung</p>
                </div>
                <div style="background: #FEF2F2; padding: 20px; border-radius: 12px; border-left: 4px solid #EF4444;">
                    <div style="font-size: 1.5rem; margin-bottom: 10px;">🤔</div>
                    <h4 style="color: #991B1B; margin: 0 0 8px 0;">"Lohnt sich eine Reparatur noch?"</h4>
                    <p style="color: #7F1D1D; margin: 0; font-size: 0.9rem;">→ Wir sagen Ihnen, was sich lohnt – und was nicht</p>
                </div>
                <div style="background: #FEF2F2; padding: 20px; border-radius: 12px; border-left: 4px solid #EF4444;">
                    <div style="font-size: 1.5rem; margin-bottom: 10px;">⚖️</div>
                    <h4 style="color: #991B1B; margin: 0 0 8px 0;">"Die Abrechnung war unfair – was tun?"</h4>
                    <p style="color: #7F1D1D; margin: 0; font-size: 0.9rem;">→ Wir verbinden Sie mit spezialisierten Fachanwälten</p>
                </div>
            </div>

            <div style="text-align: center; margin-top: 30px;">
                <p style="color: #059669; font-size: 1.1rem; font-weight: 600; margin: 0;">
                    ✓ Sie sind nicht allein. Über 1.200 Kunden hatten dieselben Fragen.
                </p>
            </div>
        </div>
    ''', unsafe_allow_html=True)

    # KUNDENBEWERTUNGEN
    st.markdown('<div class="testimonial-section">', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Das sagen unsere Kunden</h2>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">Echte Erfahrungen, echte Ersparnisse</p>', unsafe_allow_html=True)

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
            "text": "Sehr professionell und transparent. Der Quick-Check hat mir vorab schon eine gute Einschätzung gegeben. Das Ergebnis war sogar noch besser!",
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
    st.markdown('<h2 class="section-title">Kooperationspartner & Qualifikationen</h2>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">Zertifizierte Gutachter und Fachanwälte</p>', unsafe_allow_html=True)

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
                    <div class="trust-title">Fachanwälte<br/>Verkehrsrecht</div>
                </div>
                <div class="trust-badge">
                    <div class="trust-icon">🔍</div>
                    <div class="trust-title">TÜV-zertifizierte<br/>Sachverständige</div>
                </div>
                <div class="trust-badge">
                    <div class="trust-icon">🏆</div>
                    <div class="trust-title">Seit 2009<br/>aktiv</div>
                </div>
                <div class="trust-badge">
                    <div class="trust-icon">✅</div>
                    <div class="trust-title">Transparente<br/>Preisgestaltung</div>
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
                <p class="package-subtitle">Grundprüfung</p>
                <div class="package-price">99<span class="package-price-unit">€</span></div>
                <ul class="package-features">
                    <li>✓ Grundcheck Fahrzeug</li>
                    <li>✓ 20 Dokumentationsfotos</li>
                    <li>✓ PDF-Bericht per Email</li>
                    <li>✓ Bearbeitung in 48h</li>
                </ul>
            </div>
        ''', unsafe_allow_html=True)
        st.button("Paket anfragen", key="b1", use_container_width=True)

    with pkg2:
        st.markdown('''
            <div class="package-card">
                <div class="package-icon">📊</div>
                <h3 class="package-title">Standard</h3>
                <p class="package-subtitle">Erweiterte Prüfung</p>
                <div class="package-price">199<span class="package-price-unit">€</span></div>
                <ul class="package-features">
                    <li>✓ Umfassende Prüfung</li>
                    <li>✓ 50 Detailfotos</li>
                    <li>✓ Telefonberatung 1h</li>
                    <li>✓ Bearbeitung in 24h</li>
                </ul>
            </div>
        ''', unsafe_allow_html=True)
        st.button("Paket anfragen", key="b2", use_container_width=True)

    with pkg3:
        st.markdown('''
            <div class="package-card package-popular" style="position: relative;">
                <div class="popular-badge">⭐ MEISTGEWÄHLT</div>
                <div class="package-icon">🥇</div>
                <h3 class="package-title">Premium</h3>
                <p class="package-subtitle">Mit Rechtsberatung</p>
                <div class="package-price">299<span class="package-price-unit">€</span></div>
                <ul class="package-features">
                    <li>✓ Rechtliche Prüfung</li>
                    <li>✓ Anwaltsberatung 2h</li>
                    <li>✓ 24/7 Support-Hotline</li>
                    <li>✓ Sofort-Bearbeitung</li>
                </ul>
            </div>
        ''', unsafe_allow_html=True)
        st.button("Paket anfragen", key="b3", use_container_width=True)

    with pkg4:
        st.markdown('''
            <div class="package-card">
                <div class="package-icon">💎</div>
                <h3 class="package-title">VIP</h3>
                <p class="package-subtitle">Full-Service</p>
                <div class="package-price">999<span class="package-price-unit">€</span></div>
                <ul class="package-features">
                    <li>✓ Full-Service Paket</li>
                    <li>✓ Vor-Ort bundesweit</li>
                    <li>✓ Rückgabe-Garantie</li>
                    <li>✓ Persönlicher Manager</li>
                </ul>
            </div>
        ''', unsafe_allow_html=True)
        st.button("Paket anfragen", key="b4", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ABSCHLUSS-CTA - Klare Orientierung
    st.markdown('''
        <div style="background: linear-gradient(135deg, #059669 0%, #047857 100%); padding: 50px 30px; border-radius: 16px; margin: 40px 0; text-align: center;">
            <h2 style="color: white; margin: 0 0 15px 0; font-size: 1.8rem;">Nicht sicher, wo Sie anfangen sollen?</h2>
            <p style="color: rgba(255,255,255,0.9); margin: 0 0 25px 0; font-size: 1.1rem; max-width: 600px; margin-left: auto; margin-right: auto;">
                Starten Sie mit unserem kostenlosen Schnellcheck – dauert nur 2 Minuten und zeigt Ihnen sofort, wie Sie vorbereitet sind.
            </p>
            <div style="display: flex; justify-content: center; gap: 15px; flex-wrap: wrap;">
                <a href="?page=calculator#content-start-calculator" target="_self" style="background: white; color: #059669; padding: 15px 30px; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 1.1rem;">Schnellcheck starten →</a>
                <a href="tel:+498912345678" style="background: transparent; color: white; padding: 15px 30px; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 1.1rem; border: 2px solid white;">📞 Lieber anrufen?</a>
            </div>
            <p style="color: rgba(255,255,255,0.7); margin: 20px 0 0 0; font-size: 0.9rem;">
                Mo-Fr 9-18 Uhr · Keine Warteschleifen · Echte Experten
            </p>
        </div>
    ''', unsafe_allow_html=True)

# ==================== DIGITALER QUICK-CHECK ====================
elif st.session_state.view == "B2C" and st.session_state.page == 'calculator':
    st.markdown('<div id="content-start-calculator"></div>', unsafe_allow_html=True)
    st.markdown('<div class="calculator-section">', unsafe_allow_html=True)

    st.markdown('''
        <div class="calculator-box">
            <h1 class="calculator-title">📱 Digitaler Quick-Check</h1>
            <p class="calculator-subtitle">
                Finden Sie in 2 Minuten heraus, wie viel Sie bei der Rückgabe sparen könnten.<br>
                <span style="color: #059669; font-weight: 500;">Unverbindlich. Kostenlos. Keine Anmeldung.</span>
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
            whatsapp_text = f"Hallo ReturnGuard, ich habe den Quick-Check genutzt.\n\n"
            whatsapp_text += f"Fahrzeug: {st.session_state.vehicle_class}, Baujahr {st.session_state.vehicle_year}\n"
            whatsapp_text += f"Geschätzte Kosten: {total_cost:,.0f}€\n"
            whatsapp_text += f"Anzahl Schäden: {len(damage_breakdown)}\n\n"
            whatsapp_text += "Ich interessiere mich für eine Beratung!"

            import urllib.parse
            whatsapp_url = f"https://wa.me/4917698765432?text={urllib.parse.quote(whatsapp_text)}"

            # HAUPTERGEBNIS: Potenzielle Ersparnis (nicht Kosten!)
            potential_savings = total_cost * 0.60
            st.markdown(f'''
                <div class="savings-box" style="background: linear-gradient(135deg, #059669 0%, #047857 100%); padding: 40px; border-radius: 16px; text-align: center;">
                    <div style="color: rgba(255,255,255,0.9); font-size: 1rem; margin-bottom: 10px;">💰 IHRE POTENZIELLE ERSPARNIS</div>
                    <div style="color: white; font-size: 4rem; font-weight: 700; margin: 10px 0;">bis zu {potential_savings:,.0f} €</div>
                    <p style="color: rgba(255,255,255,0.85); margin: 15px 0 0 0; font-size: 1rem;">
                        Basierend auf Ihrer Eingabe · Durchschnittliche Reduktion: 60%
                    </p>
                    <p style="color: rgba(255,255,255,0.6); margin: 10px 0 0 0; font-size: 0.85rem;">
                        ⚠️ Dies ist keine Bewertung, sondern eine unverbindliche Orientierung.
                    </p>
                </div>
            ''', unsafe_allow_html=True)

            # Sekundär: Kosten-Übersicht (kleiner)
            st.markdown(f'''
                <div style="background: #F9FAFB; padding: 20px; border-radius: 12px; margin-top: 20px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;">
                        <div>
                            <span style="color: #6B7280; font-size: 0.9rem;">Mögliche Kosten ohne Vorbereitung:</span>
                            <span style="color: #1F2937; font-weight: 600; font-size: 1.1rem; margin-left: 10px;">{total_cost:,.0f} €</span>
                        </div>
                        <div style="color: #6B7280; font-size: 0.85rem;">
                            {st.session_state.vehicle_class} · Baujahr {st.session_state.vehicle_year} · {len(damage_breakdown)} Bereiche
                        </div>
                    </div>
                </div>
            ''', unsafe_allow_html=True)

            # Detaillierte Aufschlüsselung (einklappbar)
            with st.expander("📋 Detaillierte Aufschlüsselung anzeigen"):
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

            st.markdown("---")

            # HAUPT-CTA: Angebote sichern
            st.markdown(f'''
                <div style="background: #1B365D; padding: 30px; border-radius: 12px; text-align: center; margin-bottom: 25px;">
                    <h3 style="color: white; margin: 0 0 10px 0;">🎯 Jetzt Angebote von Partnerwerkstätten sichern</h3>
                    <p style="color: #94a3b8; margin: 0 0 20px 0;">
                        Erhalten Sie unverbindliche Angebote von zertifizierten Werkstätten in Ihrer Nähe.
                    </p>
                </div>
            ''', unsafe_allow_html=True)

            # KONTAKTFORMULAR
            st.markdown("### 📝 Kostenlos Angebote anfordern")
            st.markdown("Unverbindlich und ohne Risiko – Sie entscheiden, ob Sie ein Angebot annehmen.")

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
elif st.session_state.view == "B2C" and st.session_state.page == 'faq':
    st.markdown('<div id="content-start-faq"></div>', unsafe_allow_html=True)
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.markdown('<h1 class="section-title">Häufige Fragen</h1>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">Wichtiges zu Leasingrückgaben im Überblick</p>', unsafe_allow_html=True)

    faqs = [
        {
            "question": "Wie funktioniert der Quick-Check?",
            "answer": "Unser digitaler Quick-Check führt Sie in 2 Minuten durch 20 Fahrzeugbereiche. Sie bewerten den Zustand auf einer Skala von 0-4. Am Ende sehen Sie Ihre potenzielle Ersparnis – keine verbindliche Bewertung, aber eine realistische Orientierung. Dann können Sie unverbindlich Angebote von Partnerwerkstätten anfordern."
        },
        {
            "question": "Wann sollte ich ReturnGuard kontaktieren?",
            "answer": "Idealerweise 2-3 Monate vor der Leasingrückgabe. So haben wir genug Zeit für eine gründliche Prüfung und können bei Bedarf noch kleinere Reparaturen empfehlen, die sich lohnen. Aber auch kurzfristig können wir oft noch helfen!"
        },
        {
            "question": "Was kostet eine Beratung?",
            "answer": "Die Erstberatung und Kostenschätzung ist kostenfrei. Kostenpflichtig sind unsere Pakete (99€ bis 999€), die Gutachten, Dokumentation und ggf. Verhandlung umfassen."
        },
        {
            "question": "Welche Schäden sind bei Leasingrückgabe normal?",
            "answer": "Normale Gebrauchsspuren wie leichte Kratzer im Lack (kleiner als eine Kreditkarte), leichte Steinschläge auf der Windschutzscheibe (nicht im Sichtfeld) und leichte Abnutzung im Innenraum sind in der Regel akzeptabel. Alles darüber hinaus kann zu Nachzahlungen führen."
        },
        {
            "question": "Welche Einsparungen sind möglich?",
            "answer": "In unseren Fällen konnten durchschnittlich 60% der ursprünglichen Forderungen reduziert werden. Bei einer Beispielforderung von 4.200€ entspricht das etwa 2.500€."
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
elif st.session_state.view == "B2C" and st.session_state.page == 'blog':
    st.markdown('<div id="content-start-blog"></div>', unsafe_allow_html=True)
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.markdown('<h1 class="section-title">Ratgeber</h1>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">Fachwissen zu Leasingrückgaben</p>', unsafe_allow_html=True)

    # CHECKLISTE als Featured Article
    st.markdown('''
        <div style="background: linear-gradient(135deg, #1B365D 0%, #1E3A8A 100%); padding: 40px; border-radius: 12px; color: white; margin-bottom: 40px;">
            <h2 style="font-size: 2rem; margin-bottom: 15px;">✅ Checkliste: Leasingrückgabe vorbereiten</h2>
            <p style="font-size: 1.1rem; opacity: 0.9;">
                Schritt-für-Schritt-Anleitung zur Vorbereitung Ihrer Leasingrückgabe.
                Von Vertragsprüfung bis Rückgabeprotokoll.
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
elif (st.session_state.view in ["B2C", "B2B"]) and st.session_state.page == 'about':
    st.markdown('<div id="content-start-about"></div>', unsafe_allow_html=True)
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.markdown('<h1 class="section-title">👥 Über ReturnGuard</h1>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">Die unabhängige Vermittlungsplattform für Leasingrückgaben</p>', unsafe_allow_html=True)

    st.write("""
    ### Unsere Mission

    ReturnGuard ist die zentrale Vermittlungsplattform für alle Dienstleistungen
    rund um die Leasingrückgabe. Wir verbinden Leasingnehmer mit den besten
    Werkstätten, Aufbereitern, Gutachtern und Fachanwälten.

    **Was uns auszeichnet:**
    - **Unabhängige Vermittlung:** Wir sind neutral und vermitteln die besten Partner
    - **Geprüftes Netzwerk:** Über 200 Partner-Werkstätten und 50 Aufbereiter bundesweit
    - **Fachanwälte bei Streit:** Vermittlung an spezialisierte Verkehrsrechtsanwälte
    - **TÜV-zertifizierte Gutachter:** Professionelle Schadensbewertung durch unser Netzwerk
    - **Über 1.200 vermittelte Fälle** mit durchschnittlich 2.500€ Ersparnis für Kunden

    ### Unser Vermittlungsmodell

    - 🔗 **Plattform:** Wir verbinden Angebot und Nachfrage
    - 🔧 **Werkstatt-Netzwerk:** Geprüfte Betriebe für Smart Repair und Vollreparatur
    - ✨ **Aufbereiter-Netzwerk:** Professionelle Fahrzeugaufbereitung
    - ⚖️ **Anwalts-Netzwerk:** Fachanwälte für Verkehrsrecht bei Streitfällen
    - 📋 **Gutachter-Netzwerk:** Unabhängige Schadensbewertung

    ### Unsere Werte

    - ✅ **Neutralität:** Wir sind keine Werkstatt und kein Gutachter – wir vermitteln nur
    - ⚖️ **Transparenz:** Klare Provisionsmodelle, keine versteckten Kosten
    - 🎯 **Qualität:** Nur geprüfte Partner in unserem Netzwerk
    - 💙 **Kundenfokus:** Das beste Angebot für jeden Kunden
    """)

    st.markdown("---")
    st.markdown("### 🏆 Referenzfälle")
    st.markdown("Dokumentierte Verhandlungsergebnisse")

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
elif (st.session_state.view in ["B2C", "B2B"]) and st.session_state.page == 'services':
    st.markdown('<div id="content-start-services"></div>', unsafe_allow_html=True)
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.markdown('<h1 class="section-title">📦 Unsere Leistungen</h1>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">Umfassender Service für Ihre Leasingrückgabe</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        ### 🔍 Technische Prüfung
        - Fahrzeuginspektion durch Sachverständige
        - Schadensdokumentation nach DAT/Schwacke
        - Fotodokumentation (50-100 Aufnahmen)
        - Gutachten gemäß Leasingvertrag

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

elif (st.session_state.view in ["B2C", "B2B"]) and st.session_state.page == 'contact':
    st.markdown('<div id="content-start-contact"></div>', unsafe_allow_html=True)
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

elif (st.session_state.view in ["B2C", "B2B"]) and st.session_state.page == 'legal':
    st.markdown('<div id="content-start-legal"></div>', unsafe_allow_html=True)
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

# ==================== NAVIGATION VIA QUERY PARAMS UND FRAGMENTS ====================
# Navigation erfolgt jetzt über echte HTML-Links mit Query-Params und URL-Fragments
# Dies löst einen echten Page-Reload aus → Browser scrollt nativ zum Fragment
# Stabiles Verhalten auf iOS Safari ohne JavaScript
