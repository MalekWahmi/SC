import pymongo
import pandas as pd


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
tt_db = myclient["mytiktok"]
yt_db = myclient["myyoutube"]
tt_profile = tt_db["profileInfo"]
yt_profile = yt_db["profileInfo"]
yt_pro_posts = yt_db["profilePosts"]
tt_pro_posts = tt_db["profilePosts"]



def convert(value):
    import re
    values = re.sub('\s','',value)
    values = re.sub(',','.',values)
    if value:
        
        multiplier = 1
        if value.endswith('K'):
            multiplier = 1000
            value = value[0:len(value)-1] 
        elif value.endswith('M'):
            multiplier = 1000000
            value = value[0:len(value)-1] 

        return int(float(value) * multiplier)

    else:
        return 0

def convert_yt_views(value):
    import re
    values = re.sub('\s','',value)
    values = re.sub(',','.',values)
    #print(values)
    if values.endswith('vues'):
        multiplier = 1
        valuez = re.sub('vues','',values)
        if valuez.endswith('k') :
            multiplier = 1000
            valuee = re.sub('k','',valuez)
            #print(valuee)
            return int(float(valuee) * multiplier)
    return int(float(valuez) * multiplier) 


    
def convert_yt_eng(value):
    import re
    values = re.sub('\s','',value)
    values = re.sub(',','.',values)
    #print(values)
    if values.endswith("d’abonnés"):
        multiplier = 1
        valuez = re.sub("d’abonnés",'',values)
        if valuez.endswith('M') :
            multiplier = 1000000
            valuee = re.sub('M','',valuez)
            #print(valuee)
            return int(float(valuee) * multiplier)
        elif valuez.endswith('k') :
            multiplier = 1000000
            valuee = re.sub('k','',valuez)
            #print(valuee)
            return int(float(valuee) * multiplier)
    return int(float(valuez) * multiplier) 
    

def convert_yt(value):
    import re
    values =re.sub('\s','',value)
    
    if values :
            multiplier = 1
    elif values.endswith('vues') : 
            values = values.replace('vues','')
            multiplier = 1
    elif values.endswith('kvues') or values.endswith('Kvues'):
                values = values.replace('kvues','')
                multiplier = 1000
    elif values.endswith('Mvues'):
                values = values.replace('Mvues','')
                multiplier = 1000000   
    elif values.endswith("Md’abonnés") :
            values = values.replace("Md’abonnés",'')
            multiplier = 1000000
    elif values.endswith('k d’abonnés') or values.endswith('Kd’abonnés'):
                values = values.replace('kd’abonnés','')
                multiplier = 1000
    elif values.endswith('M'):
                values = values.replace('M','')
                multiplier = 1000000           
    elif values.endswith('k'):
                values = values.replace('k','')
                multiplier = 1000      
                
    return int(float(values) * multiplier)
    
    
def tok_pro_anal(tokuser) : 
    try :
        query = {'ProfileName':tokuser}
        res = tt_profile.find(query)
        data = []
        for r in res :
            data.append(r)
        
        df = pd.DataFrame(data)
        latest_time = df['scraped_at'].max()     
        df = df.reset_index()
        
        for index,row in df.iterrows():
            if row["scraped_at"] == latest_time :
                x = row
        
        output = {
            'Influencer(Username)' : x['ProfileName'],
            'Influencer Image' : x['ProfileImageUrl'],
            'profile_url' : x['InfluencerURL'],
            'verified_status' : x['VerifiedStatus'],
            'biography' : x['Biography']
        }
        msg = 'Yey'
    except KeyError :
        output = {}
        msg = 'No timestamp ! Or Name not found, please try again !'
    
    return output,msg


