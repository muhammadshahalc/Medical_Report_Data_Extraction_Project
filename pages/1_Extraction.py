import streamlit as st
from pathlib import Path
import os
import io

from medical_extraction.pdf_utils import extract_text_from_pdfs
from medical_extraction.extract_info import extract_medical_info
from medical_extraction.save_to_csv import save_medical_info
# from medical_extraction.preprocessing import preprocess_text

st.title("📄 Extraction Page")

# Upload PDFs
uploaded_files = st.file_uploader(
    "Upload PDF medical reports",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:
    pdf_paths = []
    os.makedirs("temp_uploads", exist_ok=True)
    for file in uploaded_files:
        temp_path = os.path.join("temp_uploads", file.name)
        with open(temp_path, "wb") as f:
            f.write(file.getbuffer())
        pdf_paths.append(temp_path)

    st.success(f"{len(pdf_paths)} PDFs uploaded!")

    # Extract text
    st.info("Extracting text from PDFs...")
    extracted_texts = extract_text_from_pdfs(pdf_paths)

    # Extract medical info
    st.info("Extracting patient info, tests, and diagnosis...")
    all_results = {Path(fp).name: extract_medical_info(text) for fp, text in extracted_texts.items()}

    # Show DataFrame preview
    import pandas as pd
    rows = []
    for file_name, reports in all_results.items():
        for report in reports:
            tests_combined = "; ".join([f"{t['Test']}: {t['Value']} {t['Unit']}".strip() for t in report.get("Tests", [])])
            diagnoses_combined = ", ".join(report.get("Diagnosis", []))
            rows.append({
                "File": file_name,
                "Patient Name": report.get("Patient Name", ""),
                "Age": report.get("Age", ""),
                "Gender": report.get("Gender", ""),
                "Report Date": report.get("Report Date", ""),
                "Tests": tests_combined,
                "Diagnosis": diagnoses_combined
            })
    df = pd.DataFrame(rows)
    df.replace("", pd.NA, inplace=True)

    st.subheader("Extracted Data")
    st.dataframe(df)

    # Download CSV in memory
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Extracted CSV",
        data=csv_data,
        file_name="extracted_medical_info.csv",
        mime="text/csv"
    )
