from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
import bs4
from bs4 import BeautifulSoup
import unicodedata
import time
import json
from datetime import datetime

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--lang=en')
chrome_options.add_argument("start-maximized")
chrome_options.add_experimental_option("excludeSwitches",["enable-automation","enable-logging"])
chrome_options.add_experimental_option("useAutomationExtension",False)

driver = webdriver.Chrome('Chromedriver',chrome_options=chrome_options)


def tk_post(url):
    driver.get(url)
    time.sleep(10)
    post_class = driver.find_element(By.TAG_NAME,'video').get_attribute('mediatype')
    if post_class == "video":
        post_type = 'video'
    try : 
        total_likes = driver.find_element(By.XPATH,'//*[@id="app"]/div[3]/div[2]/div[1]/div[2]/div/div[1]/div[1]/div[4]/button[1]/strong').text
    except NoSuchElementException :
        total_likes = 0
        pass
    #total = driver.find_element(By.ID,'count').find_element(By.TAG_NAME,'span').text
    try :
        total_comments = driver.find_element(By.XPATH,'//*[@id="app"]/div[3]/div[2]/div[1]/div[2]/div/div[1]/div[1]/div[4]/button[2]/strong').text
        #total_comments = unicodedata.normalize('NFKD',total_comments_encoded)
    except NoSuchElementException:
        total_comments = 0
        pass
    '''try : 
        total_shares = driver.find_element(By.XPATH,'//*[@id="app"]/div[3]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[4]/button[3]/strong').text
    except NoSuchElementException :
        total_shares = 0
        pass'''
    html  = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML;")
    soup = BeautifulSoup(html,'html.parser')
    
    l =[]
    total_shares = soup.find(attrs= {'data-e2e' : 'share-count'}).text
    for txt in soup.find_all('strong',class_ = 'tiktok-f9vo34-StrongText ejg0rhn1'):
        l.append(txt.text)
        
    hash_list = []
    i =0
    men_list = []
    j = 0
    for h in l :
        if h.startswith('#'):
            hash_list.append(h)
            i += 1
        elif h.startswith('@'):
            men_list.append(h)
            j+=1
    scraping_date = datetime.now()   
    


    data = [post_type,total_likes,hash_list,i,men_list,j,total_comments,total_shares,scraping_date]
    info = {
        'PostType' : data[0],
        'totalLikes' : data[1],
        'hashtagList' : data[2],
        'totalHashtags' : data[3],
        'mensionsList' : data[4],
        'totalMentions' : data[5],
        'total_comments' : data[6],
        'total_shares' : total_shares,
        'scraped_at' :data[8]
        
    }
            
    return info



#print(tk_post('https://www.tiktok.com/@mo_vlogs/video/7177364641100614914?is_from_webapp=v1&item_id=7177364641100614914'))
    