from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path

"""
https://www.cbc.ca/news/canada/nova-scotia/atlantic-lottery-is-retiring-the-balls-1.51075980
"""

def main():   

    base_649_site = 'https://www.playnow.com/lottery/lotto-649-winning-numbers/?date='

    data_path = Path('data')
    draw_date = datetime(year=1988,month=8,day=24)
    end_draw_date = datetime(year=1988,month=12,day=31)
    
    while draw_date < end_draw_date:
        if draw_date.strftime("%A") in ["Saturday","Wednesday"]:
            draw_site = base_649_site + draw_date.strftime('%d/%m/%Y')
            
            driver = webdriver.Chrome()
            driver.get(draw_site)
            driver.implicitly_wait(8)

            draw_soup = BeautifulSoup(driver.page_source,'html.parser')

            draw_fn_path = Path(data_path,"lotto-649-winning-numbers-"+draw_date.strftime('%d-%m-%Y')+".html")
            
            with open(draw_fn_path,'w',encoding='utf-8') as f:
                f.write(draw_soup.prettify())
    
            driver.quit()
           
        draw_date += timedelta(days=1)

if __name__ == "__main__":
    main()