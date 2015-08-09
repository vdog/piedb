import model
from sqlalchemy import (Column, Integer, String, DateTime, Float, ForeignKey, Boolean)
from sqlalchemy.orm import relationship

class Shippers(model.Base):
  __tablename__ = 'Shippers'
  ShipperID = Column(Integer, primary_key = True)
  CompanyName = Column(String(80))
  Phone = Column(String(48))


