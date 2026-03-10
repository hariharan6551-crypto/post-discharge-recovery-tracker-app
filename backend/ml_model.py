import numpy as np
from sklearn.linear_model import LinearRegression

def predict_future(df, year):

    numeric_cols = df.select_dtypes(include="number")

    if len(numeric_cols.columns) == 0:
        return 0

    y = numeric_cols.mean(axis=1)

    X = np.arange(len(y)).reshape(-1,1)

    model = LinearRegression()
    model.fit(X,y)

    prediction = model.predict([[len(X)+1]])

    return round(float(prediction[0]),2)
