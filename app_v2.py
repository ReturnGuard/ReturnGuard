"""
ReturnGuard Landingpage v2.0
Enterprise SaaS Style (inspiriert von thalamusgme.com)
"""

import streamlit as st

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="ReturnGuard – Leasingrückgabe ohne Stress",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== CSS DESIGN SYSTEM ====================
def inject_css():
    """Injiziert das komplette CSS Design-System"""
    st.markdown("""
    <style>
    /* ===== RESET & BASE ===== */
    .stApp {
        background: #ffffff;
    }

    .stApp > header {
        background: transparent;
    }

    section[data-testid="stSidebar"] {
        display: none;
    }

    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }

    /* ===== DESIGN TOKENS ===== */
    :root {
        --color-primary: #0f4c75;
        --color-primary-dark: #0a3a5c;
        --color-primary-light: #1b6ca8;
        --color-accent: #00a896;
        --color-accent-light: #02c8a7;
        --color-text: #1a202c;
        --color-text-muted: #64748b;
        --color-bg: #ffffff;
        --color-bg-soft: #f8fafc;
        --color-bg-muted: #f1f5f9;
        --color-border: #e2e8f0;
        --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
        --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.1);
        --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.1);
        --radius-sm: 6px;
        --radius-md: 12px;
        --radius-lg: 16px;
        --max-width: 1200px;
    }

    /* ===== TYPOGRAPHY ===== */
    .rg-h1 {
        font-size: clamp(2.5rem, 5vw, 3.5rem);
        font-weight: 700;
        color: var(--color-text);
        line-height: 1.2;
        margin: 0 0 1rem 0;
    }

    .rg-h2 {
        font-size: clamp(1.75rem, 3vw, 2.25rem);
        font-weight: 700;
        color: var(--color-text);
        line-height: 1.3;
        margin: 0 0 1rem 0;
    }

    .rg-h3 {
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--color-text);
        margin: 0 0 0.5rem 0;
    }

    .rg-subtitle {
        font-size: 1.125rem;
        color: var(--color-text-muted);
        line-height: 1.6;
        margin: 0;
    }

    .rg-body {
        font-size: 1rem;
        color: var(--color-text-muted);
        line-height: 1.6;
    }

    /* ===== LAYOUT ===== */
    .rg-container {
        max-width: var(--max-width);
        margin: 0 auto;
        padding: 0 24px;
    }

    .rg-section {
        padding: 80px 24px;
    }

    .rg-section-soft {
        background: var(--color-bg-soft);
    }

    .rg-grid-2 {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 48px;
        align-items: center;
    }

    .rg-grid-3 {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 24px;
    }

    .rg-grid-4 {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 20px;
    }

    .rg-grid-6 {
        display: grid;
        grid-template-columns: repeat(6, 1fr);
        gap: 16px;
    }

    @media (max-width: 1024px) {
        .rg-grid-2 { grid-template-columns: 1fr; gap: 32px; }
        .rg-grid-4 { grid-template-columns: repeat(2, 1fr); }
        .rg-grid-6 { grid-template-columns: repeat(3, 1fr); }
    }

    @media (max-width: 768px) {
        .rg-grid-3 { grid-template-columns: 1fr; }
        .rg-grid-4 { grid-template-columns: 1fr; }
        .rg-grid-6 { grid-template-columns: repeat(2, 1fr); }
        .rg-section { padding: 48px 16px; }
    }

    /* ===== BUTTONS ===== */
    .rg-btn {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        padding: 14px 28px;
        font-size: 1rem;
        font-weight: 600;
        border-radius: var(--radius-sm);
        text-decoration: none;
        cursor: pointer;
        transition: all 0.2s ease;
        border: none;
    }

    .rg-btn-primary {
        background: var(--color-accent);
        color: white !important;
    }

    .rg-btn-primary:hover {
        background: var(--color-accent-light);
        transform: translateY(-1px);
        box-shadow: var(--shadow-md);
    }

    .rg-btn-secondary {
        background: transparent;
        color: var(--color-primary) !important;
        border: 2px solid var(--color-border);
    }

    .rg-btn-secondary:hover {
        border-color: var(--color-primary);
        background: var(--color-bg-soft);
    }

    /* ===== CARDS ===== */
    .rg-card {
        background: white;
        border-radius: var(--radius-md);
        padding: 24px;
        box-shadow: var(--shadow-sm);
        border: 1px solid var(--color-border);
        transition: all 0.2s ease;
    }

    .rg-card:hover {
        box-shadow: var(--shadow-md);
        transform: translateY(-2px);
    }

    .rg-card-icon {
        width: 48px;
        height: 48px;
        background: var(--color-bg-soft);
        border-radius: var(--radius-sm);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        margin-bottom: 16px;
    }

    /* ===== HEADER ===== */
    .rg-header {
        position: sticky;
        top: 0;
        z-index: 1000;
        background: white;
        border-bottom: 1px solid var(--color-border);
        padding: 0 24px;
    }

    .rg-header-inner {
        max-width: var(--max-width);
        margin: 0 auto;
        display: flex;
        align-items: center;
        justify-content: space-between;
        height: 72px;
    }

    .rg-logo {
        display: flex;
        align-items: center;
        gap: 12px;
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--color-primary);
        text-decoration: none;
    }

    .rg-logo-icon {
        width: 40px;
        height: 40px;
        background: var(--color-primary);
        border-radius: var(--radius-sm);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 1.25rem;
    }

    .rg-nav {
        display: flex;
        align-items: center;
        gap: 32px;
    }

    .rg-nav-link {
        color: var(--color-text-muted);
        text-decoration: none;
        font-weight: 500;
        font-size: 0.95rem;
        transition: color 0.2s;
    }

    .rg-nav-link:hover {
        color: var(--color-primary);
    }

    @media (max-width: 768px) {
        .rg-nav { display: none; }
    }

    /* ===== HERO ===== */
    .rg-hero {
        padding: 80px 24px 100px;
        background: linear-gradient(180deg, var(--color-bg-soft) 0%, white 100%);
    }

    .rg-hero-inner {
        max-width: var(--max-width);
        margin: 0 auto;
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 64px;
        align-items: center;
    }

    .rg-hero-visual {
        background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-light) 100%);
        border-radius: var(--radius-lg);
        padding: 48px;
        min-height: 400px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 1.125rem;
        text-align: center;
    }

    @media (max-width: 1024px) {
        .rg-hero-inner { grid-template-columns: 1fr; text-align: center; }
        .rg-hero-visual { min-height: 300px; }
    }

    /* ===== LOGO ROW ===== */
    .rg-logos {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 48px;
        flex-wrap: wrap;
        padding: 48px 24px;
        border-bottom: 1px solid var(--color-border);
    }

    .rg-logo-item {
        color: var(--color-text-muted);
        font-size: 0.875rem;
        font-weight: 500;
        opacity: 0.6;
        padding: 12px 24px;
        background: var(--color-bg-soft);
        border-radius: var(--radius-sm);
    }

    /* ===== KPI SECTION ===== */
    .rg-kpi-card {
        text-align: center;
        padding: 32px;
    }

    .rg-kpi-number {
        font-size: 3rem;
        font-weight: 700;
        color: var(--color-primary);
        margin-bottom: 8px;
    }

    .rg-kpi-label {
        font-size: 1rem;
        font-weight: 600;
        color: var(--color-text);
        margin-bottom: 4px;
    }

    .rg-kpi-desc {
        font-size: 0.875rem;
        color: var(--color-text-muted);
    }

    /* ===== FEATURE SECTIONS ===== */
    .rg-feature-visual {
        background: var(--color-bg-muted);
        border-radius: var(--radius-lg);
        padding: 48px;
        min-height: 320px;
        display: flex;
        align-items: center;
        justify-content: center;
        border: 1px solid var(--color-border);
    }

    .rg-feature-list {
        list-style: none;
        padding: 0;
        margin: 24px 0;
    }

    .rg-feature-list li {
        padding: 8px 0;
        padding-left: 28px;
        position: relative;
        color: var(--color-text-muted);
    }

    .rg-feature-list li::before {
        content: "✓";
        position: absolute;
        left: 0;
        color: var(--color-accent);
        font-weight: 700;
    }

    /* ===== ADDON GRID ===== */
    .rg-addon-card {
        background: white;
        border: 1px solid var(--color-border);
        border-radius: var(--radius-md);
        padding: 24px;
        text-align: center;
        transition: all 0.2s;
    }

    .rg-addon-card:hover {
        border-color: var(--color-accent);
        box-shadow: var(--shadow-md);
    }

    .rg-addon-icon {
        font-size: 2rem;
        margin-bottom: 12px;
    }

    /* ===== TESTIMONIALS ===== */
    .rg-testimonial {
        background: white;
        border: 1px solid var(--color-border);
        border-radius: var(--radius-md);
        padding: 32px;
    }

    .rg-testimonial-quote {
        font-size: 1.125rem;
        font-style: italic;
        color: var(--color-text);
        margin-bottom: 24px;
        line-height: 1.6;
    }

    .rg-testimonial-author {
        font-weight: 600;
        color: var(--color-text);
    }

    .rg-testimonial-role {
        font-size: 0.875rem;
        color: var(--color-text-muted);
    }

    /* ===== INSIGHTS ===== */
    .rg-insight-card {
        background: white;
        border: 1px solid var(--color-border);
        border-radius: var(--radius-md);
        overflow: hidden;
    }

    .rg-insight-img {
        height: 160px;
        background: var(--color-bg-muted);
        display: flex;
        align-items: center;
        justify-content: center;
        color: var(--color-text-muted);
    }

    .rg-insight-body {
        padding: 24px;
    }

    .rg-insight-date {
        font-size: 0.75rem;
        color: var(--color-text-muted);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
    }

    /* ===== FINAL CTA ===== */
    .rg-cta-section {
        background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-primary-dark) 100%);
        padding: 80px 24px;
        text-align: center;
        color: white;
    }

    .rg-cta-section .rg-h2 {
        color: white;
    }

    .rg-cta-section .rg-subtitle {
        color: rgba(255,255,255,0.8);
        margin-bottom: 32px;
    }

    /* ===== FOOTER ===== */
    .rg-footer {
        background: var(--color-text);
        color: white;
        padding: 64px 24px 32px;
    }

    .rg-footer-inner {
        max-width: var(--max-width);
        margin: 0 auto;
    }

    .rg-footer-grid {
        display: grid;
        grid-template-columns: 2fr 1fr 1fr 1fr 1fr;
        gap: 48px;
        margin-bottom: 48px;
    }

    .rg-footer-brand {
        font-size: 1.25rem;
        font-weight: 700;
        margin-bottom: 16px;
    }

    .rg-footer-desc {
        color: rgba(255,255,255,0.6);
        font-size: 0.875rem;
        line-height: 1.6;
    }

    .rg-footer-title {
        font-weight: 600;
        margin-bottom: 16px;
        font-size: 0.875rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .rg-footer-links {
        list-style: none;
        padding: 0;
        margin: 0;
    }

    .rg-footer-links li {
        margin-bottom: 8px;
    }

    .rg-footer-links a {
        color: rgba(255,255,255,0.6);
        text-decoration: none;
        font-size: 0.875rem;
        transition: color 0.2s;
    }

    .rg-footer-links a:hover {
        color: white;
    }

    .rg-footer-bottom {
        border-top: 1px solid rgba(255,255,255,0.1);
        padding-top: 32px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.875rem;
        color: rgba(255,255,255,0.5);
    }

    @media (max-width: 1024px) {
        .rg-footer-grid { grid-template-columns: 1fr 1fr; }
    }

    @media (max-width: 768px) {
        .rg-footer-grid { grid-template-columns: 1fr; }
        .rg-footer-bottom { flex-direction: column; gap: 16px; text-align: center; }
    }

    /* ===== FORM STYLING ===== */
    .rg-form {
        background: white;
        border-radius: var(--radius-lg);
        padding: 48px;
        box-shadow: var(--shadow-lg);
        max-width: 600px;
        margin: 0 auto;
    }

    /* Hide Streamlit Elements */
    #MainMenu, footer, .stDeployButton { display: none !important; }

    </style>
    """, unsafe_allow_html=True)


