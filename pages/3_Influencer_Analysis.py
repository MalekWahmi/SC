import streamlit as st
import time
import pandas as pd
from streamlit_option_menu import option_menu
import pymongo
from  content_page import content_yt,content_tk
from inf_anal_prof import tok_pro_anal,yt_pro_anal,tk_inf_reach,tk_inf_engagement,yt_inf_reach,yt_inf_engagement


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
tt_db = myclient["mytiktok"]
yt_db = myclient["myyoutube"]
tt_profile = tt_db["profileInfo"]
yt_profile = yt_db["profileInfo"]

st.set_page_config(page_title="Influencer Analysis", page_icon="📈",layout='wide',menu_items={
        'Get help' : 'https://forms.gle/3GfEfkenmRjT4yMv7'})


preac = st.sidebar.radio('Influencer Analysis',('Profile','Reach','Engagement','Audience','Content'))

if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False

st.write("Select Social Media Platform :")



selected =  option_menu(
    menu_title=None,
    options=[ "Youtube","Tiktok","Instagram"],
    icons=["youtube","tiktok","instagram"],  # https://icons.getbootstrap.com/
    orientation="horizontal",
    )

text_input = st.text_input(
            "Select Influencer from database 👇",
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled,
            #placeholder=st.session_state.placeholder,
        )


c1,c2,c3,c4,c5,c6,c7 = st.columns([1,1,1,1,1,1,1])
with c7 :
    form = st.form("my_form")
    submitted = st.button(label="Analyse Influencer",type='primary')
    #submitted = form.form_submit_button(label="Analyse Influencer",type = "primary")
st.write('')
st.write('')
st.write('')


if preac == 'Profile' :
    st.markdown('# Profile')
    if selected == 'Tiktok':
        t,mess = tok_pro_anal(text_input)
        st.table(pd.DataFrame(t,index=[0,]))
        #st.error(mess)
    elif selected == 'Youtube' :
        y,mess = yt_pro_anal(text_input)
        st.table(pd.DataFrame(y,index=[0,]))
        #st.error(mess) 
        
elif preac == 'Reach' :
    m1,m2,m3,m4 = st.columns([1,1,1,1])
    #m4.radio('Choose The Period in Days :',('7 Days','14 Days','30 Days'))
    m1.markdown('# Reach')
    if selected == 'Youtube' :
        y = yt_inf_reach(text_input)
        st.table(pd.DataFrame(y,index=[0,]))
    elif selected == 'Tiktok' :
        t = tk_inf_reach(text_input) 
        st.table(pd.DataFrame(t,index=[0,]))   
    
elif preac == 'Engagement' :
    p1,p2,p3,p4 = st.columns([1,1,1,1])
    #p4.radio('Choose The Period in Days :',('7 Days','14 Days','30 Days'))
    p1.markdown('# Engagement')
    if selected == 'Tiktok' :
        t = tk_inf_engagement(text_input)
        st.table(pd.DataFrame(t,index=[0,]))
    elif selected == 'Youtube' :
        y = yt_inf_engagement(text_input) 
        st.table(pd.DataFrame(y,index=[0,]))   
elif preac == 'Audience':
    st.markdown("# Audience")
    st.radio('Choose The Period in Days :',('7 Days','14 Days','30 Days'))
    st.write('')
    st.write('')
    k1,k2,k3,k4 = st.columns([1,1,1,1])
    with k1 :
        st.markdown('Follower')
    with k4 :
        st.markdown('Likes')
    
else :
    st.markdown("# Content")
    st.write("")
    st.write("")
    s1,s2 = st.columns([3,1])
    with s1 :
        if selected == 'Youtube' :
            d = content_yt(text_input)
            st.dataframe(d)

        if selected == 'Tiktok' :
            d = content_tk(text_input)
            st.dataframe(d)
    
    