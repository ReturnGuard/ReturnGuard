import streamlit as st

st.set_page_config(page_title="ReturnGuard", layout="wide")

st.title("🚗 ReturnGuard - Experten-Check")
st.write("Prüfung nach Vest Automotive Standards")

# Die 14 Hauptpunkte in Kategorien unterteilt
kategorien = {
    "Außenhaut": ["Lackzustand", "Dellen/Beulen", "Kratzer", "Steinschläge"],
    "Fahrwerk & Räder": ["Reifenprofil", "Felgenzustand", "Bremsen"],
    "Innenraum": ["Polster/Leder", "Geruch", "Armaturen"],
    "Technik/Glas": ["Beleuchtung", "Windschutzscheibe", "Flüssigkeitsstände", "Fehlerspeicher"]
}

ergebnisse = {}

for kat, punkte in kategorien.items():
    st.header(kat)
    for punkt in punkte:
        ergebnisse[punkt] = st.radio(f"Zustand: {punkt}", ["i.O.", "n.i.O.", "Nicht geprüft"], horizontal=True)

if st.button("Bericht generieren"):
    st.success("Check abgeschlossen! (PDF-Export folgt im nächsten Schritt)")
    st.json(ergebnisse)
