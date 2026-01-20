import streamlit as st
from fpdf import FPDF

st.set_page_config(page_title="ReturnGuard Pro", layout="wide")

# DAS ERZWUNGENE FARB-DESIGN FÜR SEGMENTED CONTROL
st.markdown("""
    <style>
    /* 1. Grund-Styling der Buttons nebeneinander */
    div[data-testid="stSegmentedControl"] button {
        height: 55px !important;
        font-weight: bold !important;
        flex: 1 !important; /* Macht alle Buttons gleich breit */
    }

    /* 2. MANGEL (Rot) - Wenn der erste Button aktiv ist */
    div[data-testid="stSegmentedControl"] [data-testid="stBaseButton-secondary"]:nth-of-type(1)[aria-checked="true"] {
        background-color: #ff4b4b !important;
        color: white !important;
    }

    /* 3. GEBRAUCH (Gelb) - Wenn der zweite Button aktiv ist */
    div[data-testid="stSegmentedControl"] [data-testid="stBaseButton-secondary"]:nth-of-type(2)[aria-checked="true"] {
        background-color: #ffa500 !important;
        color: white !important;
    }

    /* 4. I.O. (Grün) - Wenn der dritte Button aktiv ist */
    div[data-testid="stSegmentedControl"] [data-testid="stBaseButton-secondary"]:nth-of-type(3)[aria-checked="true"] {
        background-color: #28a745 !important;
        color: white !important;
    }
    
    /* Hover-Effekte stabilisieren */
    div[data-testid="stSegmentedControl"] button:hover {
        border-color: #002b5c !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ ReturnGuard - Experten-Check")

# Workflow in Sektionen (Modular wie gewünscht)
sections = {
    "Außenhaut": ["Lackzustand", "Dellen/Beulen", "Kratzer"],
    "Räder/Fahrwerk": ["Reifenprofil", "Felgenzustand"]
}

check_results = {}
repair_costs = {}

for section, items in sections.items():
    st.subheader(section)
    for item in items:
        # Hier ist das schöne Element nebeneinander
        choice = st.segmented_control(
            label=f"**{item}**",
            options=["Mangel", "Gebrauch", "i.O."],
            key=f"check_{item}",
            default="i.O."
        )
        check_results[item] = choice
        
        # Smart-Repair Feld nur bei Mangel
        if choice == "Mangel":
            repair_costs[item] = st.number_input(f"Kosten {item} (€)", min_value=0, step=50, key=f"cost_{item}")
        else:
            repair_costs[item] = 0
    st.divider()

# Auswertung
total = sum(repair_costs.values())
st.metric("Voraussichtlicher Minderwert", f"{total} €")

if st.button("🏁 Protokoll abschließen"):
    st.balloons()
    st.success("Daten gespeichert. PDF kann generiert werden.")
