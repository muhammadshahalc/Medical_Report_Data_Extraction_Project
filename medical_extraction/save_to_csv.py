#save_to_csv.py
import pandas as pd
from typing import Dict, List, Union

def save_medical_info_one_row_per_patient(all_results: Dict[str, List[Dict[str, Union[str,List[Dict[str,str]],List[str]]]]], output_csv: str):
    rows = []
    for file_path, reports in all_results.items():
        for report in reports:
            tests_combined = "; ".join([f"{t['Test']}: {t['Value']} {t['Unit']}".strip() for t in report.get("Tests", [])]) if report.get("Tests") else ""
            diagnoses_combined = ", ".join(report.get("Diagnosis", []))
            rows.append({
                "File": file_path,
                "Patient Name": report.get("Patient Name", ""),
                "Age": report.get("Age", ""),
                "Gender": report.get("Gender", ""),
                "Report Date": report.get("Report Date", ""),
                "Tests": tests_combined,
                "Diagnosis": diagnoses_combined
            })
    df = pd.DataFrame(rows)
    df.replace("", pd.NA, inplace=True)
    df.to_csv(output_csv, index=False)
    print(f"CSV saved at: {output_csv}")
