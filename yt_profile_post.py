from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import pandas as pd
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from yt_posts import yt_post


options = webdriver.ChromeOptions()
#All are optional
options.add_experimental_option("detach", True)
options.add_argument("--headless")
options.add_argument('--lang=en')
options.add_argument("--disable-extensions")
options.add_argument("--disable-notifications")
options.add_argument("--disable-Advertisement")
options.add_argument("--disable-popup-blocking")
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches",["enable-automation","enable-logging"])
options.add_experimental_option("useAutomationExtension",False)


s=Service('./chromedriver')
driver= webdriver.Chrome(service=s,options=options)
def ypp(username) :
    driver.get(f'https://www.youtube.com/{username}/videos')
    time.sleep(30)

    item = []
    SCROLL_PAUSE_TIME = 1
    last_height = driver.execute_script("return document.documentElement.scrollHeight")

    item_count = 180
    #start_time = time.process_time()

    timer1 = datetime.now()
    while item_count > len(item):
        driver.execute_script("window.scrollTo(0,document.documentElement.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.documentElement.scrollHeight")

        if new_height == last_height:
            break
        last_height = new_height
        

    data = []
    try:
        for e in WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div#details'))):
            
            title = e.find_element(By.CSS_SELECTOR,'a#video-title-link').get_attribute('title')
            vurl = e.find_element(By.CSS_SELECTOR,'a#video-title-link').get_attribute('href')
            views= e.find_element(By.XPATH,'.//*[@id="metadata"]//span[@class="inline-metadata-item style-scope ytd-video-meta-block"][1]').text
            date_time = e.find_element(By.XPATH,'.//*[@id="metadata"]//span[@class="inline-metadata-item style-scope ytd-video-meta-block"][2]').text
            post_data = yt_post(vurl)
            
            data.append({   
                'video_url':vurl,
                'title':title,
                'date_time':date_time,
                'views':views,
                'totalLikes': post_data['totalLikes'],
                'totalComments': post_data['total_comments']
                })
    except:
        pass
        
    item = data
    timer2 = datetime.now()
    process_time = timer2 - timer1
    
    return item,len(item),timer1 


#print(ypp('MoVlogs'))