from tokenize import String
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import sqlite3

data_path = Path('data')

sql_insert_date="""
    INSERT INTO winnings(year,month,day)
    VALUES (?,?,?)
    """

sql_update_nums="""
    UPDATE winnings
    SET num1 = ?,
        num2 = ?,
        num3 = ?,
        num4 = ?,
        num5 = ?,
        num6 = ?
    WHERE year = ?
    AND month = ?
    AND day = ?
    """

sql_update_bonus="""
    UPDATE winnings
    SET bonus = ?
    WHERE year = ?
    AND month = ?
    AND day = ?
    """

def main():   
    con = sqlite3.connect("649_lottery.db")
    cur = con.cursor()
    
    for row in cur.execute("SELECT * FROM winnings ORDER BY year"):
        print(row)   
    
    for f in data_path.iterdir():
        yy = f.name[-15:-11]
        mm = f.name[-10:-8]
        dd = f.name[-7:-5]
    
        cur.execute(sql_insert_date,(yy,mm,dd))
        
        with open(f,'r',encoding='utf-8') as pn_html:

            pn_soup = BeautifulSoup(pn_html,'html.parser')
            
            #update numbers
            winning_nums = []
            for li in pn_soup.find_all("li",{"class":"product-winning-numbers__number product-winning-numbers__number_six49"}):
                winning_nums.append(li.text.strip('\n '))
            update_vars = tuple(winning_nums) + (yy,mm,dd)
            cur.execute(sql_update_nums,update_vars)

            #update bonus
            bonus = pn_soup.find("li",{"class":"product-winning-numbers__bonus-number product-winning-numbers__bonus-number_six49"}).text.strip('\n ')
            update_vars = (bonus,yy,mm,dd)
            cur.execute(sql_update_bonus,update_vars)

            #we'll use pandas for the table item in the HTML
            table = pn_soup.find('table',{"class":"product-prize-breakdown__table product-prize-breakdown__table_game-breakdown"})
            payout_table = pd.read_html(str(table))[0]
            print(payout_table.query('Match = 6/6'))
            

    for row in cur.execute("SELECT * FROM winnings ORDER BY year"):
        print(row)

    cur.execute("DELETE FROM winnings")
    con.commit()
    con.close()

if __name__ == "__main__":
    main()