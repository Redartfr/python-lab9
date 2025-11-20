import streamlit as st
import pandas as pd

st.title("Patient Admission Trends Dashboard")
st.write("Upload the hospital dataset to explore admission trends over time.")

# 1. File uploader
uploaded_file = st.file_uploader(
    "Upload hospital dataset (CSV or Excel)",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:
    # 2. Read file safely (CSV or Excel)
    try:
        if uploaded_file.name.lower().endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        # 3. Head & tail preview
        st.subheader("Data Preview (Head & Tail)")
        st.write(df.head())
        st.write(df.tail())

        # 4. Summary statistics
        st.subheader("Summary Statistics")
        st.write(df.describe())

        # 5. Convert date column
        date_col = df.columns[0]  # assumes first column is date
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')

        # Count admissions per month
        df["Month"] = df[date_col].dt.to_period("M")
        monthly_counts = df["Month"].value_counts().sort_index()

        st.subheader("Admissions per Month")
        st.write(monthly_counts)

        # Visual chart
        st.subheader("Monthly Admission Trend Chart")
        
        monthly_counts_df = monthly_counts.reset_index()
        monthly_counts_df["Month"] = monthly_counts_df["Month"].dt.strftime("%b-%Y")
        monthly_counts_df.columns = ["Month", "count"]

        st.bar_chart(monthly_counts_df, x="Month", y="count")

    except Exception as e:
        st.error(f"Error reading file: {e}")
