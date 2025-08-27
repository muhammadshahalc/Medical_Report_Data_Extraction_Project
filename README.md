# 🏥 Medical Report Data Extraction Project

## Overview
This project provides an end-to-end solution for extracting, analyzing, and visualizing medical report data. It allows hospitals, clinics, or researchers to process PDF medical reports and generate structured data, perform accuracy checks, and gain actionable insights.

The system uses **PDF text extraction**, **OCR for image-based PDFs**, **NER for medical entities**, and **interactive visualization** to make medical data analysis easy and efficient.

---

## Features

### 1. Extraction
- Extract **Patient Information** (Name, Age, Gender, Report Date) from PDFs.
- Extract **Tests** with values and units.
- Extract **Diagnosis** using regex and medical Named Entity Recognition (NER).
- Handles both **digital and scanned PDFs** using OCR.

### 2. Accuracy Checker
- Compare extracted data with **ground truth CSV**.
- Compute **field-wise and overall accuracy**.
- Identify discrepancies between predicted and actual values.

### 3. Data Visualization
- Interactive **charts and dashboards** for insights.
- Analyze **test and diagnosis frequency**, **gender and age distribution**, and **report timelines**.
- Supports **Altair** and **Plotly** visualizations.

---

## Technologies Used
- **Python 3.10+**
- **Streamlit** – Web interface
- **Spacy** – NLP and medical NER
- **PyMuPDF / pdfplumber** – PDF text extraction
- **Pytesseract** – OCR for scanned PDFs
- **Pandas** – Data handling
- **Altair / Plotly** – Data visualization

---

## Installation

1. Clone the repository:
```bash
git clone https://github.com/muhammadshahalc/Medical_Report_Data_Extraction_Project.git
cd Medical_Report_Data_Extraction_Project

2. Create a virtual environment and activate it.
python -m venv venv

3. Install requirements:
pip install -r requirements.txt

4.Run the Streamlit app.

## Folder Structure
Medical_Report_Data_Extraction_Project/
│
├── medical_extraction/         # Core modules
│   ├── __init__.py
│   ├── pdf_utils.py
│   ├── preprocessing.py
│   ├── extract_info.py
│   └── save_to_csv.py
│
├── pages/                      # Streamlit multi-page app
│   ├── 1_Extraction.py
│   └── 2_Accuracy.py
│
├── med_app.py                  # Main Streamlit app
├── requirements.txt
└── README.md

