from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError

# Define the database URL
DATABASE_URL = "postgresql://postgres:Hoppers3195@assignment3.c54y666q6ct9.ap-southeast-2.rds.amazonaws.com:5432/postgres?sslmode=require"

# Initialize SQLAlchemy Base
Base = declarative_base()

# Define the Product model
class Product(Base):
    __tablename__ = 'products'
    ProductID = Column(Integer, primary_key=True)
    ProductName = Column(String(100), nullable=False)
    Description = Column(String(250))
    Price = Column(Float)
    Category = Column(String(50))
    ImageURL = Column(String(200))

# Create the database engine
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)  # Creates all tables based on the Base metadata

# Bind the engine to the sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

# Define products to be added
products = [
    Product(ProductName="Apple", Description="Fresh apples.", Price=0.30, Category="Fruits", ImageURL="http://www.macdentalcare.com/pub/photo/2014-09-apple.jpg"),
    Product(ProductName="Chicken Breast", Description="High-quality skinless chicken breasts.", Price=5.50, Category="Meat", ImageURL="https://www.bowrivermeatmarket.ca/wp-content/uploads/2019/06/SKINLESS-BLESS-CHICKEN-BREASRS-scaled.jpeg"),
    Product(ProductName="Spinach", Description="Organic spinach leaves.", Price=2.00, Category="Vegetables", ImageURL="https://th.bing.com/th/id/OIP.040MMbJbiGxRxXlOLz8MHAHaHa"),
    Product(ProductName="Pasta", Description="High-quality spaghetti pasta.", Price=1.25, Category="Grains", ImageURL="http://img1.exportersindia.com/product_images/bc-full/dir_58/1739930/raw-spaghetti-554747.jpg"),
    Product(ProductName="Salmon Fillets", Description="Fresh salmon fillets.", Price=10.00, Category="Fish", ImageURL="https://2.bp.blogspot.com/-4O8qrQqV7OE/VtB99OHvtHI/AAAAAAAAAJ8/Yjw2xz3UFio/s1600/raw-salmon-fillet-salmon.jpg"),
    Product(ProductName="Eggs", Description="Organic free-range eggs.", Price=2.10, Category="Dairy", ImageURL="https://www.integrativenutrition.com/sites/default/files/eggs.jpg"),
    Product(ProductName="Tomatoes", Description="Freshly picked tomatoes.", Price=0.90, Category="Vegetables", ImageURL="https://th.bing.com/th/id/OIP.d7-YH4kCw4Ln6jlH25xuXwHaHZ"),
    Product(ProductName="Bread", Description="Whole grain bread.", Price=1.50, Category="Grains", ImageURL="https://th.bing.com/th/id/OIP.yBMc4wHrTFgie3S1V_mG8AHaFN"),
    Product(ProductName="Ground Beef", Description="Ground beef for versatile cooking.", Price=4.20, Category="Meat", ImageURL="https://th.bing.com/th/id/OIP.mkWdNhlzRNXLXz96lgDUNgHaHa"),
    Product(ProductName="Milk", Description="Fresh cow's milk.", Price=0.99, Category="Dairy", ImageURL="https://th.bing.com/th/id/OIP.KmP-yURoIMg9rTALD_t4VQAAAA"),
    Product(ProductName="Rice", Description="Long grain white rice.", Price=0.80, Category="Grains", ImageURL="https://www.parenthub.com.au/wp-content/uploads/136853131.jpg"),
    Product(ProductName="Bananas", Description="Organic bananas.", Price=0.30, Category="Fruits", ImageURL="https://images.heb.com/is/image/HEBGrocery/000377497"),
    Product(ProductName="Yogurt", Description="Plain yogurt.", Price=3.00, Category="Dairy", ImageURL="https://images.wisegeek.com/bowl-of-plain-yogurt.jpg"),
    Product(ProductName="Broccoli", Description="Fresh broccoli.", Price=1.90, Category="Vegetables", ImageURL="http://wallpapersdsc.net/wp-content/uploads/2016/09/Broccoli-Pictures.jpg"),
    Product(ProductName="Orange Juice", Description="Freshly squeezed orange juice.", Price=3.50, Category="Beverages", ImageURL="https://images.freeimages.com/images/large-previews/801/orange-juice-1321161.jpg")
]

# Add products to the session
session.add_all(products)

# Commit the session
try:
    session.commit()
    print("Products added successfully!")
except SQLAlchemyError as e:
    session.rollback()
    print("Failed to add products:", e)
finally:
    session.close()

print("Session closed.")
