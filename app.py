import streamlit as st
from fpdf import FPDF
import datetime

# Design-Einstellungen
st.set_page_config(page_title="ReturnGuard", layout="centered")
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    stButton>button { background-color: #002b5c; color: white; border-radius: 5px; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ ReturnGuard - Ihr Leasing-Schutz")
st.subheader("Experten-Check nach Vest Automotive Standards")

# Formular-Daten
with st.expander("📄 Fahrzeugdaten & Prüfer", expanded=True):
    col1, col2 = st.columns(2)
    vin = col1.text_input("VIN (Fahrgestellnummer)")
    kennzeichen = col2.text_input("Amtliches Kennzeichen")
    km = col1.number_input("Kilometerstand", step=1, value=0)
    gutachter = col2.text_input("Name des Gutachters")

# Die 14 Punkte Logik in Sektionen
check_daten = {}
sections = {
    "Außenhaut & Karosserie": ["Lackzustand", "Dellen/Beulen", "Kratzer", "Steinschläge"],
    "Fahrwerk & Räder": ["Reifenprofil", "Felgenzustand", "Bremsanlage"],
    "Verglasung & Optik": ["Windschutzscheibe", "Beleuchtung", "Spiegel"],
    "Innenraum & Technik": ["Sitze/Polster", "Geruch/Raucher", "Armaturen", "Funktionstest"]
}

for section, punkte in sections.items():
    st.header(section)
    for punkt in punkte:
        check_daten[punkt] = st.select_slider(
            f"{punkt}:",
            options=["Mangelhaft", "Gebrauchsspuren", "Einwandfrei"],
            value="Einwandfrei"
        )

# PDF-Generator Logik
def create_pdf(vin, kz, km, name, check_results):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="ReturnGuard - Zustandsbericht", ln=True, align='C')
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt=f"Erstellt am: {datetime.date.today()}", ln=True, align='C')
    
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Fahrzeugdaten:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"VIN: {vin} | Kennzeichen: {kz}", ln=True)
    pdf.cell(0, 10, f"KM-Stand: {km} | Prüfer: {name}", ln=True)
    
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Prüfungsergebnisse:", ln=True)
    pdf.set_font("Arial", size=10)
    
    for punkt, status in check_results.items():
        pdf.cell(100, 8, txt=f"{punkt}:", border=1)
        pdf.cell(80, 8, txt=f"{status}", border=1, ln=True)
    
    return pdf.output(dest='S').encode('latin-1', 'replace')

# Abschluss
st.divider()
if st.button("✅ Bericht finalisieren & PDF erstellen"):
    if not vin or not kennzeichen:
        st.error("Bitte mindestens VIN und Kennzeichen angeben!")
    else:
        pdf_data = create_pdf(vin, kennzeichen, km, gutachter, check_daten)
        st.success("Bericht erfolgreich generiert!")
        st.download_button(
            label="📥 PDF-Bericht herunterladen",
            data=pdf_data,
            file_name=f"ReturnGuard_{kennzeichen}.pdf",
            mime="application/pdf"
        )