def yt_pro_anal(ytuser) :
    try :
        query = {'channel title':ytuser}
        res = yt_profile.find(query)
        data = []
        for r in res :
            data.append(r)
        
        df = pd.DataFrame(data)
        latest_time = df['scraped_at'].max()     
        df = df.reset_index()
        
        for index,row in df.iterrows():
            if row["scraped_at"] == latest_time :
                x = row
        
        output = {
            'Influencer(Username)' : x['channel title'],
            'Influencer Image' : x['channel avatar url'],
            #'profile_url' : x['ProfileURL'],
            'verified_status' : x['verified status'],
            'biography' : x['biography']
        }
        msg = 'Yey'
    except KeyError :
        output = {}
        msg = 'No timestamp ! Or name not found, please try again !'
    
    return output,msg

def yt_inf_reach(user):
 
    query1 = { 'channel title': user }
    query2 = { 'Username': user }
    res1 = yt_profile.find(query1)
    res2 = yt_pro_posts.find(query2)
    
    
    data1 =[]
    for r in res1 :
        data1.append(r)
        
    df1 = pd.DataFrame(data1)
    recent_profile = df1['scraped_at'].max()
    df1 = df1.reset_index()
    
    for index,row in df1.iterrows():
        
        if row['scraped_at'] == recent_profile :
            output1 = row

    data2 =[]
    for r in res2 :
        data2.append(r)
        
    df2 = pd.DataFrame(data2)
    recent_posts = df2['scraped_at'].max()
    df2 = df2.reset_index()
    
    for index,row in df2.iterrows():
        if row['scraped_at'] == recent_posts :
            output2 = row
    
    total_no_comments = sum([convert(output2['PostsList'][i]['totalComments']) for i in range(len(output2['PostsList']))])
    total_no_likes = sum([convert(output2['PostsList'][i]['totalLikes']) for i in range(len(output2['PostsList']))])
    
    
    general_reach = {
        
        'no_of_subscribers' : output1['subscribers count'],
        'totalComments' : total_no_comments,
        'totalViews' : output1['total number views'],
        'totalLikes' : total_no_likes
    }
    return general_reach

def yt_inf_engagement(user):
    
    query = { 'Username': user }
    res = yt_pro_posts.find(query)
    data = []
    for r in res :
        data.append(r)
    
    df = pd.DataFrame(data)
    recent = df['scraped_at'].max()
    df.reset_index()
    
    for index,row in df.iterrows():
        if row['scraped_at'] == recent :
            output = row
    
    #print([output['PostsList'][i]['views'] for i in range(10)])
    avg_likes = sum([convert(output['PostsList'][i]['totalLikes']) for i in range(10)])/10
    avg_comments = sum([convert_yt(output['PostsList'][i]['totalComments']) for i in range(10)])/10
    avg_views = sum([convert_yt_views(output['PostsList'][i]['views']) for i in range(10)])/10
    #total_no_comments = sum([convert(output['PostsList'][i]['totalComments']) for i in range(len(output['PostsList']))])
    
    query1 = { 'channel title': user }
    data1 =[]
    res1 = yt_profile.find(query1)
    for r in res1 :
        data1.append(r)
        
    df1 = pd.DataFrame(data1)
    recent_profile = df1['scraped_at'].max()
    df1 = df1.reset_index()
    
    for index,row in df1.iterrows():
        
        if row['scraped_at'] == recent_profile :
            output1 = row
            
    total_no_likes = sum([convert_yt(output['PostsList'][i]['totalLikes']) for i in range(len(output['PostsList']))])
    total_no_comments = sum([convert_yt(output['PostsList'][i]['totalComments']) for i in range(len(output['PostsList']))])
    engagement_rate = sum([convert_yt(output['PostsList'][i]['totalLikes']) for i in range(10)])/convert_yt_eng(output1['subscribers count'])
    avg_engagement_rate = ((total_no_likes + total_no_comments)/convert_yt_eng(output1['subscribers count']))*100
    general_engagement = {
        
        'AvgLikes' : avg_likes,
        'AvgComments' : avg_comments,
        'AvgViews' : avg_views,
        'EngagementRate' : engagement_rate,
        'AvgEngagementRate' : avg_engagement_rate
        
    }
    return general_engagement

