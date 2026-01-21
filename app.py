import streamlit as st
import re

st.set_page_config(page_title="ReturnGuard", layout="wide", initial_sidebar_state="collapsed")

if 'page' not in st.session_state:
    st.session_state.page = 'home'

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif; }
.stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }

.hero-section {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.95) 0%, rgba(118, 75, 162, 0.95) 100%),
                url('https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?w=1920') center/cover;
    padding: 100px 20px; text-align: center; border-radius: 0 0 50px 50px; margin-bottom: 30px;
}
.hero-title { font-size: 4rem; font-weight: 800; color: white; text-shadow: 3px 3px 6px rgba(0,0,0,0.4); }

/* NEUE: Sticky Contact Buttons */
.sticky-contact {
    position: fixed;
    bottom: 20px;
    right: 20px;
    z-index: 1000;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.contact-button {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.8rem;
    box-shadow: 0 5px 20px rgba(0,0,0,0.3);
    cursor: pointer;
    transition: transform 0.3s;
    text-decoration: none;
}

.contact-button:hover {
    transform: scale(1.1);
}

.whatsapp-btn {
    background: #25D366;
}

.phone-btn {
    background: #667eea;
}

.urgency-banner {
    background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%);
    padding: 20px; border-radius: 15px; text-align: center;
    color: white; font-size: 1.2rem; font-weight: 700; margin: 30px 0;
}

