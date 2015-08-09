import model
from sqlalchemy import (Column, Integer, String, DateTime, Float, ForeignKey, Boolean)
from sqlalchemy.orm import relationship

class OrderDetails(model.Base):
  __tablename__ = 'Order Details'
  OrderID = Column(Integer, ForeignKey('Orders.OrderID'), primary_key=True)
  OrdDetProductID = Column(Integer, ForeignKey('Products.ProductID'), primary_key=True)
  product = relationship('Product')
  OrdDetSubProductID = Column(Integer, ForeignKey('Prod_SubProd.SubProductID'), primary_key=True)
  subproduct = relationship('Prod_SubProd')
  OrdDetCategoryID = Column(Integer, primary_key=True)
  UnitPrice = Column(Float, nullable = False, primary_key=True)
  OrdDetSalesTaxRate = Column(Integer, nullable = False, default=0)
  Discount = Column(Integer, nullable = False, default=0)
  Quantity = Column(Integer, nullable = False, primary_key=True)
  MemoOrderDetails = Column(String(255), primary_key=True)

  def serialize(self):
    ret = model.serialize(self)
    ret['product'] = model.serialize(self.product)
    ret['sub_product'] = model.serialize(self.subproduct)
    return ret

  def serialize_in(self, tail):
    print(json.dumps(tail))
    if tail['OrderID'] is not None:
      self.OrderID = tail['OrderID']
      self.OrdDetProductID = tail['OrdDetProductID']
      self.OrdDetSubProductID = tail['OrdDetSubProductID']
      self.Quantity = tail['Quantity']
      self.UnitPrice = tail['UnitPrice']
      self.MemoOrderDetails = tail['MemoOrderDetails']


class Product(model.Base):
  __tablename__ = 'Products'
  ProductID = Column(Integer, nullable = False, primary_key = True)
  ProductName = Column(String(80), nullable = False)
  QuantityPerUnit = Column(String(40))
  ProdDescription = Column(String(255))

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