def tk_inf_reach(user):
 
    query1 = { 'ProfileName': user }
    query2 = { 'Username': user }
    res1 = tt_profile.find(query1)
    res2 = tt_pro_posts.find(query2)
    
    
    data1 =[]
    for r in res1 :
        data1.append(r)
        
    df1 = pd.DataFrame(data1)
    recent_profile = df1['scraped_at'].max()
    df1 = df1.reset_index()
    
    for index,row in df1.iterrows():
        
        if row['scraped_at'] == recent_profile :
            output1 = row

    data2 =[]
    for r in res2 :
        data2.append(r)
        
    df2 = pd.DataFrame(data2)
    recent_posts = df2['scraped_at'].max()
    df2 = df2.reset_index()
    
    for index,row in df2.iterrows():
        if row['scraped_at'] == recent_posts :
            output2 = row
    
    total_no_shares = sum([convert(output2['PostsList'][i]['no_shares']) for i in range(len(output2['PostsList']))])
    total_no_comments = sum([convert(output2['PostsList'][i]['no_comments']) for i in range(len(output2['PostsList']))])
    total_no_views = sum([convert(output2['PostsList'][i]['no_view']) for i in range(len(output2['PostsList']))])        
    total_no_likes = sum([convert(output2['PostsList'][i]['no_likes']) for i in range(len(output2['PostsList']))])
    
    
    general_reach = {
        
        'no_of_followers' : output1['FollowersNumber'],
        'no_of_followees' : output1['FolloweesNumber'],
        'TotalNumberLikes' : output1['TotalNumberLikes'],
        'totalShares' : total_no_shares,
        'totalComments' : total_no_comments,
        'totalViews' : total_no_views,
        'totalLikes' : total_no_likes
    }
    return general_reach

def tk_inf_engagement(user):
    
    query = { 'Username': user }
    res = tt_pro_posts.find(query)
    data = []
    for r in res :
        data.append(r)
    
    df = pd.DataFrame(data)
    recent = df['scraped_at'].max()
    df.reset_index()
    
    for index,row in df.iterrows():
        if row['scraped_at'] == recent :
            output = row
    
    avg_likes = sum([convert(output['PostsList'][i]['no_likes']) for i in range(10)])/10
    avg_comments = sum([convert(output['PostsList'][i]['no_comments']) for i in range(10)])/10
    avg_shares = sum([convert(output['PostsList'][i]['no_shares']) for i in range(10)])/10
    avg_views = sum([convert(output['PostsList'][i]['no_view']) for i in range(10)])/10
    total_no_comments = sum([convert(output['PostsList'][i]['no_comments']) for i in range(len(output['PostsList']))])
    
    query1 = { 'ProfileName': user }
    data1 =[]
    res1 = tt_profile.find(query1)
    for r in res1 :
        data1.append(r)
        
    df1 = pd.DataFrame(data1)
    recent_profile = df1['scraped_at'].max()
    df1 = df1.reset_index()
    
    for index,row in df1.iterrows():
        
        if row['scraped_at'] == recent_profile :
            output1 = row
            
    total_no_likes = sum([convert(output['PostsList'][i]['no_likes']) for i in range(len(output['PostsList']))])
    total_no_comments = sum([convert(output['PostsList'][i]['no_comments']) for i in range(len(output['PostsList']))])
    engagement_rate = sum([convert(output['PostsList'][i]['no_likes']) for i in range(10)])/convert(output1['FollowersNumber'])
    avg_engagement_rate = ((total_no_likes + total_no_comments)/convert(output1['FollowersNumber']))*100
    general_engagement = {
        
        'AvgLikes' : avg_likes,
        'AvgComments' : avg_comments,
        'AvgViews' : avg_views,
        'AvgShares' : avg_shares,
        'EngagementRate' : engagement_rate,
        'AvgEngagementRate' : avg_engagement_rate
        
    }
    return general_engagement
#print(tk_inf_reach('mo_vlogs'))