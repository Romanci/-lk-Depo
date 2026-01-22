from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    sku = Column(String, unique=True, index=True)
    description = Column(String)
    unit_price = Column(Float)
    stock_quantity = Column(Float, default=0.0)
    reorder_level = Column(Float, default=10.0)

    # Relationship for BOM
    materials_needed = relationship("BOM", foreign_keys="BOM.product_id", back_populates="product")

class BOM(Base):
    """ Bill of Materials """
    __tablename__ = "bom"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    material_id = Column(Integer, ForeignKey("products.id"))
    quantity_required = Column(Float)

    product = relationship("Product", foreign_keys=[product_id], back_populates="materials_needed")
    material = relationship("Product", foreign_keys=[material_id])

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    status = Column(String, default="pending") # pending, producing, completed, shipped
    order_date = Column(DateTime(timezone=True), server_default=func.now())

    product = relationship("Product")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    role = Column(String, default="operator") # admin, manager, operator
    is_active = Column(Boolean, default=True)
