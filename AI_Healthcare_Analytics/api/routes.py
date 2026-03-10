import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_PATH = os.path.join(BASE_DIR, "data", "hospital_readmission_dataset.xlsx")


def load_dataset():
    df = pd.read_excel(DATA_PATH)
    return df


def get_patients():
    df = load_dataset()
    return df.to_dict(orient="records")