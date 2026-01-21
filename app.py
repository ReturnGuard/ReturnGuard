import streamlit as st
import re

# --- KONFIGURATION ---
st.set_page_config(
    page_title="ReturnGuard - Leasingrückgabe ohne Überraschungen",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- MODERNES CSS MIT QUICK WINS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Hero Section mit Audi-Bild */
    .hero-section {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.95) 0%, rgba(118, 75, 162, 0.95) 100%),
                    url('https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?w=1920&h=600&fit=crop') center/cover;
        padding: 100px 20px;
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
        font-size: 4.5rem;
        font-weight: 800;
        color: white;
        margin-bottom: 20px;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.4);
        position: relative;
        z-index: 1;
    }
    
    .hero-subtitle {
        font-size: 1.4rem;
        color: rgba(255,255,255,0.95);
        margin-bottom: 30px;
        position: relative;
        z-index: 1;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* Sticky CTA Button */
    .sticky-cta {
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 1000;
        animation: bounce 2s infinite;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    .sticky-cta-button {
        background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%);
        color: white;
        padding: 18px 35px;
        border-radius: 50px;
        font-size: 1.2rem;
        font-weight: 700;
        border: none;
        cursor: pointer;
        box-shadow: 0 10px 30px rgba(255, 107, 53, 0.4);
        transition: all 0.3s ease;
        text-decoration: none;
        display: inline-block;
    }
    
    .sticky-cta-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 40px rgba(255, 107, 53, 0.6);
    }
    
    /* Container */
    .block-container {
        max-width: 1400px !important;
        padding-top: 2rem !important;
    }
    
    /* Testimonial Section */
    .testimonial-section {
        background: white;
        padding: 60px 40px;
        border-radius: 20px;
        margin: 50px 0;
        box-shadow: 10px 10px 30px #d1d9e6, -10px -10px 30px #ffffff;
    }
    
    .testimonial-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 30px;
        border-radius: 15px;
        margin: 20px 0;
        border-left: 4px solid #667eea;
        transition: transform 0.3s ease;
    }
    
    .testimonial-card:hover {
        transform: translateX(5px);
    }
    
    .testimonial-text {
        font-size: 1.1rem;
        color: #2d3748;
        font-style: italic;
        margin-bottom: 15px;
        line-height: 1.6;
    }
    
    .testimonial-author {
        font-weight: 700;
        color: #667eea;
        font-size: 1rem;
    }
    
    .testimonial-stars {
        color: #FFD700;
        font-size: 1.2rem;
        margin-bottom: 10px;
    }
    
    /* FAQ Section */
    .faq-section {
        background: white;
        padding: 60px 40px;
        border-radius: 20px;
        margin: 50px 0;
        box-shadow: 10px 10px 30px #d1d9e6, -10px -10px 30px #ffffff;
    }
    
    .faq-item {
        background: #f8f9fa;
        padding: 25px;
        border-radius: 12px;
        margin: 15px 0;
        border-left: 4px solid #667eea;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .faq-item:hover {
        background: #e9ecef;
        transform: translateX(5px);
    }
    
    .faq-question {
        font-size: 1.2rem;
        font-weight: 700;
        color: #2d3748;
        margin-bottom: 10px;
    }
    
    .faq-answer {
        font-size: 1rem;
        color: #4a5568;
        line-height: 1.6;
    }
    
    /* Urgency Banner */
    .urgency-banner {
        background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%);
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        color: white;
        font-size: 1.2rem;
        font-weight: 700;
        margin: 30px 0;
        box-shadow: 0 10px 30px rgba(255, 107, 53, 0.3);
        animation: pulse-subtle 2s infinite;
    }
    
    @keyframes pulse-subtle {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    .urgency-icon {
        font-size: 1.5rem;
        margin-right: 10px;
    }
    
    /* Paket-Vergleich Container */
    .package-comparison {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 25px;
        margin: 40px 0;
        padding: 20px;
    }
    
    /* Moderne Paket-Karten */
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
        background: white;
        padding: 30px 25px;
        border-radius: 15px;
        box-shadow: 10px 10px 30px #d1d9e6, -10px -10px 30px #ffffff;
        transition: transform 0.3s ease;
        min-width: 200px;
    }
    
    .trust-badge:hover {
        transform: translateY(-5px);
    }
    
    .trust-icon {
        font-size: 4.5rem;
        margin-bottom: 15px;
    }
    
    .trust-text {
        font-size: 1.1rem;
        color: #4a5568;
        font-weight: 600;
        line-height: 1.4;
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
    
    /* Email Input Styling */
    input[type="text"] {
        text-align: center !important;
        font-size: 1.2rem !important;
        padding: 20px !important;
        height: 60px !important;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem;
        }
        .hero-subtitle {
            font-size: 1.1rem;
        }
        .sticky-cta {
            bottom: 10px;
            right: 10px;
        }
        .sticky-cta-button {
            padding: 15px 25px;
            font-size: 1rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Session State initialisieren
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Kunde"

# --- STICKY CTA BUTTON ---
st.markdown("""
    <div class="sticky-cta">
        <a href="#lead-form" class="sticky-cta-button">
            🚀 Jetzt Termin sichern
        </a>
    </div>
""", unsafe_allow_html=True)

# --- HERO SECTION MIT AUDI-BILD ---
st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">🛡️ Leasingrückgabe für Ihren Audi</h1>
        <p class="hero-subtitle">Schützen Sie sich vor unfairen Nachzahlungen - Professionell, transparent, rechtssicher</p>
    </div>
""", unsafe_allow_html=True)

st.write("")

# --- URGENCY BANNER ---
st.markdown("""
    <div class="urgency-banner">
        <span class="urgency-icon">⏰</span>
        Nur noch 3 Termine diese Woche verfügbar! Sichern Sie sich jetzt Ihren Platz.
    </div>
""", unsafe_allow_html=True)

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

# Pakete in Spalten aufteilen
pkg_col1, pkg_col2, pkg_col3, pkg_col4 = st.columns(4)

# BASIS PAKET
with pkg_col1:
    st.markdown("""
        <div class="package-card">
            <span class="package-icon">🥉</span>
            <h3 class="package-title">Basis</h3>
            <div class="package-price">99€</div>
            <ul class="package-features">
                <li><span class="feature-icon">✓</span> Grundcheck Fahrzeugzustand</li>
                <li><span class="feature-icon">✓</span> Fotodokumentation (20 Bilder)</li>
                <li><span class="feature-icon">✓</span> Digitaler Bericht (PDF)</li>
                <li><span class="feature-icon">✓</span> Email-Support (48h)</li>
                <li><span class="feature-icon">✓</span> Checkliste Rückgabe</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    st.button("Jetzt buchen", key="btn_basis", use_container_width=True)

# STANDARD PAKET
with pkg_col2:
    st.markdown("""
        <div class="package-card">
            <span class="package-icon">🥈</span>
            <h3 class="package-title">Standard</h3>
            <div class="package-price">199€</div>
            <ul class="package-features">
                <li><span class="feature-icon">✓</span> Umfassende Schadensbewertung</li>
                <li><span class="feature-icon">✓</span> Fotodokumentation (50 Bilder)</li>
                <li><span class="feature-icon">✓</span> Detaillierter Gutachter-Bericht</li>
                <li><span class="feature-icon">✓</span> Telefonische Beratung (1h)</li>
                <li><span class="feature-icon">✓</span> Kosteneinschätzung</li>
                <li><span class="feature-icon">✓</span> Optimierungs-Tipps</li>
                <li><span class="feature-icon">✓</span> Priority Email-Support (24h)</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    st.button("Jetzt buchen", key="btn_standard", use_container_width=True)

# PREMIUM PAKET (BELIEBT)
with pkg_col3:
    st.markdown("""
        <div class="package-card package-popular">
            <div class="popular-badge">🔥 BELIEBT</div>
            <span class="package-icon">🥇</span>
            <h3 class="package-title">Premium</h3>
            <div class="package-price">299€</div>
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
        </div>
    """, unsafe_allow_html=True)
    st.button("Jetzt buchen", key="btn_premium", use_container_width=True)

# VIP PAKET
with pkg_col4:
    st.markdown("""
        <div class="package-card">
            <span class="package-icon">💎</span>
            <h3 class="package-title">VIP All-Inclusive</h3>
            <div class="package-price">999€</div>
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
        </div>
    """, unsafe_allow_html=True)
    st.button("Jetzt buchen", key="btn_vip", use_container_width=True)

st.write("")

# Paket-Vergleichstabelle
st.markdown("""
    <div style="background: white; padding: 40px; border-radius: 20px; margin-top: 40px; box-shadow: 10px 10px 30px #d1d9e6, -10px -10px 30px #ffffff;">
        <h3 style="text-align: center; color: #2d3748; margin-bottom: 30px; font-size: 2rem;">📊 Paket-Vergleich auf einen Blick</h3>
        <table style="width: 100%; border-collapse: collapse;">
            <thead>
                <tr style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
                    <th style="padding: 15px; text-align: left; border-radius: 10px 0 0 0;">Leistung</th>
                    <th style="padding: 15px; text-align: center;">Basis</th>
                    <th style="padding: 15px; text-align: center;">Standard</th>
                    <th style="padding: 15px; text-align: center;">Premium</th>
                    <th style="padding: 15px; text-align: center; border-radius: 0 10px 0 0;">VIP</th>
                </tr>
            </thead>
            <tbody>
                <tr style="background: #f8f9fa;">
                    <td style="padding: 15px; font-weight: 600;">Fahrzeugcheck</td>
                    <td style="padding: 15px; text-align: center;">Basis</td>
                    <td style="padding: 15px; text-align: center;">Umfassend</td>
                    <td style="padding: 15px; text-align: center;">Komplett</td>
                    <td style="padding: 15px; text-align: center;">Premium</td>
                </tr>
                <tr>
                    <td style="padding: 15px; font-weight: 600;">Fotos</td>
                    <td style="padding: 15px; text-align: center;">20</td>
                    <td style="padding: 15px; text-align: center;">50</td>
                    <td style="padding: 15px; text-align: center;">100+</td>
                    <td style="padding: 15px; text-align: center;">Unbegrenzt</td>
                </tr>
                <tr style="background: #f8f9fa;">
                    <td style="padding: 15px; font-weight: 600;">Rechtliche Beratung</td>
                    <td style="padding: 15px; text-align: center;">❌</td>
                    <td style="padding: 15px; text-align: center;">Telefon 1h</td>
                    <td style="padding: 15px; text-align: center;">Anwalt 2h</td>
                    <td style="padding: 15px; text-align: center;">Vollständig</td>
                </tr>
                <tr>
                    <td style="padding: 15px; font-weight: 600;">Verhandlung mit Leasinggeber</td>
                    <td style="padding: 15px; text-align: center;">❌</td>
                    <td style="padding: 15px; text-align: center;">❌</td>
                    <td style="padding: 15px; text-align: center;">✅</td>
                    <td style="padding: 15px; text-align: center;">✅ Premium</td>
                </tr>
                <tr style="background: #f8f9fa;">
                    <td style="padding: 15px; font-weight: 600;">Support-Zeit</td>
                    <td style="padding: 15px; text-align: center;">48h</td>
                    <td style="padding: 15px; text-align: center
