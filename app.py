import streamlit as st
from fpdf import FPDF

# Konfiguration
st.set_page_config(page_title="ReturnGuard Pro", layout="wide")

# CSS für echte, farbige Buttons
st.markdown("""
    <style>
    /* Styling für die Radio-Buttons als große Block-Elemente */
    div[data-testid="stWidgetLabel"] {
        font-size: 1.2rem !important;
        font-weight: bold !important;
        margin-bottom: 10px !important;
    }
    
    /* Wir stylen die Radio-Optionen um */
    div[data-testid="stRadio"] div[role="radiogroup"] {
        flex-direction: row !important;
        gap: 10px;
    }

    div[data-testid="stRadio"] label {
        background-color: #e0e0e0; /* Standard Grau */
        padding: 15px 25px !important;
        border-radius: 10px !important;
        border: 2px solid #ccc !important;
        width: 100%;
        text-align: center;
        font-weight: bold;
    }

    /* Farbe wenn ausgewählt: Erster Button (Mangel) */
    div[data-testid="stRadio"] div[role="radiogroup"] > div:nth-child(1) input[checked] + div > div > p::before {
        content: "🚨 ";
    }
    div[data-testid="stRadio"] div[role="radiogroup"] > div:nth-child(1) label[data-baseweb="radio"] div:first-child { display: none; }
    div[data-testid="stRadio"] div[role="radiogroup"] > div:nth-child(1) input[checked] + div {
        background-color: #ff4b4b !important; /* ROT */
        color: white !important;
    }

    /* Farbe wenn ausgewählt: Zweiter Button (Gebrauch) */
    div[data-testid="stRadio"] div[role="radiogroup"] > div:nth-child(2) label[data-baseweb="radio"] div:first-child { display: none; }
    div[data-testid="stRadio"] div[role="radiogroup"] > div:nth-child(2) input[checked] + div {
        background-color: #ffa500 !important; /* GELB */
        color: white !important;
    }

    /* Farbe wenn ausgewählt: Dritter Button (i.O.) */
    div[data-testid="stRadio"] div[role="radiogroup"] > div:nth-child(3) label[data-baseweb="radio"] div:first-child { display: none; }
    div[data-testid="stRadio"] div[role="radiogroup"] > div:nth-child(3) input[checked] + div {
        background-color: #28a745 !important; /* GRÜN */
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ ReturnGuard Mobile")

# Sektionen definieren
sections = {
    "Außenhaut": ["Lackzustand", "Dellen/Beulen", "Kratzer"],
    "Räder": ["Reifenprofil", "Felgenzustand"]
}

costs = {}

for section, items in sections.items():
    st.header(section)
    for item in items:
        # Wir nutzen st.radio, das wir per CSS oben "umgebaut" haben
        choice = st.radio(
            f"{item}:",
            options=["Mangel", "Gebrauch", "i.O."],
            key=f"check_{item}",
            index=2, # Standardmäßig auf i.O.
            horizontal=True
        )
        
        if choice == "Mangel":
            costs[item] = st.number_input(f"Kosten für {item} (€)", min_value=0, step=50, key=f"cost_{item}")
        else:
            costs[item] = 0
    st.divider()

# Zusammenfassung
total = sum(costs.values())
st.metric("Gesamter Minderwert", f"{total} €")

if st.button("🏁 Protokoll abschließen"):
    st.balloons()
    st.success(f"Bericht mit {total}€ Minderwert erstellt.")
