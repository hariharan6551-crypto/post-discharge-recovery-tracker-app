def ask_ai(question, df):

    rows = df.shape[0]
    cols = df.shape[1]

    return f"The dataset currently contains {rows} records and {cols} columns. Your question was: {question}"
