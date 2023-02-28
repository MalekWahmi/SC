import undetected_chromedriver as uc
import time
from bs4 import BeautifulSoup
import random
from datetime import datetime
import pymongo
import pandas as pd
from tk_posts import tk_post


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
tt_db = myclient["mytiktok"]
yt_db = myclient["myyoutube"]
tt_profile = tt_db["profileInfo"]
yt_profile = yt_db["profileInfo"]
yt_pro_posts = yt_db["profilePosts"]
tt_pro_posts = tt_db["profilePosts"]




def ttpp(username):
    
    driver = uc.Chrome()
    driver.get(f'https://www.tiktok.com/@{username}')
    time.sleep(20)
    item = []
    SCROLL_PAUSE_TIME = random.randint(5,15)
    last_height = driver.execute_script("return document.documentElement.scrollHeight")

    item_count = 180

    # Get scroll height
    while item_count > len(item):
        driver.execute_script("window.scrollTo(0,document.documentElement.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.documentElement.scrollHeight")

        if new_height == last_height:
            break
        last_height = new_height
    
    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')
    
    videoList = soup.find("div", {"class": "tiktok-1qb12g8-DivThreeColumnContainer eegew6e2"})
    allVids = videoList.findAll("div", {"class": "tiktok-yz6ijl-DivWrapper e1cg0wnj1"})
    allViews = videoList.findAll("div",{"class": "tiktok-11u47i-DivCardFooter e148ts220"})
    urls = [vid.find("a")['href'] for vid in allVids]
    views = [view.find("strong").text for view in allViews]
    n_shares = []
    n_comments =[]
    n_likes = []
    for url in urls :
        out = tk_post(url)
        n_shares.append(out['total_shares'])
        n_comments.append(out['total_comments'])
        n_likes.append(out['totalLikes'])    
     #for txt in soup.find_all('div',class_ = 'tiktok-yz6ijl-DivWrapper e1cg0wnj1'):
        #l.append(txt.text)
    
    timeres = datetime.now()
    
    post_data =[]
    for i in range(len(urls)) :
        post_data.append(
            {
                'postUrl' :urls[i],
                'no_shares' :n_shares[i],
                'no_comments' :n_comments[i],
                'no_view' :views[i],
                'no_likes' : n_likes[i]
            }
            )
    
    return post_data,len(urls),timeres


def post_shares(user):
    query = { 'Username': user }
    res = tt_pro_posts.find(query)
    data =[]
    for r in res :
        data.append(r)
        
    df = pd.DataFrame(data)
    recent = df['scraped_at'].max()
    df = df.reset_index()
    
    for index,row in df.iterrows():
        if row['scraped_at'] == recent :
            y = row['PostsList']
    return y


#print(ttpp('z6tt'))
