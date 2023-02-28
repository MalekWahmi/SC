'''import streamlit as st
import time
import numpy as np
from streamlit_option_menu import option_menu


st.set_page_config(page_title="Brand Analysis", page_icon="📈",layout='wide')


ereac = st.sidebar.radio('Brand Analysis',('e-reputation','Reach','Engagement','Audience','Content'))


if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False
        #st.session_state.placeholder = "nike"


text_input = st.text_input(
            "Select Influencer from database 👇",
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled,
            #placeholder=st.session_state.placeholder,
        )


c1,c2,c3,c4 = st.columns([1,1,1,1])
with c4 :
    form = st.form("my_form")
    submitted = form.form_submit_button(label="Analyse Brand",type = "primary")

st.write('')
st.write('')
st.write('')
    
if ereac == "e-reputation" :
    st.markdown("# e-reputation")
    
elif ereac == "Reach" :
    m1,m2,m3,m4 = st.columns([1,1,1,1])
    m4.radio('Choose The Period in Days :',('7 Days','14 Days','30 Days'))
    m1.markdown('# Reach')    
           
elif ereac == "Engagement" :
    p1,p2,p3,p4 = st.columns([1,1,1,1])
    p4.radio('Choose The Period in Days :',('7 Days','14 Days','30 Days'))
    p1.markdown('# Engagement')

elif ereac == "Audience" :
    st.markdown("# Audience")
    st.radio('Choose The Period in Days :',('7 Days','14 Days','30 Days'))
    st.write('')
    st.write('')
    k1,k2,k3,k4 = st.columns([1,1,1,1])
    with k1 :
        st.markdown('Follower')
    with k4 :
        st.markdown('Likes')      
else:
    st.markdown("# Content")
    st.write("")
    st.write("")
    s1,s2 = st.columns([3,1])
    with s1 :
        st.markdown('Post Type')
    with s2 :
        st.radio('Choose The Period in Days :',('7 Days','14 Days','30 Days'))'''