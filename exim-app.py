import streamlit as st
import pandas as pd
import psycopg2
import time
from datetime import date
from PIL import Image


img = Image.open("logo.png")
st.sidebar.image(img, width=200)
st.header('EXPORT IMPORT MANAGEMENT SYSTEM')
st.subheader("TEAM-16")
st.markdown("***")

@st.experimental_singleton
def init_connection():
    return psycopg2.connect(dbname="exim",user="postgres",password="postgres",host="localhost",port=5432)
    

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


pages_menu = ["Home","Customer","Products",  "Inventory", "Exports", "Imports", "Shipping", "View mode"]
page_choice = st.sidebar.selectbox("Menu",pages_menu)

query_list = ["Choose Query", "View Shipping Status of Product","Update destination of exports", "View count of Inventory Products", "Average Payments made by Customer", "Display invoice of products with import tariff lesser than 15%"]
query_choice = st.sidebar.selectbox("Queries",query_list)

contact_menu = ["Phone", "Email", "Post"]
contact = st.sidebar.selectbox("Contact Us", contact_menu)

about_us = "We are a team dedicated to providing quality service. "
st.sidebar.write(about_us)

#Queries
if query_choice == query_list[1]:
    st.subheader(query_list[1])
    st.markdown("***")

    status_choice = st.radio("Choose status", ('Ordered', 'Dispatched', 'Delivered'))
    try:
        if st.button("View Details"):
            cur.execute("Select * from Shipping where shipment_status = '"+status_choice+"';")
            rows = cur.fetchall()
            df = pd.DataFrame(rows,columns = ('shipping_id',  'mode', 'shipment_status', 'location', 'shipping date','prod_ids'))
            st.write(df)
    except psycopg2.Error as e:
        error = e.pgcode
        st.write("We cannot retrieve the status at this moment")
        
elif query_choice == query_list[2]:
    st.subheader(query_list[2])
    st.markdown("***")

    old_dest = st.text_input(label="Enter current location of export product")
    new_dest = st.text_input(label="Enter new location of export product")
    
    try:
        if st.button("Update details"):
            cur.execute(f"Update export set export_dest = '{new_dest}' where export_dest = '{old_dest}';")
            cur.execute("select * from export")
            rows = cur.fetchall()
            df = pd.DataFrame(rows,columns = ('export_id', 'date_of_export', 'export_dest', 'export_prod', 'invo_no'))
            st.text("Updated!")
            st.write(df)
    except psycopg2.Error as e:
        error = e.pgcode
        st.write("We are not exporting to this location")

elif query_choice == query_list[3]:
    st.subheader(query_list[3])
    st.markdown("***")

    cur.execute("Select count(*) from inventory;")
    rows = cur.fetchall()
    for row in rows:
        st.write("Inventory Stock:", row )

    st.write("Display inventory items by order of quantity")
    if st.button("Display"):
        cur.execute("Select  inv_no, inv_id, inv_items from inventory order by inv_no desc;")
        rows = cur.fetchall()
        df = pd.DataFrame(rows,columns = ( 'Quantity', 'Inventory ID', 'Inventory Item'))
        st.write(df)

elif query_choice == query_list[4]:
    st.subheader(query_list[4])
    st.markdown("***")

    if st.button("Display"):
            cur.execute("Select payments.payment_id, avg(payments.amount) from payments group by payments.payment_id;")
            #cur.execute("Select supplier.supplier_type, supplier.supplier_id, customer.cust_company from supplier, customer where customer.customer_id = supplier.cust_id group by (supplier.supplier_type, supplier.supplier_id, customer.cust_company);")
            rows = cur.fetchall()
            df = pd.DataFrame(rows, columns = ('Payment ID', 'Average Amount'))
            #df = pd.DataFrame(rows, columns=( 'Supplier Type', 'Supplier ID', 'Customer ID'))
            st.write(df)
    

