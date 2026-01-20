import streamlit as st
from fpdf import FPDF
import datetime

# Branding & Layout
st.set_page_config(page_title="ReturnGuard Pro", layout="wide")
st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { background-color: #f0f2f6; border-radius: 5px; }
    .stTabs [aria-selected="true"] { background-color: #002b5c !important; color: white !important; }
    div[data-testid="stExpander"] { border: 1px solid #002b5c; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ ReturnGuard - Alpha Integration")

# Strukturierung nach Ihren Alpha-Controller Daten
tab1, tab2, tab3, tab4 = st.tabs([
    "👤 Kundendaten", "🚗 Fahrzeugtechnik", "📋 Expert-Check & Smart-Repair", "📤 Export"
])

with tab1:
    st.subheader("Halterinformationen")
    c1, c2 = st.columns(2)
    anrede = c1.selectbox("Anrede", ["Firma", "Herr", "Frau", "keine Angabe"])
    name = c2.text_input("Name / Firma")
    strasse = c1.text_input("Straße & Nr.")
    ort = c2.text_input("PLZ & Ort")
    bemerkung = st.text_area("Interne Notiz (Alpha Controller)", height=100)

with tab2:
    st.subheader("Technische Details")
    t1, t2, t3 = st.columns(3)
    vin = t1.text_input("VIN")
    kz = t2.text_input("Kennzeichen")
    ez = t3.text_input("Erstzulassung")
    
    getriebe = t1.selectbox("Getriebeart", ["Schaltgetriebe", "Automatik", "Doppelkupplung"])
    kraftstoff = t2.selectbox("Kraftstoff", ["Benzin", "Diesel", "Elektro", "Hybrid"])
    plakette = t3.selectbox("Umweltplakette", ["Grün (4)", "Gelb (3)", "Rot (2)", "Keine"])
    
    co2 = t1.number_input("CO2 g/km", value=0)
    leistung = t2.number_input("Leistung (kW)", value=0)

with tab3:
    st.subheader("Experten-Check (14-Punkte Vest Standard)")
    st.info("Falls ein Mangel gewählt wird, öffnet sich automatisch das Smart-Repair-Feld.")
    
    check_results = {}
    repair_costs = {}
    
    # Fokus-Punkte aus Ihrem Prozess
    points = ["Lackzustand", "Windschutzscheibe", "Felgen vorn", "Felgen hinten", "Innenraum/Polster"]
    
    for p in points:
        col_p, col_r = st.columns([2, 1])
        with col_p:
            status = st.select_slider(f"Zustand {p}", options=["Mangel", "Gebrauch", "i.O."], value="i.O.")
            check_results[p] = status
        
        with col_r:
            if status == "Mangel":
                cost = st.number_input(f"Kosten {p} (€)", step=50, key=f"cost_{p}")
                repair_costs[p] = cost
            else:
                repair_costs[p] = 0

with tab4:
    st.subheader("Protokoll-Abschluss")
    summe = sum(repair_costs.values())
    st.metric("Voraussichtliche Minderwerte (Smart-Repair)", f"{summe} €")
    
    if st.button("🚀 Finales PDF-Gutachten erstellen"):
        # PDF Logik (vereinfacht für Test)
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, "ReturnGuard - Offizielles Gutachten", ln=True, align='C')
        pdf.set_font("Arial", size=12)
        pdf.ln(10)
        pdf.cell(0, 10, f"Fahrzeug: {vin} | Kennzeichen: {kz}", ln=True)
        pdf.cell(0, 10, f"Gesamter Minderwert: {summe} EUR", ln=True)
        
        pdf_out = pdf.output(dest='S').encode('latin-1', 'replace')
        st.download_button("📥 PDF Herunterladen", data=pdf_out, file_name=f"Gutachten_{kz}.pdf")
