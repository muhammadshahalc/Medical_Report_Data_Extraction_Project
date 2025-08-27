# 🏥 Medical Report Data Extraction Project

## Overview
This project provides an end-to-end solution for extracting, analyzing, and visualizing medical report data. It allows hospitals, clinics, or researchers to process PDF medical reports and generate structured data, perform accuracy checks, and gain actionable insights.

The system uses **PDF text extraction**, **OCR for image-based PDFs**, **NER for medical entities**, and **interactive visualization** to make medical data analysis easy and efficient.

---
## Approach Taken

1. **Text Extraction**

   * Extracted text from PDFs using `pdfplumber` and `pytesseract` (OCR).

2. **Preprocessing**

   * Cleaned the text with using regex rules to fix formats and remove noise.

3. **Information Extraction**

   * **Patient Names** → Identified with spaCy’s `en_core_web_sm` model.
   * **Medical Diagnoses** → Extracted using spaCy’s `en_ner_bc5cdr_md` biomedical NER model, added list of medical terms and keywords.
   * **Other Columns** → Extracted using regex patterns.

4. **Data Storage**

   * Designed a function to save structured results into CSV format.

5. **Code Structure**

   * Refactored exploratory notebook code into a modular Python package for better maintainability.

6. **Streamlit Application**

   * **Page 1** → Data extraction & download
   * **Page 2** → Accuracy evaluation
   * **Page 3** → Data visualization

7. **Visualization**

   * Generated charts and graphs to provide insights into the extracted medical information.

--

## Challenges Faced

1.	**Mix-ups in Entity Detection**

    * The NLP models sometimes confused hospital names with patient names, which messed up the structured output.

2.	**Keeping Data Safe and Accurate**

    * Since the text contains medical details , needed to make sure that no information was changed when processing large files Keeping names, diseases, and results aligned was very important.

3.	**Gaps in Medical Coverage**

    * The medical NLP model used didn’t recognize every diagnosis. To fill these gaps, added lists of medical terms and keywords.

---
## Sample Structured Output

{
  "C:\\Users\\pessh\\Desktop\\Medical Report Data Extraction\\Med_a\\data\\samples\\report_1.pdf": [
    {
      "Patient Name": "John Doe",
      "Age": "45",
      "Gender": "Male",
      "Report Date": "15/08/2025",
      "Tests": [
        {"Test": "Blood Test", "Value": "Normal", "Unit": "ECG"},
        {"Test": "X-ray", "Value": "Detected", "Unit": ""},
        {"Test": "MRI", "Value": "Detected", "Unit": ""},
        {"Test": "blood test", "Value": "Detected", "Unit": ""},
        {"Test": "ECG", "Value": "Detected", "Unit": ""}
      ],
      "Diagnosis": ["Hypertension", "Anemia", "Hypertension"]
    }
  ],

  "C:\\Users\\pessh\\Desktop\\Medical Report Data Extraction\\Med_a\\data\\samples\\report_2.pdf": [
    {
      "Patient Name": "Sarah Lee",
      "Age": "32",
      "Gender": "Female",
      "Report Date": "20-08-2025",
      "Tests": [
        {"Test": "mIU/L Ultrasound Abdomen", "Value": "Normal", "Unit": ""},
        {"Test": "Ultrasound", "Value": "Detected", "Unit": ""},
        {"Test": "Thyroid Function Test", "Value": "Detected", "Unit": ""}
      ],
      "Diagnosis": ["Diabetes", "Hypothyroidism", "Diabetes Mellitus"]
    }
  ]
}


File,Patient Name,Age,Gender,Report Date,Tests,Diagnosis
report_1.pdf,John Doe,45,Male,2025-08-15,"Blood Test: Normal; ECG: Detected; X-ray: Detected; MRI: Detected","Anemia, Hypertension"
report_2.pdf,Sarah Lee,32,Female,2025-08-20,"Ultrasound Abdomen: Normal; Ultrasound: Detected; Thyroid Function Test: Detected","Diabetes Mellitus, Hypothyroidism"
report_3.pdf,Michael Smith,60,Male,2025-08-10,"ECG: Normal; CT Scan: Detected; Blood Test: Detected","Pneumonia"
report_4.pdf,Priya Kumar,28,Female,2025-08-18,"Ultrasound Pelvis: Normal; Pap Smear: Negative; Blood Test: Detected","None"
report_5.pdf,Ahmed Ali,55,Male,2025-08-22,"CT Scan: Detected; Liver Function Test: Detected; Kidney Function Test: Detected","Fatty Liver, Hypertension"
report_6.pdf,Emily Davis,40,Female,2025-08-19,"X-ray Spine: Normal; Blood Test: Normal; X-ray: Detected; MRI: Detected","Lower Back Pain"






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


### 4. Remedies Recommendations

* Powered by **Groq API (LLaMA 3)** for smart and fast suggestions.
* Generate **personalized remedies** and lifestyle tips based on diagnosis.
* Export remedies to **CSV** for easy sharing and tracking.

---

Want me to also tweak your **Data Visualization** section to mention Groq (if it’s being used there too), so everything looks consistent in the README?




















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
│   ├── 2_Accuracy.py
│   ├── 3_Analytics.py
│   └── 4_Remedies.py
│
├── med_app.py                  # Main Streamlit app
├── requirements.txt
└── README.md