elif query_choice == query_list[5]:
    st.subheader(query_list[5])
    st.markdown("***")

    if st.button("Display"):
        cur.execute("Select invoice.invoice_no, invoice.product, invoice.date_of_purchase, import.tariff from invoice, import where import.tariff < 15 and invoice.invoice_no = import.inv_no; ")
        rows = cur.fetchall()
        df = pd.DataFrame(rows, columns = ('Invoice ID', 'Product Name', 'Date of Purchase','Tariff' ))
        st.write(df)



#CRUD Operations
if page_choice == pages_menu[0] :
    st.image(["1.png", "2.png", "3.png", "5.png", "4.png"], width=244)
    st.balloons()

if page_choice == pages_menu[1] :
    st.subheader('Customer Details')
    st.markdown("***")

    st.write("Add customer details:")
    id = st.text_input(label='Enter Customer ID')
    phone = st.text_input(label='Enter Phone Number')
    cust_company = st.text_input(label='Enter customer company')

    #INSERT OPERATION
    if st.button("Add Customer Details"):
        cur.execute("Insert into customer values (%s,%s,%s);",(id, phone, cust_company))
        st.text("Data added")

    #DELETE OPERATION
    with st.expander("Delete Customer details"):
        cid = st.selectbox("Choose customer id for deleting",retrieve_customer())       
        if st.button("Delete entry"):
            cur.execute("DELETE from customer where customer_id = %s;",[cid])
    
     #VIEW
    if st.button("View"):
        cur.execute("select * from customer;")
        rows = cur.fetchall()
        df = pd.DataFrame(rows,columns = ('Customer ID','Phone', 'Customer Company'))
        st.write(df)
    

elif page_choice == pages_menu[2]:
    st.subheader('Products')
    st.markdown("***")

    st.write("Add product details:")
    
    id = st.text_input(label='Enter Product ID')
    unit_price = st.text_input(label='Enter Unit Price')
    quantity = st.text_input(label='Enter Quantity')
    name = st.text_input(label='Enter Product Name')
    cust_id = st.text_input(label='Enter Customer ID')

    #INSERT OPERATION
    if st.button("Add Product Details"):
        cur.execute("Insert into product values (%s,%s,%s,%s,%s);",(id, unit_price, quantity, name, cust_id))
        st.text("Data added")

    #DELETE OPERATION    
    with st.expander("Delete Product"):
        pid = st.selectbox("Choose product id for deleting",retrieve_product())       
        if st.button("Delete entry"):
            cur.execute("DELETE from product where prod_id = %s;",[pid])

     #VIEW
    if st.button("View Details"):
        cur.execute("SELECT * from product")
        rows = cur.fetchall()
        df = pd.DataFrame(rows,columns = ('Prod_ID','Unit_Price','Quantity', 'Product_Name', 'Cust_ID'))
        st.write(df)

        
elif page_choice == pages_menu[3]:
    st.subheader('Inventory')
    st.markdown("***")

    st.write("Add Inventory Item details:")
    id = st.text_input(label='Enter Inventory ID')
    inv_no = st.text_input(label='Enter Inventory Number')
    inv_item = st.text_input(label='Enter Item Name')
    desc = st.radio('Choose item description', ('Finished', 'Raw', 'Component', 'MRO'))
    prod_id = st.text_input(label='Enter prod ID')

    #INSERT OPERATION
    if st.button("Add Details"):
        cur.execute("Insert into inventory values(%s,%s,%s,%s,%s);", ( id, inv_no, inv_item, desc, prod_id))
        st.text("Reocord added!")
    
    #DELETE OPERATION
    with st.expander("Delete Inventory product details"):
        cid = st.selectbox("Choose customer id for deleting",retrieve_customer())       
        if st.button("Delete entry"):
            cur.execute("DELETE from customer where customer_id = %s;",[cid])
            st.write('Record deleted')

     #VIEW
    if st.button("View"):
        cur.execute("select * from inventory;")
        rows = cur.fetchall()
        df = pd.DataFrame(rows,columns = ('inv_id', 'inv_no', 'inv_items', 'inventory_desc', 'prod_id'))
        st.write(df)
     

