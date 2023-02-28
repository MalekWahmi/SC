import pymongo
import pandas as pd


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
tt_db = myclient["mytiktok"]
yt_db = myclient["myyoutube"]
tt_profile = tt_db["profileInfo"]
yt_profile = yt_db["profileInfo"]
yt_pro_posts = yt_db["profilePosts"]
tt_pro_posts = tt_db["profilePosts"]

def content_yt(user) :
    
    query = { 'Username': user }
    res = yt_pro_posts.find(query)
    
    content =[]
    for r in res :
        content.append(r)
        
    df = pd.DataFrame(content)
    recent_profile = df['scraped_at'].max()
    df = df.reset_index()
    
    for index,row in df.iterrows():
        
        if row['scraped_at'] == recent_profile :
            output = row
            
    data = []
    for i in range(output['PostsNumber']) :
        data.append({
            'Post_Type' : 'Video',
            'Post_URL' : output['PostsList'][i]['video_url'],
            'Post_title' : output['PostsList'][i]['title'],
            'Number_of_Likes': output['PostsList'][i]['totalLikes'],
            'Number_of_Comments' : output['PostsList'][i]['totalComments']
        })
    
    dframe = pd.DataFrame(data)
    
    return dframe



def content_tk(user) :
    query = { 'Username': user }
    res = tt_pro_posts.find(query)
    
    content =[]
    for r in res :
        content.append(r)
        
    df = pd.DataFrame(content)
    recent_profile = df['scraped_at'].max()
    df = df.reset_index()
    
    for index,row in df.iterrows():
        
        if row['scraped_at'] == recent_profile :
            output = row
            
    data = []
    for i in range(output['PostsNumber']) :
        data.append({
            'Post_Type' : 'Video',
            'Post_URL' : output['PostsList'][i]['postUrl'],
            'Number_of_Views' : output['PostsList'][i]['no_view'],
            'Number_of_Likes': output['PostsList'][i]['no_likes'],
            'Number_of_Comments' : output['PostsList'][i]['no_comments']
        })
    
    dframe = pd.DataFrame(data)
    
    return dframe
#print(content_tk('mo_vlogs'))