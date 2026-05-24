from sqlalchemy import Column, Integer, String
from app.database import Base

class InventoryItem(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    category = Column(String)
    quantity = Column(Integer)
    minimum_stock = Column(Integer)
    supplier = Column(String)