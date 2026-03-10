from sklearn.linear_model import LinearRegression
import numpy as np

def predict_future(df,year):

    numeric_cols = df.select_dtypes(include="number").columns

    if len(numeric_cols) < 2:
        return 0

    X = df[[numeric_cols[0]]]
    y = df[numeric_cols[1]]

    model = LinearRegression()

    model.fit(X,y)

    pred = model.predict(np.array([[year]]))

    return round(pred[0],2)