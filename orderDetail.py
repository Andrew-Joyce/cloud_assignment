from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'
    CustomerID = Column(Integer, primary_key=True)
    Name = Column(String(100), nullable=False)
    Email = Column(String(100), unique=True, nullable=False)
    Address = Column(String(255))
    City = Column(String(100))
    State = Column(String(100))
    PostalCode = Column(String(20))
    Phone = Column(String(20))

class Product(Base):
    __tablename__ = 'products'
    ProductID = Column(Integer, primary_key=True)
    ProductName = Column(String(100), nullable=False)
    Description = Column(String(250))
    Price = Column(Float)
    Category = Column(String(50))
    ImageURL = Column(String(200))

class Order(Base):
    __tablename__ = 'orders'
    OrderID = Column(Integer, primary_key=True)
    CustomerID = Column(Integer, ForeignKey('customers.CustomerID'), nullable=False)
    OrderDate = Column(Date, default=datetime.datetime.utcnow)
    TotalAmount = Column(Float)
    ShippingAddress = Column(String(255), nullable=True)
    items = relationship('OrderDetail', back_populates='order')

class OrderDetail(Base):
    __tablename__ = 'order_details'
    OrderDetailID = Column(Integer, primary_key=True)
    OrderID = Column(Integer, ForeignKey('orders.OrderID'), nullable=False)
    ProductID = Column(Integer, ForeignKey('products.ProductID'), nullable=False)
    Quantity = Column(Integer)
    Price = Column(Float)
    order = relationship('Order', back_populates='items')
    product = relationship('Product')

DATABASE_URL = "postgresql://postgres:Hoppers3195@assignment3.c54y666q6ct9.ap-southeast-2.rds.amazonaws.com:5432/postgres?sslmode=require"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)