# ==================== COMPONENTS ====================

def render_header():
    """Sticky Header mit Logo, Navigation und CTA"""
    st.markdown('''
    <div class="rg-header">
        <div class="rg-header-inner">
            <a href="#top" class="rg-logo">
                <div class="rg-logo-icon">🛡️</div>
                ReturnGuard
            </a>
            <nav class="rg-nav">
                <a href="#features" class="rg-nav-link">So funktioniert's</a>
                <a href="#services" class="rg-nav-link">Leistungen</a>
                <a href="#faq" class="rg-nav-link">FAQ</a>
                <a href="#contact" class="rg-nav-link">Kontakt</a>
            </nav>
            <a href="#contact" class="rg-btn rg-btn-primary">Kostenlose Beratung</a>
        </div>
    </div>
    ''', unsafe_allow_html=True)


def render_hero():
    """Hero Section mit Headline, Subline und Visual"""
    st.markdown('''
    <div class="rg-hero" id="top">
        <div class="rg-hero-inner">
            <div class="rg-hero-content">
                <h1 class="rg-h1">Leasingrückgabe<br>ohne böse Überraschungen</h1>
                <p class="rg-subtitle" style="margin-bottom: 32px;">
                    Schäden vorab einschätzen, Kosten verstehen, optimal vorbereitet sein –
                    bevor die Leasinggesellschaft Ihnen die Rechnung präsentiert.
                </p>
                <div style="display: flex; gap: 16px; flex-wrap: wrap;">
                    <a href="#contact" class="rg-btn rg-btn-primary">Kostenlose Beratung anfordern</a>
                    <a href="#features" class="rg-btn rg-btn-secondary">So funktioniert's</a>
                </div>
            </div>
            <div class="rg-hero-visual">
                <div>
                    <div style="font-size: 3rem; margin-bottom: 16px;">📊</div>
                    <div style="font-weight: 600; margin-bottom: 8px;">Produktvorschau</div>
                    <div style="opacity: 0.8; font-size: 0.875rem;">
                        Digitaler Fahrzeugzustands-Check<br>
                        mit Kosteneinschätzung
                    </div>
                </div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)


def render_logo_row():
    """Partner/Trust Logos"""
    st.markdown('''
    <div class="rg-logos">
        <div class="rg-logo-item">Partner A</div>
        <div class="rg-logo-item">Partner B</div>
        <div class="rg-logo-item">Partner C</div>
        <div class="rg-logo-item">Partner D</div>
        <div class="rg-logo-item">Partner E</div>
        <div class="rg-logo-item">Partner F</div>
    </div>
    ''', unsafe_allow_html=True)


def render_kpis():
    """KPI Stats Section"""
    st.markdown('''
    <div class="rg-section">
        <div class="rg-container">
            <div class="rg-grid-3">
                <div class="rg-kpi-card">
                    <div class="rg-kpi-number">2.500€</div>
                    <div class="rg-kpi-label">Durchschnittliche Ersparnis</div>
                    <div class="rg-kpi-desc">(Beispiel)</div>
                </div>
                <div class="rg-kpi-card">
                    <div class="rg-kpi-number">1.200+</div>
                    <div class="rg-kpi-label">Betreute Rückgaben</div>
                    <div class="rg-kpi-desc">(Beispiel)</div>
                </div>
                <div class="rg-kpi-card">
                    <div class="rg-kpi-number">200+</div>
                    <div class="rg-kpi-label">Partner im Netzwerk</div>
                    <div class="rg-kpi-desc">(Beispiel)</div>
                </div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)


