import json
import model
from sqlalchemy import (Column, Integer, String, DateTime, Float, ForeignKey, Boolean)
from sqlalchemy.orm import relationship

class OrderDetails(model.Base):
  __tablename__ = 'Order Details'
  DetailID = Column(Integer, primary_key = True)
  OrderID = Column(Integer, ForeignKey('Orders.OrderID'))
  OrdDetProductID = Column(Integer, ForeignKey('Products.ProductID'))
  product = relationship('Product')
  OrdDetSubProductID = Column(Integer, ForeignKey('Prod_SubProd.SubProductID'))
  subproduct = relationship('Prod_SubProd')
  OrdDetCategoryID = Column(Integer)
  UnitPrice = Column(Float )
  OrdDetSalesTaxRate = Column(Integer, nullable = False, default=0)
  Discount = Column(Integer, nullable = False, default=0)
  Quantity = Column(Integer, nullable = False, default=1)
  MemoOrderDetails = Column(String(255))

  def serialize(self):
    ret = model.serialize(self)
    ret['product'] = model.serialize(self.product)
    return ret

  def serialize_in(self, tail):
    if tail['OrderID'] is not None:
      self.OrderID = tail['OrderID']
      self.OrdDetProductID = tail['product']['ProductID']
      product = model.db.query(Product).get(self.OrdDetProductID)
      self.Quantity = tail['Quantity']
      self.UnitPrice = product.UnitPrice
      self.MemoOrderDetails = tail['MemoOrderDetails']


class Product(model.Base):
  __tablename__ = 'Products'
  ProductID = Column(Integer, nullable = False, primary_key = True)
  ProductName = Column(String(80), nullable = False)
  QuantityPerUnit = Column(String(40))
  ProdDescription = Column(String(255))
  UnitPrice = Column(Float, default= 0.0)
  Discontinued = Column(Boolean, default = False)
  #ProductSalesTaxRate = Column(Float)
  subproducts = relationship('Prod_SubProd')

  def serialize(self):
    ret = model.serialize(self)
    ret['subproducts'] = []
    for s in self.subproducts:
      ret['subproducts'].append(model.serialize(s))
    return ret

class Prod_SubProd(model.Base):
  __tablename__ = 'Prod_SubProd'
  SubProductID = Column(Integer, nullable = False, primary_key = True)
  ProductID = Column(Integer, ForeignKey('Products.ProductID'))
  Flavor = Column(String(100))
  Size = Column(String(20))
  Type = Column(String(50))
  SubProductMemo = Column(String(255))


class Employee(model.Base):
  __tablename__ = 'Employees'
  EmployeeID = Column(Integer, primary_key=True)
  EmpLastName = Column(String (40))
  EmpFirstName = Column(String (20))


