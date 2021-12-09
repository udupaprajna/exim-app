drop database exim;
create database exim;

\c exim

CREATE TABLE  CUSTOMER
(	Customer_ID int NOT NULL,
	Phone  text,
	Cust_Company varchar(50),
	PRIMARY KEY (Customer_ID)
);

CREATE TABLE  CUST_ADDRESS
(	Cust_Address text,	
	Cust_ID int,
	FOREIGN KEY (Cust_ID) REFERENCES CUSTOMER (Customer_ID) ON DELETE CASCADE 
	
);

CREATE TABLE  PRODUCT
(	Prod_ID int,
	Unit_price float NOT NULL,
	Quantity int default 50000,
	Prod_name varchar(25),
	Cust_ID int,
	PRIMARY KEY (Prod_ID),
	FOREIGN KEY (Cust_ID) references CUSTOMER (Customer_ID) ON DELETE CASCADE
);
CREATE TABLE  INVOICE
(	Invoice_NO text NOT NULL,
	Product varchar(15),
	Statement float,
	Date_of_purchase date,
	Cust_ID int,
	PRIMARY KEY (Invoice_NO),
	FOREIGN KEY (Cust_ID) REFERENCES CUSTOMER (Customer_ID) ON DELETE CASCADE
);

CREATE TABLE  IMPORT
(	Import_ID int NOT NULL,
	Import_prod varchar(30),
	Quantity int check (Quantity > 4500),
	Tariff float NOT NULL,
	Inv_NO text,
	PRIMARY KEY (Import_ID),
	FOREIGN KEY (Inv_NO) REFERENCES INVOICE (Invoice_NO) ON DELETE CASCADE
);

CREATE TABLE  IMPORT_MANAGER
(	Manager_ID int NOT NULL,
	Import_ID int,
	PRIMARY KEY (Manager_ID),
	FOREIGN KEY (Import_ID) references IMPORT (Import_ID) ON DELETE CASCADE
);

CREATE TABLE  EXPORT
(	Export_ID int NOT NULL,
	Date_of_export date,
	Export_dest varchar(15),  
	Export_prod varchar(25),
	Invo_NO text,
	PRIMARY KEY (Export_ID),
	FOREIGN KEY (Invo_NO) references INVOICE (Invoice_NO) ON DELETE CASCADE
);


CREATE TABLE  INVENTORY
(	Inv_ID int,
	Inv_No int,
	Inv_Items varchar(25),
	Inventory_desc text,
	Prod_ID int,
	PRIMARY KEY (Inv_ID),
	FOREIGN KEY (Prod_ID) references PRODUCT (Prod_ID) ON DELETE CASCADE
);


CREATE TABLE  PAYMENTS
(	Payment_ID int NOT NULL,
	Amount float,
	Payment_desc text,
	Cust_ID int,
	PRIMARY KEY (Payment_ID),
	FOREIGN KEY (Cust_ID) REFERENCES CUSTOMER (Customer_ID)ON DELETE CASCADE
);


CREATE TABLE  SUPPLIER
(	Supplier_ID int,
	Supplier_type varchar(25),
	Cust_ID int,
	PRIMARY KEY (Supplier_ID),
	FOREIGN KEY (Cust_ID) references CUSTOMER(Customer_ID) ON DELETE CASCADE
	
);

CREATE TABLE  PROVIDES
(		
	Suppl_ID int,
	Prod_ID int,
	FOREIGN KEY (Suppl_ID) references SUPPLIER (Supplier_ID) ON DELETE CASCADE,
	FOREIGN KEY (Prod_ID) references PRODUCT (Prod_ID) ON DELETE CASCADE
);

CREATE TABLE  SHIPPING
(	Shipping_ID int NOT NULL,
	Mode varchar(15), 
	Shipment_status varchar(15), 
	Location varchar(30),
	Shipping_date date,
	Prod_ID int,
	PRIMARY KEY (Shipping_ID),
	FOREIGN KEY (Prod_ID) references PRODUCT (Prod_ID) ON DELETE CASCADE
);

