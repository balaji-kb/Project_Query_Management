import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime

# -----------------------
# Database Connection
# -----------------------
def get_connection():
    engine = create_engine("mysql+pymysql://root:root@localhost/guvi_query")
    return engine

# -----------------------
# Streamlit App UI
# -----------------------
st.title("Kb Software Solutions - Client Query Management")

st.subheader("Login Portal")
tab1, tab2 = st.tabs(["Customer Login", "Support Team Login"])

# -----------------------
# Customer Login Tab
# -----------------------
with tab1:
    st.header("Submit Your Query")

    client_email = st.text_input("Email")
    client_mobile = st.text_input("Mobile")
    query_heading = st.text_input("Query Heading")
    query_description = st.text_area("Query Description")

    if st.button("Submit Query"):
        if client_email and client_mobile and query_heading and query_description:
            engine = get_connection()
            with engine.connect() as conn:
                conn.execute(
                    text("""
                        INSERT INTO client_queries
                        (client_email, client_mobile, query_heading, query_description, status, date_raised)
                        VALUES (:e, :m, :h, :d, 'Open', NOW())
                    """),
                    {"e": client_email, "m": client_mobile, "h": query_heading, "d": query_description}
                )
                conn.commit()
            st.success("✅ Your query has been submitted successfully!")
        else:
            st.error("⚠️ Please fill in all fields before submitting.")

# -----------------------
# Support Team Login Tab
# -----------------------
with tab2:
    st.header("Support Team - Manage Queries")

    engine = get_connection()
    with engine.connect() as conn:
        df = pd.read_sql("SELECT * FROM client_queries", conn)

    if df.empty:
        st.info("No queries found.")
    else:
        # Filter toggle
        show_closed = st.checkbox("Show closed queries", value=False)

        if not show_closed:
            df = df[df["status"] == "Open"]

        st.dataframe(df)

        # Close query
        query_id = st.number_input("Enter Query ID to close", min_value=1, step=1)
        if st.button("Close Query"):
            with engine.connect() as conn:
                conn.execute(
                    text("UPDATE client_queries SET status='Closed', date_closed=NOW() WHERE id=:id"),
                    {"id": query_id}
                )
                conn.commit()
            st.success(f"✅ Query {query_id} marked as Closed!")
