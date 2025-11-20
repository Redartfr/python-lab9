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
    except pd.errors.EmptyDataError:
        st.error("The uploaded file is empty or not a valid CSV/Excel file.")
        st.stop()

    st.subheader("Data Preview")

    # 2a. Head
    st.markdown("**First 5 rows (head):**")
    st.dataframe(df.head())

    # 2b. Tail
    st.markdown("**Last 5 rows (tail):**")
    st.dataframe(df.tail())

    # 3. Summary statistics
    st.subheader("Summary Statistics (Numeric Columns)")
    st.dataframe(df.describe(include="number"))

    # 4. Let user choose which column is the date
    st.subheader("Select Date Column")
    date_col = st.selectbox("Choose the date column for admissions:", df.columns)

    # Convert chosen column to datetime
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

    if df[date_col].isna().all():
        st.error(
            f"Could not parse any dates from column '{date_col}'. "
            "Please choose a different column or check the dataset."
        )
        st.stop()

    # 4. Count admissions per month
    # Create Month label like 'Jan-2017'
    df["Month"] = df[date_col].dt.strftime("%b-%Y")

    monthly_counts = df["Month"].value_counts().sort_index()

    st.subheader("Monthly Admission Counts")
    st.dataframe(monthly_counts)

    # 5. Monthly Admissions Chart
    st.subheader("Monthly Admission Trend Chart")

    monthly_counts_df = monthly_counts.reset_index()
    monthly_counts_df.columns = ["Month", "count"]

    st.bar_chart(monthly_counts_df, x="Month", y="count")

else:
    st.info("Please upload a dataset to begin.")