def render_feature_sections():
    """Feature Sections mit abwechselndem Layout"""
    st.markdown('''
    <div class="rg-section rg-section-soft" id="features">
        <div class="rg-container">
            <div style="text-align: center; margin-bottom: 64px;">
                <h2 class="rg-h2">So funktioniert ReturnGuard</h2>
                <p class="rg-subtitle">In wenigen Schritten zur optimalen Rückgabe-Vorbereitung</p>
            </div>

            <!-- Feature 1 -->
            <div class="rg-grid-2" style="margin-bottom: 80px;">
                <div>
                    <h3 class="rg-h3" style="color: var(--color-accent);">Schritt 1</h3>
                    <h2 class="rg-h2">Leasingende einordnen</h2>
                    <p class="rg-body">Wann läuft Ihr Leasingvertrag aus? Je nach Zeitraum empfehlen wir unterschiedliche Vorgehensweisen.</p>
                    <ul class="rg-feature-list">
                        <li>Unter 1 Monat: Schnelle Schadensprüfung</li>
                        <li>1–3 Monate: Zeit für Smart Repair</li>
                        <li>3–6 Monate: Optimale Planungsphase</li>
                        <li>Über 6 Monate: Frühzeitige Vorsorge</li>
                    </ul>
                </div>
                <div class="rg-feature-visual">
                    <div style="text-align: center; color: var(--color-text-muted);">
                        <div style="font-size: 3rem; margin-bottom: 16px;">📅</div>
                        Zeitraum-Auswahl Interface
                    </div>
                </div>
            </div>

            <!-- Feature 2 -->
            <div class="rg-grid-2" style="margin-bottom: 80px;">
                <div class="rg-feature-visual" style="order: 1;">
                    <div style="text-align: center; color: var(--color-text-muted);">
                        <div style="font-size: 3rem; margin-bottom: 16px;">✅</div>
                        Schaden-Checkliste Interface
                    </div>
                </div>
                <div style="order: 2;">
                    <h3 class="rg-h3" style="color: var(--color-accent);">Schritt 2</h3>
                    <h2 class="rg-h2">Schäden strukturiert erfassen</h2>
                    <p class="rg-body">Welche Bereiche Ihres Fahrzeugs weisen mögliche Mängel auf?</p>
                    <ul class="rg-feature-list">
                        <li>Kratzer & Lackschäden</li>
                        <li>Dellen & Beulen</li>
                        <li>Felgenschäden</li>
                        <li>Glasschäden (Windschutzscheibe, etc.)</li>
                        <li>Innenraum-Schäden</li>
                        <li>Unsicher? Wir helfen!</li>
                    </ul>
                </div>
            </div>

            <!-- Feature 3 -->
            <div class="rg-grid-2">
                <div>
                    <h3 class="rg-h3" style="color: var(--color-accent);">Schritt 3</h3>
                    <h2 class="rg-h2">Klare Empfehlung erhalten</h2>
                    <p class="rg-body">Auf Basis Ihrer Angaben erhalten Sie eine erste Einschätzung und konkrete nächste Schritte.</p>
                    <ul class="rg-feature-list">
                        <li>Vorläufige Kosteneinschätzung</li>
                        <li>Empfehlung: Reparieren oder nicht?</li>
                        <li>Vermittlung an geprüfte Partner</li>
                        <li>Dokumentationsunterstützung</li>
                    </ul>
                    <a href="#contact" class="rg-btn rg-btn-primary" style="margin-top: 24px;">Jetzt starten</a>
                </div>
                <div class="rg-feature-visual">
                    <div style="text-align: center; color: var(--color-text-muted);">
                        <div style="font-size: 3rem; margin-bottom: 16px;">📋</div>
                        Ergebnis & Empfehlungs-Dashboard
                    </div>
                </div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)


def render_addon_grid():
    """Add-on/Module Grid"""
    st.markdown('''
    <div class="rg-section" id="services">
        <div class="rg-container">
            <div style="text-align: center; margin-bottom: 48px;">
                <h2 class="rg-h2">Unsere Leistungen</h2>
                <p class="rg-subtitle">Modulare Services für Ihre Leasingrückgabe</p>
            </div>

            <div class="rg-grid-3">
                <div class="rg-addon-card">
                    <div class="rg-addon-icon">🔍</div>
                    <h3 class="rg-h3">Gutachter-Check</h3>
                    <p class="rg-body">Unabhängige Fahrzeugbewertung durch zertifizierte Sachverständige</p>
                </div>
                <div class="rg-addon-card">
                    <div class="rg-addon-icon">✨</div>
                    <h3 class="rg-h3">Aufbereitung</h3>
                    <p class="rg-body">Professionelle Innen- und Außenreinigung vor der Rückgabe</p>
                </div>
                <div class="rg-addon-card">
                    <div class="rg-addon-icon">🔧</div>
                    <h3 class="rg-h3">Smart Repair</h3>
                    <p class="rg-body">Kostengünstige Reparatur von Kleinschäden</p>
                </div>
                <div class="rg-addon-card">
                    <div class="rg-addon-icon">🏭</div>
                    <h3 class="rg-h3">Werkstatt-Netzwerk</h3>
                    <p class="rg-body">Zugang zu geprüften Partnerwerkstätten bundesweit</p>
                </div>
                <div class="rg-addon-card">
                    <div class="rg-addon-icon">📸</div>
                    <h3 class="rg-h3">Dokumentation</h3>
                    <p class="rg-body">Lückenlose Fotodokumentation des Fahrzeugzustands</p>
                </div>
                <div class="rg-addon-card">
                    <div class="rg-addon-icon">📝</div>
                    <h3 class="rg-h3">Rückgabe-Strategie</h3>
                    <p class="rg-body">Individuelle Beratung für optimale Verhandlungsposition</p>
                </div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)


