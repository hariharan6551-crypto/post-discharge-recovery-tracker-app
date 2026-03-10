import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

from backend.ml_model import predict_future
from backend.ai_agent import ask_ai

st.set_page_config(layout="wide")

st.title("AI Healthcare Readmission Risk Dashboard")

# -----------------------------
# Upload Dataset
# -----------------------------

uploaded_file = st.file_uploader("Upload Dataset", type=["csv","xlsx"])

if uploaded_file is None:
    st.info("Upload the hospital dataset to continue")
    st.stop()

# -----------------------------
# Load Dataset
# -----------------------------

if uploaded_file.name.endswith("csv"):
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_excel(uploaded_file)

# -----------------------------
# Clean Column Names
# -----------------------------

df.columns = df.columns.str.strip().str.lower().str.replace(" ","_")

# -----------------------------
# Auto Detect Columns
# -----------------------------

year_col = None
sex_col = None
avg_col = None
num_col = None
den_col = None

for col in df.columns:

    if "year" in col:
        year_col = col

    if "sex" in col or "gender" in col:
        sex_col = col

    if "avg" in col or "indicator" in col or "rate" in col:
        avg_col = col

    if "numerator" in col or "count" in col:
        num_col = col

    if "denominator" in col or "total" in col:
        den_col = col

# fallback for numeric columns
numeric_cols = df.select_dtypes(include="number").columns

if avg_col is None:
    avg_col = numeric_cols[0]

if num_col is None:
    num_col = numeric_cols[1]

if den_col is None:
    den_col = numeric_cols[-1]

# -----------------------------
# Sidebar Filters
# -----------------------------

st.sidebar.title("Filters")

if year_col:
    years = st.sidebar.multiselect(
        "Select Year",
        sorted(df[year_col].dropna().unique()),
        default=sorted(df[year_col].dropna().unique())
    )
else:
    years = []

if sex_col:
    sex = st.sidebar.multiselect(
        "Select Sex",
        df[sex_col].dropna().unique(),
        default=df[sex_col].dropna().unique()
    )
else:
    sex = []

filtered_df = df.copy()

if year_col:
    filtered_df = filtered_df[filtered_df[year_col].isin(years)]

if sex_col:
    filtered_df = filtered_df[filtered_df[sex_col].isin(sex)]

# -----------------------------
# AI Chat Assistant
# -----------------------------

st.sidebar.subheader("AI Chat Assistant")

question = st.sidebar.text_input("Ask about dataset")

if question:
    response = ask_ai(question, filtered_df)
    st.sidebar.write(response)

# -----------------------------
# KPI Metrics
# -----------------------------

st.subheader("Healthcare KPIs")

c1,c2,c3 = st.columns(3)

c1.metric("Average Indicator", round(filtered_df[avg_col].mean(),2))
c2.metric("Total Numerator", int(filtered_df[num_col].sum()))
c3.metric("Total Denominator", int(filtered_df[den_col].sum()))

# -----------------------------
# Line Chart
# -----------------------------

if year_col:
    st.subheader("Indicator Trend")

    line = px.line(
        filtered_df,
        x=year_col,
        y=avg_col,
        color=sex_col if sex_col else None,
        markers=True
    )

    st.plotly_chart(line,use_container_width=True)

# -----------------------------
# Bar Chart
# -----------------------------

st.subheader("Indicator Comparison")

bar = px.bar(
    filtered_df,
    x=year_col if year_col else avg_col,
    y=avg_col,
    color=sex_col if sex_col else None
)

st.plotly_chart(bar,use_container_width=True)

# -----------------------------
# Donut Chart
# -----------------------------

st.subheader("Distribution by Sex")

donut = px.pie(
    filtered_df,
    names=sex_col if sex_col else avg_col,
    values=num_col,
    hole=0.5
)

st.plotly_chart(donut)

# -----------------------------
# Funnel Chart
# -----------------------------

st.subheader("Healthcare Funnel")

funnel = px.funnel(
    filtered_df,
    x=num_col,
    y=sex_col if sex_col else year_col
)

st.plotly_chart(funnel)

# -----------------------------
# Prediction Visualization
# -----------------------------

st.subheader("Future Prediction")

future_year = st.number_input("Enter Future Year",2025)

prediction = predict_future(filtered_df,future_year)

st.success(f"Predicted Indicator Value for {future_year}: {prediction}")

# Predict next 5 years

future_years = np.arange(future_year,future_year+5)

pred_values = [predict_future(filtered_df,y) for y in future_years]

pred_df = pd.DataFrame({
    "Year":future_years,
    "Predicted Indicator":pred_values
})

pred_chart = px.line(
    pred_df,
    x="Year",
    y="Predicted Indicator",
    markers=True
)

st.plotly_chart(pred_chart,use_container_width=True)

# -----------------------------
# Dataset Table
# -----------------------------

st.subheader("Dataset")

st.dataframe(filtered_df)