.trust-badges { display: flex; justify-content: center; gap: 30px; margin: 40px 0; flex-wrap: wrap; }
.trust-badge { background: white; padding: 25px; border-radius: 15px; min-width: 180px; text-align: center; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
.trust-icon { font-size: 4rem; margin-bottom: 10px; }

.package-card {
    background: white; border-radius: 20px; padding: 30px 20px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.1); transition: transform 0.3s; position: relative;
}
.package-card:hover { transform: translateY(-5px); }
.package-popular { border: 3px solid #667eea; }
.popular-badge {
    position: absolute; top: -10px; right: 20px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white; padding: 5px 15px; border-radius: 20px; font-size: 0.75rem; font-weight: 700;
}
.package-icon { font-size: 2.5rem; margin-bottom: 10px; }
.package-title { font-size: 1.5rem; font-weight: 700; color: #2d3748; margin: 10px 0; }
.package-price {
    font-size: 2rem; font-weight: 800;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 15px 0;
}
.package-features { text-align: left; list-style: none; padding: 0; margin: 20px 0; }
.package-features li { padding: 8px 0; color: #4a5568; border-bottom: 1px solid #e2e8f0; }

.content-section { background: white; padding: 50px 40px; border-radius: 20px; margin: 30px 0; box-shadow: 0 5px 20px rgba(0,0,0,0.1); }

.calculator-box { background: white; padding: 40px; border-radius: 20px; box-shadow: 0 10px 40px rgba(0,0,0,0.15); margin: 40px 0; }
.cost-display { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 15px; text-align: center; color: white; margin: 20px 0; }
.savings-box { background: linear-gradient(135deg, #48bb78 0%, #38a169 100%); padding: 25px; border-radius: 15px; text-align: center; color: white; margin: 20px 0; }

.team-card { background: #f8f9fa; padding: 25px; border-radius: 15px; text-align: center; margin: 15px 0; }
.team-avatar { width: 100px; height: 100px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
    border-radius: 50%; margin: 0 auto 15px; display: flex; align-items: center; justify-content: center; font-size: 2.5rem; color: white; }

div.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white; border: none; padding: 12px 30px; border-radius: 50px; font-weight: 700; width: 100%;
}

@media (max-width: 768px) { 
    .hero-title { font-size: 2rem; }
    .sticky-contact { bottom: 10px; right: 10px; }
    .contact-button { width: 50px; height: 50px; font-size: 1.5rem; }
}
</style>
""", unsafe_allow_html=True)

# STICKY CONTACT BUTTONS (IMMER SICHTBAR!)
st.markdown("""
    <div class="sticky-contact">
        <a href="https://wa.me/4917698765432?text=Hallo%20ReturnGuard,%20ich%20interessiere%20mich%20für%20eine%20Leasingrückgabe" 
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

# ========== STARTSEITE ==========
if st.session_state.page == 'home':
    st.markdown('<div class="hero-section"><h1 class="hero-title">🛡️ Leasingrückgabe für Ihren Audi</h1><p style="font-size: 1.3rem; color: white; margin-top: 20px;">Schützen Sie sich vor unfairen Nachzahlungen</p></div>', unsafe_allow_html=True)
    
    # Schnellkontakt prominent
    st.markdown("""
        <div style="background: white; padding: 25px; border-radius: 15px; text-align: center; margin: 20px 0; box-shadow: 0 5px 15px rgba(0,0,0,0.1);">
            <h3 style="margin-bottom: 15px;">📞 Sofortkontakt</h3>
            <p style="font-size: 1.3rem; font-weight: 700; color: #667eea; margin: 10px 0;">
                <a href="tel:+498912345678" style="text-decoration: none; color: #667eea;">+49 89 123 456 78</a>
            </p>
            <p style="font-size: 1.1rem; color: #4a5568;">
                <a href="https://wa.me/4917698765432" target="_blank" style="text-decoration: none; color: #25D366;">
                    💬 WhatsApp: +49 176 987 654 32
                </a>
            </p>
            <p style="color: #718096; margin-top: 10px;">Mo-Fr: 8:00-18:00 Uhr | Sa: 9:00-14:00 Uhr</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="urgency-banner">⏰ Nur noch 3 Termine diese Woche verfügbar!</div>', unsafe_allow_html=True)
    
    st.markdown('''<div class="trust-badges">
        <div class="trust-badge"><div class="trust-icon">⚖️</div><div style="font-size: 1rem; color: #4a5568; font-weight: 600;">Rechtsanwälte<br/>Verkehrsrecht</div></div>
        <div class="trust-badge"><div class="trust-icon">🔍</div><div style="font-size: 1rem; color: #4a5568; font-weight: 600;">TÜV-zertifizierte<br/>KFZ-Gutachter</div></div>
        <div class="trust-badge"><div class="trust-icon">💰</div><div style="font-size: 1rem; color: #4a5568; font-weight: 600;">Ø 2.500€<br/>Ersparnis</div></div>
        <div class="trust-badge"><div class="trust-icon">⭐</div><div style="font-size: 1rem; color: #4a5568; font-weight: 600;">500+ zufriedene<br/>Kunden</div></div>
    </div>''', unsafe_allow_html=True)
    
    # Kostenrechner Teaser
    st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px; border-radius: 20px; text-align: center; margin: 30px 0;">
            <h2 style="color: white; font-size: 2rem; margin-bottom: 20px;">💰 Kostenloser Kostenrechner</h2>
            <p style="color: white; font-size: 1.2rem;">Ermitteln Sie in 2 Minuten Ihre voraussichtlichen Rückgabekosten!</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔍 Jetzt Kosten berechnen", use_container_width=True, key="calc_teaser"):
        st.session_state.page = 'calculator'
        st.rerun()
    
    st.write("")
    
    # USP Section
    st.markdown("## 🚀 Warum ReturnGuard?")
    usp1, usp2, usp3, usp4 = st.columns(4)
    with usp1:
        st.markdown("""<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 25px; border-radius: 15px; text-align: center; height: 250px;">
            <div style="font-size: 3rem; margin-bottom: 10px;">🎯</div>
            <h4 style="color: white; margin-bottom: 10px;">Spezialisiert</h4>
            <p style="color: white; font-size: 0.9rem;">NUR Leasingrückgaben - keine Ablenkung</p>
        </div>""", unsafe_allow_html=True)
    with usp2:
        st.markdown("""<div style="background: linear-gradient(135deg, #48bb78 0%, #38a169 100%); padding: 25px; border-radius: 15px; text-align: center; height: 250px;">
            <div style="font-size: 3rem; margin-bottom: 10px;">🤝</div>
            <h4 style="color: white; margin-bottom: 10px;">Komplettservice</h4>
            <p style="color: white; font-size: 0.9rem;">Gutachter + Anwalt + Werkstatt</p>
        </div>""", unsafe_allow_html=True)
    with usp3:
        st.markdown("""<div style="background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%); padding: 25px; border-radius: 15px; text-align: center; height: 250px;">
            <div style="font-size: 3rem; margin-bottom: 10px;">💎</div>
            <h4 style="color: white; margin-bottom: 10px;">Transparent</h4>
            <p style="color: white; font-size: 0.9rem;">Feste Preise, keine versteckten Kosten</p>
        </div>""", unsafe_allow_html=True)
    with usp4:
        st.markdown("""<div style="background: linear-gradient(135deg, #E53E3E 0%, #C53030 100%); padding: 25px; border-radius: 15px; text-align: center; height: 250px;">
            <div style="font-size: 3rem; margin-bottom: 10px;">🏆</div>
            <h4 style="color: white; margin-bottom: 10px;">Garantie</h4>
            <p style="color: white; font-size: 0.9rem;">Geld-zurück bei VIP-Paket</p>
        </div>""", unsafe_allow_html=True)
    
    st.write("")
    
    # Wie berechnen wir die Ersparnis? (NEU - TRANSPARENZ!)
    st.markdown("## 💡 So erreichen wir Ihre Ersparnis")
    st.markdown("""
        <div style="background: white; padding: 40px; border-radius: 20px; box-shadow: 0 5px 20px rgba(0,0,0,0.1); margin: 30px 0;">
            <h3 style="color: #2d3748; margin-bottom: 25px;">Transparenz ist uns wichtig - So funktioniert's:</h3>
        </div>
    """, unsafe_allow_html=True)
    
    sav1, sav2, sav3 = st.columns(3)
    with sav1:
        st.info("""
        **1️⃣ Frühzeitige Erkennung**
        
        - Check 3-6 Monate VOR Rückgabe
        - Noch Zeit für günstige Reparatur
        - Smart Repair statt Neulackierung
        - Ø Ersparnis: 40%
        """)
    with sav2:
        st.info("""
        **2️⃣ Unser Werkstatt-Netzwerk**
        
        - 50+ Partner-Werkstätten
        - Sonderkonditionen für Kunden
        - Zertifizierte Qualität
        - Ø Ersparnis: 30%
        """)
    with sav3:
        st.info("""
        **3️⃣ Rechtsberatung**
        
        - Ungerechtfertigte Forderungen abwehren
        - Verhandlung auf Augenhöhe
        - Juristische Absicherung
        - Ø Ersparnis: 30%
        """)
    
    st.success("### 🎯 Gesamtersparnis: Durchschnittlich 2.500€ (60-70% der ursprünglichen Kosten)")
    
    st.write("")
    
    # Pakete
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
                <li>✓ Email-Support</li>
            </ul>
        </div>''', unsafe_allow_html=True)
        st.button("Buchen", key="b1")
    
    with pkg2:
        st.markdown('''<div class="package-card">
            <span class="package-icon">🥈</span>
            <h3 class="package-title">Standard</h3>
            <div class="package-price">199€</div>
            <ul class="package-features">
                <li>✓ Umfassender Check</li>
                <li>✓ 50 Fotos</li>
                <li>✓ Beratung 1h</li>
                <li>✓ Priority Support</li>
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
                <li>✓ Verhandlung</li>
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
                <li>✓ Vor-Ort Begleitung</li>
                <li>✓ Geld-zurück-Garantie</li>
                <li>✓ Premium Hotline</li>
            </ul>
        </div>''', unsafe_allow_html=True)
        st.button("Buchen", key="b4")
    
    st.write("")
    
    # Testimonials
    st.markdown("## 💬 Echte Kundenstimmen")
    t1, t2, t3 = st.columns(3)
    with t1:
        st.info("⭐⭐⭐⭐⭐\n\n*'Hatte Angst vor 4.000€ Nachzahlung. Mit ReturnGuard nur 1.200€ bezahlt. Ersparnis: 2.800€!'*\n\n— Michael S., Audi A4 (2021-2024)")
    with t2:
        st.info("⭐⭐⭐⭐⭐\n\n*'Die anwaltliche Beratung war Gold wert. Leasinggeber wollte 3.200€, am Ende nur 800€!'*\n\n— Sandra K., Audi Q5 (2020-2023)")
    with t3:
        st.info("⭐⭐⭐⭐⭐\n\n*'Schnell, professionell, transparent. Das Premium-Paket hat sich mehr als gelohnt!'*\n\n— Thomas B., Audi A6 (2019-2024)")

# ========== ÜBER UNS (ERWEITERT!) ==========
elif st.session_state.page == 'about':
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.title("👥 Über ReturnGuard - Wer wir sind")
    st.write("---")
    
    st.markdown("""
    ## 🎯 Unsere Geschichte
    
    ReturnGuard wurde 2020 von Max Mustermann gegründet, nachdem er selbst eine frustrierende Erfahrung 
    bei einer Leasingrückgabe gemacht hatte. **3.800€ Nachzahlung** für Schäden, die er selbst für 
    800€ hätte reparieren können - wenn er es nur früher gewusst hätte.
    
    **Unsere Mission:** Nie wieder soll ein Leasingnehmer übervorteilt werden!
    
    ### 📊 Fakten über uns:
    - ✅ **Über 500 erfolgreiche Rückgaben** seit 2020
    - ✅ **Durchschnittliche Ersparnis: 2.500€** pro Kunde
    - ✅ **50+ Partner-Werkstätten** in ganz Deutschland
    - ✅ **15+ Fachanwälte** im Netzwerk
    - ✅ **TÜV-zertifizierte Gutachter**
    
    ### 🏆 Unsere Qualifikationen:
    - IHK-geprüfte KFZ-Sachverständige
    - Fachanwälte für Verkehrsrecht
    - DAT/Schwacke zertifiziert
    - Unabhängig & neutral
    """)
    
    st.write("")
    st.markdown("## 👨‍👩‍👧‍👦 Unser Team")
    
    team1, team2, team3 = st.columns(3)
    with team1:
        st.markdown("""
            <div class="team-card">
                <div class="team-avatar">👨‍💼</div>
                <h3>Max Mustermann</h3>
                <p style="color: #667eea; font-weight: 600; margin: 10px 0;">Geschäftsführer & Gründer</p>
                <p style="font-size: 0.9rem;">15 Jahre Automotive-Branche<br/>Ex-Audi Flotten-Manager<br/>IHK-zertifiziert</p>
            </div>
        """, unsafe_allow_html=True)
    
    with team2:
        st.markdown("""
            <div class="team-card">
                <div class="team-avatar">👨‍🔧</div>
                <h3>Stefan Schmidt</h3>
                <p style="color: #667eea; font-weight: 600; margin: 10px 0;">Lead KFZ-Gutachter</p>
                <p style="font-size: 0.9rem;">TÜV-Süd zertifiziert<br/>20+ Jahre Erfahrung<br/>Audi-Spezialist</p>
            </div>
        """, unsafe_allow_html=True)
    
    with team3:
        st.markdown("""
            <div class="team-card">
                <div class="team-avatar">⚖️</div>
                <h3>Dr. Anna Weber</h3>
                <p style="color: #667eea; font-weight: 600; margin: 10px 0;">Fachanwältin Verkehrsrecht</p>
                <p style="font-size: 0.9rem;">Spezialisiert auf Leasing<br/>300+ gewonnene Fälle<br/>Verhandlungsexpertin</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.write("")
    
    # Partner-Netzwerk (NEU!)
    st.markdown("## 🤝 Unser Partner-Netzwerk")
    st.markdown("""
        <div style="background: #f8f9fa; padding: 30px; border-radius: 15px; margin: 20px 0;">
            <h4 style="color: #2d3748; margin-bottom: 20px;">Wir arbeiten ausschließlich mit zertifizierten Partnern:</h4>
            
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px;">
                <div>
                    <h5 style="color: #667eea;">🔧 Werkstätten</h5>
                    <ul style="color: #4a5568;">
                        <li>ATU - bundesweit</li>
                        <li>Euromaster - Reifenservice</li>
                        <li>Lokale Meisterbetriebe</li>
                        <li>Smart Repair Spezialisten</li>
                    </ul>
                </div>
                <div>
                    <h5 style="color: #667eea;">⚖️ Anwaltskanzleien</h5>
                    <ul style="color: #4a5568;">
                        <li>Kanzlei Weber & Partner (München)</li>
                        <li>Rechtsanwälte Müller (Berlin)</li>
                        <li>Fachanwälte Automotive</li>
                    </ul>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ========== KONTAKT (ERWEITERT!) ==========
elif st.session_state.page == 'contact':
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.title("📞 Kontakt - Wir sind für Sie da!")
    st.write("---")
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("""
        ## 📧 Kontaktdaten
        
        **Telefon (Festnetz):**  
        <a href="tel:+498912345678" style="font-size: 1.3rem; color: #667eea; text-decoration: none;">
        +49 89 123 456 78
        </a>
        
        **Mobil/WhatsApp:**  
        <a href="https://wa.me/4917698765432" style="font-size: 1.3rem; color: #25D366; text-decoration: none;">
        +49 176 987 654 32
        </a>
        
        **E-Mail:**  
        info@returnguard.de
        
        ---
        
        **Öffnungszeiten:**  
        Montag - Freitag: 8:00 - 18:00 Uhr  
        Samstag: 9:00 - 14:00 Uhr  
        Sonntag: Geschlossen
        
        **24/7 Notfall-Hotline** (nur für Premium/VIP):  
        +49 176 111 222 33
        
        ---
        
        **Adresse:**  
        ReturnGuard GmbH  
        Musterstraße 123  
        80331 München  
        Deutschland
        
        📍 [Google Maps öffnen](https://maps.google.com)
        
        ---
        
        **Einsatzgebiet:**  
        - München & Umgebung (50km Radius)
        - Bundesweit auf Anfrage
        - Österreich & Schweiz: In Planung
        """, unsafe_allow_html=True)
    
    with c2:
        st.markdown("## ✉️ Nachricht senden")
        name = st.text_input("Ihr Name *")
        email = st.text_input("Ihre E-Mail *")
        phone = st.text_input("Telefon (optional)")
        fahrzeug = st.text_input("Fahrzeug (z.B. Audi A4, 2021)")
        rueckgabe = st.date_input("Geplante Rückgabe")
        message = st.text_area("Ihre Nachricht *")
        
        if st.button("📨 Nachricht absenden", use_container_width=True):