def render_audience_tabs():
    """Zielgruppen-Tabs mit st.tabs"""
    st.markdown('''
    <div class="rg-section rg-section-soft">
        <div class="rg-container">
            <div style="text-align: center; margin-bottom: 48px;">
                <h2 class="rg-h2">Für wen ist ReturnGuard?</h2>
                <p class="rg-subtitle">Lösungen für verschiedene Anforderungen</p>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    # Streamlit Tabs
    tab1, tab2, tab3 = st.tabs(["🚗 Privatkunden", "🏢 Flottenmanager", "🤝 Partner"])

    with tab1:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            ### Transparenz
            Verstehen Sie, welche Kosten auf Sie zukommen könnten – bevor die Leasinggesellschaft entscheidet.
            """)
        with col2:
            st.markdown("""
            ### Vorbereitung
            Optimal vorbereitet in die Rückgabe gehen. Wir zeigen, was sich zu reparieren lohnt.
            """)
        with col3:
            st.markdown("""
            ### Unterstützung
            Bei Streitfällen: Zugang zu spezialisierten Fachanwälten und unabhängigen Gutachtern.
            """)

    with tab2:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            ### Standardisierung
            Ein Prozess für alle Fahrzeuge Ihrer Flotte – unabhängig von Hersteller oder Leasinggeber.
            """)
        with col2:
            st.markdown("""
            ### Planbarkeit
            Fixe Konditionen, kalkulierbare Kosten, weniger Überraschungen bei der Rückgabe.
            """)
        with col3:
            st.markdown("""
            ### Effizienz
            Weniger Verwaltungsaufwand durch zentrale Koordination und digitale Dokumentation.
            """)

    with tab3:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            ### Qualifizierte Leads
            Erhalten Sie vorqualifizierte Anfragen von Kunden mit konkretem Reparaturbedarf.
            """)
        with col2:
            st.markdown("""
            ### Netzwerk
            Werden Sie Teil unseres bundesweiten Partner-Netzwerks für Werkstätten und Gutachter.
            """)
        with col3:
            st.markdown("""
            ### Wachstum
            Erschließen Sie den wachsenden Markt der Leasingrückgaben als neuen Geschäftsbereich.
            """)


def render_testimonials():
    """Testimonials Section"""
    st.markdown('''
    <div class="rg-section">
        <div class="rg-container">
            <div style="text-align: center; margin-bottom: 48px;">
                <h2 class="rg-h2">Das sagen unsere Kunden</h2>
                <p class="rg-subtitle">Erfahrungen aus der Praxis</p>
            </div>

            <div class="rg-grid-3">
                <div class="rg-testimonial">
                    <p class="rg-testimonial-quote">"Die Leasinggesellschaft wollte über 4.000€. Dank ReturnGuard konnte ich das auf unter 1.500€ reduzieren."</p>
                    <p class="rg-testimonial-author">Max M.</p>
                    <p class="rg-testimonial-role">Privatkunde, BMW 3er</p>
                </div>
                <div class="rg-testimonial">
                    <p class="rg-testimonial-quote">"Endlich ein Anbieter, der uns als Flottenmanager versteht. Standardisierte Prozesse für alle 45 Fahrzeuge."</p>
                    <p class="rg-testimonial-author">Sandra K.</p>
                    <p class="rg-testimonial-role">Fuhrparkleiterin, Mittelstand</p>
                </div>
                <div class="rg-testimonial">
                    <p class="rg-testimonial-quote">"Ich wusste nicht, dass man bei einer Leasingrückgabe so viel falsch machen kann. Gut, dass ich ReturnGuard gefunden habe."</p>
                    <p class="rg-testimonial-author">Thomas R.</p>
                    <p class="rg-testimonial-role">Privatkunde, Audi A4</p>
                </div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)


