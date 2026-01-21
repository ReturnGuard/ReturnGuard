import streamlit as st
import re

st.set_page_config(page_title="ReturnGuard", layout="wide", initial_sidebar_state="collapsed")

if 'page' not in st.session_state:
    st.session_state.page = 'home'

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
* { font-family: 'Inter', sans-serif; }

/* BANKING OPTIK - CLEAN & MINIMAL */
.stApp { 
    background: #FAFBFC;
}

.hero-section {
    background: linear-gradient(180deg, #FFFFFF 0%, #F5F7FA 100%);
    padding: 80px 20px 60px 20px; 
    text-align: center; 
    border-bottom: 1px solid #E8EBED;
    margin-bottom: 40px;
}

.hero-title { 
    font-size: 3.5rem; 
    font-weight: 300; 
    color: #1A2332; 
    margin-bottom: 15px;
    letter-spacing: -1px;
}

.hero-subtitle {
    font-size: 1.25rem;
    color: #5F6B7A;
    font-weight: 400;
    margin-top: 10px;
}

.sticky-contact {
    position: fixed; 
    bottom: 30px; 
    right: 30px; 
    z-index: 1000;
    display: flex; 
    flex-direction: column; 
    gap: 12px;
}

.contact-button {
    width: 56px; 
    height: 56px; 
    border-radius: 50%;
    display: flex; 
    align-items: center; 
    justify-content: center;
    font-size: 1.5rem; 
    box-shadow: 0 2px 12px rgba(26, 35, 50, 0.15);
    cursor: pointer; 
    transition: all 0.3s ease;
    text-decoration: none;
    border: 1px solid rgba(255, 255, 255, 0.8);
}

.contact-button:hover { 
    transform: translateY(-3px); 
    box-shadow: 0 4px 20px rgba(26, 35, 50, 0.25);
}

.whatsapp-btn { background: #25D366; }
.phone-btn { background: #2E5BFF; }

.info-banner {
    background: #FFFFFF;
    border: 1px solid #E8EBED;
    padding: 20px 30px;
    border-radius: 8px;
    text-align: center;
    margin: 30px auto;
    max-width: 600px;
    box-shadow: 0 1px 3px rgba(26, 35, 50, 0.04);
}

.info-banner-text {
    color: #2E5BFF;
    font-size: 1rem;
    font-weight: 500;
    margin: 0;
}

.trust-badges { 
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    margin: 50px auto;
    max-width: 1000px;
}

.trust-badge { 
    background: #FFFFFF;
    padding: 30px 20px;
    border-radius: 8px;
    text-align: center;
    box-shadow: 0 1px 3px rgba(26, 35, 50, 0.04);
    border: 1px solid #E8EBED;
    transition: all 0.3s ease;
}

.trust-badge:hover {
    box-shadow: 0 4px 12px rgba(26, 35, 50, 0.08);
    transform: translateY(-2px);
}

.trust-icon { 
    font-size: 2.5rem; 
    margin-bottom: 15px;
    opacity: 0.9;
}

.trust-title {
    font-size: 0.875rem;
    color: #5F6B7A;
    font-weight: 500;
    line-height: 1.5;
}

.package-card {
    background: #FFFFFF;
    border-radius: 8px;
    padding: 35px 25px;
    box-shadow: 0 1px 3px rgba(26, 35, 50, 0.04);
    border: 1px solid #E8EBED;
    transition: all 0.3s ease;
    position: relative;
    height: 100%;
}

.package-card:hover { 
    box-shadow: 0 4px 16px rgba(26, 35, 50, 0.1);
    transform: translateY(-4px);
    border-color: #2E5BFF;
}

.package-popular { 
    border: 2px solid #2E5BFF;
    box-shadow: 0 2px 8px rgba(46, 91, 255, 0.15);
}

.popular-badge {
    position: absolute;
    top: -12px;
    right: 20px;
    background: #2E5BFF;
    color: white;
    padding: 4px 14px;
    border-radius: 4px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.5px;
}

.package-icon { 
    font-size: 2rem; 
    margin-bottom: 15px;
    opacity: 0.8;
}

.package-title { 
    font-size: 1.5rem; 
    font-weight: 500; 
    color: #1A2332; 
    margin: 10px 0 5px 0;
    letter-spacing: -0.5px;
}

.package-subtitle {
    font-size: 0.875rem;
    color: #5F6B7A;
    margin-bottom: 20px;
}

.package-price { 
    font-size: 2.5rem; 
    font-weight: 300; 
    color: #1A2332; 
    margin: 20px 0;
    letter-spacing: -1px;
}

.package-price-unit {
    font-size: 1rem;
    color: #5F6B7A;
    font-weight: 400;
}

.package-features { 
    text-align: left; 
    list-style: none; 
    padding: 0; 
    margin: 25px 0;
}

.package-features li { 
    padding: 12px 0;
    color: #5F6B7A;
    border-bottom: 1px solid #F5F7FA;
    font-size: 0.9rem;
    line-height: 1.5;
}

.package-features li:last-child {
    border-bottom: none;
}

.content-section { 
    background: #FFFFFF;
    padding: 50px 40px;
    border-radius: 8px;
    margin: 30px auto;
    max-width: 1200px;
    box-shadow: 0 1px 3px rgba(26, 35, 50, 0.04);
    border: 1px solid #E8EBED;
}

.section-title {
    font-size: 2rem;
    font-weight: 500;
    color: #1A2332;
    margin-bottom: 10px;
    letter-spacing: -0.5px;
}

.section-subtitle {
    font-size: 1.1rem;
    color: #5F6B7A;
    font-weight: 400;
    margin-bottom: 30px;
}

.calculator-box { 
    background: #FFFFFF;
    padding: 40px;
    border-radius: 8px;
    box-shadow: 0 1px 3px rgba(26, 35, 50, 0.04);
    margin: 40px auto;
    max-width: 800px;
    border: 1px solid #E8EBED;
}

.cost-display { 
    background: linear-gradient(135deg, #2E5BFF 0%, #0040DD 100%);
    padding: 35px;
    border-radius: 8px;
    text-align: center;
    color: white;
    margin: 25px 0;
    box-shadow: 0 4px 16px rgba(46, 91, 255, 0.25);
}

.savings-box { 
    background: linear-gradient(135deg, #00C48C 0%, #00A374 100%);
    padding: 30px;
    border-radius: 8px;
    text-align: center;
    color: white;
    margin: 25px 0;
    box-shadow: 0 4px 16px rgba(0, 196, 140, 0.25);
}

.team-card { 
    background: #FFFFFF;
    padding: 30px;
    border-radius: 8px;
    text-align: center;
    margin: 20px 0;
    border: 1px solid #E8EBED;
    box-shadow: 0 1px 3px rgba(26, 35, 50, 0.04);
}

.team-avatar { 
    width: 80px;
    height: 80px;
    background: linear-gradient(135deg, #2E5BFF 0%, #0040DD 100%);
    border-radius: 50%;
    margin: 0 auto 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2rem;
    color: white;
}

.contact-box {
    background: #FFFFFF;
    padding: 30px;
    border-radius: 8px;
    text-align: center;
    margin: 25px auto;
    max-width: 600px;
    box-shadow: 0 1px 3px rgba(26, 35, 50, 0.04);
    border: 1px solid #E8EBED;
}

.contact-title {
    font-size: 1.25rem;
    font-weight: 500;
    color: #1A2332;
    margin-bottom: 20px;
}

.contact-phone {
    font-size: 2rem;
    font-weight: 300;
    color: #2E5BFF;
    margin: 15px 0;
    letter-spacing: -0.5px;
}

.contact-phone a {
    color: #2E5BFF;
    text-decoration: none;
}

.contact-whatsapp {
    font-size: 1.1rem;
    margin: 15px 0;
}

.contact-whatsapp a {
    color: #25D366;
    text-decoration: none;
    font-weight: 500;
}

.contact-hours {
    color: #5F6B7A;
    font-size: 0.95rem;
    margin-top: 15px;
}

div.stButton > button {
    background: #2E5BFF;
    color: white;
    border: none;
    padding: 14px 28px;
    border-radius: 6px;
    font-weight: 500;
    font-size: 0.95rem;
    width: 100%;
    transition: all 0.3s ease;
    letter-spacing: 0.3px;
    box-shadow: 0 2px 8px rgba(46, 91, 255, 0.2);
}

div.stButton > button:hover {
    background: #0040DD;
    box-shadow: 0 4px 16px rgba(46, 91, 255, 0.35);
    transform: translateY(-1px);
}

/* Navigation Buttons */
div[data-testid="column"] > div.stButton > button {
    background: transparent;
    color: #5F6B7A;
    border: 1px solid #E8EBED;
    box-shadow: none;
    font-weight: 500;
    padding: 10px 20px;
}

div[data-testid="column"] > div.stButton > button:hover {
    background: #F5F7FA;
    color: #1A2332;
    border-color: #2E5BFF;
    transform: none;
}

@media (max-width: 768px) { 
    .hero-title { 
        font-size: 2rem; 
    }
    
    .hero-subtitle {
        font-size: 1rem;
    }
    
    .sticky-contact { 
        bottom: 15px; 
        right: 15px; 
    }
    
    .contact-button { 
        width: 48px; 
        height: 48px; 
        font-size: 1.3rem; 
    }
    
    .trust-badges {
        grid-template-columns: 1fr;
    }
    
    .package-price {
        font-size: 2rem;
    }
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
st.markdown('<div style="padding: 20px 0 10px 0; border-bottom: 1px solid #E8EBED; margin-bottom: 0;">', unsafe_allow_html=True)
st.markdown('<div style="text-align: center; font-size: 1.5rem; font-weight: 500; color: #1A2332; margin-bottom: 20px;">🛡️ ReturnGuard</div>', unsafe_allow_html=True)

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

st.markdown('</div>', unsafe_allow_html=True)

# STARTSEITE
if st.session_state.page == 'home':
    st.markdown('''
        <div class="hero-section">
            <h1 class="hero-title">Leasingrückgabe leicht gemacht</h1>
            <p class="hero-subtitle">Schützen Sie sich vor unfairen Nachzahlungen bei Ihrer Audi-Rückgabe</p>
        </div>
    ''', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="contact-box">
            <h3 class="contact-title">Sprechen Sie mit unseren Experten</h3>
            <p class="contact-phone">
                <a href="tel:+498912345678">+49 89 123 456 78</a>
            </p>
            <p class="contact-whatsapp">
                <a href="https://wa.me/4917698765432" target="_blank">
                    💬 WhatsApp: +49 176 987 654 32
                </a>
            </p>
            <p class="contact-hours">Mo-Fr: 8:00-18:00 Uhr | Sa: 9:00-14:00 Uhr</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="info-banner"><p class="info-banner-text">Noch 3 Beratungstermine diese Woche verfügbar</p></div>', unsafe_allow_html=True)
    
    st.markdown('''
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
                <div class="trust-icon">💰</div>
                <div class="trust-title">Ø 2.500€<br/>Ersparnis</div>
            </div>
            <div class="trust-badge">
                <div class="trust-icon">⭐</div>
                <div class="trust-title">500+ zufriedene<br/>Kunden</div>
            </div>
        </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('<div style="text-align: center; margin: 50px 0 30px 0;"><h2 class="section-title">Unsere Pakete</h2><p class="section-subtitle">Wählen Sie den Service, der zu Ihnen passt</p></div>', unsafe_allow_html=True)
    
    pkg1, pkg2, pkg3, pkg4 = st.columns(4)
    
    with pkg1:
        st.markdown('''
            <div class="package-card">
                <span class="package-icon">📋</span>
                <h3 class="package-title">Basis</h3>
                <p class="package-subtitle">Für einfache Prüfungen</p>
                <div class="package-price">99<span class="package-price-unit">€</span></div>
                <ul class="package-features">
                    <li>✓ Grundcheck des Fahrzeugs</li>
                    <li>✓ 20 Dokumentationsfotos</li>
                    <li>✓ PDF-Bericht per Email</li>
                    <li>✓ Bearbeitungszeit 48h</li>
                </ul>
            </div>
        ''', unsafe_allow_html=True)
        st.button("Jetzt buchen", key="b1")
    
    with pkg2:
        st.markdown('''
            <div class="package-card">
                <span class="package-icon">📊</span>
                <h3 class="package-title">Standard</h3>
                <p class="package-subtitle">Umfassende Beratung</p>
                <div class="package-price">199<span class="package-price-unit">€</span></div>
                <ul class="package-features">
                    <li>✓ Umfassende Fahrzeugprüfung</li>
                    <li>✓ 50 Detailfotos</li>
                    <li>✓ Telefonberatung 1 Stunde</li>
                    <li>✓ Bearbeitungszeit 24h</li>
                </ul>
            </div>
        ''', unsafe_allow_html=True)
        st.button("Jetzt buchen", key="b2")
    
    with pkg3:
        st.markdown('''
            <div class="package-card package-popular">
                <div class="popular-badge">BELIEBT</div>
                <span class="package-icon">⭐</span>
                <h3 class="package-title">Premium</h3>
                <p class="package-subtitle">Mit Rechtsschutz</p>
                <div class="package-price">299<span class="package-price-unit">€</span></div>
                <ul class="package-features">
                    <li>✓ Rechtliche Prüfung</li>
                    <li>✓ Anwaltsberatung 2 Stunden</li>
                    <li>✓ 24/7 Support-Hotline</li>
                    <li>✓ Sofort-Bearbeitung</li>
                </ul>
            </div>
        ''', unsafe_allow_html=True)
        st.button("Jetzt buchen", key="b3")
    
    with pkg4:
        st.markdown('''
            <div class="package-card">
                <span class="package-icon">💎</span>
                <h3 class="package-title">VIP</h3>
                <p class="package-subtitle">Rundum-Sorglos</p>
                <div class="package-price">999<span class="package-price-unit">€</span></div>
                <ul class="package-features">
                    <li>✓ Full-Service Komplettpaket</li>
                    <li>✓ Vor-Ort Service bundesweit</li>
                    <li>✓ Rückgabe-Garantie</li>
                    <li>✓ Persönlicher Ansprechpartner</li>
                </ul>
            </div>
        ''', unsafe_allow_html=True)
        st.button("Jetzt buchen", key="b4")

elif st.session_state.page == 'calculator':
    st.markdown('<div class="calculator-box">', unsafe_allow_html=True)
    st.markdown('<h1 class="section-title">💰 Kostenrechner</h1>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">Ermitteln Sie Ihre voraussichtlichen Rückgabekosten</p>', unsafe_allow_html=True)
    
    st.write("Fahrzeugmodell:")
    model = st.selectbox("", ["Audi A3", "Audi A4", "Audi A6", "Audi Q3", "Audi Q5", "Audi Q7"], label_visibility="collapsed")
    
    st.write("Laufleistung (km):")
    mileage = st.number_input("", min_value=0, max_value=200000, value=50000, step=1000, label_visibility="collapsed")
    
    st.write("Leasingdauer (Monate):")
    duration = st.number_input("", min_value=12, max_value=60, value=36, step=6, label_visibility="collapsed")
    
    if st.button("Kosten berechnen", use_container_width=True):
        estimated_cost = 1500 + (mileage / 1000) * 0.5
        savings = estimated_cost * 0.6
        
        st.markdown(f'''
            <div class="cost-display">
                <h3 style="font-weight: 300; margin-bottom: 10px;">Geschätzte Rückgabekosten</h3>
                <div style="font-size: 3rem; font-weight: 300; letter-spacing: -1px;">{estimated_cost:,.0f} €</div>
            </div>
            
            <div class="savings-box">
                <h3 style="font-weight: 400; margin-bottom: 10px;">Mögliche Ersparnis mit ReturnGuard</h3>
                <div style="font-size: 2.5rem; font-weight: 400; letter-spacing: -1px;">bis zu {savings:,.0f} €</div>
            </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == 'about':
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.markdown('<h1 class="section-title">👥 Über uns</h1>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">Ihr Partner für faire Leasingrückgaben</p>', unsafe_allow_html=True)
    
    st.write("""
    ReturnGuard ist Ihr spezialisierter Partner für professionelle Leasingrückgaben. 
    Mit unserem Team aus erfahrenen Rechtsanwälten und TÜV-zertifizierten KFZ-Gutachtern 
    sorgen wir dafür, dass Sie bei der Rückgabe Ihres Audi nicht mehr zahlen als nötig.
    
    **Unsere Expertise:**
    - Über 500 erfolgreich begleitete Leasingrückgaben
    - Durchschnittliche Ersparnis von 2.500€ pro Kunde
    - Spezialisierung auf Premium-Fahrzeuge (Audi, BMW, Mercedes)
    - Bundesweiter Service
    """)
    
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == 'services':
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.markdown('<h1 class="section-title">📦 Unsere Leistungen</h1>', unsafe_allow_html=True)
    st.markdown('<p class="section-subtitle">Was wird bei der Rückgabe geprüft?</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🔍 Technische Prüfung
        - Karosserie und Lackzustand
        - Innenraum und Polster
        - Reifen und Felgen
        - Elektronische Systeme
        - Motor und Getriebe
        """)
        
        st.markdown("""
        ### 📋 Dokumentation
        - Professionelle Fotodokumentation
        - Detaillierter Zustandsbericht
        - Vergleich mit Leasingvertrag
        - Rechtliche Einschätzung
        """)
    
    with col2:
        st.markdown("""
        ### ⚖️ Rechtliche Beratung
        - Prüfung des Leasingvertrags
        - Bewertung von Nachforderungen
        - Verhandlung mit Leasinggesellschaft
        - Durchsetzung Ihrer Rechte
        """)
        
        st.markdown("""
        ### 💼 Service
        - Flexible Terminvereinbarung
        - Bundesweiter Vor-Ort-Service
        - 24/7 Erreichbarkeit (Premium/VIP)
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
        ### 📱 Telefon & WhatsApp
        **Telefon:** [+49 89 123 456 78](tel:+498912345678)  
        **WhatsApp:** [+49 176 987 654 32](https://wa.me/4917698765432)
        
        ### 🕒 Öffnungszeiten
        **Mo-Fr:** 8:00 - 18:00 Uhr  
        **Sa:** 9:00 - 14:00 Uhr  
        **So:** Geschlossen
        
        ### 📧 E-Mail
        info@returnguard.de  
        support@returnguard.de
        """)
    
    with col2:
        st.markdown("""
        ### 📍 Standort
        ReturnGuard GmbH  
        Musterstraße 123  
        80333 München
        
        ### 🚗 Anfahrt
        Direkt am Hauptbahnhof München  
        Parkplätze vorhanden  
        Öffentliche Verkehrsmittel:  
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
        
        **Kontakt:**  
        Telefon: +49 89 123 456 78  
        E-Mail: info@returnguard.de
        
        **Umsatzsteuer-ID:** DE123456789
        """)
    
    with tab2:
        st.markdown("""
        ### Datenschutzerklärung
        
        Der Schutz Ihrer persönlichen Daten ist uns wichtig. Wir verarbeiten Ihre Daten 
        ausschließlich auf Grundlage der gesetzlichen Bestimmungen (DSGVO, TKG 2003).
        
        **Datenverarbeitung:**
        - Kontaktdaten (Name, E-Mail, Telefon)
        - Fahrzeugdaten für Gutachten
        - Zahlungsinformationen
        
        **Ihre Rechte:**
        - Auskunft über Ihre gespeicherten Daten
        - Berichtigung unrichtiger Daten
        - Löschung Ihrer Daten
        - Einschränkung der Verarbeitung
        - Widerspruch gegen die Verarbeitung
        """)
    
    with tab3:
        st.markdown("""
        ### Allgemeine Geschäftsbedingungen
        
        **1. Geltungsbereich**  
        Diese AGB gelten für alle Leistungen der ReturnGuard GmbH.
        
        **2. Leistungsumfang**  
        Der Leistungsumfang richtet sich nach dem gebuchten Paket.
        
        **3. Preise und Zahlung**  
        Alle Preise verstehen sich inkl. gesetzlicher MwSt. Zahlung per Rechnung 
        oder Vorkasse möglich.
        
        **4. Haftung**  
        Wir haften für Vorsatz und grobe Fahrlässigkeit.
        
        **5. Widerrufsrecht**  
        Sie haben ein 14-tägiges Widerrufsrecht ab Vertragsschluss.
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown('''
    <div style="text-align: center; color: #5F6B7A; padding: 30px 20px; font-size: 0.9rem;">
        © 2024 ReturnGuard GmbH - Ihr Partner für faire Leasingrückgaben
    </div>
''', unsafe_allow_html=True)
