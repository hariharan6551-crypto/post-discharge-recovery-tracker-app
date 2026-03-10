def ask_ai(question,df):

    q = question.lower()

    if "average" in q:
        return f"Average indicator value is {round(df.select_dtypes('number').mean().mean(),2)}"

    if "numerator" in q:
        return f"Total numerator is {int(df.select_dtypes('number').sum()[0])}"

    if "denominator" in q:
        return f"Total denominator is {int(df.select_dtypes('number').sum()[-1])}"

    if "highest" in q:
        row = df.iloc[df.select_dtypes('number').idxmax()[0]]
        return f"Highest value row: {row.to_dict()}"

    return "Ask about average, numerator, denominator, or highest values."