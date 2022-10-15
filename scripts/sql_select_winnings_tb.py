import sqlite3


con = sqlite3.connect("649_lottery.db")
cur = con.cursor()

# [print(row) for row in cur.execute("SELECT * FROM winnings WHERE num1 is null ORDER BY year")]
# [print(row) for row in cur.execute("SELECT * FROM winnings WHERE prize_6_6 is null ORDER BY year")]
# [print(row) for row in cur.execute("SELECT * FROM winnings WHERE prize_6_6 is not null ORDER BY year")]


res = cur.execute("""
SELECT count(*)
FROM winnings     
WHERE num1 is null
ORDER BY year,month,day
""")
[print(row) for row in res]

res = cur.execute("""
SELECT count(*)
FROM winnings     
WHERE num1 is not null
ORDER BY year,month,day
""")
[print(row) for row in res]

con.commit()
con.close()

