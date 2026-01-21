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

# ==================== SCROLL TO TOP ====================
# Hinweis: Scroll-to-Top funktioniert in Streamlit nur begrenzt wegen iFrame
# Für bessere UX: Nutzer können mit Tastatur (Pos1) oder Browser-Scroll nach oben
# Alternative: Streamlit's st.rerun() nutzt automatisch Scroll-to-Top

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
