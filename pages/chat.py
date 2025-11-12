import os
import asyncio
import streamlit as st
from dotenv import load_dotenv

from openai import OpenAI
from agents import Agent, Runner, function_tool

from src.utils import extract_text_from_pdf, extract_receipt_info
from src.database.local_database import ReceiptDatabase
from datetime import datetime


assert load_dotenv(), "Failed to load .env file"


# Initialize OpenAI client
# @st.cache_resource
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

# Initialize receipt database
receipt_database = ReceiptDatabase(db_path="data/receipts.db")
schema = receipt_database.get_schema()
st.json(schema, expanded=False)

AGENT_PROMPT = """
You are an AI assistant that helps users with information extracted from their food delivery receipts. Use the tools available to you to answer questions about the receipt data.
Here is the schema of the receipt database you can query:
{schema}

Current time: {current_time}

When answering questions, refer to the relevant fields in the database schema to provide accurate information. You can use the current time to provide context for time-based queries or comparisons.
"""


# Tool definition for the agent
@function_tool
def run_query(query: str) -> str:
    return receipt_database.execute_query(query)


agent = Agent(
    name="Agent-Receipt-Chatbot",
    instructions=AGENT_PROMPT.format(schema=schema, current_time=datetime.now().isoformat()),
    tools=[run_query],
)

async def run_agent(user_input: str):
    """Runs the OpenAI Agent with the given user input."""
    result = await Runner.run(agent, user_input)
    return result.final_output

# Tabs for upload/extract and chat
tab_chat, tab_insert = st.tabs(["Chat with Receipt", "Upload & Extract"])

# Upload & Extract Tab
with tab_insert:
    # Upload receipt file
    uploaded_file = st.file_uploader(
        "Upload your food receipt", 
        type=["png", "jpg", "jpeg", "pdf"],
        help="Supported formats: PNG, JPG, JPEG, PDF",
        key="receipt_uploader"  # Add unique key for better session handling
    )

    if uploaded_file is not None:
        st.success("File uploaded successfully!")
        uploaded_file_type = "pdf" if uploaded_file.name.lower().endswith(".pdf") else "image"
        
        # Display the uploaded image
        if uploaded_file_type == "image":
            st.image(uploaded_file, caption="Uploaded Receipt", use_column_width=True)
        else:
            st.info("PDF file uploaded. Preview not available.")
        
    else:
        st.info("📤 Please upload a food receipt to start chatting.")

    # Extract receipt information
    receipt_data = st.session_state.get("receipt_data", None)
    extract = st.button("Extract Receipt Information")
    if extract or (receipt_data is None and uploaded_file is not None):
        # Extract receipt information
        with st.spinner("🔍 Analyzing your receipt..."):
            try:
                if uploaded_file_type == "image":
                    # Get file bytes with error handling
                    file_bytes = uploaded_file.getvalue()
                    if len(file_bytes) == 0:
                        st.error("❌ Uploaded file is empty. Please try uploading again.")
                        st.stop()
                    receipt_data = extract_receipt_info(client, file_bytes)
                else:
                    # Get file bytes with error handling for PDF
                    file_bytes = uploaded_file.getvalue()
                    if len(file_bytes) == 0:
                        st.error("❌ Uploaded PDF is empty. Please try uploading again.")
                        st.stop()
                    text = extract_text_from_pdf(file_bytes)
                    st.write("Extracted Text from PDF:")
                    st.write(text)
                    receipt_data = extract_receipt_info(client, text)

                st.session_state["receipt_data"] = receipt_data
                st.success("✅ Receipt analysis completed!")
                
            except Exception as e:
                st.error(f"❌ Error processing file: {str(e)}")
                st.error("This might be due to a session issue. Please try uploading the file again.")
                # Clear the problematic data
                if "receipt_data" in st.session_state:
                    del st.session_state["receipt_data"]
    st.divider()

    # Display extracted receipt information
    st.title("Receipt Analysis Results")
    if receipt_data:
        # st.write(receipt_data)
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
    receipts = receipt_database.execute_query("SELECT * FROM receipts as r RIGHT JOIN receipt_items as ri ON r.id = ri.receipt_id")
    st.dataframe(receipts)

    schema = receipt_database.get_schema()
    with st.expander("Show Database Schema"):
        st.json(schema)
            

# Chat with Receipt Tab
chats = st.session_state.get("chats", [])
with tab_chat:
    # Show conversation history
    for chat in chats:
        st.chat_message(chat["role"]).write(chat["content"])

    # User input for chat
    user_question = st.chat_input("Ask a question about your receipt:")
    if user_question:
        chats.append({"role": "user", "content": user_question})
        st.session_state["chats"] = chats

        with st.spinner("🤖 Thinking..."):
            agent_response = asyncio.run(run_agent(user_question))

            chats.append({"role": "assistant", "content": agent_response})
            st.session_state["chats"] = chats
        
        st.rerun()
