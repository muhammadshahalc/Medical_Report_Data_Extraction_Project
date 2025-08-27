#med_app.py
import streamlit as st

st.set_page_config(page_title="Medical Report App", layout="wide")

st.title("🏥 Medical Report Extraction & Accuracy Checker")
st.write(
    """
    Use the sidebar to navigate between pages:
    1. **Extraction** – Extract patient info, tests, and diagnosis from PDFs.
    2. **Accuracy Checker** – Compare extracted data with ground truth CSV.
    """
)
