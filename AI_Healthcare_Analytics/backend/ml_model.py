import pandas as pd
from sklearn.linear_model import LinearRegression

def train_model(df):

    X = df[['Year_numeric']]
    y = df['Avg_Indicator']

    model = LinearRegression()

    model.fit(X,y)

    return model


def predict_future(df, year):

    model = train_model(df)

    prediction = model.predict([[year]])

    return round(prediction[0],2)