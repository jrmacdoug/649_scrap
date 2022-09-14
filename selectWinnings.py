import sqlite3


con = sqlite3.connect("649_lottery.db")
cur = con.cursor()

# [print(row) for row in cur.execute("SELECT * FROM winnings WHERE num1 is null ORDER BY year")]
# [print(row) for row in cur.execute("SELECT * FROM winnings WHERE prize_6_6 is null ORDER BY year")]
[print(row) for row in cur.execute("SELECT * FROM winnings WHERE prize_6_6 is not null ORDER BY year")]

cur.execute("""
SELECT year,COUNT(num1) FROM winnings WHERE prize_6_6 is not null group BY year
""")

con.commit()
con.close()

