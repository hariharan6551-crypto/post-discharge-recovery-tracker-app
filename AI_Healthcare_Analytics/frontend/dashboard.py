import streamlit as st
import pandas as pd

from backend.chart_generator import line_chart, pie_chart
from backend.ml_model import predict_future
from backend.ai_agent import ask_ai

st.set_page_config(layout="wide")

st.title("Post-Discharge Social Support and Recovery Tracker")

uploaded_file = st.file_uploader("Upload Dataset", type=["csv","xlsx"])

if uploaded_file:

    if uploaded_file.name.endswith("csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

else:

    df = pd.read_excel("hospital_readmission_dataset.xlsx")



# Sidebar Filters

st.sidebar.header("Filters")

year = st.sidebar.multiselect(
    "Select Year",
    df["Year_numeric"].unique(),
    default=df["Year_numeric"].unique()
)

sex = st.sidebar.multiselect(
    "Select Sex",
    df["Sex Breakdown"].unique(),
    default=df["Sex Breakdown"].unique()
)

filtered_df = df[
    (df["Year_numeric"].isin(year)) &
    (df["Sex Breakdown"].isin(sex))
]



# KPI Metrics

col1,col2,col3 = st.columns(3)

col1.metric(
    "Average Indicator Value",
    round(filtered_df["Avg_Indicator"].mean(),2)
)

col2.metric(
    "Total Numerator",
    int(filtered_df["Total_Numerator"].sum())
)

col3.metric(
    "Total Denominator",
    int(filtered_df["Total_Denominator"].sum())
)



# Charts

st.subheader("Average Indicator Value by Year")

fig1 = line_chart(filtered_df)

st.plotly_chart(fig1,use_container_width=True)



st.subheader("Numerator Distribution by Sex")

fig2 = pie_chart(filtered_df)

st.plotly_chart(fig2)



# Dataset Table

st.subheader("Aggregated Dataset")

st.dataframe(filtered_df)



# AI Prediction Panel

st.subheader("AI Prediction Panel")

future_year = st.number_input("Enter Future Year", 2025)

prediction = predict_future(df, future_year)

st.success(f"Predicted Indicator Value for {future_year}: {prediction}")



# AI Assistant

st.subheader("AI Chat Assistant")

question = st.text_input("Ask a question about the dataset")

if question:

    answer = ask_ai(question, df)

    st.write(answer)