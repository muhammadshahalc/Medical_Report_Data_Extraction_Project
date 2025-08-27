
import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate

# Load environment variables
load_dotenv()

# Initialize Groq LLM
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model="llama3-70b-8192"
)

# Streamlit UI
st.title("🩺 Medical Remedies Assistant")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    if "Diagnosis" not in df.columns or "Patient Name" not in df.columns:
        st.error("❌ The file must contain both 'Diagnosis' and 'Patient Name' columns.")
    else:
        st.success("✅ File uploaded successfully!")
        st.dataframe(df.head())

        # Strict system-style prompt
        template = (
            "You are a highly knowledgeable and reliable medical assistant. "
            "Your role is to provide accurate, concise explanations and remedies "
            "based strictly on the given diagnosis provided below. "
            "If the diagnosis is unclear or not provided, reply exactly with: "
            "'I don’t know based on the available diagnosis.' "
            "Do not include this phrase if the diagnosis is clear. "
            "Limit your answer to a maximum of four sentences, "
            "and keep the language clear, direct, and professional.\n\n"
            "Patient Name: {patient_name}\n"
            "Diagnosis: {diagnosis}\n\n"
            "Recommended Remedies and Lifestyle Suggestions:"
        )
        prompt = PromptTemplate(template=template, input_variables=["diagnosis", "patient_name"])

        # Generate remedies
        results = []
        for _, row in df.dropna(subset=["Diagnosis", "Patient Name"]).iterrows():
            query = prompt.format(diagnosis=row["Diagnosis"], patient_name=row["Patient Name"])
            response = llm.invoke(query)
            results.append({
                "Patient Name": row["Patient Name"],
                "Diagnosis": row["Diagnosis"],
                "Remedies": response.content
            })

        result_df = pd.DataFrame(results)
        st.subheader("📋 Remedies and Solutions")
        st.dataframe(result_df)

        # Option to download
        csv = result_df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download Remedies CSV", csv, "remedies.csv", "text/csv")
