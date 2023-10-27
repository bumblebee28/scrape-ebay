from urllib.request import urlopen
import selenium.webdriver as wd
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd
import mysql.connector as myconn
import dotenv

def scraping(url, flag):
    
    # options = wd.EdgeOptions()
    # options.add_argument('--headless')
    dr = wd.Edge()
# options=options

    def view_items(url):
        dr.get(url)
        divs = dr.find_elements(By.CLASS_NAME, 'srp-controls__count-heading')
        num_items = divs[0].find_elements(By.CLASS_NAME, 'BOLD')[0].get_attribute('innerText')
        return num_items
    
    
    def find_products(url):
        
        names, prices, urls, info, sellers = [], [], [], [], []
        p = 1
        
        while(p > 0):
            
            dr.get(f'{url}&_pgn={p}')
            name_list = dr.find_elements(By.CLASS_NAME, 's-item__title')
            price_list = dr.find_elements(By.CLASS_NAME, 's-item__price')
            url_list = dr.find_elements(By.CLASS_NAME, 's-item__link')
            info_list = dr.find_elements(By.CLASS_NAME, 'SECONDARY_INFO')
            seller_list = dr.find_elements(By.CLASS_NAME, 's-item__seller-info-text')
            seller_list = ['Nan'] + seller_list

            if (len(url_list)) > 0 :
                for i in range(len(url_list)):
                    try:
                        url_list[i] = url_list[i].get_attribute('href')
                    except:
                        url_list[i] = 'NAN'
                    try:
                        name_list[i] = name_list[i].get_attribute('innerText')
                    except:
                        name_list[i] = 'NAN'
                    try:
                        price_list[i] = price_list[i].get_attribute('innerText')
                    except:
                        price_list[i] = 'NAN'
                    try:
                        info_list = info_list[i].get_attribute('href')
                    except:
                        info_list[i] = 'NAN'
                    try:
                        seller_list[i] = useller_list[i].get_attribute('href')
                    except:
                        seller_list[i] = 'NAN'
                    
                names.extend(name_list)
                prices.extend(price_list)
                urls.extend(url_list)
                sellers.extend(seller_list)
                info.extend(info_list)
                p = p + 1
                sleep(5)
                
            else:
                p = 0
        
        il = pd.DataFrame(data=[names, prices, urls, sellers, info]).transpose()
        il.columns = ['name','price', 'url', 'seller', 'info']
        return il

    if flag == 'scrape':
        item_list = find_products(url)
        return item_list.to_csv('AMAT' + '.csv')
    
    if flag == 'view':
        num_items = view_items(url)
        return num_items

scraping('https://www.ebay.com/sch/i.html?_dcat=58295&_fsrp=1&Brand=Amat&rt=nc&_from=R40&_nkw=amat&_sacat=0&LH_ItemCondition=4&_udhi=350&_fss=1', 'scrape')
        