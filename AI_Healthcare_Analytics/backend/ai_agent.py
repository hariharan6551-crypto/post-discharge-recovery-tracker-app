def ask_ai(question, df):

    question = question.lower()

    if "average" in question:
        return f"Average Indicator Value is {round(df['Avg_Indicator'].mean(),2)}"

    if "highest year" in question:
        year = df.loc[df['Avg_Indicator'].idxmax()]['Year_numeric']
        return f"Highest indicator value occurred in {year}"

    if "records" in question:
        return f"The dataset contains {len(df)} records."

    return "Please ask about the dataset such as average, highest year or records."