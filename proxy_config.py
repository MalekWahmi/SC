'''import time
from threading import Thread
import pyautogui
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

hostname = "gate.smartproxy.com"
port = "7000"
proxy_username = "sp40328552"
proxy_password = "12345678"

chrome_options = Options()
chrome_options.add_argument('--proxy-server={}'.format(hostname + ":" + port))
driver = webdriver.Chrome(options=chrome_options)


def enter_proxy_auth(proxy_username, proxy_password):
    time.sleep(1)
    pyautogui.typewrite(proxy_username)
    pyautogui.press('tab')
    pyautogui.typewrite(proxy_password)
    pyautogui.press('enter')


def open_a_page(driver, url):
    driver.get(url)
    time.sleep(100)


Thread(target=open_a_page, args=(driver, "http://www.intagram.com/movlogs")).start()
Thread(target=enter_proxy_auth, args=(proxy_username, proxy_password)).start()'''