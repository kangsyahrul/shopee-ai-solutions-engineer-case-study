import streamlit as st

# Define the pages
main_page = st.Page("main.py", title="Main Page", icon="🎈")
page_chat = st.Page("pages/chat.py", title="Chat", icon="💬")
page_database = st.Page("pages/qdrant_vectordb.py", title="Qdrant Vector DB", icon="❄️")
page_custom_vectordb = st.Page("pages/custom_vectordb.py", title="Custom Vector DB", icon="❄️")

# Set up navigation
pg = st.navigation([main_page, page_custom_vectordb, page_database, page_chat])

# Run the selected page
pg.run()
