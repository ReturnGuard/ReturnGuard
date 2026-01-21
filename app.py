import streamlit as st
import re

st.set_page_config(page_title="ReturnGuard - Leasingrückgabe ohne Sorgen", layout="wide", initial_sidebar_state="collapsed")

if 'page' not in st.session_state:
    st.session_state.page = 'home'

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

/* EMOTIONALER HERO - OHNE FORMULAR */
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
    border: 2px solid transparent;
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

/* SOCIAL PROOF BANNER - DIREKT UNTER HERO */
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

.testimonial-preview {
    margin-top: 25px;
    font-size: 1.05rem;
    color: #1F2937;
    font-style: italic;
}

.stars {
    color: #FFB800;
    font-size: 1.3rem;
    margin-top: 10px;
}

/* 3-SCHRITTE PROZESS - GROß & VISUELL */
.process-section {
    padding: 80px 20px;
    background: white;
}

.process-container {
    max-width: 1200px;
    margin: 0 auto;
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

.process-steps {
    display: flex;
    gap: 40px;
    position: relative;
}

.process-step {
    text-align: center;
    padding: 40px 30px;
    background: white;
    border-radius: 12px;
    border: 2px solid #E5E7EB;
    transition: all 0.3s ease;
    position: relative;
    flex: 1;
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

/* STICKY FLOATING ACTION BUTTON */
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

/* URGENCY BANNER */
.urgency-banner {
    background: linear-gradient(135deg, #DC2626 0%, #B91C1C 100%);
    color: white;
    padding: 18px 30px;
    text-align: center;
    font-size: 1.1rem;
    font-weight: 600;
    margin: 40px auto;
    max-width: 800px;
    border-radius: 8px;
    box-shadow: 0 4px 15px rgba(220, 38, 38, 0.3);
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.02); }
}

/* TRUST BADGES - VERBESSERT */
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

/* PAKETE - MIT MEHR KONTRAST */
.packages-section {
    padding: 80px 20px;
    background: white;
}

.section-header {
    text-align: center;
    margin-bottom: 60px;
}

.section-title {
    font-size: 2.5rem;
    font-weight: 600;
    color: #1F2937;
    margin-bottom: 15px;
}

.section-subtitle {
    font-size: 1.2rem;
    color: #6B7280;
}

.packages-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 30px;
    max-width: 1200px;
    margin: 0 auto;
}

.package-card {
    background: white;
    border-radius: 12px;
    padding: 40px 30px;
    border: 2px solid #E5E7EB;
    transition: all 0.4s ease;
    position: relative;
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
    letter-spacing: 1px;
    box-shadow: 0 4px 15px rgba(5, 150, 105, 0.4);
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
    line-height: 1;
}

.package-price-unit {
    font-size: 1.2rem;
    color: #6B7280;
    font-weight: 400;
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
    line-height: 1.5;
}

.package-features li:last-child {
    border-bottom: none;
}

/* FORMULAR-SECTION */
.calculator-section {
    background: linear-gradient(135deg, #F3F4F6 0%, #E5E7EB 100%);
    padding: 80px 20px;
}

.calculator-box {
    background: white;
    padding: 50px 40px;
    border-radius: 12px;
    max-width: 700px;
    margin: 0 auto;
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
    margin-bottom: 40px;
}

.form-label {
    display: block;
    font-weight: 600;
    color: #1F2937;
    margin-bottom: 8px;
    font-size: 0.95rem;
}

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
    line-height: 1;
}

