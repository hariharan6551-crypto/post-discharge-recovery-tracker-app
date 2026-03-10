# AI Healthcare Analytics Dashboard

Features:

* Dataset Upload
* Machine Learning Prediction
* AI Insights
* Data Visualization
* KPI Metrics
* Filters
* AI Chat Assistant
* FastAPI Backend
* Streamlit Dashboard
* Power BI Integration

Run Locally:

pip install -r requirements.txt
uvicorn backend.main:app --reload
streamlit run frontend/dashboard.py

API Endpoint:

http://127.0.0.1:8000/patients

Power BI Connection:

Get Data → Web →
http://127.0.0.1:8000/patients
