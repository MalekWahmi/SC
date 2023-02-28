from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import unicodedata
import time
from datetime import datetime


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--lang=en')
chrome_options.add_argument("start-maximized")
chrome_options.add_experimental_option("excludeSwitches",["enable-automation","enable-logging"])
chrome_options.add_experimental_option("useAutomationExtension",False)

driver = webdriver.Chrome('Chromedriver',chrome_options=chrome_options)

def yt_browser(username):
    url = f'https://youtube.com/{username}/about'
    driver.get(""+url)
    time.sleep(10)
    try : 
        channel_title = driver.find_element(By.XPATH,'//*[@id="text"]').text
        pass
    except NoSuchElementException :
        channel_title = driver.find_element(By.XPATH,'/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/div[3]/ytd-c4-tabbed-header-renderer/tp-yt-app-header-layout/div/tp-yt-app-header/div[2]/div[2]/div/div[1]/div/div[1]/ytd-channel-name/div/div/yt-formatted-string')
        pass
    except :
        channel_title = 'Not Found'
        pass
    
    channel_avatar = driver.find_element(By.XPATH,'//*[@id="img"]').get_attribute('src')
    bio = driver.find_element(By.XPATH,'//*[@id="description-container"]').text
    #contact_info = driver.find_element(By.XPATH,"")
    links = driver.find_element(By.ID,'link-list-container')
    links_list = links.find_elements(By.TAG_NAME,'a')
    ll = [l.get_attribute('href') for l in links_list]
    sub_count = driver.find_element(By.XPATH,'//*[@id="subscriber-count"]').text
    date_joined = driver.find_element(By.XPATH,'//*[@id="right-column"]/yt-formatted-string[2]/span[2]').text
    total_views_encoded = driver.find_element(By.XPATH,'//*[@id="right-column"]/yt-formatted-string[3]').text
    total_views = unicodedata.normalize('NFKD',total_views_encoded)
    try :
        is_verified = driver.find_element(By.XPATH,'//*[@id="channel-name"]/ytd-badge-supported-renderer/div').get_attribute('aria-label')# add try except NoSuchElementException
        if is_verified == "Validé" or is_verified == "Verified" :
            verified = 'verified'
        else : 
            verified = 'Not verified'
    except NoSuchElementException :
        verified = 'Not verified'
        pass
    
    scraping_date = datetime.now()
    
    data = [channel_title,channel_avatar,bio,ll,sub_count,date_joined,total_views,verified]
    
    info = {
        'channel title' : data[0],
        'channel avatar url' : channel_avatar,
        'biography' : data[2],
        'links list' : data[3],
        'subscribers count' : data[4],
        'date joined' : data[5],
        'total number views' : data[6],
        'verified status' : data[7],
        'scraped_at' : scraping_date,
        'ProfileURL' :url
        
    }
    
    return info
#print(yt_browser('@samara_riahi'))