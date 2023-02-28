from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime


chrome_options = webdriver.ChromeOptions()
#proxy = "gate.smartproxy.com:7000"
#chrome_options.add_argument(f'--proxy-server={proxy}')
chrome_options.add_argument("--headless")
chrome_options.add_argument('--lang=en')
chrome_options.add_argument("start-maximized")
chrome_options.add_experimental_option("excludeSwitches",["enable-automation","enable-logging"])
chrome_options.add_experimental_option("useAutomationExtension",False)
driver = webdriver.Chrome('Chromedriver',chrome_options=chrome_options)


def tok_browser(username):
    driver.get(""+"https://www.tiktok.com/@"+username)
    time.sleep(60)
    try :
        profile_name = driver.find_element(By.XPATH,'//*[@id="app"]/div[3]/div[2]/div/div[1]/div[1]/div[2]/h2').text
    except NoSuchElementException :
        pass 
    nb_followers = driver.find_element(By.XPATH,'//*[@id="app"]/div[3]/div[2]/div/div[1]/h2[1]/div[2]/strong').text
    nb_followees = driver.find_element(By.XPATH,'//*[@id="app"]/div[3]/div[2]/div/div[1]/h2[1]/div[1]/strong').text
    total_nb_likes =driver.find_element(By.XPATH,'//*[@id="app"]/div[3]/div[2]/div/div[1]/h2[1]/div[3]/strong').text
    bio = driver.find_element(By.XPATH,'//*[@id="app"]/div[3]/div[2]/div/div[1]/h2[2]').text
    profile_image = driver.find_element(By.TAG_NAME,"img").get_attribute('src')
    for text in driver.find_elements(By.XPATH,'//*[@id="app"]/div[3]/div[2]/div/div[1]/div[1]/div[2]/h2'):
        try : 
            is_verified = text.find_element(By.TAG_NAME,'circle').get_attribute('fill')
        except NoSuchElementException :
            is_verified = 'Not Verified'
            pass
        
        if is_verified == '#20D5EC' :
            verified = 'verified'
        else :
            verified = 'Not verified'

    scraping_date = datetime.now()
    
    data = [profile_name,nb_followers,nb_followees,total_nb_likes,bio,profile_image,verified]
    info = {
        'ProfileName' : data[0],
        'FollowersNumber' : data[1],
        'FolloweesNumber' : data[2],
        'TotalNumberLikes' : data[3],
        'Biography' : data[4],
        'ProfileImageUrl' : data[5],
        'VerifiedStatus' : data[6],
        'scraped_at' : scraping_date,
        'InfluencerURL' : "https://www.tiktok.com/@"+username
    }
    
    return info

#print(tok_browser("artvibe_isetch"))