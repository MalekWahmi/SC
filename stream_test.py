import streamlit as st  # pip install streamlit
#from streamlit_option_menu import option_menu  # pip install streamlit-option-menu

#import json
import pandas as pd
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")


# --- HIDE STREAMLIT STYLE ---

st.set_page_config("Scraping Tool",layout="wide")
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False

def hello():
    import streamlit as st
    st.title("Welcome to the data heaven 👋 ",)
    #st.write("")
    st.markdown("<h1 style='text-align: center; color: powderblue;'>To select a scraping job, Please chack out the sidebar for more options</h1>", unsafe_allow_html=True)
    st.sidebar.success("The choice is yours.")
    st.balloons()

def influencer_profile_info():
    import streamlit as st
    
    from tiktok_crawl import tok_browser
    from yt_crawl import yt_browser
    from streamlit_option_menu import option_menu
   
    tt_db = myclient["mytiktok"]
    yt_db = myclient["myyoutube"]
    tt_profile = tt_db["profileInfo"]
    yt_profile = yt_db["profileInfo"]
    
    
    st.markdown(f"# {list(page_names_to_funcs.keys())[1]}")
    
    

    text_input = st.text_input(
            "Enter influencer name 👇",
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled,
            #placeholder=st.session_state.placeholder,
        )

    selected =  option_menu(
        menu_title=None,
        options=[ "Youtube","Tiktok","Instagram"],
        icons=["youtube","tiktok","instagram"],  # https://icons.getbootstrap.com/
        orientation="horizontal",
    )


    form = st.form("my_form")
    submitted = form.form_submit_button(label="Scrape Influencer Profile")

    if submitted :
        if selected == "Tiktok" :
            data = tok_browser(text_input)
            
            tt_profile.insert_one(data)
         
            df = pd.Series(data).to_frame("Influencer Profile")
            st.write(df)
        
        if selected == "Youtube" :
            data = yt_browser(text_input)
            yt_profile.insert_one(data)
            df = pd.Series(data).to_frame("Influencer Profile")
            st.write(df)
            
        if selected == "Instagram" :
            st.write("Sorry this feature is curently under development !") 
            
        
        
        
    else: st.write("please enter a valid name !")
    
def post_info() :
    from tk_posts import tk_post
    from yt_posts import yt_post
    import streamlit as st
    from streamlit_option_menu import option_menu
    
    tt_db = myclient["mytiktok"]
    yt_db = myclient["myyoutube"]
    tt_posts = tt_db["postsInfo"]
    yt_posts = yt_db["postsInfo"]
    
    
    
    st.markdown(f"# {list(page_names_to_funcs.keys())[2]}")


    text_input = st.text_input(
            "Enter Post URL 👇",
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled,
            #placeholder=st.session_state.placeholder,
        )

    selected =  option_menu(
        menu_title=None,
        options=[ "Youtube","Tiktok","Instagram"],
        icons=["youtube","tiktok","instagram"],  # https://icons.getbootstrap.com/
        orientation="horizontal",
    )


    form = st.form("my_form")
    submitted = form.form_submit_button(label="Scrape")

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
    
page_names_to_funcs = {
    "Welcome page": hello,
    "Influencer Profile Info": influencer_profile_info,
    "Posts KPIs": post_info
}    
    
job_name = st.sidebar.radio("Choose a Job", page_names_to_funcs.keys())
page_names_to_funcs[job_name]()  
    
    
    
    
    
    
    
    
    
    
       