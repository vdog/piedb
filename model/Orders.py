import datetime
import model
from .Customer import Customer
from .OrderDetails import OrderDetails
from .OrderDetails import Product
from .OrderDetails import Employee
from .Shippers import Shippers
from sqlalchemy import (Column, Integer, String, DateTime, Float, ForeignKey, Boolean)
from sqlalchemy.orm import relationship

class Orders(model.Base):
  __tablename__ = 'Orders'
  OrderID = Column(Integer, primary_key=True)
  CustomerID = Column(String (28), ForeignKey('Customers.CustomerID'))
  customer = relationship("Customer")
  EmployeeID = Column(Integer, ForeignKey('Employees.EmployeeID'))
  employee = relationship("Employee")
  OrderDate = Column(DateTime, default=datetime.datetime.utcnow)
  RequiredDate = model.Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
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
    ret = model.serialize(self)
    print(self.employee.__class__)
    if isinstance(self.employee, Employee):
        ret['employee'] = model.serialize(self.employee)
    if isinstance(self.shipper, Shippers):
        ret['shipper'] = model.serialize(self.shipper)
    if isinstance(self.customer, Customer):
        ret['customer'] = model.serialize(self.customer)
    else:
         ret['customer'] = model.serialize(Customer())
    ret['details'] = []
    for d in self.details:
      ret['details'].append(d.serialize())
    return ret

