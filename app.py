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
.hero-subtitle { font-size: 1.3rem; color: white; margin-top: 20px; }

.calculator-box {
    background: white;
    padding: 40px;
    border-radius: 20px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.15);
    margin: 40px 0;
}

.cost-display {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 30px;
    border-radius: 15px;
    text-align: center;
    color: white;
    margin: 20px 0;
}

.savings-box {
    background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    color: white;
    margin: 20px 0;
}

.urgency-banner {
    background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%);
    padding: 20px; border-radius: 15px; text-align: center;
    color: white; font-size: 1.2rem; font-weight: 700; margin: 30px 0;
}

.trust-badges { display: flex; justify-content: center; gap: 30px; margin: 40px 0; flex-wrap: wrap; }
.trust-badge { background: white; padding: 25px; border-radius: 15px; min-width: 180px; text-align: center; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
.trust-icon { font-size: 4rem; margin-bottom: 10px; }
.trust-text { font-size: 1rem; color: #4a5568; font-weight: 600; }

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

div.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white; border: none; padding: 12px 30px; border-radius: 50px; font-weight: 700; width: 100%;
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
    if st.button("💰 Kostenrechner", use_container_width=True): st.session_state.page = 'calculator'; st.rerun()
with nav_cols[4]:
    if st.button("📞 Kontakt", use_container_width=True): st.session_state.page = 'contact'; st.rerun()
with nav_cols[5]:
    if st.button("⚖️ Rechtliches", use_container_width=True): st.session_state.page = 'legal'; st.rerun()

st.markdown("---")

# ========== KOSTENRECHNER ==========
if st.session_state.page == 'calculator':
    st.markdown('<div class="calculator-box">', unsafe_allow_html=True)
    st.title("💰 Kostenrechner - Was könnte Ihre Rückgabe kosten?")
    st.write("Geben Sie die Schäden an Ihrem Fahrzeug ein und sehen Sie die geschätzten Kosten:")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🚗 Exterieur-Schäden")
        
        kratzer = st.selectbox(
            "Kratzer im Lack",
            ["Keine", "Leicht (1-2)", "Mittel (3-5)", "Stark (6+)"],
            help="Oberflächliche Kratzer bis zum Grundlack"
        )
        
        dellen = st.selectbox(
            "Dellen/Beulen",
            ["Keine", "Klein (< 2cm)", "Mittel (2-5cm)", "Groß (> 5cm)"],
            help="Eindrückungen in der Karosserie"
        )
        
        steinschlag = st.selectbox(
            "Steinschläge Frontscheibe",
            ["Keine", "1-2 kleine", "3-5 kleine", "Größer als 5mm"],
            help="Beschädigungen an der Windschutzscheibe"
        )
        
        felgen = st.selectbox(
            "Felgenschäden",
            ["Keine", "Leichte Kratzer", "Tiefe Kratzer", "Verbogen"],
            help="Beschädigungen an den Felgen"
        )
        
        reifen = st.selectbox(
            "Reifenzustand",
            ["Gut (>4mm)", "Grenzwertig (3-4mm)", "Schlecht (<3mm)"],
            help="Profiltiefe der Reifen"
        )
    
    with col2:
        st.subheader("🪑 Interieur-Schäden")
        
        sitze = st.selectbox(
            "Sitze/Polster",
            ["Einwandfrei", "Leichte Abnutzung", "Flecken", "Risse/Löcher"],
            help="Zustand der Sitzbezüge"
        )
        
        lenkrad = st.selectbox(
            "Lenkrad",
            ["Einwandfrei", "Abgenutzt", "Beschädigt"],
            help="Abnutzung am Lenkrad"
        )
        
        armatur = st.selectbox(
            "Armaturenbrett",
            ["Einwandfrei", "Leichte Kratzer", "Risse"],
            help="Zustand des Armaturenbretts"
        )
        
        teppich = st.selectbox(
            "Teppiche/Fußmatten",
            ["Sauber", "Flecken", "Stark verschmutzt"],
            help="Zustand der Teppiche"
        )
        
        geruch = st.selectbox(
            "Geruch (Raucher/Tiere)",
            ["Neutral", "Leicht", "Stark"],
            help="Geruchsbelästigung im Innenraum"
        )
    
    st.markdown("---")
    
    # BERECHNUNG
    kosten = 0
    
    # Exterieur
    if kratzer == "Leicht (1-2)": kosten += 150
    elif kratzer == "Mittel (3-5)": kosten += 400
    elif kratzer == "Stark (6+)": kosten += 800
    
    if dellen == "Klein (< 2cm)": kosten += 200
    elif dellen == "Mittel (2-5cm)": kosten += 500
    elif dellen == "Groß (> 5cm)": kosten += 1000
    
    if steinschlag == "1-2 kleine": kosten += 80
    elif steinschlag == "3-5 kleine": kosten += 150
    elif steinschlag == "Größer als 5mm": kosten += 400
    
    if felgen == "Leichte Kratzer": kosten += 100
    elif felgen == "Tiefe Kratzer": kosten += 300
    elif felgen == "Verbogen": kosten += 800
    
    if reifen == "Grenzwertig (3-4mm)": kosten += 200
    elif reifen == "Schlecht (<3mm)": kosten += 600
    
    # Interieur
    if sitze == "Leichte Abnutzung": kosten += 100
    elif sitze == "Flecken": kosten += 300
    elif sitze == "Risse/Löcher": kosten += 800
    
    if lenkrad == "Abgenutzt": kosten += 150
    elif lenkrad == "Beschädigt": kosten += 400
    
    if armatur == "Leichte Kratzer": kosten += 100
    elif armatur == "Risse": kosten += 400
    
    if teppich == "Flecken": kosten += 150
    elif teppich == "Stark verschmutzt": kosten += 400
    
    if geruch == "Leicht": kosten += 200
    elif geruch == "Stark": kosten += 600
    
    # ERGEBNIS
    if st.button("🔍 Kosten berechnen", use_container_width=True):
        st.markdown(f"""
            <div class="cost-display">
                <h2>Geschätzte Nachzahlung ohne ReturnGuard</h2>
                <h1 style="font-size: 3.5rem; margin: 20px 0;">{kosten:,.0f}€</h1>
                <p style="font-size: 1.1rem;">Diese Kosten könnten auf Sie zukommen!</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Ersparnis berechnen
        if kosten > 0:
            # Mit Premium-Paket (299€)
            ersparnis_premium = kosten * 0.6  # 60% Ersparnis
            restkosten_premium = kosten - ersparnis_premium + 299
            
            st.markdown(f"""
                <div class="savings-box">
                    <h2>💰 Mit ReturnGuard Premium-Paket (299€)</h2>
                    <h3>Ihre Ersparnis: {ersparnis_premium:,.0f}€ (60%)</h3>
                    <h3>Ihre Gesamtkosten: {restkosten_premium:,.0f}€</h3>
                    <p style="font-size: 1.2rem; margin-top: 15px;">
                        ✅ Sie sparen <b>{kosten - restkosten_premium:,.0f}€</b> im Vergleich zu ohne ReturnGuard!
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            st.success("### 🎯 So helfen wir Ihnen:")
            col_a, col_b = st.columns(2)
            with col_a:
                st.write("""
                - ✅ Frühzeitige Schadenserkennung
                - ✅ Günstige Reparatur-Partner
                - ✅ Smart Repair statt Neulackierung
                """)
            with col_b:
                st.write("""
                - ✅ Verhandlung mit Leasinggeber
                - ✅ Rechtliche Prüfung der Forderungen
                - ✅ Professionelle Dokumentation
                """)
            
            st.markdown("---")
            st.markdown("### 📞 Jetzt Beratung sichern!")
            
            col_c1, col_c2, col_c3 = st.columns([1, 2, 1])
            with col_c2:
                email = st.text_input("E-Mail", placeholder="ihre.email@beispiel.de", label_visibility="collapsed")
                if st.button("🚀 Kostenlose Erstberatung anfordern", use_container_width=True):
                    if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
                        st.success("✅ Vielen Dank! Wir kontaktieren Sie innerhalb von 24h.")
                        st.balloons()
                    else:
                        st.error("❌ Bitte gültige E-Mail eingeben.")
        else:
            st.info("🎉 Glückwunsch! Ihr Fahrzeug scheint in sehr gutem Zustand zu sein. Eine Überprüfung lohnt sich trotzdem!")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ========== STARTSEITE ==========
elif st.session_state.page == 'home':
    st.markdown('<div class="hero-section"><h1 class="hero-title">🛡️ Leasingrückgabe für Ihren Audi</h1><p class="hero-subtitle">Schützen Sie sich vor unfairen Nachzahlungen</p></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="urgency-banner">⏰ Nur noch 3 Termine diese Woche verfügbar!</div>', unsafe_allow_html=True)
    
    # Quick Kostenrechner Teaser
    st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px; border-radius: 20px; text-align: center; margin: 30px 0;">
            <h2 style="color: white; font-size: 2rem; margin-bottom: 20px;">💰 Was könnte Ihre Rückgabe kosten?</h2>
            <p style="color: white; font-size: 1.2rem;">Nutzen Sie unseren kostenlosen Kostenrechner!</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔍 Jetzt Kosten berechnen", use_container_width=True, key="calc_teaser"):
        st.session_state.page = 'calculator'
        st.rerun()
    
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

# ========== ANDERE SEITEN ==========
elif st.session_state.page == 'about':
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.title("👥 Über ReturnGuard")
    st.write("Wir helfen Leasingnehmern seit 2020...")
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == 'services':
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.title("📦 Unsere Leistungen")
    st.write("Was wird geprüft?...")
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == 'contact':
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.title("📞 Kontakt")
    st.write("**Telefon:** +49 89 123 456 78")
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == 'legal':
    st.markdown('<div class="content-section">', unsafe_allow_html=True)
    st.title("⚖️ Rechtliches")
    tabs = st.tabs(["AGB", "Datenschutz", "Impressum"])
    with tabs[0]:
        st.write("AGB...")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown('<div style="text-align: center; color: #718096; padding: 20px;">🛡️ ReturnGuard</div>', unsafe_allow_html=True)
