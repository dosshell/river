import apsw
import pandas
from typing import Tuple, List


def sql_to_df(conn: apsw.Connection, table_name: str) -> pandas.DataFrame:
    c = conn.cursor()
    rh = c.execute(f'''PRAGMA table_info({table_name})''').fetchall()
    headers = [x[1] for x in rh]
    r = c.execute(f'''select * from {table_name}''')
    data = r.fetchall()
    df = pandas.DataFrame.from_records(data, columns=headers)
    return df


def df_to_sql(conn: apsw.Connection, table_name: str, df: pandas.DataFrame) -> None:
    qs = ','.join(['?'] * len(df.columns))
    cs = ','.join(df.columns.tolist())
    conn.cursor().executemany(f'''insert or ignore into {table_name} ({cs}) values({qs})''', df.values.tolist())


def tuplelist_to_sql(conn: apsw.Connection, table_name: str, values: List[Tuple]) -> None:
    if len(values) < 1:
        return
    columns = len(values[0])
    qs = ','.join(['?'] * columns)
    c = conn.cursor()
    c.execute("BEGIN TRANSACTION")
    c.executemany(f'''insert or ignore into {table_name} values ({qs})''', values)
    c.execute("COMMIT")


def create_tables(conn: apsw.Connection) -> None:
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS fund_list(
                    "orderbook_id" INTEGER PRIMARY KEY NOT NULL,
                    "name" TEXT NOT NULL UNIQUE,
                    "start_date" TEXT NOT NULL,
                    "active" BOOLEAN NOT NULL DEFAULT 1 CHECK (active IN (0,1))
                    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS fund_chart(
                    orderbook_id INTEGER NOT NULL,
                    x TEXT NOT NULL,
                    y REAL,
                    PRIMARY KEY(orderbook_id, x),
                    FOREIGN KEY(orderbook_id) REFERENCES fund_list(orderbook_id)
                    )''')
