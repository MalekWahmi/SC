import streamlit as st
from tiktok_crawl import tok_browser
from yt_crawl import yt_browser
from streamlit_option_menu import option_menu
from yt_profile_post import ypp
from tk_profile_post import ttpp
#from shares_comments import shares_comments

import pandas as pd
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
tt_db = myclient["mytiktok"]
yt_db = myclient["myyoutube"]
tt_profile = tt_db["profileInfo"]
yt_profile = yt_db["profileInfo"]
yt_pro_posts = yt_db["profilePosts"]
tt_pro_posts = tt_db["profilePosts"]


st.set_page_config(page_title="🔎 Search engine",layout='wide',menu_items={
        'Get help' : 'https://forms.gle/3GfEfkenmRjT4yMv7'})

if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False

st.write("Select Social Media Platform :")
st.sidebar.header("Search Engine")


selected =  option_menu(
    menu_title=None,
    options=[ "Youtube","Tiktok","Instagram"],
    icons=["youtube","tiktok","instagram"],  # https://icons.getbootstrap.com/
    orientation="horizontal",
    )

text_input = st.text_input(
            "Search for influencer by username 👇",
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled,
            #placeholder=st.session_state.placeholder,
        )


c1,c2,c3,c4,c5 = st.columns([1,1,1,1,1])
with c5 :
    form = st.form("my_form")
    submitted = st.button(label="Scrape Influencer Profile",type='primary')
    #submitted = form.form_submit_button(label="Scrape Influencer Profile",type = "primary")

if submitted :
    if selected == "Tiktok" :
        
        data = tok_browser(text_input)
        posts_kpis,no_posts,time = ttpp(text_input)
        #shares,comments = shares_comments(text_input)
        
        posts_info = {
            'Username' : data['ProfileName'],
            'PostsList' : posts_kpis,
            'PostsNumber' : no_posts,
            'scraped_at' : time
        }
        tt_pro_posts.insert_one(posts_info)
        tt_profile.insert_one(data)         
        df = pd.Series(data).to_frame("Influencer Profile")
        st.write(df)
        st.balloons()
        
    if selected == "Youtube" :
        data = yt_browser(text_input)
        posts_list,no_posts,scrap_time = ypp(text_input)
        posts_info = {
            'Username' : data['channel title'],
            'PostsList' : posts_list,
            'PostsNumber' : no_posts,
            'scraped_at' : scrap_time
        }
        yt_profile.insert_one(data)
        yt_pro_posts.insert_one(posts_info)
        df = pd.Series(data).to_frame("Influencer Profile")
        st.write(df)
        st.balloons()
            
    if selected == "Instagram" :
        st.write("Sorry this feature is curently under development !") 
                
    else: st.write("please enter a valid name !")





