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

# ------------------------------------------------
# Title
# ------------------------------------------------

st.title("Post Discharge Social Support and Recovery Tracker")

# ------------------------------------------------
# Upload Dataset
# ------------------------------------------------

uploaded_file = st.file_uploader("Upload Healthcare Dataset", type=["csv", "xlsx"])

if uploaded_file is None:
    st.info("Upload dataset to continue")
    st.stop()

# ------------------------------------------------
# Load Dataset
# ------------------------------------------------

if uploaded_file.name.endswith("csv"):
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_excel(uploaded_file)

df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

# ------------------------------------------------
# Detect Columns
# ------------------------------------------------

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

    if "indicator" in col or "rate" in col or "avg" in col:
        avg_col = col

    if "numerator" in col or "count" in col:
        num_col = col

    if "denominator" in col or "total" in col:
        den_col = col

numeric_cols = df.select_dtypes(include="number").columns

if avg_col is None:
    avg_col = numeric_cols[0]

if num_col is None:
    num_col = numeric_cols[1]

if den_col is None:
    den_col = numeric_cols[-1]

# ------------------------------------------------
# SIDEBAR FILTERS
# ------------------------------------------------

st.sidebar.header("Dashboard Filters")

if year_col:
    selected_year = st.sidebar.selectbox(
        "Select Year",
        sorted(df[year_col].dropna().unique())
    )
else:
    selected_year = None

if sex_col:
    selected_gender = st.sidebar.multiselect(
        "Select Gender",
        df[sex_col].dropna().unique(),
        default=df[sex_col].dropna().unique()
    )
else:
    selected_gender = []

# ------------------------------------------------
# Filter Dataset
# ------------------------------------------------

filtered_df = df.copy()

if year_col and selected_year is not None:
    filtered_df = filtered_df[filtered_df[year_col] == selected_year]

if sex_col:
    filtered_df = filtered_df[filtered_df[sex_col].isin(selected_gender)]

# ------------------------------------------------
# AI Chat Assistant
# ------------------------------------------------

st.sidebar.subheader("AI Healthcare Assistant")

question = st.sidebar.text_input("Ask about recovery trends")

if question:
    response = ask_ai(question, filtered_df)
    st.sidebar.write(response)

# ------------------------------------------------
# KPI Metrics
# ------------------------------------------------

st.subheader("Post-Discharge Recovery Metrics")

total_patients = int(filtered_df[num_col].sum())
total_population = int(filtered_df[den_col].sum())

support_coverage = 0
if total_population > 0:
    support_coverage = round((total_patients / total_population) * 100, 2)

avg_recovery = round(filtered_df[avg_col].mean(), 2)
followup_rate = round(filtered_df[avg_col].median(), 2)

k1, k2, k3, k4, k5 = st.columns(5)

k1.metric("Avg Recovery Indicator", avg_recovery)
k2.metric("Patients Monitored", total_patients)
k3.metric("Total Population", total_population)
k4.metric("Support Coverage %", f"{support_coverage}%")
k5.metric("Avg Follow-up Rate", followup_rate)

# ------------------------------------------------
# Row 1 Charts
# ------------------------------------------------

col1, col2 = st.columns([2, 1])

with col1:

    st.subheader("Recovery Indicator by Gender")

    cluster_chart = px.bar(
        filtered_df,
        x=sex_col if sex_col else year_col,
        y=avg_col,
        color=sex_col if sex_col else None,
        barmode="group"
    )

    st.plotly_chart(cluster_chart, use_container_width=True)

with col2:

    st.subheader("Social Support Distribution")

    donut_chart = px.pie(
        filtered_df,
        names=sex_col if sex_col else year_col,
        values=num_col,
        hole=0.55
    )

    st.plotly_chart(donut_chart, use_container_width=True)

# ------------------------------------------------
# Row 2 Charts
# ------------------------------------------------

col3, col4 = st.columns(2)

with col3:

    st.subheader("Recovery Trend")

    trend_chart = px.line(
        filtered_df,
        x=year_col if year_col else avg_col,
        y=avg_col,
        color=sex_col if sex_col else None,
        markers=True
    )

    st.plotly_chart(trend_chart, use_container_width=True)

with col4:

    st.subheader("Support Comparison")

    comparison_chart = px.bar(
        filtered_df,
        x=sex_col if sex_col else year_col,
        y=avg_col,
        color=sex_col if sex_col else None
    )

    st.plotly_chart(comparison_chart, use_container_width=True)

# ------------------------------------------------
# Prediction Section
# ------------------------------------------------

st.subheader("Recovery Forecast")

future_year = st.number_input(
    "Enter Prediction Year",
    min_value=2000,
    max_value=2100,
    value=2025
)

prediction = predict_future(filtered_df, future_year)

st.success(f"Predicted Recovery Indicator for {future_year}: {prediction}")

future_years = np.arange(future_year, future_year + 5)

pred_values = [predict_future(filtered_df, y) for y in future_years]

pred_df = pd.DataFrame({
    "Year": future_years,
    "Predicted Recovery": pred_values
})

forecast_chart = px.line(
    pred_df,
    x="Year",
    y="Predicted Recovery",
    markers=True
)

st.plotly_chart(forecast_chart, use_container_width=True)

# ------------------------------------------------
# Dataset Table
# ------------------------------------------------

st.subheader("Filtered Dataset")

st.dataframe(filtered_df)