.savings-box {
    background: linear-gradient(135deg, #00C48C 0%, #00A374 100%);
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
    letter-spacing: 0.3px;
    box-shadow: 0 4px 15px rgba(27, 54, 93, 0.3);
}

div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(27, 54, 93, 0.4);
    background: linear-gradient(135deg, #1E3A8A 0%, #1B365D 100%);
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
    .process-title { font-size: 1.8rem; }
    .section-title { font-size: 1.8rem; }
    .floating-cta { bottom: 15px; right: 15px; }
    .floating-btn { width: 56px; height: 56px; font-size: 1.5rem; }
    .floating-main { width: 60px; height: 60px; font-size: 1.7rem; }
    .package-price { font-size: 2.5rem; }
    .packages-grid { grid-template-columns: 1fr; gap: 20px; }
    .package-popular { transform: scale(1); }
}
</style>
""", unsafe_allow_html=True)

# FLOATING ACTION BUTTONS
st.markdown("""
    <div class="floating-cta">
        <a href="tel:+498912345678" class="floating-btn floating-phone" title="Jetzt anrufen">
            📞
        </a>
        <a href="https://wa.me/4917698765432?text=Hallo%20ReturnGuard" 
           target="_blank" class="floating-btn floating-whatsapp" title="WhatsApp">
            💬
        </a>
        <a href="#calculator" class="floating-btn floating-main" title="Jetzt berechnen">
            🧮
        </a>
    </div>
""", unsafe_allow_html=True)

# NAVIGATION
st.markdown('<div class="top-nav">', unsafe_allow_html=True)
st.markdown('<div class="nav-brand">🛡️ ReturnGuard</div>', unsafe_allow_html=True)

nav_cols = st.columns(6)
with nav_cols[0]:
    if st.button("🏠 Home", use_container_width=True): st.session_state.page = 'home'; st.rerun()
with nav_cols[1]:
    if st.button("👥 Über uns", use_container_width=True): st.session_state.page = 'about'; st.rerun()
with nav_cols[2]:
    if st.button("📦 Leistungen", use_container_width=True): st.session_state.page = 'services'; st.rerun()
with nav_cols[3]:
    if st.button("💰 Rechner", use_container_width=True): st.session_state.page = 'calculator'; st.rerun()
with nav_cols[4]:
    if st.button("📞 Kontakt", use_container_width=True): st.session_state.page = 'contact'; st.rerun()
with nav_cols[5]:
    if st.button("⚖️ Rechtliches", use_container_width=True): st.session_state.page = 'legal'; st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# ==================== STARTSEITE ====================
if st.session_state.page == 'home':
    
    # EMOTIONALER HERO
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
                    <div class="stat-number">500+</div>
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
            <div class="testimonial-preview">
                "ReturnGuard hat mir über 3.000€ gespart. Absolut empfehlenswert!"
            </div>
            <div class="stars">⭐⭐⭐⭐⭐</div>
        </div>
    ''', unsafe_allow_html=True)
    
    # 3-SCHRITTE PROZESS
    st.markdown('<div class="process-section"><div class="process-container">', unsafe_allow_html=True)
    st.markdown('<h2 class="process-title">So einfach funktioniert\'s</h2>', unsafe_allow_html=True)
    st.markdown('<p class="process-subtitle">In nur 3 Schritten zu Ihrer fairen Leasingrückgabe</p>', unsafe_allow_html=True)
    
    step1, step2, step3 = st.columns(3)
    
    with step1:
        st.markdown('''
            <div class="process-step">
                <div class="step-number">1</div>
                <div class="step-icon">📋</div>
                <h3 class="step-title">Daten eingeben</h3>
                <p class="step-description">
                    Geben Sie die wichtigsten Infos zu Ihrem Fahrzeug ein. 
                    Dauert weniger als 2 Minuten.
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
                    Unsere Experten prüfen Ihr Fahrzeug und erstellen 
                    eine detaillierte Bewertung.
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
                    Wir verhandeln für Sie mit der Leasinggesellschaft 
                    und sorgen für faire Bedingungen.
                </p>
            </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    # URGENCY BANNER
    st.markdown('''
        <div class="urgency-banner">
            ⏰ Nur noch 3 Beratungstermine diese Woche verfügbar!
        </div>
    ''', unsafe_allow_html=True)
    
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
    st.markdown('''
        <div class="packages-section">
            <div class="section-header">
                <h2 class="section-title">Unsere Pakete</h2>
                <p class="section-subtitle">Wählen Sie den Service, der zu Ihnen passt</p>
            </div>
        </div>
    ''', unsafe_allow_html=True)
    
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
            <div class="package-card package-popular">
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

# ==================== ANDERE SEITEN ====================
elif st.session_state.page == 'calculator':
    # GUTACHTERTABELLE - Basierend auf typischen Leasingrücknahmegutachten
    damage_costs = {
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

    damage_levels = [
        '0 - Keine Beschädigung',
        '1 - Leichte Kratzer/Gebrauchsspuren',
        '2 - Mittlere Kratzer/Dellen',
        '3 - Starke Beschädigungen',
        '4 - Sehr starke Beschädigungen/Austausch'
    ]

    st.markdown('<div class="calculator-section">', unsafe_allow_html=True)
    st.markdown('''
        <div class="calculator-box" style="max-width: 900px;">
            <h1 class="calculator-title">🔧 Schadensrechner</h1>
            <p class="calculator-subtitle">
                Bewerten Sie die Beschädigungen an Ihrem Fahrzeug basierend auf einem Leasingrücknahmegutachten
            </p>
        </div>
    ''', unsafe_allow_html=True)

    st.markdown("---")

    # Initialisiere Session State für Beschädigungen
    if 'damages' not in st.session_state:
        st.session_state.damages = {part: 0 for part in damage_costs.keys()}

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
                help=f"0 = Keine Schäden | 4 = Sehr starke Schäden",
                key=f"slider_{part}"
            )
            st.session_state.damages[part] = current_value
            st.caption(f"Stufe {current_value}: {damage_levels[current_value].split(' - ')[1]}")

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
            help="Allgemeiner Lackzustand des Fahrzeugs",
            key="slider_Lackierung gesamt"
        )
        st.session_state.damages['Lackierung gesamt'] = lackierung_value
        st.caption(f"Stufe {lackierung_value}: {damage_levels[lackierung_value].split(' - ')[1]}")

        windschutz_value = st.slider(
            "**Windschutzscheibe**",
            min_value=0,
            max_value=4,
            value=st.session_state.damages.get('Windschutzscheibe', 0),
            format="%d",
            help="Steinschläge, Risse, etc.",
            key="slider_Windschutzscheibe"
        )
        st.session_state.damages['Windschutzscheibe'] = windschutz_value
        st.caption(f"Stufe {windschutz_value}: {damage_levels[windschutz_value].split(' - ')[1]}")

    with col4:
        felgen_value = st.slider(
            "**Felgen (Satz)**",
            min_value=0,
            max_value=4,
            value=st.session_state.damages.get('Felgen (Satz)', 0),
            format="%d",
            help="Bordsteinschäden, Kratzer an allen Felgen",
            key="slider_Felgen (Satz)"
        )
        st.session_state.damages['Felgen (Satz)'] = felgen_value
        st.caption(f"Stufe {felgen_value}: {damage_levels[felgen_value].split(' - ')[1]}")

        seiten_value = st.slider(
            "**Seitenscheiben**",
            min_value=0,
            max_value=4,
            value=st.session_state.damages.get('Seitenscheiben', 0),
            format="%d",
            help="Alle Seitenscheiben",
            key="slider_Seitenscheiben"
        )
        st.session_state.damages['Seitenscheiben'] = seiten_value
        st.caption(f"Stufe {seiten_value}: {damage_levels[seiten_value].split(' - ')[1]}")

    st.markdown("---")
    st.markdown("### 🪑 Innenraum")

    col5, col6 = st.columns(2)

    interior_parts = ['Sitze', 'Armaturenbrett', 'Teppich/Fußmatten']

    with col5:
        sitze_value = st.slider(
            "**Sitze**",
            min_value=0,
            max_value=4,
            value=st.session_state.damages.get('Sitze', 0),
            format="%d",
            help="Flecken, Risse, Abnutzung",
            key="slider_Sitze"
        )
        st.session_state.damages['Sitze'] = sitze_value
        st.caption(f"Stufe {sitze_value}: {damage_levels[sitze_value].split(' - ')[1]}")

        armatur_value = st.slider(
            "**Armaturenbrett**",
            min_value=0,
            max_value=4,
            value=st.session_state.damages.get('Armaturenbrett', 0),
            format="%d",
            help="Kratzer, Risse im Kunststoff",
            key="slider_Armaturenbrett"
        )
        st.session_state.damages['Armaturenbrett'] = armatur_value
        st.caption(f"Stufe {armatur_value}: {damage_levels[armatur_value].split(' - ')[1]}")

    with col6:
        teppich_value = st.slider(
            "**Teppich/Fußmatten**",
            min_value=0,
            max_value=4,
            value=st.session_state.damages.get('Teppich/Fußmatten', 0),
            format="%d",
            help="Flecken, Abnutzung, Gerüche",
            key="slider_Teppich/Fußmatten"
        )
        st.session_state.damages['Teppich/Fußmatten'] = teppich_value
        st.caption(f"Stufe {teppich_value}: {damage_levels[teppich_value].split(' - ')[1]}")

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

        if total_cost > 0:
            st.markdown(f'''
                <div class="result-box">
                    <div class="result-label">Geschätzte Gesamtkosten der Beschädigungen</div>
                    <div class="result-amount">{total_cost:,.0f} €</div>
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

            # Ersparnis mit ReturnGuard
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
            st.markdown("### 📞 Nächste Schritte")

            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.markdown("""
                <div style="text-align: center; padding: 20px; background: white; border-radius: 8px; border: 2px solid #E5E7EB;">
                    <div style="font-size: 2.5rem; margin-bottom: 10px;">📞</div>
                    <strong>Kostenlose Beratung</strong>
                    <div style="margin-top: 10px; color: #1B365D; font-weight: 600;">+49 89 123 456 78</div>
                </div>
                """, unsafe_allow_html=True)

            with col_b:
                st.markdown("""
                <div style="text-align: center; padding: 20px; background: white; border-radius: 8px; border: 2px solid #E5E7EB;">
                    <div style="font-size: 2.5rem; margin-bottom: 10px;">💬</div>
                    <strong>WhatsApp Kontakt</strong>
                    <div style="margin-top: 10px; color: #25D366; font-weight: 600;">Jetzt chatten</div>
                </div>
                """, unsafe_allow_html=True)

            with col_c:
                st.markdown("""
                <div style="text-align: center; padding: 20px; background: white; border-radius: 8px; border: 2px solid #E5E7EB;">
                    <div style="font-size: 2.5rem; margin-bottom: 10px;">📧</div>
                    <strong>E-Mail Anfrage</strong>
                    <div style="margin-top: 10px; color: #1B365D; font-weight: 600;">info@returnguard.de</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("ℹ️ Bitte bewerten Sie mindestens eine Beschädigung, um eine Schätzung zu erhalten.")

    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == 'about':
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.markdown('<h1 class="section-title">👥 Über ReturnGuard</h1>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">Ihr Partner für faire Leasingrückgaben</p>', unsafe_allow_html=True)
    st.write("""
    ReturnGuard wurde 2008 gegründet mit der Mission, Leasingnehmern zu helfen, 
    unfaire Nachzahlungen zu vermeiden. Unser Team besteht aus erfahrenen Rechtsanwälten 
    im Verkehrsrecht und TÜV-zertifizierten KFZ-Gutachtern.
    
    **Unsere Werte:**
    - Transparenz in allen Prozessen
    - Faire Preise ohne versteckte Kosten
    - Persönliche Betreuung jedes Kunden
    - Höchste Qualitätsstandards
    """)
    st.markdown('</div>', unsafe_allow_html=True)

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

# FOOTER
st.markdown("---")
st.markdown('''
    <div style="text-align: center; color: #5F6B7A; padding: 40px 20px; font-size: 0.95rem;">
        <div style="margin-bottom: 20px;">
            <strong style="color: #1A2332; font-size: 1.1rem;">🛡️ ReturnGuard GmbH</strong>
        </div>
        <div style="margin-bottom: 15px;">
            📞 +49 89 123 456 78 | 💬 +49 176 987 654 32 | 📧 info@returnguard.de
        </div>
        <div>
            © 2024 ReturnGuard - Ihr Partner für faire Leasingrückgaben
        </div>
    </div>
''', unsafe_allow_html=True)
