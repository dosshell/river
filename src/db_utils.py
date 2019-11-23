# import apsw # APSW has no apsw.Cursor attribute bug
import pandas


def sql_to_df(cursor, table_name: str) -> pandas.DataFrame:
    rh = cursor.execute(f'''PRAGMA table_info({table_name})''').fetchall()
    headers = [x[1] for x in rh]
    r = cursor.execute(f'''select * from {table_name}''')
    data = r.fetchall()
    df = pandas.DataFrame.from_records(data, columns=headers)
    return df


def df_to_sql(cursor, table_name: str, df: pandas.DataFrame) -> None:
    qs = ','.join(['?'] * len(df.columns))
    cs = ','.join(df.columns.tolist())
    cursor.executemany(f'''insert or ignore into {table_name} ({cs}) values({qs})''', df.values.tolist())


def tuplelist_to_sql(cursor, table_name: str, values: pandas.DataFrame) -> None:
    if len(values) < 1:
        return
    columns = len(values[0])
    qs = ','.join(['?'] * columns)
    cursor.execute("BEGIN TRANSACTION")
    cursor.executemany(f'''insert or ignore into {table_name} values ({qs})''', values)
    cursor.execute("COMMIT")


def create_tables(cursor) -> None:
    cursor.execute('''CREATE TABLE IF NOT EXISTS fund_list(
                        orderbook_id INTEGER PRIMARY KEY NOT NULL,
                        name TEXT NOT NULL UNIQUE,
                        start_date TEXT NOT NULL
                      )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS fund_chart(
                        orderbook_id INTEGER NOT NULL,
                        x TEXT NOT NULL,
                        y REAL,
                        PRIMARY KEY(orderbook_id, x),
                        FOREIGN KEY(orderbook_id) REFERENCES fund_list(orderbook_id)
                      )''')
