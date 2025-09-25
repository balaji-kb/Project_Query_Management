# Project Query Management
A Streamlit application for query management.

# Packages
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime

# Customer Login Tab
client_email = st.text_input("Email")
client_mobile = st.text_input("Mobile")
query_heading = st.text_input("Query Heading")
query_description = st.text_area("Query Description") 

# Support Team Login Tab

with tab2:
st.header("Support Team - Manage Queries")

engine = get_connection()
with engine.connect() as conn:
df = pd.read_sql("SELECT * FROM client_queries", conn)

if df.empty:
st.info("No queries found.")

    