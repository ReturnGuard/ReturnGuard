import streamlit as st
import re

# --- 1. KONFIGURATION & ERWEITERTES DESIGN ---
st.set_page_config(page_title="ReturnGuard", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* Hintergrundfarbe */
    .stApp {
        background-color: #f4f4f4;
    }

    /* Hero-Balken */
    .hero-header {
        background: #003366;
        height: 200px;
        position: relative;
        z-index: 0;
        text-align: center;
        color: white;
        padding: 50px 0;
    }

    /* Container für den Inhalt */
    .block-container {
        max-width: 1200px !important;
        padding-top: 20px !important;
        z-index: 1;
    }

    /* Hauptkarte */
    .main-card {
        background-color: white;
        padding: 30px;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.15);
        margin-top: 20px;
        position: relative;
    }

    .hero-title {
        font-size: 2.5rem !important;
        font-weight: bold;
        color
