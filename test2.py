import streamlit as st
import pandas as pd
import psycopg2
import time
from datetime import date
st.write("hey")
st.write("!!!!!!")

@st.experimental_singleton
def init_connection():
    
    return psycopg2.connect(dbname="exim",user="postgres",password="postgres",host="localhost",port=5432)
    #return psycopg2.connect(**st.secrets["postgres"])

conn = init_connection()
cur=conn.cursor()
conn.autocommit=True

cur.execute("Select * from customer")
rows= list(cur.fetchall())
init=[]
for i in range(len(rows)):
    init.append(rows[i][0])
st.write(init)

def retrieve_customer():
    cur.execute("Select * from customer")
    rows= list(cur.fetchall())
    init=[]
    for i in range(len(rows)):
        init.append(rows[i][0])
    return init
