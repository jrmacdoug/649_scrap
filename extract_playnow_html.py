from tokenize import String
from turtle import update
from types import NoneType
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
        num6 = ?,
        bonus = ?
    WHERE year = ?
    AND month = ?
    AND day = ?
    """

def sql_match_insert(payout_t,a,b,p=False):
    if p:
        sql = """UPDATE winnings SET prize_{}_{}p = \"{}\", winners_{}_{}p = \"{}\" WHERE year = ? AND month = ? AND day = ?"""
        match = "{}/{}+".format(a,b)
    else:
        sql = """UPDATE winnings SET prize_{}_{} = \"{}\", winners_{}_{} = \"{}\" WHERE year = ? AND month = ? AND day = ?"""
        match = "{}/{}".format(a,b)    
    prize = payout_t.loc[payout_t['Match'] == match]['Prize'].values[0]
    winner = payout_t.loc[payout_t['Match'] == match]['Winners'].values[0]
    return sql.format(a,b,prize,a,b,winner)

def main():   
    con = sqlite3.connect("649_lottery.db")
    cur = con.cursor()
    
    for f in data_path.iterdir():
        yy = f.name[-15:-11]
        mm = f.name[-10:-8]
        dd = f.name[-7:-5]
        winning_nums = []
        bonus = ''
                
        cur.execute(sql_insert_date,(yy,mm,dd))

        with open(f,'r',encoding='utf-8') as pn_html:
            pn_soup = BeautifulSoup(pn_html,'html.parser')
            
            #649 draw
            for li in pn_soup.find_all("li",{"class":"product-winning-numbers__number product-winning-numbers__number_six49"}):
                winning_nums.append(li.text.strip('\n '))
            #bonus
            try:
                bonus = pn_soup.find("li",{"class":"product-winning-numbers__bonus-number product-winning-numbers__bonus-number_six49"}).text.strip('\n ')
            except:
                bonus = ''
            #if no numbers, then do not update and leave blank
            if winning_nums != []:
                cur.execute(sql_update_nums,tuple(winning_nums) + (bonus,yy,mm,dd))
            else:
                print("no numbers for",yy,mm,dd)

            #find table and add prizes
            try:
                table = pn_soup.find('table',{"class":"product-prize-breakdown__table product-prize-breakdown__table_game-breakdown"})
                payout_table = pd.read_html(str(table))[0]
                cur.execute(sql_match_insert(payout_table,6,6),(yy,mm,dd))
                cur.execute(sql_match_insert(payout_table,5,6,True),(yy,mm,dd))
                cur.execute(sql_match_insert(payout_table,5,6),(yy,mm,dd))
                cur.execute(sql_match_insert(payout_table,4,6),(yy,mm,dd))
                try:
                    cur.execute(sql_match_insert(payout_table,3,6),(yy,mm,dd))
                except IndexError:
                    pass  
                try:
                    cur.execute(sql_match_insert(payout_table,2,6,True),(yy,mm,dd))
                except IndexError:
                    pass
            except ValueError:
                print("no listed prizes for",yy,mm,dd)

        con.commit()
            
    con.close()

if __name__ == "__main__":
    main()