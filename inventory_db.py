from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, Date
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy_utils import database_exists, create_database

# Using the declarative_base from sqlalchemy.orm
Base = declarative_base()

# Define the database URL
DATABASE_URL = "postgresql://postgres:Hoppers3195@assignment3.c54y666q6ct9.ap-southeast-2.rds.amazonaws.com:5432/postgres?sslmode=require"

print("Connecting to the database...")
try:
    engine = create_engine(DATABASE_URL)
    print("Database connected successfully!")
except SQLAlchemyError as e:
    print("Failed to connect to the database:", e)

# Check if the database exists, if not, create it
if not database_exists(engine.url):
    print("Database does not exist. Attempting to create...")
    try:
        create_database(engine.url)
        print("Database created successfully!")
    except SQLAlchemyError as e:
        print("Failed to create the database:", e)
else:
    print("Database already exists.")

# Bind the engine to the sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

# Your table definitions and other code here...
class Product(Base):
    __tablename__ = 'products'
    ProductID = Column(Integer, primary_key=True)
    ProductName = Column(String(100), nullable=False)
    Description = Column(String(250))
    Price = Column(Float)
    Category = Column(String(50))
    ImageURL = Column(String(200))

class Inventory(Base):
    __tablename__ = 'inventory'
    InventoryID = Column(Integer, primary_key=True)
    ProductID = Column(Integer, ForeignKey('products.ProductID'), nullable=False)
    QuantityAvailable = Column(Integer)
    SupplierID = Column(Integer)
    WarehouseLocation = Column(String(100))

class Order(Base):
    __tablename__ = 'orders'
    OrderID = Column(Integer, primary_key=True)
    CustomerID = Column(Integer)
    OrderDate = Column(Date)
    TotalAmount = Column(Float)

class OrderDetail(Base):
    __tablename__ = 'order_details'
    OrderDetailID = Column(Integer, primary_key=True)
    OrderID = Column(Integer, ForeignKey('orders.OrderID'), nullable=False)
    ProductID = Column(Integer, ForeignKey('products.ProductID'), nullable=False)
    Quantity = Column(Integer)
    Price = Column(Float)

# Create tables in the database
print("Creating tables...")
Base.metadata.create_all(engine)
print("Tables created successfully!")
