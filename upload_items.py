from sqlalchemy.exc import SQLAlchemyError

from inventory_db import Inventory, Session

updated_inventory_items = [
    Inventory(ProductID=1, QuantityAvailable=200, SupplierID=101, WarehouseLocation="Warehouse A"),
    Inventory(ProductID=2, QuantityAvailable=180, SupplierID=102, WarehouseLocation="Warehouse B"),
    Inventory(ProductID=3, QuantityAvailable=320, SupplierID=103, WarehouseLocation="Warehouse C"),
    Inventory(ProductID=4, QuantityAvailable=150, SupplierID=104, WarehouseLocation="Warehouse D"),
    Inventory(ProductID=5, QuantityAvailable=100, SupplierID=105, WarehouseLocation="Warehouse E"),
    Inventory(ProductID=6, QuantityAvailable=280, SupplierID=106, WarehouseLocation="Warehouse F"),
    Inventory(ProductID=7, QuantityAvailable=200, SupplierID=107, WarehouseLocation="Warehouse G"),
    Inventory(ProductID=8, QuantityAvailable=170, SupplierID=108, WarehouseLocation="Warehouse H"),
    Inventory(ProductID=9, QuantityAvailable=210, SupplierID=109, WarehouseLocation="Warehouse I"),
    Inventory(ProductID=10, QuantityAvailable=320, SupplierID=110, WarehouseLocation="Warehouse J"),
    Inventory(ProductID=11, QuantityAvailable=240, SupplierID=111, WarehouseLocation="Warehouse K"),
    Inventory(ProductID=12, QuantityAvailable=220, SupplierID=112, WarehouseLocation="Warehouse L"),
    Inventory(ProductID=13, QuantityAvailable=150, SupplierID=113, WarehouseLocation="Warehouse M"),
    Inventory(ProductID=14, QuantityAvailable=160, SupplierID=114, WarehouseLocation="Warehouse N"),
    Inventory(ProductID=15, QuantityAvailable=250, SupplierID=115, WarehouseLocation="Warehouse O")
]

session = Session()
try:
    for item in updated_inventory_items:
        session.merge(item) 
    session.commit()
    print("Inventory updated successfully!")
except SQLAlchemyError as e:
    session.rollback()
    print("Failed to update inventory:", e)
finally:
    session.close()

print("Session closed.")
