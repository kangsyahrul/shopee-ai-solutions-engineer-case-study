import streamlit as st
import os
from openai import OpenAI
from src.utils import extract_receipt_info
from src.database.local_database import ReceiptDatabase

# Initialize OpenAI client
@st.cache_resource
def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("OpenAI API key not found. Please set OPENAI_API_KEY environment variable.")
        return None
    return OpenAI(api_key=api_key)

st.title("Online Food Receipt Chatbot")
st.markdown("This chatbot extracts important information from your food delivery receipts.")

# Get OpenAI client
client = get_openai_client()
receipt_database = ReceiptDatabase(db_path="data/receipts.db")

tab_insert, tab_chat = st.tabs(["Upload & Extract", "Chat with Receipt"])
with tab_insert:
    # Upload receipt file
    uploaded_file = st.file_uploader(
        "Upload your food receipt", 
        type=["png", "jpg", "jpeg"],
        help="Supported formats: PNG, JPG, JPEG"
    )

    if uploaded_file is not None:
        st.success("File uploaded successfully!")
        
        # Display the uploaded image
        st.image(uploaded_file, caption="Uploaded Receipt", use_column_width=True)
        
    else:
        st.info("📤 Please upload a food receipt to start chatting.")

    # Extract receipt information
    receipt_data = st.session_state.get("receipt_data", None)
    extract = st.button("Extract Receipt Information")
    if extract or (receipt_data is None and uploaded_file is not None):
        # Extract receipt information
        with st.spinner("🔍 Analyzing your receipt..."):
            bytes_data = uploaded_file.getvalue()
            receipt_data = extract_receipt_info(client, bytes_data)
            st.session_state["receipt_data"] = receipt_data
        
        st.success("✅ Receipt analysis completed!")
    st.divider()

    # Display extracted receipt information
    st.title("Receipt Analysis Results")
    if receipt_data:
        st.write(receipt_data.to_dict())

        # Insert into database
        if st.button("Store Receipt in Local Database"):
            with st.spinner("💾 Storing receipt data..."):
                res = receipt_database.insert_receipt(receipt_data)
                if res:
                    st.success("✅ Receipt data stored successfully!")
                else:
                    st.error("❌ Failed to store receipt data.")
    else:
        st.info("No receipt data extracted yet.")
    st.divider()

    # Show all stored receipts
    st.title("Stored Receipts in Local Database")
    receipts = receipt_database.execute_query("SELECT * FROM receipts")
    st.dataframe(receipts)
            