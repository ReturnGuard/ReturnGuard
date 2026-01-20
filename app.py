import streamlit as st
from fpdf import FPDF
import datetime

# Design & Branding
st.set_page_config(page_title="ReturnGuard Pro", layout="wide")
st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #f0f2f6; border-radius: 5px; padding: 10px; }
    .stTabs [aria-selected="true"] { background-color: #002b5c !format; color: white !format; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ ReturnGuard - Alpha Controller Integration")

# Struktur über Tabs (wie in Ihrer Software)
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "👤 Fahrzeughalter", "🚗 Fahrzeugdaten", "⛽ Kraftstoff/Umwelt", "🛠️ Vorschäden", "📋 Expert-Check"
])

with tab1:
    st.subheader("Fahrzeughalter / Grunddaten")
    col1, col2, col3 = st.columns(3)
    anrede = col1.selectbox("Anrede", ["keine Angabe", "Herr", "Frau", "Firma"])
    name = col2.text_input("Name/Firma")
    vorname = col3.text_input("Vorname")
    strasse = col1.text_input("Straße & Nr.")
    plz = col2.text_input("PLZ")
    ort = col3.text_input("Ort")
    bemerkung = st.text_area("Interne Bemerkung", height=100)

with tab2:
    st.subheader("Technische Fahrzeugdaten")
    c1, c2, c3 = st.columns(3)
    vin = c1.text_input("VIN (Fahrgestellnummer)")
    kz = c2.text_input("Amtliches Kennzeichen")
    ez = c3.text_input("Erstzulassung (MM/JJJJ)")
    hersteller = c1.text_input("Hersteller")
    modell = c2.text_input("Modell")
    leistung = c3.number_input("Leistung (kW)", step=1)
    km = c1.number_input("Kilometerstand (aktuell)", step=1)
    km_max = c2.number_input("Max. KM-Stand bei Übergabe", step=1)

with tab3:
    st.subheader("Kraftstoff & Emissionen")
    e1, e2 = st.columns(2)
    kraftstoff = e1.selectbox("Kraftstoffart", ["keine Angabe", "Benzin", "Diesel", "Elektro", "Hybrid"])
    batterie = e2.number_input("HV-Batterie (kWh)", step=0.1)
    co2 = e1.text_input("CO2-Emission (kombiniert g/km)")
    effizienz = e2.selectbox("Energieeffizienz", ["keine Angabe", "A+", "A", "B", "C", "D"])

with tab4:
    st.subheader("Vorschäden & Historie")
    v1, v2 = st.columns(2)
    unfallfrei = v1.checkbox("Fahrzeug ist unfallfrei")
    nachlackierung = v2.selectbox("Nachlackierung", ["Nicht vorhanden", "Vorhanden", "Unbekannt"])
    tech_mangel = st.text_area("Technische Mängel / Sonstiges")
    rauer = st.radio("Raucherfahrzeug", ["k.A.", "Ja", "Nein"], horizontal=True)

with tab5:
    st.subheader("Modularer Experten-Check (Vest Standard)")
    # Hier nutzen wir Ihre 14-Punkte Logik
    check_results = {}
    points = ["Lackzustand", "Reifenprofil", "Bremsen", "Innenraum", "Beleuchtung", "Windschutzscheibe"]
    for p in points:
        check_results[p] = st.select_slider(f"{p}:", options=["Mangel", "Gebrauch", "i.O."], value="i.O.")

# PDF Export Funktion (vereinfacht für alle neuen Felder)
def create_pro_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "ReturnGuard PRO - Zustandsbericht", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(0, 10, f"Halter: {name} | Fahrzeug: {hersteller} {modell}", ln=True)
    pdf.cell(0, 10, f"VIN: {vin} | Kennzeichen: {kz}", ln=True)
    pdf.ln(5)
    pdf.cell(0, 10, "Zustandspunkte:", ln=True)
    for k, v in check_results.items():
        pdf.cell(100, 8, f"{k}: {v}", ln=True)
    return pdf.output(dest='S').encode('latin-1', 'replace')

st.divider()
if st.button("🚀 Gesamten Datensatz finalisieren & PDF generieren"):
    if not vin:
        st.error("Bitte mindestens die VIN in Tab 2 eingeben.")
    else:
        pdf_out = create_pro_pdf()
        st.download_button("📥 Profi-Bericht herunterladen", data=pdf_out, file_name=f"Bericht_{kz}.pdf")
