from flask import Flask, request, session
from sqlalchemy import (create_engine, MetaData, Table, Column, Integer,
    String, DateTime, Float, ForeignKey, and_, or_, Boolean, desc, inspect)
from sqlalchemy.orm import mapper, relationship, Session, class_mapper
from sqlalchemy.ext.declarative import declarative_base
import dateutil.parser

import json
import datetime

app = Flask(__name__)
Base = declarative_base()

# engine, suppose it has two tables 'user' and 'address' set up
engine = create_engine("sqlite:///hubbard.sql3")
db = Session(engine)

def date_handler(obj):
    if hasattr(obj, 'isoformat'):
        print(obj.isoformat())
        return obj.isoformat()
    else:
        return obj

def serialize(model):
  """Transforms a model into a dictionary which can be dumped to JSON."""
  # first we get the names of all the columns on your model
  columns = [c.key for c in class_mapper(model.__class__).columns]
  # then we return their values in a dict
  return dict((c, date_handler(getattr(model, c))) for c in columns)

class Customer(Base):
  __tablename__ = 'Customers'
  CustomerID = Column(String(28), primary_key=True)
  CompanyName = Column(String(80))
  CustomerFirstname = Column(String(100))
  ContactName = Column(String(60))
  ContactTitle = Column(String(60))
  Address = Column(String(120))
  City = Column(String(30))
  Region = Column(String(4))
  PostalCode = Column(String(20))
  Country = Column(String(30))
  Fax = Column(String(48))
  CusBDay = Column(DateTime)

class Orders(Base):
  __tablename__ = 'Orders'
  OrderID = Column(Integer, primary_key=True)
  CustomerID = Column(String (28), ForeignKey('Customers.CustomerID'))
  customer = relationship("Customer")
  EmployeeID = Column(Integer, ForeignKey('Employees.EmployeeID'))
  employee = relationship("Employee")
  OrderDate = Column(DateTime, default=datetime.datetime.utcnow)
  RequiredDate = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
  PickUpTime = Column(DateTime, default=datetime.datetime.utcnow)
  ShipVia = Column(Integer, ForeignKey('Shippers.ShipperID'))
  shipper = relationship('Shippers')
  ShipName = Column(String(80))
  ShipAddress = Column(String(120))
  ShipCity = Column(String(30))
  ShipRegion = Column(String(4))
  ShipPostalCode = Column(String(10))
  ShipCountry = Column(String(30))
  OrdPaid = Column(Boolean, nullable=False, default=False)
  details = relationship("OrderDetails")

  def serialize(self):
    ret = serialize(self)
    print(self.employee.__class__)
    if isinstance(self.employee, Employee):
        ret['employee'] = serialize(self.employee)
    if isinstance(self.shipper, Shippers):
        ret['shipper'] = serialize(self.shipper)
    if isinstance(self.customer, Customer):
        ret['customer'] = serialize(self.customer)
    else:
         ret['customer'] = serialize(Customer())
    ret['details'] = []
    for d in self.details:
      ret['details'].append(d.serialize())
    return ret

class Shippers(Base):
  __tablename__ = 'Shippers'
  ShipperID = Column(Integer, primary_key = True)
  CompanyName = Column(String(80))
  Phone = Column(String(48))


class OrderDetails(Base):
  __tablename__ = 'Order Details'
  OrderID = Column(Integer, ForeignKey('Orders.OrderID'), primary_key=True)
  OrdDetProductID = Column(Integer, ForeignKey('Products.ProductID'), primary_key=True)
  product = relationship('Product')
  OrdDetSubProductID = Column(Integer, ForeignKey('Prod_SubProd.SubProductID'), primary_key=True)
  subproduct = relationship('Prod_SubProd')
  OrdDetCategoryID = Column(Integer, primary_key=True)
  UnitPrice = Column(Float, nullable = False, primary_key=True)
  Quantity = Column(Integer, nullable = False, primary_key=True)
  MemoOrderDetails = Column(String(255), primary_key=True)

  def serialize(self):
    ret = serialize(self)
    ret['product'] = serialize(self.product)
    ret['sub_product'] = serialize(self.subproduct)
    return ret

class Product(Base):
  __tablename__ = 'Products'
  ProductID = Column(Integer, nullable = False, primary_key = True)
  ProductName = Column(String(80), nullable = False)
  QuantityPerUnit = Column(String(40))
  ProdDescription = Column(String(255))

class Prod_SubProd(Base):
  __tablename__ = 'Prod_SubProd'
  SubProductID = Column(Integer, nullable = False, primary_key = True)
  ProductID = Column(Integer, ForeignKey('Products.ProductID'))
  Flavor = Column(String(100))
  Size = Column(String(20))
  Type = Column(String(50))
  SubProductMemo = Column(String(255))


class Employee(Base):
  __tablename__ = 'Employees'
  EmployeeID = Column(Integer, primary_key=True)
  EmpLastName = Column(String (40))
  EmpFirstName = Column(String (20))

@app.route("/7dayoutlook")
def get_orders_7day():
    startDate = datetime.now
    endDate = startDate + timedelta(days=7)
    orders = db.query(Orders).filter(and_(Orders.RequiredDate > startDate, Orders.RequiredDate < endDate))
    return json.dumps([order.serialize() for order in orders.all()])

