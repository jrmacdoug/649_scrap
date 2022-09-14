import sqlite3

con = sqlite3.connect("649_lottery.db")
cur = con.cursor()
cur.execute(
"""
CREATE TABLE winnings (
	draw_id INTEGER PRIMARY KEY,
	year TEXT NOT NULL,
	month TEXT NOT NULL,
	day TEXT NOT NULL,
	num1 INTEGER,
    num2 INTEGER,
    num3 INTEGER,
    num4 INTEGER,
    num5 INTEGER,
    num6 INTEGER,
    bonus INTEGER,
    prize_6_6 TEXT,
    prize_5_6p TEXT,
    prize_5_6 TEXT,	
    prize_4_6 TEXT,	
    prize_3_6 TEXT,	
    prize_2_6p TEXT,	
    winners_6_6 TEXT,	
    winners_5_6p TEXT,	
    winners_5_6 TEXT,	
    winners_4_6 TEXT,	
    winners_3_6 TEXT,	
    winners_2_6p TEXT
);
"""
)

con.commit()
con.close()