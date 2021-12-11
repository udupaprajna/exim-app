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



pages_menu = ["Products", "Customer", "Inventory", "Exports", "Imports", "Shipping"]
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
    

    
    id = st.text_input(label='Enter Product ID')
    unit_price = st.text_input(label='Enter Unit Price')
    quantity = st.text_input(label='Enter Quantity')
    name = st.text_input(label='Enter Product Name')
    cust_id = st.text_input(label='Enter Customer ID')

    if st.button("Add Product Details"):
        cur.execute("Insert into product values (%s,%s,%s,%s,%s);",(id, unit_price, quantity, name, cust_id))
        st.text("Data added")
        
    if st.button("View Details"):
        cur.execute("SELECT * from product")
        rows = cur.fetchall()
        df = pd.DataFrame(rows,columns = ('Prod_ID','Unit_Price','Quantity', 'Product_Name', 'Cust_ID'))
        st.write(df)

    with st.expander("Delete Product"):
        pid = st.selectbox("Choose product id for deleting",retrieve_product())       
        if st.button("Delete entry"):
            cur.execute("DELETE from product where prod_id = %s;",[pid])
    
    
elif page_choice == pages_menu[1]:
    st.subheader('Customer Details')
    st.markdown("***")

    id = st.text_input(label='Enter Customer ID')
    phone = st.text_input(label='Enter Phone Number')
    cust_company = st.text_input(label='Enter customer company')

    if st.button("Add Customer Details"):
        cur.execute("Insert into customer values (%s,%s,%s);",(id, phone, cust_company))
        st.text("Data added")

    with st.expander("Delete Customer details"):
        cid = st.selectbox("Choose customer id for deleting",retrieve_customer())       
        if st.button("Delete entry"):
            cur.execute("DELETE from customer where customer_id = %s;",[cid])
    

    if st.button("View"):
        cur.execute("select * from customer;")
        rows = cur.fetchall()
        df = pd.DataFrame(rows,columns = ('Customer ID','Phone', 'Customer Company'))
        st.write(df)

        
elif page_choice == pages_menu[2]:
    st.subheader('Inventory')
    st.markdown("***")

    id = st.text_input(label='Enter Inventory ID')
    inv_no = st.text_input(label='Enter Inventory Number')
    inv_item = st.text_input(label='Enter Item Name')
    desc = st.radio('Choose item description', ('Finished', 'Raw', 'Component', 'MRO'))
    prod_id = st.text_input(label='Enter prod ID')


    if st.button("Add Details"):
        cur.execute("Insert into inventory values(%s,%s,%s,%s,%s);", ( id, inv_no, inv_item, desc, prod_id))
        st.test("Reocord added!")
    
    with st.expander("Delete Customer details"):
        cid = st.selectbox("Choose customer id for deleting",retrieve_customer())       
        if st.button("Delete entry"):
            cur.execute("DELETE from customer where customer_id = %s;",[cid])
            st.write('Record deleted')

    if st.button("View"):
        cur.execute("select * from inventory;")
        rows = cur.fetchall()
        df = pd.DataFrame(rows,columns = ('inv_id', 'inv_no', 'inv_items', 'inventory_desc', 'prod_id'))
        st.write(df)
     

elif page_choice == pages_menu[3]:
    st.subheader('Exports')
    st.markdown("***")

    id = st.text_input(label='Enter Export ID')
    date = st.date_input(label='Enter  date of export')
    dest = st.text_input(label='Enter destination')
    prod = st.text_input(label = 'Enter prod name')
    inv_no = st.text_input(label = 'Enter invoice number')



    if st.button("Add Details"):
        cur.execute("Insert into export values(%s,%s,%s,%s,%s);",( id, date, dest, prod, inv_no))
        st.test("Record added!")

    with st.expander("Delete Customer details"):
        eid = st.selectbox("Choose export id for deleting",retrieve_export())       
        if st.button("Delete entry"):
            cur.execute("DELETE from export where export_id = %s;",[eid])
            st.write('Record deleted')

    if st.button("View"):
        cur.execute("select * from export;")
        rows = cur.fetchall()
        df = pd.DataFrame(rows,columns = ('export_id', 'date_of_export', 'export_dest', 'export_prod', 'invo_no'))
        st.write(df)
    

elif page_choice == pages_menu[4]:
    st.subheader('Imports')
    st.markdown("***")

    id = st.text_input(label='Enter import ID')
    prod = st.text_input(label='Enter Product name')
    quantity = st.text_input(label='Enter quantity')
    tariff = st.text_input(label='Tariff')
    inv_no = st.text_input(label='Enter invoice no')
    

    if st.button("Add Details"):
        cur.execute("Insert into import values(%s,%s,%s,%s,%s);" (id, prod, quantity, tariff, inv_no))
        st.test("Data added!")

    with st.expander("Delete Customer details"):
        imid = st.selectbox("Choose import id for deleting",retrieve_import())       
        if st.button("Delete entry"):
            cur.execute("DELETE from import where import_id = %s;",[imid])
            st.write('Record deleted')

    if st.button("View"):
        cur.execute("select * from import;")
        rows = cur.fetchall()
        df = pd.DataFrame(rows,columns = ('import_id', 'import_prod', 'quantity', 'tariff', 'inv_no'))
        st.write(df)

elif page_choice == pages_menu[5]:
    st.subheader('Shipping')
    st.markdown("***")

    id = st.text_input(label='Enter shipping ID')
    mode = st.text_input(label='Enter shipping mode')
    status = st.radio("Choose status", ('Ordered', 'Dispatched', 'Delivered'))
    location = st.text_input(label='enter location')
    date = st.date_input(label='Enter date')
    prod_id = st.text_input(label='Enter prod id')

    
    if st.button("Add Details"):
        cur.execute("Insert into shipping values(%s,%s,%s,%s,%s,%s);", (id, mode, status, location, date, prod_id))
        st.test("Data added!")

    with st.expander("Delete Customer details"):
        sid = st.selectbox("Choose shipping id for deleting",retrieve_shipping())       
        if st.button("Delete entry"):
            cur.execute("DELETE from shipping where shipping_id = %s;",[sid])
            st.write('Record deleted')

    if st.button("View"):
        cur.execute("select * from shipping")
        rows = cur.fetchall()
        df = pd.DataFrame(rows,columns = ('shipping_id',  'mode', 'shipment_status', 'location', 'shipping date','prod_ids'))
        st.write(df)
    
