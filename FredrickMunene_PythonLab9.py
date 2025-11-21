# FredrickMunene_PythonLab9.py
# Lab 9 – Hospital Admission Trends Dashboard

import streamlit as st
import pandas as pd

st.title("Hospital Admission Trends Dashboard")
st.write(
    "Upload the hospital dataset to explore admissions over time, "
    "view basic stats, and see monthly trends."
)

# 1. File upload
uploaded_file = st.file_uploader("Upload hospital CSV file", type=["csv"])

if uploaded_file is not None:
    # Read CSV into DataFrame
    df = pd.read_csv(uploaded_file)

    # 2. Display head and tail
    st.subheader("Data Preview")
    st.write("First 5 rows:")
    st.dataframe(df.head())

    st.write("Last 5 rows:")
    st.dataframe(df.tail())

    # 3. Summary stats for numeric columns
    st.subheader("Summary Statistics (Numeric Columns)")
    st.dataframe(df.describe())

    # --- Date column selection & conversion ---
    st.subheader("Admission Date Column")

    # Try to detect datetime columns
    datetime_cols = df.select_dtypes(include=["datetime64[ns]"]).columns.tolist()

    # If no true datetime columns yet, let user pick any column and we'll parse it
    if datetime_cols:
        st.write("Detected date-like columns:", ", ".join(datetime_cols))
        default_col = datetime_cols[0]
    else:
        st.write("No datetime columns detected. Please choose the date column to convert.")
        default_col = df.columns[0]

    date_col = st.selectbox("Select the admission date column:", df.columns, index=df.columns.get_loc(default_col))

    # Convert chosen column to datetime
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

    # Drop rows where date failed to parse
    df = df.dropna(subset=[date_col])

    if df.empty:
        st.error("No valid dates found in the selected column. Try another column.")
    else:
        # 4. Calculate number of admissions per month
        st.subheader("Admissions per Month")

        # Create a Month period column (Year-Month)
        df["Month"] = df[date_col].dt.to_period("M")

        monthly_counts = df["Month"].value_counts().sort_index()

        # Show counts as a small table
        st.write("Monthly admission counts:")
        st.dataframe(
            monthly_counts.rename("Admissions")
            .reset_index()
            .rename(columns={"Month": "Month"})
        )

        # 5. Visualize monthly admissions (bar or line)
        chart_type = st.radio("Choose chart type:", ["Bar chart", "Line chart"])

        monthly_counts_df = monthly_counts.reset_index()
        monthly_counts_df.columns = ["Month", "Admissions"]

        # Convert Period to string like "Jan-2017" for nice labels
        monthly_counts_df["Month"] = monthly_counts_df["Month"].dt.strftime("%b-%Y")

        st.subheader("Monthly Admission Trend Chart")

        if chart_type == "Bar chart":
            st.bar_chart(data=monthly_counts_df, x="Month", y="Admissions")
        else:
            st.line_chart(data=monthly_counts_df, x="Month", y="Admissions")
else:
    st.info("Please upload the hospital CSV file to begin.")
