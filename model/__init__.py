from sqlalchemy import (create_engine, MetaData, Table, Column, Integer, String, DateTime, Float, ForeignKey, and_, or_, Boolean, desc, inspect)
from sqlalchemy.orm import mapper, relationship, Session, class_mapper
from sqlalchemy.ext.declarative import declarative_base
import datetime

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
    """
    Transforms a model into a dictionary which can be dumped to JSON.
    """
    # first we get the names of all the columns on your model
    columns = [c.key for c in class_mapper(model.__class__).columns]
    # then we return their values in a dict
    return dict((c, date_handler(getattr(model, c))) for c in columns)

from .Orders import Orders
from .Customer import Customer
from .OrderDetails import OrderDetails
from .OrderDetails import Product
from .OrderDetails import Employee
from .Shippers import Shippers

