#extract_info.py
import re
from typing import List, Dict, Union
import spacy
from .preprocessing import preprocess_text  # <-- relative import fixed

# Load spaCy models
nlp_general = spacy.load("en_core_web_sm")   # For general entities
nlp_medical = spacy.load("en_ner_bc5cdr_md") # For medical entities

# ------------------- Patient Info -------------------
def extract_patient_info(text: str) -> Dict[str, str]:
    info = {}
    name_match = re.search(r"(?:Patient Name|Name)[:\s]+([A-Za-z\s]+?)(?=\n|Age|$)", text, re.IGNORECASE)
    if name_match: info["Patient Name"] = name_match.group(1).strip()

    age_match = re.search(r"\bAge\b[:=\s]{0,8}(\d{1,3})(?:\s*(?:years?|yrs?|y/o|year-old))?", text, re.IGNORECASE)
    if age_match: info["Age"] = age_match.group(1)

    gender_match = re.search(r"(?:Gender|Sex)[:\s]*(Male|Female|M|F)", text, re.IGNORECASE)
    if gender_match:
        gender = gender_match.group(1)
        info["Gender"] = "Male" if gender.upper() in ["M", "MALE"] else "Female"

    date_match = re.search(r"(?:Report Date|Date)[:\s]*(\d{2}[/-]\d{2}[/-]\d{4})", text, re.IGNORECASE)
    if date_match: info["Report Date"] = date_match.group(1)

    return info

# ------------------- Tests -------------------
def extract_tests(text: str) -> List[Dict[str, str]]:
    tests = []
    test_list = [
        "X-ray","CT scan","MRI","ultrasound","blood test","ECG","echocardiogram","biopsy",
        "urinalysis","stool test","colonoscopy","endoscopy","pulmonary function test",
        "mammogram","Pap smear","bone density test","angiogram","PET scan","lumbar puncture",
        "stress test","Holter monitor","EEG","EMG","allergy test","genetic testing",
        "vital signs","physical examination","glucose tolerance test","thyroid function test",
        "lipid panel","liver function test","kidney function test","coagulation test",
        "C-reactive protein test","troponin test","arterial blood gas","culture and sensitivity",
        "COVID-19 test","influenza test","pregnancy test"
    ]

    # Extract test results section
    test_section_match = re.search(r"(?:Test Results|Laboratory Results)[:\s]*(.*?)(?=Diagnosis|Observations|$)", text, re.IGNORECASE | re.DOTALL)
    if test_section_match:
        test_text = test_section_match.group(1)
        pattern = r"([A-Za-z\s\(\)/\-]+?):\s*([\d\.\-x^/]+|Normal|Abnormal|Positive|Negative)\s*([a-zA-Z/%\^\-\u00B5]*)(?:\s*\([^\)]+\))?"
        for match in re.findall(pattern, test_text, re.IGNORECASE):
            test_name, value, unit = match
            tests.append({"Test": test_name.strip(),"Value": value.strip(),"Unit": unit.strip()})

    # Also detect test mentions
    for test_name in test_list:
        if re.search(r"\b" + re.escape(test_name) + r"\b", text, re.IGNORECASE):
            tests.append({"Test": test_name, "Value": "Detected", "Unit": ""})
    
    return tests

# ------------------- Diagnosis -------------------
def extract_diagnosis(text: str) -> List[str]:
    diagnoses = []

    diag_section_match = re.search(r"(?:Diagnosis|Diagnosis/Observations|Observations|Impression)[:\s]*(.*?)(?=Test Results|Patient|$)", text, re.IGNORECASE | re.DOTALL)
    if diag_section_match:
        diag_text = diag_section_match.group(1)
        doc = nlp_medical(diag_text)
        for ent in doc.ents:
            if ent.label_ == "DISEASE": diagnoses.append(ent.text)

        common_diagnoses = ["diabetes","hypertension","asthma","pneumonia","cancer","stroke",
                            "myocardial infarction","heart failure","arrhythmia","coronary artery disease",
                            "COPD","bronchitis","influenza","tuberculosis","HIV","AIDS","hepatitis",
                            "cirrhosis","GERD","IBS","Crohn's disease","ulcerative colitis","appendicitis",
                            "rheumatoid arthritis","osteoarthritis","osteoporosis","lupus","fibromyalgia",
                            "migraine","epilepsy","Alzheimer's","Parkinson's","multiple sclerosis",
                            "anxiety","depression","bipolar disorder","schizophrenia","anemia",
                            "hyperthyroidism","hypothyroidism","chronic kidney disease","psoriasis","eczema","Early Pregnancy"]
        for diag in common_diagnoses:
            if re.search(r"\b" + diag + r"\b", diag_text, re.IGNORECASE) and diag not in diagnoses:
                diagnoses.append(diag)

    return list(set(diagnoses))

# ------------------- Combine -------------------
def extract_medical_info(text: str) -> List[Dict[str, Union[str,List[Dict[str,str]],List[str]]]]:
    clean_text = preprocess_text(text)
    patient_info = extract_patient_info(clean_text)
    tests = extract_tests(clean_text)
    diagnosis = extract_diagnosis(clean_text)

    return [ {
        "Patient Name": patient_info.get("Patient Name", ""),
        "Age": patient_info.get("Age", ""),
        "Gender": patient_info.get("Gender", ""),
        "Report Date": patient_info.get("Report Date", ""),
        "Tests": tests,
        "Diagnosis": diagnosis
    } ]
