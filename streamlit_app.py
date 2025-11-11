import streamlit as st

# Define the pages
main_page = st.Page("main.py", title="Main Page", icon="🎈")
page_database = st.Page("pages/database.py", title="Vector Database", icon="❄️")

# Set up navigation
pg = st.navigation([main_page, page_database])

# Run the selected page
pg.run()
