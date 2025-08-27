import streamlit as st
import pandas as pd
from collections import Counter
import altair as alt

st.set_page_config(page_title="Medical Data Analytics", layout="wide")

st.title("📊 Medical Data Analytics Dashboard")
st.write(
    """
    Explore extracted medical reports: field completeness, test/diagnosis frequency, 
    gender/age distribution, and report timeline.
    """
)

# Upload CSV 
uploaded_csv = st.file_uploader("Upload Extracted Medical CSV", type=["csv"])

if uploaded_csv:
    df = pd.read_csv(uploaded_csv)
    
    # Convert Report Date to datetime
    df['Report Date'] = pd.to_datetime(df['Report Date'], dayfirst=True, errors='coerce')

    # Field Completeness
    st.subheader("📌 Field Completeness")
    missing_counts = df.isna().sum()
    st.bar_chart(missing_counts)
    st.write("Missing fields per column:", missing_counts)

    # Filters
    st.sidebar.header("Filters")
    genders = df['Gender'].dropna().unique().tolist()
    selected_gender = st.sidebar.multiselect("Select Gender", options=genders, default=genders)

    age_min = int(df['Age'].min())
    age_max = int(df['Age'].max())
    selected_age = st.sidebar.slider("Select Age Range", min_value=age_min, max_value=age_max,
                                     value=(age_min, age_max))

    filtered_df = df[
        df['Gender'].isin(selected_gender) &
        df['Age'].between(selected_age[0], selected_age[1])
    ]

    # Test Frequency
    st.subheader("🧪 Test Frequency")
    all_tests = []
    for tests in filtered_df['Tests'].dropna():
        for t in tests.split(';'):
            t_name = t.split(':')[0].strip()
            all_tests.append(t_name)
    test_counts = Counter(all_tests)
    test_df = pd.DataFrame(test_counts.items(), columns=['Test', 'Frequency']).sort_values(by='Frequency', ascending=False)

    test_chart = alt.Chart(test_df).mark_bar().encode(
        x=alt.X('Test', sort='-y'),
        y='Frequency',
        tooltip=['Test', 'Frequency']
    )
    st.altair_chart(test_chart.properties(height=400), use_container_width=True)

    # Diagnosis Frequency 
    st.subheader("💉 Diagnosis Frequency")
    all_diag = []
    for diag in filtered_df['Diagnosis'].dropna():
        for d in diag.split(','):
            all_diag.append(d.strip().lower())
    diag_counts = Counter(all_diag)
    diag_df = pd.DataFrame(diag_counts.items(), columns=['Diagnosis', 'Frequency']).sort_values(by='Frequency', ascending=False)

    diag_chart = alt.Chart(diag_df).mark_bar(color="#f28e2b").encode(
        x=alt.X('Diagnosis', sort='-y'),
        y='Frequency',
        tooltip=['Diagnosis', 'Frequency']
    )
    st.altair_chart(diag_chart.properties(height=400), use_container_width=True)

    # Gender Distribution 
    st.subheader("👥 Gender Distribution")
    gender_chart = alt.Chart(filtered_df).mark_bar().encode(
        x='Gender',
        y='count()',
        color='Gender'
    )
    st.altair_chart(gender_chart, use_container_width=True)

    # Age Distribution 
    st.subheader("📈 Age Distribution")
    age_chart = alt.Chart(filtered_df).mark_bar().encode(
        x='Age',
        y='count()',
        color='Gender'
    )
    st.altair_chart(age_chart, use_container_width=True)

    # Report Timeline 
    st.subheader("🗓️ Reports Over Time")
    timeline_chart = alt.Chart(filtered_df).mark_line(point=True, color="#4e79a7").encode(
        x='Report Date',
        y='count()',
        tooltip=['Report Date', 'count()']
    )
    st.altair_chart(timeline_chart.properties(height=300), use_container_width=True)

    # Preview Filtered Data
    st.subheader("📝 Filtered Data Preview")
    st.dataframe(filtered_df)