elif page_choice == pages_menu[4]:
    st.subheader('Exports')
    st.markdown("***")

    st.write("Add Export Product details:")
    id = st.text_input(label='Enter Export ID')
    date = st.date_input(label='Enter  date of export')
    dest = st.text_input(label='Enter destination')
    prod = st.text_input(label = 'Enter prod name')
    inv_no = st.text_input(label = 'Enter invoice number')

    #INSERT OPERATION
    if st.button("Add Details"):
        cur.execute("Insert into export values(%s,%s,%s,%s,%s);",( id, date, dest, prod, inv_no))
        st.text("Record added!")

    #DELETE OPERATION
    with st.expander("Delete Export product details"):
        eid = st.selectbox("Choose export id for deleting",retrieve_export())       
        if st.button("Delete entry"):
            cur.execute("DELETE from export where export_id = %s;",[eid])
            st.write('Record deleted')

    #VIEW OPERATION
    if st.button("View"):
        cur.execute("select * from export;")
        rows = cur.fetchall()
        df = pd.DataFrame(rows,columns = ('export_id', 'date_of_export', 'export_dest', 'export_prod', 'invo_no'))
        st.write(df)
    

elif page_choice == pages_menu[5]:
    st.subheader('Imports')
    st.markdown("***")

    st.write("Add Import Product details:")
    id = st.text_input(label='Enter import ID')
    prod = st.text_input(label='Enter Product name')
    quantity = st.text_input(label='Enter quantity')
    tariff = st.text_input(label='Tariff')
    inv_no = st.text_input(label='Enter invoice no')
    
    #INSERT OPERATION
    if st.button("Add Details"):
        cur.execute("Insert into import values(%s,%s,%s,%s,%s);" (id, prod, quantity, tariff, inv_no))
        st.text("Data added!")

    #DELETE OPERATION
    with st.expander("Delete Import product  details"):
        imid = st.selectbox("Choose import id for deleting",retrieve_import())       
        if st.button("Delete entry"):
            cur.execute("DELETE from import where import_id = %s;",[imid])
            st.write('Record deleted')

    #VIEW
    if st.button("View"):
        cur.execute("select * from import;")
        rows = cur.fetchall()
        df = pd.DataFrame(rows,columns = ('import_id', 'import_prod', 'quantity', 'tariff', 'inv_no'))
        st.write(df)

elif page_choice == pages_menu[6]:
    st.subheader('Shipping')
    st.markdown("***")

     
    id = st.text_input(label='Enter shipping ID')
    mode = st.text_input(label='Enter shipping mode')
    status = st.radio("Choose status", ('Ordered', 'Dispatched', 'Delivered'))
    location = st.text_input(label='Enter Location')
    date = st.date_input(label='Enter date')
    prod_id = st.text_input(label='Enter prod id')

    #INSERT OPERATION
    if st.button("Add Details"):
        cur.execute("Insert into shipping values(%s,%s,%s,%s,%s,%s);", (id, mode, status, location, date, prod_id))
        st.text("Data added!")

    #DELETE OPERATION
    with st.expander("Delete Shipping details"):
        sid = st.selectbox("Choose shipping id for deleting",retrieve_shipping())       
        if st.button("Delete entry"):
            cur.execute("DELETE from shipping where shipping_id = %s;",[sid])
            st.write('Record deleted')

     #VIEW
    if st.button("View"):
        cur.execute("select * from shipping")
        rows = cur.fetchall()
        df = pd.DataFrame(rows,columns = ('shipping_id',  'mode', 'shipment_status', 'location', 'shipping date','prod_ids'))
        st.write(df)
    
elif page_choice == pages_menu[7]:
    st.markdown(":)")
