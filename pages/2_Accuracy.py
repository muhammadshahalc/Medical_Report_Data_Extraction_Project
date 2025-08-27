#2_Accuracy.py
import streamlit as st
import pandas as pd
from pathlib import Path
from medical_extraction.pdf_utils import extract_text_from_pdfs
from medical_extraction.extract_info import extract_medical_info

st.title("📊 Accuracy Checker Page")

# Upload PDFs
uploaded_files = st.file_uploader(
    "Upload PDF medical reports",
    type=["pdf"],
    accept_multiple_files=True
)

# Upload ground truth CSV
ground_truth_file = st.file_uploader(
    "Upload Ground Truth CSV",
    type=["csv"]
)

if uploaded_files and ground_truth_file:
    # Save PDFs temporarily
    pdf_paths = []
    import os
    os.makedirs("temp_uploads", exist_ok=True)
    for file in uploaded_files:
        temp_path = os.path.join("temp_uploads", file.name)
        with open(temp_path, "wb") as f:
            f.write(file.getbuffer())
        pdf_paths.append(temp_path)
    
    st.success(f"{len(pdf_paths)} PDFs uploaded!")

    # Extract text and info
    extracted_texts = extract_text_from_pdfs(pdf_paths)
    all_results = {Path(fp).name: extract_medical_info(text) for fp, text in extracted_texts.items()}

    # Convert to DataFrame
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
    df_pred = pd.DataFrame(rows)
    df_pred.replace("", pd.NA, inplace=True)

    st.subheader("Extracted Data Preview")
    st.dataframe(df_pred)

    # Load ground truth
    df_true = pd.read_csv(ground_truth_file)

    # Accuracy Calculation
    def calculate_accuracy(df_pred, df_true):
        accuracies = {}
        fields = ["Patient Name", "Age", "Gender", "Tests", "Diagnosis"]
        for field in fields:
            correct = 0
            total = 0
            for _, row in df_true.iterrows():
                file_name = row["File"]
                pred_row = df_pred[df_pred["File"] == file_name]
                if pred_row.empty: continue
                pred_val = str(pred_row.iloc[0][field]) if not pd.isna(pred_row.iloc[0][field]) else ""
                true_val = str(row[field]) if not pd.isna(row[field]) else ""

                if field in ["Tests", "Diagnosis"]:
                    pred_set = set([x.strip().lower() for x in pred_val.split(";") if x.strip()]) if pred_val else set()
                    true_set = set([x.strip().lower() for x in true_val.split(";") if x.strip()]) if true_val else set()
                    total += len(true_set)
                    correct += len(pred_set & true_set)
                else:
                    total += 1
                    if pred_val.strip().lower() == true_val.strip().lower():
                        correct += 1
            accuracies[field] = (correct / total) if total > 0 else 0
        return accuracies

    accuracy = calculate_accuracy(df_pred, df_true)
    overall_accuracy = sum(accuracy.values()) / len(accuracy)

    st.write("### Field-wise Accuracy")
    st.json({k: f"{v*100:.2f}%" for k,v in accuracy.items()})
    st.write(f"**Overall Accuracy:** {overall_accuracy*100:.2f}%")