def render_insights():
    """News/Insights Grid"""
    st.markdown('''
    <div class="rg-section rg-section-soft">
        <div class="rg-container">
            <div style="text-align: center; margin-bottom: 48px;">
                <h2 class="rg-h2">Wissen & Insights</h2>
                <p class="rg-subtitle">Tipps und Neuigkeiten rund um die Leasingrückgabe</p>
            </div>

            <div class="rg-grid-3">
                <div class="rg-insight-card">
                    <div class="rg-insight-img">📄 Bild-Platzhalter</div>
                    <div class="rg-insight-body">
                        <p class="rg-insight-date">Januar 2026</p>
                        <h3 class="rg-h3">5 häufige Fehler bei der Leasingrückgabe</h3>
                        <p class="rg-body">Was Sie unbedingt vermeiden sollten, um keine bösen Überraschungen zu erleben.</p>
                        <a href="#" class="rg-nav-link" style="color: var(--color-accent);">Mehr lesen →</a>
                    </div>
                </div>
                <div class="rg-insight-card">
                    <div class="rg-insight-img">📄 Bild-Platzhalter</div>
                    <div class="rg-insight-body">
                        <p class="rg-insight-date">Dezember 2025</p>
                        <h3 class="rg-h3">Smart Repair vs. Werkstatt: Was lohnt sich?</h3>
                        <p class="rg-body">Wann kleine Reparaturen sinnvoll sind und wann Sie besser verzichten.</p>
                        <a href="#" class="rg-nav-link" style="color: var(--color-accent);">Mehr lesen →</a>
                    </div>
                </div>
                <div class="rg-insight-card">
                    <div class="rg-insight-img">📄 Bild-Platzhalter</div>
                    <div class="rg-insight-body">
                        <p class="rg-insight-date">November 2025</p>
                        <h3 class="rg-h3">Leasingrückgabe: Ihre Rechte kennen</h3>
                        <p class="rg-body">Was die Leasinggesellschaft verlangen darf – und was nicht.</p>
                        <a href="#" class="rg-nav-link" style="color: var(--color-accent);">Mehr lesen →</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)


def render_final_cta():
    """Final CTA Section"""
    st.markdown('''
    <div class="rg-cta-section" id="contact">
        <div class="rg-container">
            <h2 class="rg-h2">Bereit für eine stressfreie Leasingrückgabe?</h2>
            <p class="rg-subtitle">Lassen Sie uns gemeinsam Ihre Situation analysieren – kostenlos und unverbindlich.</p>
        </div>
    </div>
    ''', unsafe_allow_html=True)


def render_contact_form():
    """Kontaktformular"""
    st.markdown("""
    <div class="rg-section">
        <div class="rg-container">
            <div class="rg-form">
                <h3 class="rg-h2" style="text-align: center; margin-bottom: 32px;">Kostenlose Beratung anfordern</h3>
    """, unsafe_allow_html=True)

    # Formular mit Streamlit Widgets
    with st.form("contact_form", clear_on_submit=False):
        st.markdown("**Wann endet Ihr Leasingvertrag?** *")
        leasingende = st.selectbox(
            "Leasingende",
            ["Bitte wählen...", "Unter 1 Monat", "1–3 Monate", "3–6 Monate", "Über 6 Monate"],
            key="form_leasingende",
            label_visibility="collapsed"
        )

        st.markdown("**Welche Schäden sind vorhanden?**")
        col1, col2 = st.columns(2)
        with col1:
            kratzer = st.checkbox("Kratzer & Lackschäden", key="form_kratzer")
            dellen = st.checkbox("Dellen & Beulen", key="form_dellen")
            felgen = st.checkbox("Felgenschäden", key="form_felgen")
        with col2:
            glas = st.checkbox("Glasschäden", key="form_glas")
            innen = st.checkbox("Innenraum-Schäden", key="form_innen")
            unsicher = st.checkbox("Nicht sicher / Sonstiges", key="form_unsicher")

        st.markdown("**Ihre Nachricht** (optional)")
        nachricht = st.text_area(
            "Nachricht",
            placeholder="Beschreiben Sie kurz Ihre Situation...",
            key="form_nachricht",
            label_visibility="collapsed"
        )

        st.markdown("**Fotos hochladen** (optional, max. 5)")
        fotos = st.file_uploader(
            "Fotos",
            type=["jpg", "jpeg", "png"],
            accept_multiple_files=True,
            key="form_fotos",
            label_visibility="collapsed"
        )
        if fotos and len(fotos) > 5:
            st.warning("Maximal 5 Fotos erlaubt.")

        st.markdown("---")
        st.caption("*Hinweis: Dies ist Version 1 – Fotos werden noch nicht verarbeitet/gespeichert.*")

        submitted = st.form_submit_button(
            "Kostenlose Beratung anfordern",
            use_container_width=True,
            type="primary"
        )

        if submitted:
            if leasingende == "Bitte wählen...":
                st.error("Bitte wählen Sie, wann Ihr Leasingvertrag endet.")
            else:
                st.success("Vielen Dank! Wir melden uns innerhalb von 24 Stunden bei Ihnen.")

    st.markdown("</div></div></div>", unsafe_allow_html=True)


def render_footer():
    """Footer"""
    st.markdown('''
    <div class="rg-footer">
        <div class="rg-footer-inner">
            <div class="rg-footer-grid">
                <div>
                    <div class="rg-footer-brand">🛡️ ReturnGuard</div>
                    <p class="rg-footer-desc">
                        Die unabhängige Plattform für Leasingrückgaben in Deutschland.
                        Wir verbinden Kunden mit Gutachtern, Werkstätten und Experten.
                    </p>
                </div>
                <div>
                    <div class="rg-footer-title">Produkt</div>
                    <ul class="rg-footer-links">
                        <li><a href="#features">So funktioniert's</a></li>
                        <li><a href="#services">Leistungen</a></li>
                        <li><a href="#">Preise</a></li>
                    </ul>
                </div>
                <div>
                    <div class="rg-footer-title">Ressourcen</div>
                    <ul class="rg-footer-links">
                        <li><a href="#">Blog</a></li>
                        <li><a href="#faq">FAQ</a></li>
                        <li><a href="#">Ratgeber</a></li>
                    </ul>
                </div>
                <div>
                    <div class="rg-footer-title">Unternehmen</div>
                    <ul class="rg-footer-links">
                        <li><a href="#">Über uns</a></li>
                        <li><a href="#">Partner werden</a></li>
                        <li><a href="#contact">Kontakt</a></li>
                    </ul>
                </div>
                <div>
                    <div class="rg-footer-title">Rechtliches</div>
                    <ul class="rg-footer-links">
                        <li><a href="#">Impressum</a></li>
                        <li><a href="#">Datenschutz</a></li>
                        <li><a href="#">AGB</a></li>
                    </ul>
                </div>
            </div>
            <div class="rg-footer-bottom">
                <div>© 2026 ReturnGuard. Alle Rechte vorbehalten.</div>
                <div>Made with ❤️ in Deutschland</div>
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)


# ==================== MAIN APP ====================
def main():
    # CSS injizieren
    inject_css()

    # Sections rendern
    render_header()
    render_hero()
    render_logo_row()
    render_kpis()
    render_feature_sections()
    render_addon_grid()
    render_audience_tabs()
    render_testimonials()
    render_insights()
    render_final_cta()
    render_contact_form()
    render_footer()


if __name__ == "__main__":
    main()
