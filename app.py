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

/* OPTIMIERTE BANKING OPTIK */
.stApp { 
    background: #FAFBFC;
}

/* EMOTIONALER HERO - OHNE FORMULAR */
.hero-section {
    background: linear-gradient(135deg, rgba(30, 60, 114, 0.95) 0%, rgba(46, 91, 255, 0.85) 100%),
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
    background: #FF6B35;
    color: white;
    padding: 18px 50px;
    border-radius: 8px;
    font-size: 1.2rem;
    font-weight: 600;
    text-decoration: none;
    box-shadow: 0 8px 25px rgba(255, 107, 53, 0.4);
    transition: all 0.3s ease;
    animation: fadeInUp 0.8s ease-out 0.4s backwards;
    border: 2px solid transparent;
}

.hero-cta:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 35px rgba(255, 107, 53, 0.5);
    background: #FF8555;
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
    border-top: 3px solid #FF6B35;
    border-bottom: 1px solid #E8EBED;
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
    color: #2E5BFF;
    line-height: 1;
    margin-bottom: 8px;
}

.stat-label {
    font-size: 0.95rem;
    color: #5F6B7A;
    font-weight: 500;
}

.testimonial-preview {
    margin-top: 25px;
    font-size: 1.05rem;
    color: #1A2332;
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
    color: #1A2332;
    margin-bottom: 15px;
}

.process-subtitle {
    text-align: center;
    font-size: 1.2rem;
    color: #5F6B7A;
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
    background: #FAFBFC;
    border-radius: 12px;
    border: 2px solid #E8EBED;
    transition: all 0.3s ease;
    position: relative;
    flex: 1;
}

.process-step:hover {
    transform: translateY(-8px);
    box-shadow: 0 12px 30px rgba(46, 91, 255, 0.15);
    border-color: #2E5BFF;
}

