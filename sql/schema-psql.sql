
CREATE TABLE "Customers"
 (
   "CustomerID"         varchar(28) NOT NULL, 
   "CompanyName"         varchar(80) NOT NULL, 
   "CustomerFirstName"         varchar(100), 
   "ContactName"         varchar(60), 
   "ContactTitle"         varchar(60), 
   "Address"         varchar(120), 
   "City"         varchar(30), 
   "Region"         varchar(4), 
   "PostalCode"         varchar(20), 
   "Country"         varchar(30), 
   "Fax"         varchar(48), 
   "CusBDay"         timestamp
);

CREATE TABLE "Employees"
 (
   "EmployeeID"         bigint, 
   "EmpLastName"         varchar(40) NOT NULL, 
   "EmpFirstName"         varchar(20) NOT NULL
);

CREATE TABLE "Order Details"
 (
   "OrderID"         bigint NOT NULL, 
   "OrdDetProductID"         bigint, 
   "OrdDetSubProductID"         bigint, 
   "OrdDetCategoryID"         bigint, 
   "UnitPrice"         money NOT NULL, 
   "OrdDetSalesTaxRate"         boolean NOT NULL, 
   "Quantity"         Integer NOT NULL, 
   "Discount"         boolean NOT NULL, 
   "MemoOrderDetails"         varchar(255)
);

CREATE TABLE "Orders"
 (
   "OrderID"         Integer Primary Key Autoincrement, 
   "CustomerID"         varchar(28), 
   "EmployeeID"         bigint, 
   "OrderDate"         timestamp, 
   "RequiredDate"         timestamp NOT NULL, 
   "PickUpTime"         timestamp NOT NULL, 
   "ShipVia"         bigint, 
   "Freight"         money, 
   "ShipName"         varchar(80), 
   "ShipAddress"         varchar(120), 
   "ShipCity"         varchar(30), 
   "ShipRegion"         varchar(4), 
   "ShipPostalCode"         varchar(10), 
   "ShipCountry"         varchar(30), 
   "OrdPaid"         Boolean NOT NULL, 
   "chris test"         varchar(510)
);

CREATE TABLE "Prod_SubProd"
 (
   "SubProductID"         bigint, 
   "ProductID"         bigint, 
   "Flavor"         varchar(100), 
   "Size"         varchar(20), 
   "Type"         varchar(50), 
   "SubProductMemo"         varchar(255)
);

CREATE TABLE "Shippers"
 (
   "ShipperID"         bigint, 
   "CompanyName"         varchar(80) NOT NULL, 
   "Phone"         varchar(48)
);

CREATE TABLE "Products"
 (
   "ProductID"         bigint, 
   "ProductName"         varchar(80) NOT NULL, 
   "CategoryID"         bigint NOT NULL, 
   "QuantityPerUnit"         varchar(40), 
   "UnitPrice"         money, 
   "ProductSalesTaxRate"         boolean, 
   "Discontinued"         Boolean NOT NULL, 
   "LeadTime"         boolean, 
   "ProdDescription"         varchar(255)
);



