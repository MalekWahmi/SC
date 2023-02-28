from tk_posts import tk_post
from yt_posts import yt_post
import streamlit as st
from streamlit_option_menu import option_menu
import pymongo
import pandas as pd


myclient = pymongo.MongoClient("mongodb://localhost:27017/")

tt_db = myclient["mytiktok"]
yt_db = myclient["myyoutube"]
tt_posts = tt_db["postsInfo"]
yt_posts = yt_db["postsInfo"]

st.set_page_config(page_title="Post Analysis", page_icon="📈",layout='wide',menu_items={
        'Get help' : 'https://forms.gle/3GfEfkenmRjT4yMv7'})

if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False
        
st.sidebar.header("Post Analysis")

st.write("Select Social Media Platform :")
selected =  option_menu(
        menu_title=None,
        options=[ "Youtube","Tiktok","Instagram"],
        icons=["youtube","tiktok","instagram"],  
        orientation="horizontal",
    )


text_input = st.text_input(
            "Enter Post URL 👇",
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled,
            #placeholder=st.session_state.placeholder,
        )
c1,c2,c3,c4,c5,c6,c7,c8 = st.columns([1,1,1,1,1,1,1,1])
with c8 :
    form = st.form("my_form")
    submitted = st.button(label="Analyse Post",type='primary')
    #submitted = form.form_submit_button(label="Analyse Post",type = "primary")

if submitted :
    if selected == "Tiktok" :
        
        data = tk_post(text_input)        
        tt_posts.insert_one(data) 
        df = pd.Series(data).to_frame("Post KPIs")
        st.write(df)
        
    if selected == "Youtube" :
        data = yt_post(text_input)
        yt_posts.insert_one(data)
        df = pd.Series(data).to_frame("Post KPIs")
        st.write(df)
            
    if selected == "Instagram" :
        st.write("Sorry this feature is curently under development !") 
            
else: st.write("please enter a valid URL !")