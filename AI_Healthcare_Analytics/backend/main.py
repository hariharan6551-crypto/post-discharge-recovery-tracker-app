from fastapi import FastAPI
from backend.api.routes import get_patients

app = FastAPI(title="AI Healthcare Analytics API")


@app.get("/")
def home():
    return {"message": "AI Healthcare Analytics API Running"}


@app.get("/patients")
def patients():
    return get_patients()