import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text

def get_connection():
    
    engine = create_engine("mysql+pymysql://root:root@host.docker.internal:3306/query_mgt")

    return engine

st.title("Tesla Software Solutions")
st.title("Tesla Solutions Pro delivers cutting-edge software solutions that transform how businesses operate in the digital age." \
"We specialize in custom application development, cloud integration, and enterprise automation to streamline your processes")
st.subheader("Login Portal")
tab1, tab2 = st.tabs(["Customer Login", "Support Team Login"])


from sqlalchemy import text


with tab1:
    st.header("Submit Your Query")
    email = st.text_input("Your Email")
    mobile = st.text_input("Your Mobile Number")
    heading = st.text_input("Query Heading")
    description = st.text_area("Query Description")

    if st.button("Submit Query"):
        if email and mobile and heading and description:
            conn = get_connection()
            with conn.begin() as connection:
                connection.execute(
                    text("""
                        INSERT INTO client_qry
                        (client_email, client_mobile, query_heading, query_description, status) 
                        VALUES (:e, :m, :h, :d, 'Open')
                    """),
                    {"e": email, "m": mobile, "h": heading, "d": description}
                )
            st.success("Query submitted successfully!")
        else:
            st.error("Please fill all fields.")





   
       
 

 


    



  


  
            


            
               
        
        
                    

with tab2:
    st.header("Support Dashboard")
    conn = get_connection()
    with conn.begin() as connection:
        result = connection.execute(text("SELECT * FROM client_qry WHERE status != 'Closed'"))
        rows = result.fetchall()
        if rows:
            df = pd.DataFrame(rows, columns=result.keys())
            for _, row in df.iterrows():
                st.subheader(f"Query #{row['id']} - {row['query_heading']}")
                st.write(f"Email: {row['client_email']}")
                st.write(f"Mobile: {row['client_mobile']}")
                st.write(f"Description: {row['query_description']}")
                st.write(f"Status: {row['status']}")
                st.write(f"Raised on: {row['date_raised']}")

                if st.button(f"Mark as Closed", key=row['id']):
                    connection.execute(
                        text("UPDATE client_qry SET status='Closed', date_closed=NOW() WHERE id=:i"),
                        {"i": row['id']}
                    )
                    st.success(f"✅ Query #{row['id']} closed")
        else:
            st.info("No open queries right now")
