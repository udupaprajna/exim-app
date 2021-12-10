import streamlit as st
import pandas as pd
import psycopg2
import time
from datetime import date
from PIL import Image

img = Image.open("logo.png")
st.sidebar.image(img, width=200)
st.header("EXPORT IMPORT MANAGEMENT SYSTEM")
st.subheader("TEAM-16")
st.markdown("***")

@st.experimental_singleton
def init_connection():
    
    return psycopg2.connect(dbname="exim",user="postgres",password="postgres",host="localhost",port=5432)
    #return psycopg2.connect(**st.secrets["postgres"])

conn = init_connection()
cur=conn.cursor()
conn.autocommit=True



def retrieve_customer():
    cur.execute("Select * from customer")
    rows= list(cur.fetchall())
    init=[]
    for i in range(len(rows)):
        init.append(rows[i][0])
    return init

def retrieve_product():
    cur.execute("Select * from product")
    rows= list(cur.fetchall())
    init=[]
    for i in range(len(rows)):
        init.append(rows[i][0])
    return init

def retrieve_invoice():
    cur.execute("Select * from invoice")
    rows= list(cur.fetchall())
    init=[]
    for i in range(len(rows)):
        init.append(rows[i][0])
    return init

def retrieve_export():
    cur.execute("Select * from export")
    rows= list(cur.fetchall())
    init=[]
    for i in range(len(rows)):
        init.append(rows[i][0])
    return init

def retrieve_import():
    cur.execute("Select * from import")
    rows= list(cur.fetchall())
    init=[]
    for i in range(len(rows)):
        init.append(rows[i][0])
    return init

def retrieve_shipping():
    cur.execute("Select * from shipping")
    rows= list(cur.fetchall())
    init=[]
    for i in range(len(rows)):
        init.append(rows[i][0])
    return init

def retrieve_inventory():
    cur.execute("Select * from inventory")
    rows= list(cur.fetchall())
    init=[]
    for i in range(len(rows)):
        init.append(rows[i][0])
    return init



pages_menu = ["Products", "Customer", "Inventory", "Logistics", "Exports", "Imports"]
page_choice = st.sidebar.selectbox("Menu",pages_menu)
#side_menu = st.sidebar.selectbox("Menu", pages_menu)

contact_menu = ["Phone", "Email", "Post"]
contact = st.sidebar.selectbox("Contact Us", contact_menu)

about_us = "We are a team dedicated to providing quality service. "
st.sidebar.write(about_us)


if page_choice == pages_menu[0] :
    st.subheader('Products')
    st.markdown("***")

    st.write("Add product details:")
    

    name = st.text_input(label='Enter Product Name')
    id = st.text_input(label='Enter Product ID')
    quantity = st.text_input(label='Enter Quantity')
    unit_price = st.text_input(label='Enter Unit Price')
    cust_id = st.text_input(label='Enter Customer ID')

    try:
            col1,col2= st.columns([5,1])
            with col1:
                if st.button("Add Product Details"):
                    cur.execute("insert into product values (id,unit_price, quantity, name, cust_id)")
                    st.text("Data added")
            with col2:
                if st.button("Show data"):
                    cur.execute("SELECT * from product")
                    rows=cur.fetchall()
                    df = pd.DataFrame(rows,columns = ('Prod_ID','Quantity','Unit_Price', 'Product_Name', 'Cust_ID'))
    except psycopg2.Error as e:
            error = e.pgcode
            st.write("The data already exists or the value entered is null")
            if st.button("Show data"):
                cur.execute("SELECT * from product")
                rows=cur.fetchall()
    
    




elif page_choice == pages_menu[1]:
    st.subheader('Customer Details')
    st.markdown("***")
    form = st.form(key='my_form')
    form.text_input(label='Enter some text')
    submit_button = form.form_submit_button(label='Submit')
    '''if st.button("Add Details"):
        cur.execute("Insert into product values(id,unit_price, quantity, name, cust_id);")
        st.test("Data added!")

    if st.button("View"):
        cur.execute("select * from product;")
        rows = cur.fetchall()
        print(rows)
        df = pd.DataFrame(rows,columns = ('Prod_ID','Quantity','Unit_Price', 'Product_Name', 'Cust_ID'))'''
elif page_choice == pages_menu[2]:
    st.subheader('Inventory')
    st.markdown("***")
    form = st.form(key='my_form')
    form.text_input(label='Enter some text')
    submit_button = form.form_submit_button(label='Submit')

elif page_choice == pages_menu[3]:
    st.subheader('Logistics')
    st.markdown("***")
    form = st.form(key='my_form')
    form.text_input(label='Enter some text')
    submit_button = form.form_submit_button(label='Submit')

elif page_choice == pages_menu[4]:
    st.subheader('Exports')
    st.markdown("***")
    form = st.form(key='my_form')
    form.text_input(label='Enter some text')
    submit_button = form.form_submit_button(label='Submit')

elif page_choice == pages_menu[5]:
    st.subheader('Imports')
    st.markdown("***")
    form = st.form(key='my_form')
    form.text_input(label='Enter some text')
    submit_button = form.form_submit_button(label='Submit')

