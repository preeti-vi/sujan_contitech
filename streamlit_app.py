import streamlit as st
from core import main
from streamlit import logger

__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import sqlite3

app_logger = logger.get_logger("SMI_APP")
app_logger.info(f"SQLite version : {sqlite3.sqlite_version}")

st.title("Sujan Contitech AVS Pvt. Ltd. -AI-Powered Assistant")
st.text("How may I assist you ...")

user_query = st.text_input("Ask a query: ", max_chars=60)

btn = st.button("Find Answer")

if btn or user_query:
    placeholder = st.empty()
    placeholder.write("I am getting the answer...")

    response = main.get_response(user_query) #, app_logger)

    placeholder.empty()
    st.write(response)