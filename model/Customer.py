import model
from sqlalchemy import (Column, Integer, String, DateTime, Float, ForeignKey, Boolean)
from sqlalchemy.orm import relationship

class Customer(model.Base):
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

