import sqlite3

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path


def main():   
    
    data_path = Path('data-extra')
    base_649_site = 'https://www.playnow.com/lottery/lotto-649-winning-numbers/?date='
    
    con = sqlite3.connect("649_lottery.db")
    cur = con.cursor()

    res = cur.execute("""
    SELECT day, month, year
    FROM winnings     
    WHERE num1 is null
    ORDER BY year,month,day
    """)

    for d in res:

        draw_site = base_649_site + d[0] +'/' + d[1] + '/' + d[2]
        
        driver = webdriver.Chrome()
        driver.get(draw_site)
        driver.implicitly_wait(15)

        draw_soup = BeautifulSoup(driver.page_source,'html.parser')

        draw_fn_path = Path(data_path,"lotto-649-winning-numbers-"+ d[2] + '-' + d[1] + '-' + d[0]+".html")
        
        with open(draw_fn_path,'w',encoding='utf-8') as f:
            f.write(draw_soup.prettify())

        driver.quit()
        
    con.close()

if __name__ == "__main__":
    main()


