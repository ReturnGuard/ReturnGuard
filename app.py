import streamlit as st
import re

st.set_page_config(page_title="ReturnGuard", layout="wide", initial_sidebar_state="collapsed")

if 'page' not in st.session_state:
    st.session_state.page = 'home'

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif; }

/* PREMIUM NEUTRAL FARBSCHEMA */
.stApp { background: #F8F8F8; }

.hero-section {
    background: linear-gradient(135deg, rgba(54, 69, 79, 0.95) 0%, rgba(44, 44, 44, 0.95) 100%),
                url('https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?w=1920') center/cover;
    padding: 100px 20px; text-align: center; border-radius: 0 0 30px 30px; margin-bottom: 30px;
}
.hero-title { font-size: 4rem; font-weight: 800; color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }

.sticky-contact {
    position: fixed; bottom: 20px; right: 20px; z-index: 1000;
    display: flex; flex-direction: column; gap: 10px;
}
.contact-button {
    width: 60px; height: 60px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.8rem; box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    cursor: pointer; transition: transform 0.3s; text-decoration: none;
}
.contact-button:hover { transform: scale(1.1); }
.whatsapp-btn { background: #25D366; }
.phone-btn { background: #36454F; }

.urgency-banner {
    background: linear-gradient(135deg, #36454F 0%, #2C2C2C 100%);
    padding: 20px; border-radius: 12px; text-align: center;
    color: white; font-size: 1.2rem; font-weight: 700; margin: 30px 0;
    border-left: 4px solid #D4AF37;
}

.trust-badges { display: flex; justify-content: center; gap: 30px; margin: 40px 0; flex-wrap: wrap; }
.trust-badge { 
    background: white; padding: 25px; border-radius: 12px; min-width: 180px; 
    text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    border: 1px solid #E8E8E8;
}
.trust-icon { font-size: 4rem; margin-bottom: 10px; }

.package-card {
    background: white; border-radius: 15px; padding: 30px 20px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.08); transition: transform 0.3s; 
    position: relative; border: 1px solid #E8E8E8;
}
.package-card:hover { transform: translateY(-5px); box-shadow: 0 4px 20px rgba(0,0,0,0.12); }
.package-popular { border: 2px solid #D4AF37; }
.popular-badge {
    position: absolute; top: -10px; right: 20px;
    background: linear-gradient(135deg, #D4AF37 0%, #B8941F 100%);
    color: white; padding: 5px 15px; border-radius: 20px; 
    font-size: 0.75rem; font-weight: 700;
}
.package-icon { font-size: 2.5rem; margin-bottom: 10px; }
.package-title { font-size: 1.5rem; font-weight: 700; color: #2C2C2C; margin: 10px 0; }
.package-price { font-size: 2rem; font-weight: 800; color: #36454F; margin: 15px 0; }
.package-features { text-align: left; list-style: none; padding: 0; margin: 20px 0; }
.package-features li { 
    padding: 8px 0; color: #5A5A5A; border-bottom: 1px solid #F0F0F0;
    font-size: 0.95rem;
}

.content-section { 
    background: white; padding: 50px 40px; border-radius: 15px; 
    margin: 30px 0; box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    border: 1px solid #E8E8E8;
}

.calculator-box { 
    background: white; padding: 40px; border-radius: 15px; 
    box-shadow: 0 2px 15px rgba(0,0,0,0.1); margin: 40px 0;
    border: 1px solid #E8E8E8;
}
.cost-display { 
    background: linear-gradient(135deg, #36454F 0%, #2C2C2C 100%); 
    padding: 30px; border-radius: 12px; text-align: center; 
    color: white; margin: 20px 0;
}
.savings-box { 
    background: linear-gradient(135deg, #27AE60 0%, #229954 100%); 
    padding: 25px; border-radius: 12px; text-align: center; 
    color: white; margin: 20px 0;
}

.team-card { 
    background: #FAFAFA; padding: 25px; border-radius: 12px; 
    text-align: center; margin: 15px 0; border: 1px solid #E8E8E8;
}
.team-avatar { 
    width: 100px; height: 100px; 
    background: linear-gradient(135deg, #36454F 0%, #2C2C2C 100%); 
    border-radius: 50%; margin: 0 auto 15px; display: flex; 
    align-items: center; justify-content: center; font-size: 2.5rem; color: white;
}

div.stButton > button {
    background: linear-gradient(135deg, #36454F 0%, #2C2C2C 100%);
    color: white; border: none; padding: 12px 30px; border-radius: 8px; 
    font-weight: 700; width: 100%; transition: all 0.3s;
}

div.stButton > button:hover {
    background: linear-gradient(135deg, #2C2C2C 0%, #36454F 100%);
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}

@media (max-width: 768px) { 
    .hero-title { font-size: 2rem; }
    .sticky-contact { bottom: 10px; right: 10px; }
    .contact-button { width: 50px; height: 50px; font-size: 1.5rem; }
}
</style>
""", unsafe_allow_html=True)

# STICKY CONTACT BUTTONS
st.markdown("""
    <div class="sticky-contact">
        <a href="https://wa.me/4917698765432?text=Hallo%20ReturnGuard" 
           target="_blank" class="contact-button whatsapp-btn" title="WhatsApp">
            📱
        </a>
        <a href="tel:+498912345678" class="contact-button phone-btn" title="Anrufen">
            📞
        </a>
    </div>
""", unsafe_allow_html=True)

# NAVIGATION
st.markdown("### 🛡️ ReturnGuard | ☎️ +49 89 123 456 78")
nav_cols = st.columns(6)
with nav_cols[0]:
    if st.button("🏠 Home", use_container_width=True): st.session_state.page = 'home'; st.rerun()
with nav_cols[1]:
    if st.button("👥 Über uns", use_container_width=True): st.session_state.page = 'about'; st.rerun()
with nav_cols[2]:
    if st.button("📦 Leistungen", use_container_width=True): st.session_state.page = 'services'; st.rerun()
with nav_cols[3]:
    if st.button("💰 Kostenrechner", use_container_width=True): st.session_state.page = 'calculator'; st.rerun()
with nav_cols[4]:
    if st.button("📞 Kontakt", use_container_width=True): st.session_state.page = 'contact'; st.rerun()
with nav_cols[5]:
    if st.button("⚖️ Rechtliches", use_container_width=True): st.session_state.page = 'legal'; st.rerun()

st.markdown("---")

# STARTSEITE
if st.session_state.page == 'home':
    st.markdown('<div class="hero-section"><h1 class="hero-title">🛡️ Leasingrückgabe für Ihren Audi</h1><p style="font-size: 1.3rem; color: white; margin-top: 20px;">Schützen Sie sich vor unfairen Nachzahlungen</p></div>', unsafe_allow_html=True)
    
    st.markdown("""
        <div style="background: white; padding: 25px; border-radius: 15px; text-align: center; margin: 20px 0; box-shadow: 0 2px 10px rgba(0,0,0,0.08);">
            <h3>📞 Sofortkontakt</h3>
            <p style="font-size: 1.3rem; font-weight: 700; color: #36454F;">
                <a href="tel:+498912345678" style="text-decoration: none; color: #36454F;">+49 89 123 456 78</a>
            </p>
            <p style="font-size: 1.1rem;">
                <a href="https://wa.me/4917698765432" target="_blank" style="text-decoration: none; color: #25D366;">
                    💬 WhatsApp: +49 176 987 654 32
                </a>
            </p>
            <p style="color: #718096;">Mo-Fr: 8:00-18:00 | Sa: 9:00-14:00</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="urgency-banner">⏰ Nur noch 3 Termine diese Woche verfügbar!</div>', unsafe_allow_html=True)
    
    st.markdown('''<div class="trust-badges">
        <div class="trust-badge"><div class="trust-icon">⚖️</div><div style="font-size: 1rem; color: #5A5A5A; font-weight: 600;">Rechtsanwälte<br/>Verkehrsrecht</div></div>
        <div class="trust-badge"><div class="trust-icon">🔍</div><div style="font-size: 1rem; color: #5A5A5A; font-weight: 600;">TÜV-zertifizierte<br/>KFZ-Gutachter</div></div>
        <div class="trust-badge"><div class="trust-icon">💰</div><div style="font-size: 1rem; color: #5A5A5A; font-weight: 600;">Ø 2.500€<br/>Ersparnis</div></div>
        <div class="trust-badge"><div class="trust-icon">⭐</div><div style="font-size: 1rem; color: #5A5A5A; font-weight: 600;">500+ zufriedene<br/>Kunden</div></div>
    </div>''', unsafe_allow_html=True)
    
    st.markdown("## 🎁 Unsere Pakete")
    pkg1, pkg2, pkg3, pkg4 = st.columns(4)
    
    with pkg1:
        st.markdown('''<div class="package-card">
            <span class="package-icon">🥉</span>
            <h3 class="package-title">Basis</h3>
            <div class="package-price">99€</div>
            <ul class="package-features">
                <li>✓ Grundcheck</li>
                <li>✓ 20 Fotos</li>
                <li>✓ PDF-Bericht</li>
            </ul>
        </div>''', unsafe_allow_html=True)
        st.button("Buchen", key="b1")
    
    with pkg2:
        st.markdown('''<div class="package-card">
            <span class="package-icon">🥈</span>
            <h3 class="package-title">Standard</h3>
            <div class="package-price">199€</div>
            <ul class="package-features">
                <li>✓ Umfassend</li>
                <li>✓ 50 Fotos</li>
                <li>✓ Beratung 1h</li>
            </ul>
        </div>''', unsafe_allow_html=True)
        st.button("Buchen", key="b2")
    
    with pkg3:
        st.markdown('''<div class="package-card package-popular" style="position:relative;">
            <div class="popular-badge">🏆 PREMIUM</div>
            <span class="package-icon">🥇</span>
            <h3 class="package-title">Premium</h3>
            <div class="package-price">299€</div>
            <ul class="package-features">
                <li>✓ Rechtsprüfung</li>
                <li>✓ Anwalt 2h</li>
                <li>✓ 24/7 Support</li>
            </ul>
        </div>''', unsafe_allow_html=True)
        st.button("Buchen", key="b3")
    
    with pkg4:
        st.markdown('''<div class="package-card">
            <span class="package-icon">💎</span>
            <h3 class="package-title">VIP</h3>
            <div class="package-price">999€</div>
            <ul class="package-features">
                <li>✓ Full-Service</li>
                <li>✓ Vor-Ort</li>
                <li>✓ Garantie</li>
            </ul>
        </div>''', unsafe_allow_html=True)
        st.button("Buchen", key="b4")

elif st.session_state.page == 'calculator':
    st.markdown('<div class="calculator-box">', unsafe_allow_html=True)
    st.title("💰 Kostenrechner")
    st.write("Ermitteln Sie Ihre voraussichtlichen Rückgabekosten")
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == 'about':
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.title("👥 Über uns")
    st.write("Mehr über ReturnGuard...")
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == 'services':
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.title("📦 Leistungen")
    st.write("Was wird geprüft?")
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == 'contact':
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.title("📞 Kontakt")
    st.write("**Telefon:** +49 89 123 456 78")
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == 'legal':
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.title("⚖️ Rechtliches")
    st.write("AGB, Datenschutz, Impressum")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown('<div style="text-align: center; color: #5A5A5A; padding: 20px;">🛡️ ReturnGuard - Ihr Partner für faire Leasingrückgaben</div>', unsafe_allow_html=True)
