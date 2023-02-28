import streamlit as st

st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    layout="wide",
    menu_items={
        'Get help' : 'https://forms.gle/3GfEfkenmRjT4yMv7'
    }
)

st.title("Hello and Welcome aboard 👏")
st.markdown(
    """This app shows you how you can crawl social media platforms and fetch influencers or profile post information. 
Available platforms YouTube, TikTok and Instagram

    * Instagram : Search by username or a specific post URL
    * Tiktok : Search by username or specific post URL 
    * Youtube : Search by channel ID or  video URL of a specific

Available sections in the app

    1. Home
    2. Search Engine
    3. Database
    4. Influencers Analysis
    5. Post Analysis

Getting started 

* How to scrape an influencers profile 
    * To try scrape the profile, you first need to specify the account @handler/username
    * Copy and paste from the influencer social media profile and past into the search box
* How to scrape a brand profile
    * To try scrape the profile, you first need to specify the account @handler/username
    * Copy and paste from the influencer social media profile and past into the search box
* How to scrape a post
    * To try scrape the profile, you first need to specify the account @handler/username
    * Copy and paste from the influencer social media profile and past into the search box
* How to analyze a brand or an influencers profile 
* How to access an influencer analysis 

Go ahead, click on the menu to start exploring the tool :) 

    """
)



if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False

st.sidebar.success("Select a scraping job.")