@app.route("/orders")
def get_orders():
  orderDate = request.args.get('orderDate','')
  startDate = request.args.get('startDate','')
  endDate = request.args.get('endDate','')
  lastDate = request.args.get('lastDate','')
  orderBy = request.args.get('orderBy','')
  offset = request.args.get('offset',0)

  if orderDate != '':
    # http://127.0.0.1:5000/orders?orderDate=2014-08-14%2000:00:00
    #orders = db.query(Orders).filter(Orders.RequiredDate > orderDate)
    orders = db.query(Orders).from_statement('select * from Orders where Datetime(RequiredDate) > Datetime(\'' + orderDate + '\')')
  elif startDate != '' and endDate != '':
    orders = db.query(Orders).filter(and_(Orders.RequiredDate > startDate, Orders.RequiredDate < endDate)).order_by(desc(Orders.RequiredDate)).limit(200)
    #orders = db.query(Orders).from_statement('select * from Orders where Datetime(\'' + startDate + '\') < Datetime(RequiredDate) and Datetime(\'' + endDate + '\') > Datetime(RequiredDate) order by Datetime(RequiredDate) desc')
  elif lastDate != '':
    orders = db.query(Orders).from_statement('select *, Datetime(RequiredDate) as othercol from Orders where othercol < Datetime(\'' + lastDate + '\') order by othercol desc limit 10')
  elif orderBy == 'OrderDate':
    orders = db.query(Orders).order_by(desc(Orders.OrderDate)).offset(offset).limit(10)
  else:
    orders = db.query(Orders).order_by(desc(Orders.RequiredDate)).offset(offset).limit(10)
  return json.dumps([order.serialize() for order in orders.all()])

@app.route("/customers")
def get_customers():
    searchTerm = request.args.get('search','')
    offset = request.args.get('offset',0)
    limit = request.args.get('limit',0)
    customers = db.query(Customer).filter(or_(Customer.CustomerID.like('%' + searchTerm + '%'), or_(Customer.CustomerFirstname.like('%' + searchTerm + '%'), Customer.CompanyName.like('%' + searchTerm + '%')))).offset(offset).limit(10)
    if limit == 1:
            return json.dumps(serialize(customers[0]))
    return json.dumps([serialize(customer) for customer in customers])

@app.route("/customers/<customerID>")
def get_customer_orders(customerID):
  orders = db.query(Orders).filter(Orders.CustomerID == customerID).order_by(desc(Orders.OrderDate))
  return json.dumps([order.serialize() for order in orders.all()])

@app.route("/orders/<int:orderID>")
def get_order(orderID):
    order = db.query(Orders).filter(Orders.OrderID == orderID)
    return json.dumps(order.all()[0].serialize())

@app.route("/orders/-1")
def get_new_order():
    order = Orders();
    order.OrderID = -1
    return json.dumps(order.serialize())

@app.route("/employees")
def get_employees():
  employees = db.query(Employee)
  return json.dumps([serialize(employee) for employee in employees])

@app.route("/subproducts")
def get_subproducts():
  productID = request.args.get('productID','NONE')
  if productID != 'NONE':
    subproducts = db.query(Prod_SubProd).filter(Prod_SubProd.ProductID == productID)
  else:
    subproducts = db.query(Prod_SubProd)
  return json.dumps([serialize(sub) for sub in subproducts])

@app.route("/products")
def get_products():
  products = db.query(Product)
  return json.dumps([serialize(product) for product in products])

@app.route("/orderdetail")
def new_detail():
   detail = OrderDetails()
   return json.dumps(serialize(detail))

@app.route("/orders", methods=['POST','PUT'])
def upsert_order():
    incoming = request.get_json()
    print(incoming)
    if 'OrderID' not in incoming:
        order = Orders();
        #order.ShipAddress = incoming['ShipAddress']
        #order.ShipName = incoming['ShipName']
        order.RequiredDate = dateutil.parser.parse(incoming['RequiredDate'])
        order.CustomerID = incoming['CustomerID']
        #order.ShipCity = incoming['ShipCity']
        #order.ShipRegion = incoming['ShipRegion']
        #order.ShipPostalCode = incoming['ShipPostalCode']
        db.add(order)
        db.commit()
    else:
        order = db.query(Orders).get(incoming['OrderID'])
        print(json.dumps(order.serialize()))
        #order.ShipCountry = 'UAE'
        #db.commit()
        #for key in incoming:
        #    if key != 'details' and key != 'shipper' and key != 'employee':
        #        print key
        #        order.key = incoming[key]
        #        setattr(order, key, incoming[key])
        #        print getattr(order, key)
        order.ShipAddress = incoming['ShipAddress']
        order.ShipName = incoming['ShipName']
        order.RequiredDate = dateutil.parser.parse(incoming['RequiredDate'])
        order.ShipCity = incoming['ShipCity']
        order.ShipRegion = incoming['ShipRegion']
        order.ShipPostalCode = incoming['ShipPostalCode']
        order.OrdPaid = incoming['OrdPaid']
        order.CustomerID = incoming['CustomerID']
    db.commit()
    return json.dumps(incoming)

@app.before_request
def before_request():
  print("before_request handler")
  pass


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
