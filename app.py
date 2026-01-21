import streamlit as st
import re

st.set_page_config(page_title="ReturnGuard", layout="wide", initial_sidebar_state="collapsed")

# Session State
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif; }
.stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }

.hero-section {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.95) 0%, rgba(118, 75, 162, 0.95) 100%),
                url('https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?w=1920') center/cover;
    padding: 100px 20px;
    text-align: center;
    border-radius: 0 0 50px 50px;
    margin-bottom: 30px;
}
.hero-title { font-size: 4rem; font-weight: 800; color: white; text-shadow: 3px 3px 6px rgba(0,0,0,0.4); }
.hero-subtitle { font-size: 1.3rem; color: white; margin-top: 20px; }

.urgency-banner {
    background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%);
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    color: white;
    font-size: 1.2rem;
    font-weight: 700;
    margin: 30px 0;
}

.trust-badges { display: flex; justify-content: center; gap: 30px; margin: 40px 0; flex-wrap: wrap; }
.trust-badge { background: white; padding: 25px; border-radius: 15px; min-width: 180px; text-align: center; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
.trust-icon { font-size: 4rem; margin-bottom: 10px; }
.trust-text { font-size: 1rem; color: #4a5568; font-weight: 600; }

.package-card {
    background: white;
    border-radius: 20px;
    padding: 30px 20px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.1);
    transition: transform 0.3s;
    position: relative;
}
.package-card:hover { transform: translateY(-5px); }
.package-popular { border: 3px solid #667eea; }
.popular-badge {
    position: absolute;
    top: -10px;
    right: 20px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 5px 15px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
}
.package-icon { font-size: 2.5rem; margin-bottom: 10px; }
.package-title { font-size: 1.5rem; font-weight: 700; color: #2d3748; margin: 10px 0; }
.package-price {
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 15px 0;
}
.package-features { text-align: left; list-style: none; padding: 0; margin: 20px 0; }
.package-features li { padding: 8px 0; color: #4a5568; border-bottom: 1px solid #e2e8f0; }

.content-section { background: white; padding: 50px 40px; border-radius: 20px; margin: 30px 0; box-shadow: 0 5px 20px rgba(0,0,0,0.1); }
.team-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 25px; margin: 30px 0; }
.team-card { background: #f8f9fa; padding: 25px; border-radius: 15px; text-align: center; }
.team-avatar { width: 100px; height: 100px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
    border-radius: 50%; margin: 0 auto 15px; display: flex; align-items: center; justify-content: center; font-size: 2.5rem; color: white; }

div.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    padding: 12px 30px;
    border-radius: 50px;
    font-weight: 700;
    width: 100%;
}

@media (max-width: 768px) { .hero-title { font-size: 2rem; } }
</style>
""", unsafe_allow_html=True)

# NAVIGATION
st.markdown("### 🛡️ ReturnGuard")
nav_cols = st.columns(6)
with nav_cols[0]:
    if st.button("🏠 Home", use_container_width=True): st.session_state.page = 'home'; st.rerun()
with nav_cols[1]:
    if st.button("👥 Über uns", use_container_width=True): st.session_state.page = 'about'; st.rerun()
with nav_cols[2]:
    if st.button("📦 Leistungen", use_container_width=True): st.session_state.page = 'services'; st.rerun()
with nav_cols[3]:
    if st.button("📞 Kontakt", use_container_width=True): st.session_state.page = 'contact'; st.rerun()
with nav_cols[4]:
    if st.button("📰 Blog", use_container_width=True): st.session_state.page = 'blog'; st.rerun()
with nav_cols[5]:
    if st.button("⚖️ Rechtliches", use_container_width=True): st.session_state.page = 'legal'; st.rerun()

st.markdown("---")

# ========== STARTSEITE ==========
if st.session_state.page == 'home':
    st.markdown('<div class="hero-section"><h1 class="hero-title">🛡️ Leasingrückgabe für Ihren Audi</h1><p class="hero-subtitle">Schützen Sie sich vor unfairen Nachzahlungen</p></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="urgency-banner">⏰ Nur noch 3 Termine diese Woche verfügbar!</div>', unsafe_allow_html=True)
    
    st.markdown('''<div class="trust-badges">
        <div class="trust-badge"><div class="trust-icon">⚖️</div><div class="trust-text">Rechtsanwälte</div></div>
        <div class="trust-badge"><div class="trust-icon">🔍</div><div class="trust-text">KFZ-Gutachter</div></div>
        <div class="trust-badge"><div class="trust-icon">💰</div><div class="trust-text">60% Ersparnis</div></div>
        <div class="trust-badge"><div class="trust-icon">⭐</div><div class="trust-text">500+ Kunden</div></div>
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
            <div class="popular-badge">🔥 BELIEBT</div>
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
    
    st.write("")
    st.markdown("## 💬 Kundenstimmen")
    t1, t2, t3 = st.columns(3)
    with t1:
        st.info("⭐⭐⭐⭐⭐\n\n*'2.500€ erspart!'*\n\n— Michael S.")
    with t2:
        st.info("⭐⭐⭐⭐⭐\n\n*'Perfekte Beratung!'*\n\n— Sandra K.")
    with t3:
        st.info("⭐⭐⭐⭐⭐\n\n*'Top Service!'*\n\n— Thomas B.")
    
    st.write("")
    st.markdown("## ❓ FAQ")
    with st.expander("Wann sollte ich checken?"):
        st.write("3-6 Monate vor Rückgabe")
    with st.expander("Wie lange dauert es?"):
        st.write("1-3 Stunden je nach Paket")

# ========== ÜBER UNS ==========
elif st.session_state.page == 'about':
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.title("👥 Über ReturnGuard")
    st.write("---")
    
    st.markdown("""
    ## 🎯 Unsere Mission
    ReturnGuard wurde gegründet, um Leasingnehmern eine faire Rückgabe zu ermöglichen.
    
    **Vision:** Faire Chance für jeden Leasingnehmer!
    """)
    
    st.markdown("## 👨‍👩‍👧‍👦 Unser Team")
    st.markdown('''<div class="team-grid">
        <div class="team-card">
            <div class="team-avatar">👨‍💼</div>
            <h3>Max Mustermann</h3>
            <p style="color: #667eea; font-weight: 600;">Geschäftsführer</p>
            <p>15 Jahre Erfahrung</p>
        </div>
        <div class="team-card">
            <div class="team-avatar">👨‍🔧</div>
            <h3>Stefan Schmidt</h3>
            <p style="color: #667eea; font-weight: 600;">TÜV-Gutachter</p>
            <p>Zertifiziert</p>
        </div>
        <div class="team-card">
            <div class="team-avatar">⚖️</div>
            <h3>Dr. Anna Weber</h3>
            <p style="color: #667eea; font-weight: 600;">Fachanwältin</p>
            <p>Verkehrsrecht</p>
        </div>
    </div>''', unsafe_allow_html=True)
    
    st.markdown("## 🏆 Unsere Werte")
    v1, v2, v3 = st.columns(3)
    with v1:
        st.success("**🎯 Transparenz**\n\nKeine versteckten Kosten")
    with v2:
        st.success("**⚖️ Fairness**\n\nUnabhängige Bewertung")
    with v3:
        st.success("**💪 Expertise**\n\nJahrelange Erfahrung")
    st.markdown('</div>', unsafe_allow_html=True)

# ========== LEISTUNGEN ==========
elif st.session_state.page == 'services':
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.title("📦 Unsere Leistungen")
    st.write("---")
    
    st.markdown("## 🔍 Was wird geprüft?")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        ### Exterieur
        - ✅ Lackzustand & Kratzer
        - ✅ Dellen & Beulen
        - ✅ Steinschläge
        - ✅ Scheiben & Beleuchtung
        - ✅ Reifen & Felgen
        """)
    with c2:
        st.markdown("""
        ### Interieur
        - ✅ Sitze & Polster
        - ✅ Armaturenbrett
        - ✅ Lenkrad
        - ✅ Teppiche
        - ✅ Funktionen
        """)
    
    st.write("")
    st.markdown("## 📋 Checkliste")
    with st.expander("📸 Fotodokumentation"):
        st.write("Hochauflösende Bilder aller Schäden mit GPS-Stempel")
    with st.expander("📄 Gutachten"):
        st.write("Detaillierter Bericht nach DAT/Schwacke Standards")
    with st.expander("⚖️ Rechtsprüfung"):
        st.write("Überprüfung der Leasingvertrags-Klauseln")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ========== KONTAKT ==========
elif st.session_state.page == 'contact':
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.title("📞 Kontakt")
    st.write("---")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        ## 📧 Kontaktdaten
        
        **Telefon:** +49 89 123 456 78  
        **WhatsApp:** +49 176 987 654 32  
        **E-Mail:** info@returnguard.de
        
        **Öffnungszeiten:**  
        Mo-Fr: 8:00 - 18:00 Uhr  
        Sa: 9:00 - 14:00 Uhr
        
        **Einsatzgebiet:**  
        München & Umgebung (50km)
        """)
    
    with c2:
        st.markdown("## ✉️ Nachricht senden")
        name = st.text_input("Name")
        email = st.text_input("E-Mail")
        message = st.text_area("Nachricht")
        if st.button("Absenden"):
            if name and email and message:
                st.success("✅ Nachricht gesendet!")
                st.balloons()
            else:
                st.error("Bitte alle Felder ausfüllen")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ========== BLOG ==========
elif st.session_state.page == 'blog':
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.title("📰 Ratgeber & Blog")
    st.write("---")
    
    with st.expander("📝 10 Tipps für eine erfolgreiche Leasingrückgabe"):
        st.write("Hier kommen die Tipps...")
    with st.expander("🚗 Häufige Fehler bei Audi-Leasingrückgaben"):
        st.write("Diese Fehler sollten Sie vermeiden...")
    with st.expander("💰 So sparen Sie bei der Rückgabe"):
        st.write("Geld-Spar-Tipps...")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ========== RECHTLICHES ==========
elif st.session_state.page == 'legal':
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.title("⚖️ Rechtliches")
    
    tabs = st.tabs(["📄 AGB", "🔒 Datenschutz", "ℹ️ Impressum"])
    
    with tabs[0]:
        st.markdown("""
        ## Allgemeine Geschäftsbedingungen
        
        **§1 Geltungsbereich**  
        Diese AGB gelten für alle Leistungen von ReturnGuard...
        
        **§2 Leistungen**  
        ReturnGuard bietet...
        """)
    
    with tabs[1]:
        st.markdown("""
        ## Datenschutzerklärung
        
        Wir nehmen den Schutz Ihrer Daten ernst...
        """)
    
    with tabs[2]:
        st.markdown("""
        ## Impressum
        
        **ReturnGuard GmbH**  
        Musterstraße 123  
        80331 München
        
        **Geschäftsführer:** Max Mustermann  
        **USt-ID:** DE123456789
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown('<div style="text-align: center; color: #718096; padding: 20px;">🛡️ ReturnGuard - Ihr Partner für faire Leasingrückgaben<br/>Datenschutz | AGB | Impressum</div>', unsafe_allow_html=True)
