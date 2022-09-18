import pandas as pd
import sqlite3

cnx = sqlite3.connect('649_lottery.db')

df = pd.read_sql_query("SELECT * FROM winnings", cnx)



print(df)

cnx.close()