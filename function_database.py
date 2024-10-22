import sqlite3
import pandas as pd


def query(table):
    return pd.read_sql_query(f"SELECT * FROM {table}",
                             con=sqlite3.connect('E:/BaiduNetdiskDownload/database/CheckIndata.db'))
