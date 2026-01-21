import streamlit as st
import re

# --- KONFIGURATION ---
st.set_page_config(
    page_title="ReturnGuard - Leasingrückgabe ohne Überraschungen",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- MODERNES CSS MIT AKTUELLEN TRENDS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Hero Section mit Glassmorphism */
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 80px 20px;
        text-align: center;
        position: relative;
        overflow: hidden;
        border-radius: 0 0 50px 50px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: pulse 15s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        color: white;
        margin-bottom: 20px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        position: relative;
        z-index: 1;
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        color: rgba(255,255,255,0.95);
        margin-bottom: 30px;
        position: relative;
        z-index: 1;
    }
    
    /* Container */
    .block-container {
        max-width: 1400px !important;
        padding-top: 2rem !important;
    }
    
    /* Paket-Vergleich Container */
    .package-comparison {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 25px;
        margin: 40px 0;
        padding: 20px;
    }
    
    /* Moderne Paket-Karten mit Neumorphism & Hover-Effekten */
    .package-card {
        background: white;
        border-radius: 20px;
        padding: 35px 25px;
        box-shadow: 20px 20px 60px #d1d9e6, -20px -20px 60px #ffffff;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.5);
    }
    
    .package-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.5s;
    }
    
    .package-card:hover::before {
        left: 100%;
    }
    
    .package-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 30px 30px 80px #b8bfcc, -30px -30px 80px #ffffff;
    }
    
    .package-popular {
        border: 3px solid #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1), 20px 20px 60px #d1d9e6;
    }
    
    .popular-badge {
        position: absolute;
        top: -10px;
        right: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 5px 20px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 700;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    .package-icon {
        font-size: 3rem;
        margin-bottom: 15px;
        display: block;
    }
    
    .package-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #2d3748;
        margin-bottom: 15px;
    }
    
    .package-price {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 20px 0;
    }
    
    .package-price-period {
        font-size: 1rem;
        color: #718096;
        font-weight: 400;
    }
    
    .package-features {
        text-align: left;
        margin: 25px 0;
        list-style: none;
        padding: 0;
    }
    
    .package-features li {
        padding: 12px 0;
        color: #4a5568;
        font-size: 0.95rem;
        border-bottom: 1px solid #e2e8f0;
        display: flex;
        align-items: center;
    }
    
    .package-features li:last-child {
        border-bottom: none;
    }
    
    .feature-icon {
        margin-right: 10px;
        color: #48bb78;
        font-weight: bold;
    }
    
    /* CTA Button mit Micro-Interaktionen */
    .cta-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 15px 35px;
        border-radius: 50px;
        font-size: 1.1rem;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .cta-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);
    }
    
    .cta-button:active {
        transform: translateY(0);
    }
    
    /* Features Section */
    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 30px;
        margin: 50px 0;
    }
    
    .feature-card {
        background: white;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 10px 10px 30px #d1d9e6, -10px -10px 30px #ffffff;
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
    }
    
    .feature-icon-large {
        font-size: 3.5rem;
        margin-bottom: 15px;
        display: block;
    }
    
    /* Prozess-Schritte */
    .process-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
        margin: 40px 0;
    }
    
    .process-step {
        background: white;
        padding: 30px 20px;
        border-radius: 15px;
        text-align: center;
        position: relative;
        box-shadow: 10px 10px 30px #d1d9e6, -10px -10px 30px #ffffff;
    }
    
    .process-number {
        width: 50px;
        height: 50px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        font-weight: 700;
        margin: 0 auto 15px;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Lead-Formular */
    .lead-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 50px;
        border-radius: 20px;
        margin: 50px 0;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
        text-align: center;
    }
    
    .lead-section h2 {
        color: white;
        font-size: 2.5rem;
        margin-bottom: 15px;
    }
    
    .lead-section p {
        color: rgba(255,255,255,0.9);
        font-size: 1.2rem;
        margin-bottom: 30px;
    }
    
    /* Trust Badges */
    .trust-badges {
        display: flex;
        justify-content: center;
        gap: 40px;
        margin: 40px 0;
        flex-wrap: wrap;
    }
    
    .trust-badge {
        text-align: center;
    }
    
    .trust-icon {
        font-size: 3rem;
        color: #667eea;
        margin-bottom: 10px;
    }
    
    .trust-text {
        font-size: 0.9rem;
        color: #4a5568;
        font-weight: 600;
    }
    
    /* Streamlit Button Override */
    div.stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 15px 35px;
        border-radius: 50px;
        font-size: 1.1rem;
        font-weight: 700;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
    }
    
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2rem;
        }
        .hero-subtitle {
            font-size: 1rem;
        }
        .package-comparison {
            grid-template-columns: 1fr;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Session State initialisieren
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Kunde"

# --- HERO SECTION ---
st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">🛡️ Leasingrückgabe für Ihren Audi</h1>
        <p class="hero-subtitle">Schützen Sie sich vor unfairen Nachzahlungen - Professionell, transparent, rechtssicher</p>
    </div>
""", unsafe_allow_html=True)

st.write("")
st.write("")

# --- TRUST BADGES ---
st.markdown("""
    <div class="trust-badges">
        <div class="trust-badge">
            <div class="trust-icon">⚖️</div>
            <div class="trust-text">Rechtsanwälte<br/>Verkehrsrecht</div>
        </div>
        <div class="trust-badge">
            <div class="trust-icon">🔍</div>
            <div class="trust-text">Unabhängige<br/>KFZ-Gutachter</div>
        </div>
        <div class="trust-badge">
            <div class="trust-icon">💰</div>
            <div class="trust-text">Bis zu 60%<br/>Ersparnis</div>
        </div>
        <div class="trust-badge">
            <div class="trust-icon">⭐</div>
            <div class="trust-text">500+ zufriedene<br/>Kunden</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- FEATURES SECTION ---
st.markdown("## ✨ Warum ReturnGuard?")
st.markdown("""
    <div class="features-grid">
        <div class="feature-card">
            <span class="feature-icon-large">📋</span>
            <h3>Detaillierte Dokumentation</h3>
            <p>Professionelle Schadensdokumentation mit Fotos und Beschreibungen</p>
        </div>
        <div class="feature-card">
            <span class="feature-icon-large">🎯</span>
            <h3>Präzise Bewertung</h3>
            <p>Bewertung nach offiziellen Audi-Standards durch zertifizierte Gutachter</p>
        </div>
        <div class="feature-card">
            <span class="feature-icon-large">⚖️</span>
            <h3>Rechtssicherheit</h3>
            <p>Juristische Begleitung durch spezialisierte Verkehrsrechtsanwälte</p>
        </div>
        <div class="feature-card">
            <span class="feature-icon-large">💡</span>
            <h3>Optimierungs-Tipps</h3>
            <p>Konkrete Handlungsempfehlungen zur Kostenreduzierung</p>
        </div>
    </div>
""", unsafe_allow_html=True)

st.write("")
st.write("")

# --- PAKET-VERGLEICH ---
st.markdown("## 🎁 Wählen Sie Ihr perfektes Paket")
st.markdown('<p style="text-align: center; font-size: 1.1rem; color: #4a5568; margin-bottom: 40px;">Transparente Preise - Keine versteckten Kosten - Volle Kontrolle</p>', unsafe_allow_html=True)

st.markdown("""
    <div class="package-comparison">
        <!-- BASIS PAKET -->
        <div class="package-card">
            <span class="package-icon">🥉</span>
            <h3 class="package-title">Basis</h3>
            <div class="package-price">199€</div>
            <ul class="package-features">
                <li><span class="feature-icon">✓</span> Grundcheck Fahrzeugzustand</li>
                <li><span class="feature-icon">✓</span> Fotodokumentation (20 Bilder)</li>
                <li><span class="feature-icon">✓</span> Digitaler Bericht (PDF)</li>
                <li><span class="feature-icon">✓</span> Email-Support (48h)</li>
                <li><span class="feature-icon">✓</span> Checkliste Rückgabe</li>
            </ul>
            <button class="cta-button">Jetzt buchen</button>
        </div>
        
        <!-- STANDARD PAKET -->
        <div class="package-card">
            <span class="package-icon">🥈</span>
            <h3 class="package-title">Standard</h3>
            <div class="package-price">399€</div>
            <ul class="package-features">
                <li><span class="feature-icon">✓</span> Umfassende Schadensbewertung</li>
                <li><span class="feature-icon">✓</span> Fotodokumentation (50 Bilder)</li>
                <li><span class="feature-icon">✓</span> Detaillierter Gutachter-Bericht</li>
                <li><span class="feature-icon">✓</span> Telefonische Beratung (1h)</li>
                <li><span class="feature-icon">✓</span> Kosteneinschätzung</li>
                <li><span class="feature-icon">✓</span> Optimierungs-Tipps</li>
                <li><span class="feature-icon">✓</span> Priority Email-Support (24h)</li>
            </ul>
            <button class="cta-button">Jetzt buchen</button>
        </div>
        
        <!-- PREMIUM PAKET (BELIEBT) -->
        <div class="package-card package-popular">
            <div class="popular-badge">🔥 BELIEBT</div>
            <span class="package-icon">🥇</span>
            <h3 class="package-title">Premium</h3>
            <div class="package-price">699€</div>
            <ul class="package-features">
                <li><span class="feature-icon">✓</span> Vollständige Rechtsprüfung</li>
                <li><span class="feature-icon">✓</span> Fotodokumentation (100+ Bilder)</li>
                <li><span class="feature-icon">✓</span> Anwaltliche Erstberatung (2h)</li>
                <li><span class="feature-icon">✓</span> Verhandlung mit Leasinggeber</li>
                <li><span class="feature-icon">✓</span> Kostenreduzierungs-Garantie</li>
                <li><span class="feature-icon">✓</span> Detaillierte Handlungsempfehlung</li>
                <li><span class="feature-icon">✓</span> 24/7 Hotline-Support</li>
                <li><span class="feature-icon">✓</span> Schadensbehebungs-Netzwerk</li>
            </ul>
            <button class="cta-button">Jetzt buchen</button>
        </div>
        
        <!-- VIP PAKET -->
        <div class="package-card">
            <span class="package-icon">💎</span>
            <h3 class="package-title">VIP All-Inclusive</h3>
            <div class="package-price">1.299€</div>
            <ul class="package-features">
                <li><span class="feature-icon">✓</span> Persönlicher Ansprechpartner</li>
                <li><span class="feature-icon">✓</span> Vollständige Rückgabe-Begleitung</li>
                <li><span class="feature-icon">✓</span> Unbegrenzte Fotodokumentation</li>
                <li><span class="feature-icon">✓</span> Umfassende Rechtsvertretung</li>
                <li><span class="feature-icon">✓</span> Koordination Schadensbehebung</li>
                <li><span class="feature-icon">✓</span> Verhandlungsführung (komplett)</li>
                <li><span class="feature-icon">✓</span> Geld-zurück-Garantie</li>
                <li><span class="feature-icon">✓</span> Vor-Ort Begleitung Rückgabe</li>
                <li><span class="feature-icon">✓</span> Premium-Hotline 24/7</li>
            </ul>
            <button class="cta-button">Jetzt buchen</button>
        </div>
    </div>
""", unsafe_allow_html=True)

st.write("")
st.write("")

# --- PROZESS ---
st.markdown("## 🚀 So funktioniert's - In 3 einfachen Schritten")
st.markdown("""
    <div class="process-container">
        <div class="process-step">
            <div class="process-number">1</div>
            <h4>Paket wählen & Termin buchen</h4>
            <p>Online in 2 Minuten - Flexibel vor Ort oder per App</p>
        </div>
        <div class="process-step">
            <div class="process-number">2</div>
            <h4>Experten-Analyse</h4>
            <p>Unabhängige Begutachtung nach Audi-Standards</p>
        </div>
        <div class="process-step">
            <div class="process-number">3</div>
            <h4>Digitaler Bericht & Beratung</h4>
            <p>Detailliertes Protokoll mit konkreten Handlungsempfehlungen</p>
        </div>
    </div>
""", unsafe_allow_html=True)

st.write("")
st.write("")

# --- LEAD-GENERIERUNG ---
st.markdown("""
    <div class="lead-section">
        <h2>🎯 Kostenlose Erstberatung sichern</h2>
        <p>Unsere Experten melden sich innerhalb von 24 Stunden bei Ihnen</p>
    </div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    email_input = st.text_input(
        "E-Mail-Adresse",
        placeholder="ihre.email@beispiel.de",
        label_visibility="collapsed"
    )
    
    if st.button("Jetzt kostenlose Beratung anfordern", use_container_width=True):
        if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email_input):
            st.success("✅ Vielen Dank! Wir kontaktieren Sie innerhalb von 24 Stunden.")
            st.balloons()
        else:
            st.error("❌ Bitte geben Sie eine gültige E-Mail-Adresse ein.")

st.write("")
st.write("")

# --- FOOTER ---
st.markdown("""
    <div style="text-align: center; padding: 40px 20px; color: #718096;">
        <p style="font-size: 0.9rem;">🛡️ ReturnGuard - Ihr Partner für faire Leasingrückgaben</p>
        <p style="font-size: 0.8rem; margin-top: 10px;">
            Datenschutz | AGB | Impressum | Kontakt
        </p>
    </div>
""", unsafe_allow_html=True)
