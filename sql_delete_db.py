import sqlite3


con = sqlite3.connect("649_lottery.db")
cur = con.cursor()


cur.execute("DELETE FROM winnings")

con.commit()
con.close()