.step-number {
    width: 70px;
    height: 70px;
    background: linear-gradient(135deg, #2E5BFF 0%, #0040DD 100%);
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
    font-weight: 700;
    margin: 0 auto 25px auto;
    box-shadow: 0 8px 20px rgba(46, 91, 255, 0.3);
}

.step-icon {
    font-size: 3.5rem;
    margin-bottom: 20px;
}

.step-title {
    font-size: 1.5rem;
    font-weight: 600;
    color: #1A2332;
    margin-bottom: 15px;
}

.step-description {
    font-size: 1rem;
    color: #5F6B7A;
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
    background: linear-gradient(135deg, #2E5BFF 0%, #0040DD 100%);
}

.floating-whatsapp {
    background: #25D366;
}

.floating-main {
    background: linear-gradient(135deg, #FF6B35 0%, #FF8555 100%);
    width: 70px;
    height: 70px;
    font-size: 2rem;
}

/* URGENCY BANNER */
.urgency-banner {
    background: linear-gradient(135deg, #FF6B35 0%, #FF8555 100%);
    color: white;
    padding: 18px 30px;
    text-align: center;
    font-size: 1.1rem;
    font-weight: 600;
    margin: 40px auto;
    max-width: 800px;
    border-radius: 8px;
    box-shadow: 0 4px 15px rgba(255, 107, 53, 0.3);
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
    box-shadow: 0 2px 10px rgba(26, 35, 50, 0.06);
    border: 2px solid #E8EBED;
    transition: all 0.3s ease;
}

.trust-badge:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(26, 35, 50, 0.12);
    border-color: #2E5BFF;
}

.trust-icon { 
    font-size: 3.5rem; 
    margin-bottom: 18px;
}

.trust-title {
    font-size: 1rem;
    color: #1A2332;
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
    color: #1A2332;
    margin-bottom: 15px;
}

.section-subtitle {
    font-size: 1.2rem;
    color: #5F6B7A;
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
    border: 2px solid #E8EBED;
    transition: all 0.4s ease;
    position: relative;
    text-align: center;
}

.package-card:hover {
    transform: translateY(-10px) scale(1.02);
    box-shadow: 0 15px 40px rgba(26, 35, 50, 0.15);
    border-color: #2E5BFF;
}

.package-popular {
    border: 3px solid #FF6B35;
    background: linear-gradient(180deg, #FFFAF7 0%, white 100%);
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
    background: linear-gradient(135deg, #FF6B35 0%, #FF8555 100%);
    color: white;
    padding: 6px 20px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 1px;
    box-shadow: 0 4px 15px rgba(255, 107, 53, 0.4);
}

.package-icon {
    font-size: 3rem;
    margin-bottom: 20px;
}

.package-title {
    font-size: 1.8rem;
    font-weight: 700;
    color: #1A2332;
    margin-bottom: 8px;
}

.package-subtitle {
    font-size: 0.95rem;
    color: #5F6B7A;
    margin-bottom: 25px;
}

.package-price {
    font-size: 3.5rem;
    font-weight: 300;
    color: #2E5BFF;
    margin: 25px 0;
    line-height: 1;
}

.package-price-unit {
    font-size: 1.2rem;
    color: #5F6B7A;
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
    color: #1A2332;
    border-bottom: 1px solid #F5F7FA;
    font-size: 0.95rem;
    line-height: 1.5;
}

.package-features li:last-child {
    border-bottom: none;
}

/* FORMULAR-SECTION */
.calculator-section {
    background: linear-gradient(135deg, #F5F7FA 0%, #E8EBED 100%);
    padding: 80px 20px;
}

.calculator-box {
    background: white;
    padding: 50px 40px;
    border-radius: 12px;
    max-width: 700px;
    margin: 0 auto;
    box-shadow: 0 10px 40px rgba(26, 35, 50, 0.1);
    border: 2px solid #E8EBED;
}

.calculator-title {
    font-size: 2rem;
    font-weight: 600;
    color: #1A2332;
    text-align: center;
    margin-bottom: 15px;
}

.calculator-subtitle {
    font-size: 1.1rem;
    color: #5F6B7A;
    text-align: center;
    margin-bottom: 40px;
}

.form-label {
    display: block;
    font-weight: 600;
    color: #1A2332;
    margin-bottom: 8px;
    font-size: 0.95rem;
}

.result-box {
    background: linear-gradient(135deg, #2E5BFF 0%, #0040DD 100%);
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
    box-shadow: 0 2px 15px rgba(26, 35, 50, 0.06);
    border: 1px solid #E8EBED;
}

/* BUTTONS */
div.stButton > button {
    background: linear-gradient(135deg, #2E5BFF 0%, #0040DD 100%);
    color: white;
    border: none;
    padding: 16px 35px;
    border-radius: 8px;
    font-weight: 600;
    font-size: 1rem;
    width: 100%;
    transition: all 0.3s ease;
    letter-spacing: 0.3px;
    box-shadow: 0 4px 15px rgba(46, 91, 255, 0.3);
}

div.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(46, 91, 255, 0.4);
    background: linear-gradient(135deg, #0040DD 0%, #2E5BFF 100%);
}

/* NAVIGATION */
.top-nav {
    background: white;
    border-bottom: 1px solid #E8EBED;
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
    color: #1A2332;
    margin-bottom: 15px;
}

div[data-testid="column"] > div.stButton > button {
    background: transparent;
    color: #5F6B7A;
    border: 1px solid #E8EBED;
    box-shadow: none;
    font-weight: 500;
    padding: 12px 20px;
}

div[data-testid="column"] > div.stButton > button:hover {
    background: #F5F7FA;
    color: #1A2332;
    border-color: #2E5BFF;
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
    
    # CALCULATOR SECTION
    st.markdown('<div id="calculator" class="calculator-section">', unsafe_allow_html=True)
    st.markdown('''
        <div class="calculator-box">
            <h2 class="calculator-title">💰 Kostenrechner</h2>
            <p class="calculator-subtitle">Berechnen Sie Ihre voraussichtlichen Rückgabekosten</p>
        </div>
    ''', unsafe_allow_html=True)
    
    calc_col1, calc_col2 = st.columns(2)
    
    with calc_col1:
        st.markdown('<label class="form-label">Fahrzeugmarke</label>', unsafe_allow_html=True)
        brand = st.selectbox("", ["Audi", "BMW", "Mercedes", "VW", "Andere"], label_visibility="collapsed", key="brand")
    
    with calc_col2:
        st.markdown('<label class="form-label">Modell</label>', unsafe_allow_html=True)
        model = st.selectbox("", ["A3", "A4", "A6", "Q3", "Q5", "Q7"], label_visibility="collapsed", key="model")
    
    calc_col3, calc_col4 = st.columns(2)
    
    with calc_col3:
        st.markdown('<label class="form-label">Laufleistung (km)</label>', unsafe_allow_html=True)
        mileage = st.number_input("", min_value=0, max_value=200000, value=50000, step=1000, label_visibility="collapsed", key="mileage")
    
    with calc_col4:
        st.markdown('<label class="form-label">Leasingdauer (Monate)</label>', unsafe_allow_html=True)
        duration = st.number_input("", min_value=12, max_value=60, value=36, step=6, label_visibility="collapsed", key="duration")
    
    if st.button("Jetzt kostenlos berechnen", key="calc", use_container_width=True):
        estimated_cost = 1500 + (mileage / 1000) * 0.5
        savings = estimated_cost * 0.65
        
        st.markdown(f'''
            <div class="result-box">
                <div class="result-label">Geschätzte Rückgabekosten</div>
                <div class="result-amount">{estimated_cost:,.0f} €</div>
            </div>
            
            <div class="savings-box">
                <div class="result-label">Mögliche Ersparnis mit ReturnGuard</div>
                <div class="result-amount" style="font-size: 3rem;">bis zu {savings:,.0f} €</div>
            </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==================== ANDERE SEITEN ====================
elif st.session_state.page == 'calculator':
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.markdown('<h1 class="section-title">💰 Kostenrechner</h1>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">Detaillierte Kostenberechnung für Ihre Leasingrückgabe</p>', unsafe_allow_html=True)
    st.write("Vollständiger Rechner hier...")
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
