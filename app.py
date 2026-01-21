import streamlit as st
import re

st.set_page_config(
    page_title="ReturnGuard - Leasingrückgabe ohne Überraschungen",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif; }
    .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    
    .hero-section {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.95) 0%, rgba(118, 75, 162, 0.95) 100%),
                    url('https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?w=1920') center/cover;
        padding: 100px 20px;
        text-align: center;
        border-radius: 0 0 50px 50px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    }
    
    .hero-title {
        font-size: 4.5rem;
        font-weight: 800;
        color: white;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.4);
    }
    
    .hero-subtitle {
        font-size: 1.4rem;
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        margin-top: 20px;
    }
    
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
        box-shadow: 0 10px 30px rgba(255, 107, 53, 0.4);
        text-decoration: none;
        display: inline-block;
    }
    
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
    }
    
    .testimonial-section {
        background: white;
        padding: 60px 40px;
        border-radius: 20px;
        margin: 50px 0;
        box-shadow: 10px 10px 30px #d1d9e6;
    }
    
    .testimonial-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 30px;
        border-radius: 15px;
        margin: 20px 0;
        border-left: 4px solid #667eea;
    }
    
    .testimonial-stars { color: #FFD700; font-size: 1.2rem; }
    .testimonial-text { font-size: 1.1rem; color: #2d3748; font-style: italic; margin: 15px 0; }
    .testimonial-author { font-weight: 700; color: #667eea; }
    
    .faq-section {
        background: white;
        padding: 60px 40px;
        border-radius: 20px;
        margin: 50px 0;
        box-shadow: 10px 10px 30px #d1d9e6;
    }
    
    .faq-item {
        background: #f8f9fa;
        padding: 25px;
        border-radius: 12px;
        margin: 15px 0;
        border-left: 4px solid #667eea;
    }
    
    .faq-question { font-size: 1.2rem; font-weight: 700; color: #2d3748; margin-bottom: 10px; }
    .faq-answer { font-size: 1rem; color: #4a5568; line-height: 1.6; }
    
    .trust-badges { display: flex; justify-content: center; gap: 40px; margin: 40px 0; flex-wrap: wrap; }
    .trust-badge {
        background: white;
        padding: 30px 25px;
        border-radius: 15px;
        box-shadow: 10px 10px 30px #d1d9e6;
        min-width: 200px;
        text-align: center;
    }
    .trust-icon { font-size: 4.5rem; margin-bottom: 15px; }
    .trust-text { font-size: 1.1rem; color: #4a5568; font-weight: 600; }
    
    .features-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 30px; margin: 50px 0; }
    .feature-card {
        background: white;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 10px 10px 30px #d1d9e6;
    }
    .feature-icon-large { font-size: 3.5rem; margin-bottom: 15px; display: block; }
    
    .package-card {
        background: white;
        border-radius: 20px;
        padding: 35px 25px;
        box-shadow: 20px 20px 60px #d1d9e6;
        transition: all 0.3s;
    }
    .package-card:hover { transform: translateY(-10px); }
    .package-popular { border: 3px solid #667eea; }
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
    }
    .package-icon { font-size: 3rem; margin-bottom: 15px; display: block; }
    .package-title { font-size: 1.8rem; font-weight: 700; color: #2d3748; margin-bottom: 15px; }
    .package-price {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 20px 0;
    }
    .package-features { text-align: left; margin: 25px 0; list-style: none; padding: 0; }
    .package-features li {
        padding: 12px 0;
        color: #4a5568;
        border-bottom: 1px solid #e2e8f0;
    }
    .feature-icon { margin-right: 10px; color: #48bb78; font-weight: bold; }
    
    .process-container { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 40px 0; }
    .process-step {
        background: white;
        padding: 30px 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 10px 10px 30px #d1d9e6;
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
    }
    
    .lead-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 50px;
        border-radius: 20px;
        margin: 50px 0;
        text-align: center;
    }
    .lead-section h2 { color: white; font-size: 2.5rem; }
    .lead-section p { color: white; font-size: 1.2rem; }
    
    div.stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 15px 35px;
        border-radius: 50px;
        font-size: 1.1rem;
        font-weight: 700;
        width: 100%;
    }
    input[type="text"] { text-align: center !important; font-size: 1.2rem !important; padding: 20px !important; height: 60px !important; }
    
    @media (max-width: 768px) {
        .hero-title { font-size: 2.5rem; }
        .sticky-cta { bottom: 10px; right: 10px; }
    }
    </style>
""", unsafe_allow_html=True)

# Sticky CTA Button
st.markdown("""
    <div class="sticky-cta">
        <a href="#lead-form" class="sticky-cta-button">🚀 Jetzt Termin sichern</a>
    </div>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">🛡️ Leasingrückgabe für Ihren Audi</h1>
        <p class="hero-subtitle">Schützen Sie sich vor unfairen Nachzahlungen - Professionell, transparent, rechtssicher</p>
    </div>
""", unsafe_allow_html=True)

st.write("")

# Urgency Banner
st.markdown("""
    <div class="urgency-banner">
        ⏰ Nur noch 3 Termine diese Woche verfügbar! Sichern Sie sich jetzt Ihren Platz.
    </div>
""", unsafe_allow_html=True)

# Trust Badges
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

# Features
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

# Pakete
st.markdown("## 🎁 Wählen Sie Ihr perfektes Paket")
pkg_col1, pkg_col2, pkg_col3, pkg_col4 = st.columns(4)

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
            </ul>
        </div>
    """, unsafe_allow_html=True)
    st.button("Jetzt buchen", key="btn_basis", use_container_width=True)

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
            </ul>
        </div>
    """, unsafe_allow_html=True)
    st.button("Jetzt buchen", key="btn_standard", use_container_width=True)

with pkg_col3:
    st.markdown("""
        <div class="package-card package-popular" style="position: relative;">
            <div class="popular-badge">🔥 BELIEBT</div>
            <span class="package-icon">🥇</span>
            <h3 class="package-title">Premium</h3>
            <div class="package-price">299€</div>
            <ul class="package-features">
                <li><span class="feature-icon">✓</span> Vollständige Rechtsprüfung</li>
                <li><span class="feature-icon">✓</span> Anwaltliche Erstberatung (2h)</li>
                <li><span class="feature-icon">✓</span> Verhandlung mit Leasinggeber</li>
                <li><span class="feature-icon">✓</span> 24/7 Hotline-Support</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    st.button("Jetzt buchen", key="btn_premium", use_container_width=True)

with pkg_col4:
    st.markdown("""
        <div class="package-card">
            <span class="package-icon">💎</span>
            <h3 class="package-title">VIP All-Inclusive</h3>
            <div class="package-price">999€</div>
            <ul class="package-features">
                <li><span class="feature-icon">✓</span> Persönlicher Ansprechpartner</li>
                <li><span class="feature-icon">✓</span> Vollständige Rückgabe-Begleitung</li>
                <li><span class="feature-icon">✓</span> Umfassende Rechtsvertretung</li>
                <li><span class="feature-icon">✓</span> Vor-Ort Begleitung Rückgabe</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    st.button("Jetzt buchen", key="btn_vip", use_container_width=True)

st.write("")
st.write("")

# TESTIMONIALS (NEU!)
st.markdown("## 💬 Das sagen unsere Kunden")
st.write("")

test_col1, test_col2, test_col3 = st.columns(3)

with test_col1:
    st.markdown("""
        <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 30px; border-radius: 15px; border-left: 4px solid #667eea; height: 100%;">
            <div style="color: #FFD700; font-size: 1.2rem; margin-bottom: 10px;">⭐⭐⭐⭐⭐</div>
            <p style="font-size: 1.1rem; color: #2d3748; font-style: italic; margin: 15px 0; line-height: 1.6;">"ReturnGuard hat mir über 2.500€ an Nachzahlungen erspart! Die Gutachter waren extrem professionell und haben jeden Schaden genau dokumentiert. Absolute Empfehlung!"</p>
            <p style="font-weight: 700; color: #667eea; font-size: 1rem;">— Michael S., Audi A4 Leasing</p>
        </div>
    """, unsafe_allow_html=True)

with test_col2:
    st.markdown("""
        <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 30px; border-radius: 15px; border-left: 4px solid #667eea; height: 100%;">
            <div style="color: #FFD700; font-size: 1.2rem; margin-bottom: 10px;">⭐⭐⭐⭐⭐</div>
            <p style="font-size: 1.1rem; color: #2d3748; font-style: italic; margin: 15px 0; line-height: 1.6;">"Ich war skeptisch, aber der Service ist sein Geld absolut wert. Die anwaltliche Beratung hat bei der Verhandlung mit dem Leasinggeber den entscheidenden Unterschied gemacht."</p>
            <p style="font-weight: 700; color: #667eea; font-size: 1rem;">— Sandra K., Audi Q5 Leasing</p>
        </div>
    """, unsafe_allow_html=True)

with test_col3:
    st.markdown("""
        <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 30px; border-radius: 15px; border-left: 4px solid #667eea; height: 100%;">
            <div style="color: #FFD700; font-size: 1.2rem; margin-bottom: 10px;">⭐⭐⭐⭐⭐</div>
            <p style="font-size: 1.1rem; color: #2d3748; font-style: italic; margin: 15px 0; line-height: 1.6;">"Schnell, unkompliziert und transparent. Das Premium-Paket war jeden Cent wert. Die Experten wussten genau, worauf es ankommt."</p>
            <p style="font-weight: 700; color: #667eea; font-size: 1rem;">— Thomas B., Audi A6 Leasing</p>
        </div>
    """, unsafe_allow_html=True)

st.write("")
st.write("")

# Prozess
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

# FAQ (NEU!)
st.write("")
st.write("")
st.markdown("## ❓ Häufig gestellte Fragen")
st.write("")

with st.expander("❓ Wann sollte ich einen Check durchführen lassen?"):
    st.write("Idealerweise 3-6 Monate vor der Rückgabe. So haben Sie genügend Zeit, eventuelle Schäden noch kostengünstig zu beheben.")

with st.expander("❓ Wie lange dauert der Check?"):
    st.write("Ein Basis-Check dauert ca. 1 Stunde, ein Premium-Check mit vollständiger Dokumentation 2-3 Stunden vor Ort.")

with st.expander("❓ Was passiert nach dem Check?"):
    st.write("Sie erhalten innerhalb von 48 Stunden einen detaillierten digitalen Bericht mit Handlungsempfehlungen und Kosteneinschätzung.")

with st.expander("❓ Sind die Gutachter wirklich unabhängig?"):
    st.write("Ja, alle unsere Gutachter sind TÜV-zertifiziert und arbeiten vollkommen unabhängig von Leasinggebern und Herstellern.")

with st.expander("❓ Was ist, wenn ich mit dem Ergebnis nicht zufrieden bin?"):
    st.write("Bei unserem VIP-Paket bieten wir eine Geld-zurück-Garantie. Wenn wir Ihnen nicht mindestens den doppelten Paketpreis einsparen, erhalten Sie Ihr Geld zurück.")

st.write("")
st.write("")

# Lead-Form
st.markdown('<div id="lead-form"></div>', unsafe_allow_html=True)
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
        label_visibility="collapsed",
        key="email_main"
    )
    
    if st.button("🚀 Jetzt kostenlose Beratung anfordern", use_container_width=True, key="main_cta"):
        if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email_input):
            st.success("✅ Vielen Dank! Wir kontaktieren Sie innerhalb von 24 Stunden.")
            st.balloons()
        else:
            st.error("❌ Bitte geben Sie eine gültige E-Mail-Adresse ein.")

st.write("")
st.write("")

# Footer
st.markdown("""
    <div style="text-align: center; padding: 40px 20px; color: #718096;">
        <p style="font-size: 0.9rem;">🛡️ ReturnGuard - Ihr Partner für faire Leasingrückgaben</p>
        <p style="font-size: 0.8rem; margin-top: 10px;">
            Datenschutz | AGB | Impressum | Kontakt
        </p>
    </div>
""", unsafe_allow_html=True)
