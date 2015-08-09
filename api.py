from flask import Flask, request, session
from sqlalchemy import (and_, or_, desc, inspect)
import dateutil.parser

import json

import model
from model.Orders import Orders
from model.Customer import Customer
from model.OrderDetails import OrderDetails
from model.OrderDetails import Product
from model.OrderDetails import Employee
from model.Shippers import Shippers

app = Flask(__name__)

@app.route("/7dayoutlook")
def get_orders_7day():
    startDate = datetime.now
    endDate = startDate + timedelta(days=7)
    orders = model.db.query(Orders).filter(and_(Orders.RequiredDate > startDate, Orders.RequiredDate < endDate))
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
    #orders = model.db.query(Orders).filter(Orders.RequiredDate > orderDate)
    orders = model.db.query(Orders).from_statement('select * from Orders where Datetime(RequiredDate) > Datetime(\'' + orderDate + '\')')
  elif startDate != '' and endDate != '':
    orders = model.db.query(Orders).filter(and_(Orders.RequiredDate > startDate, Orders.RequiredDate < endDate)).order_by(desc(Orders.RequiredDate)).limit(200)
    #orders = model.db.query(Orders).from_statement('select * from Orders where Datetime(\'' + startDate + '\') < Datetime(RequiredDate) and Datetime(\'' + endDate + '\') > Datetime(RequiredDate) order by Datetime(RequiredDate) desc')
  elif lastDate != '':
    orders = model.db.query(Orders).from_statement('select *, Datetime(RequiredDate) as othercol from Orders where othercol < Datetime(\'' + lastDate + '\') order by othercol desc limit 10')
  elif orderBy == 'OrderDate':
    orders = model.db.query(Orders).order_by(desc(Orders.OrderDate)).offset(offset).limit(10)
  else:
    orders = model.db.query(Orders).order_by(desc(model.Orders.RequiredDate)).offset(offset).limit(10)
  return json.dumps([order.serialize() for order in orders.all()])

@app.route("/customers")
def get_customers():
    searchTerm = request.args.get('search','')
    offset = request.args.get('offset',0)
    limit = request.args.get('limit',0)
    customers = model.db.query(Customer).filter(or_(Customer.CustomerID.like('%' + searchTerm + '%'), or_(Customer.CustomerFirstname.like('%' + searchTerm + '%'), Customer.CompanyName.like('%' + searchTerm + '%')))).offset(offset).limit(10)
    if limit == 1:
            return json.dumps(serialize(customers[0]))
    return json.dumps([model.serialize(customer) for customer in customers])

@app.route("/customers/<customerID>")
def get_customer_orders(customerID):
  orders = model.db.query(Orders).filter(Orders.CustomerID == customerID).order_by(desc(Orders.OrderDate))
  return json.dumps([order.serialize() for order in orders.all()])

@app.route("/orders/<int:orderID>")
def get_order(orderID):
    order = model.db.query(Orders).filter(Orders.OrderID == orderID)
    return json.dumps(order.all()[0].serialize())

@app.route("/orders/-1")
def get_new_order():
    order = Orders();
    order.OrderID = -1
    return json.dumps(order.serialize())

@app.route("/employees")
def get_employees():
  employees = model.db.query(Employee)
  return json.dumps([model.serialize(employee) for employee in employees])

@app.route("/subproducts")
def get_subproducts():
  productID = request.args.get('productID','NONE')
  if productID != 'NONE':
    subproducts = model.db.query(Prod_SubProd).filter(Prod_SubProd.ProductID == productID)
  else:
    subproducts = model.db.query(Prod_SubProd)
  return json.dumps([model.serialize(sub) for sub in subproducts])

@app.route("/products")
def get_products():
  products = model.db.query(Product)
  return json.dumps([model.serialize(product) for product in products])

@app.route("/orderdetail")
def new_detail():
   detail = OrderDetails()
   return json.dumps(model.serialize(detail))

@app.route("/orders", methods=['POST','PUT'])
def upsert_order():
    incoming = request.get_json()
    print(incoming)
    order = Orders();
    orderid = incoming.get('OrderID', -1)
    if orderid != -1:
        order = model.db.query(Orders).get(incoming['OrderID'])
        model.db.query(OrderDetails).filter(OrderDetails.OrderID == incoming['OrderID']).delete()
    order.ShipAddress = incoming['ShipAddress']
    order.ShipName = incoming['ShipName']
    order.RequiredDate = dateutil.parser.parse(incoming['RequiredDate'])
    order.CustomerID = incoming['CustomerID']
    order.ShipCity = incoming['ShipCity']
    order.ShipRegion = incoming['ShipRegion']
    order.ShipPostalCode = incoming['ShipPostalCode']
    order.OrdPaid = incoming['OrdPaid']
    model.db.add(order)
    model.db.commit()
    for tail in incoming['details']:
        print(tail['OrderID'])
        if tail['OrderID'] is None:
            tail['OrderID'] = order.OrderID
        detail = OrderDetails()
        detail.serialize_in(tail)
        model.db.add(detail)

    model.db.commit()
    return json.dumps(incoming)

@app.before_request
def before_request():
  #print("before_request handler")
  pass


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
