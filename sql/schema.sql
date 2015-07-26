-- ----------------------------------------------------------
-- MDB Tools - A library for reading MS Access database files
-- Copyright (C) 2000-2011 Brian Bruns and others.
-- Files in libmdb are licensed under LGPL and the utilities under
-- the GPL, see COPYING.LIB and COPYING files respectively.
-- Check out http://mdbtools.sourceforge.net
-- ----------------------------------------------------------

-- That file uses encoding UTF-8

CREATE TABLE [Customers]
 (
	[CustomerID]			Text (28) NOT NULL, 
	[CompanyName]			Text (80) NOT NULL, 
	[CustomerFirstName]			Text (100), 
	[ContactName]			Text (60), 
	[ContactTitle]			Text (60), 
	[Address]			Text (120), 
	[City]			Text (30), 
	[Region]			Text (4), 
	[PostalCode]			Text (20), 
	[Country]			Text (30), 
	[Fax]			Text (48), 
	[CusBDay]			DateTime
);

CREATE TABLE [Employees]
 (
	[EmployeeID]			Long Integer, 
	[EmpLastName]			Text (40) NOT NULL, 
	[EmpFirstName]			Text (20) NOT NULL
);

CREATE TABLE [Order Details]
 (
	[OrderID]			Long Integer NOT NULL, 
	[OrdDetProductID]			Long Integer, 
	[OrdDetSubProductID]			Long Integer, 
	[OrdDetCategoryID]			Long Integer, 
	[UnitPrice]			Currency NOT NULL, 
	[OrdDetSalesTaxRate]			Single NOT NULL, 
	[Quantity]			Integer NOT NULL, 
	[Discount]			Single NOT NULL, 
	[MemoOrderDetails]			Text (255)
);

CREATE TABLE [Orders]
 (
	[OrderID]			Integer Primary Key Autoincrement, 
	[CustomerID]			Text (28), 
	[EmployeeID]			Long Integer, 
	[OrderDate]			DateTime, 
	[RequiredDate]			DateTime NOT NULL, 
	[PickUpTime]			DateTime NOT NULL, 
	[ShipVia]			Long Integer, 
	[Freight]			Currency, 
	[ShipName]			Text (80), 
	[ShipAddress]			Text (120), 
	[ShipCity]			Text (30), 
	[ShipRegion]			Text (4), 
	[ShipPostalCode]			Text (10), 
	[ShipCountry]			Text (30), 
	[OrdPaid]			Boolean NOT NULL, 
	[chris test]			Text (510)
);

CREATE TABLE [Paste Errors]
 (
	[Field0]			Text (255)
);

CREATE TABLE [Prod_SubProd]
 (
	[SubProductID]			Long Integer, 
	[ProductID]			Long Integer, 
	[Flavor]			Text (100), 
	[Size]			Text (20), 
	[Type]			Text (50), 
	[SubProductMemo]			Text (255)
);

CREATE TABLE [Shippers]
 (
	[ShipperID]			Long Integer, 
	[CompanyName]			Text (80) NOT NULL, 
	[Phone]			Text (48)
);

CREATE TABLE [Products]
 (
	[ProductID]			Long Integer, 
	[ProductName]			Text (80) NOT NULL, 
	[CategoryID]			Long Integer NOT NULL, 
	[QuantityPerUnit]			Text (40), 
	[UnitPrice]			Currency, 
	[ProductSalesTaxRate]			Single, 
	[Discontinued]			Boolean NOT NULL, 
	[LeadTime]			Single, 
	[ProdDescription]			Text (255)
);


