import duckdb

def run_query(df, query):

    con = duckdb.connect()

    con.register("data", df)

    result = con.execute(query).df()

    return result