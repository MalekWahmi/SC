import streamlit as st
import time
import numpy as np
import pymongo
import pandas as pd 
from jsonmerge import Merger


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
tt_db = myclient["mytiktok"]
yt_db = myclient["myyoutube"]
tt_profile = tt_db["profileInfo"]
yt_profile = yt_db["profileInfo"]

st.set_page_config(page_title="Database", page_icon="database-symbol.png",layout='wide',menu_items={
        'Get help' : 'https://forms.gle/3GfEfkenmRjT4yMv7'})

if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False

def counter(collection):
    count_my_doc = collection.count_documents({})
    return count_my_doc

st.sidebar.header("Database")
m1,m2,m3,m4 = st.columns((1,1,1,1))

tiktok_count = counter(tt_profile)
yt_count = counter(yt_profile)

m1.metric(label ='Total Scraped Accounts',value = tiktok_count + yt_count)
m2.metric(label ='Instagram',value= 0)
m3.metric(label = 'TikTok',value=tiktok_count)
m4.metric(label = 'Youtube',value=yt_count)


m1.write("")
m1.write("")
m1.write("")
select = m1.selectbox(label='Select Social Media Platform',options=['Instagram','Youtube','Tiktok'])
st.write("")
st.write("")
text_input = st.text_input(
            "Search for influencer in scraped account 👇",
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled,
            #placeholder=st.session_state.placeholder,
        )

c1,c2,c3,c4,c5,c6,c7 = st.columns([1,1,1,1,1,1,1])
with c7 :
    form = st.form("my_form")
    submitted = st.button(label="Get Account Infos",type='primary')

if select == 'Tiktok' :
    if submitted :
        query = { 'ProfileName': text_input }
        res = tt_profile.find(query)
        d= []
        for x in res :
            d.append(x)
            #st.write(d) # insert value in a dataframe !!!!!!!!!!!!!!!!! to do tomorrow
        df = pd.DataFrame(d)
        output = {
            'First scraped at' : df["scraped_at"].min(),
            'Last scraped at' : df["scraped_at"].max(),
            'Profile URL' : 'https://www.tiktok.com/@'+ text_input,
            'Profile Analysis' : 'Ready'
        }
        st.table(pd.DataFrame(output,index=[0,]))
        
if select == 'Youtube' :
    if submitted :
        query = { 'channel title': text_input }
        res = yt_profile.find(query)
        d= []
        for x in res :
            d.append(x)
            #st.write(d) # insert value in a dataframe !!!!!!!!!!!!!!!!! to do tomorrow
        df = pd.DataFrame(d)
        st.dataframe(df)