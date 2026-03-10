import plotly.express as px

def line_chart(df):

    fig = px.bar(
        df,
        x="Year_numeric",
        y="Avg_Indicator",
        title="Average Indicator Value by Year"
    )

    return fig


def pie_chart(df):

    fig = px.pie(
        df,
        names="Sex Breakdown",
        values="Total_Numerator",
        title="Numerator Distribution by Sex"
    )

    return fig