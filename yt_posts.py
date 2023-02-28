from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

import unicodedata
import time
from datetime import datetime
import numpy as np

import re


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--lang=en')
chrome_options.add_argument("start-maximized")
chrome_options.add_experimental_option("excludeSwitches",["enable-automation","enable-logging"])
chrome_options.add_experimental_option("useAutomationExtension",False)

driver = webdriver.Chrome('Chromedriver',chrome_options=chrome_options)


def yt_post(url):
    driver.get(url)
    time.sleep(5)
    post_class = driver.find_element(By.TAG_NAME,'video').get_attribute('class')
    
    if post_class == "video-stream html5-main-video":
        post_type = 'video'
    
    try :
        total_likes = driver.find_element(By.XPATH,'//*[@id="segmented-like-button"]/ytd-toggle-button-renderer/yt-button-shape/button/div[2]/span').text
    except NoSuchElementException :
        total_likes = driver.find_element(By.XPATH,'/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[2]/ytd-watch-metadata/div/div[2]/div[2]/div/div/ytd-menu-renderer/div[1]/ytd-segmented-like-dislike-button-renderer/div[1]/ytd-toggle-button-renderer/yt-button-shape/button/div[2]/span').text     
    except :
        total_likes = 0
        pass
      
    html  = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML;")
    soup = BeautifulSoup(html,'html.parser')
    
   
    l =[]
    
    for txt in soup.find_all('a',class_ = 'yt-simple-endpoint style-scope yt-formatted-string'):
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
    hashtags = np.unique(hash_list).tolist()
    mentions = np.unique(men_list).tolist()        
    total_views = driver.find_element(By.XPATH,'//*[@id="info"]/span[1]').text
    
    com =[]
    
    driver.find_element(by=By.TAG_NAME, value="body").send_keys(Keys.PAGE_DOWN)
    time.sleep(2)
    
    nc = driver.find_elements(By.ID,'title')
    ftnc = 0
    for t in nc :
        if t.get_attribute('class') == 'style-scope ytd-comments-header-renderer' :
            total_comments = unicodedata.normalize('NFKD',t.text)
            com.append(total_comments)
            ftn = re.findall(r'\b\d+\b',com[0])
            ftnc = ' '.join(str(e) for e in ftn)
            #print(type(t.text))
    
    scraping_date = datetime.now()
    
    data = [post_type,total_likes,hashtags,i,mentions,j,ftnc,total_views,scraping_date]
    info = {
        'PostType' : data[0],
        'totalLikes' : data[1],
        'hashtagList' : data[2],
        'totalHashtags' : data[3],
        'mensionsList' : data[4],
        'totalMentions' : data[5],
        'total_comments' : data[6],
        'totalViews': data[7],
        'scraped_at' : data[8]
    }
            
    return info



#print(yt_post('https://www.youtube.com/watch?v=AB-l3obr8dY'))
    