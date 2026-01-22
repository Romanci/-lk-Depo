from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base

# --- CORE ---

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    role = Column(String, default="operator") # admin, manager, operator, etc.
    is_active = Column(Boolean, default=True)

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    sku = Column(String, unique=True, index=True)
    description = Column(Text)
    unit_price = Column(Float)
    currency = Column(String, default="TRY")
    stock_quantity = Column(Float, default=0.0)
    reorder_level = Column(Float, default=10.0)

    # Types: raw_material, sub_assembly, final_product, unit, module
    category = Column(String, index=True)
    production_type = Column(String) # in_house, purchased, outsourced

    # Relationships
    materials_needed = relationship("BOM", foreign_keys="BOM.product_id", back_populates="parent")
    routings = relationship("Routing", back_populates="product")

class BOM(Base):
    """ Bill of Materials (Hiyerarşik Ürün Ağacı) """
    __tablename__ = "bom"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id")) # Parent (e.g., Oven)
    material_id = Column(Integer, ForeignKey("products.id")) # Child (e.g., Motor)
    quantity_required = Column(Float)

    parent = relationship("Product", foreign_keys=[product_id], back_populates="materials_needed")
    child = relationship("Product", foreign_keys=[material_id])

# --- PRODUCTION & ROUTING ---

class WorkCenter(Base):
    """ İş İstasyonları (Kaynak, Montaj, Torna vb.) """
    __tablename__ = "work_centers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    hourly_cost = Column(Float)

class Routing(Base):
    """ Üretim Rotası """
    __tablename__ = "routings"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    sequence = Column(Integer) # Operasyon sırası
    work_center_id = Column(Integer, ForeignKey("work_centers.id"))
    operation_name = Column(String)
    estimated_duration_minutes = Column(Float)

    product = relationship("Product", back_populates="routings")
    work_center = relationship("WorkCenter")

class WorkOrder(Base):
    """ Üretim Emri """
    __tablename__ = "work_orders"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Float)
    status = Column(String, default="planned") # planned, in_progress, completed, cancelled
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    assigned_employee_id = Column(Integer, ForeignKey("employees.id"), nullable=True)

    product = relationship("Product")
    assigned_employee = relationship("Employee")

# --- HUMAN RESOURCES ---

class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    department = Column(String)
    skills = Column(String) # Comma separated skills: "welding,assembly,cnc"
    hourly_rate = Column(Float)
    performance_score = Column(Float, default=100.0) # AI usage

# --- CRM & SUPPLY CHAIN ---

class Supplier(Base):
    __tablename__ = "suppliers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    contact_info = Column(String)
    category = Column(String) # electrical, pneumatic, steel, etc.
    reliability_score = Column(Float, default=100.0) # AI usage

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String)
    contact_person = Column(String)
    email = Column(String)
    phone = Column(String)

class SalesOrder(Base):
    __tablename__ = "sales_orders"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Float)
    order_date = Column(DateTime, server_default=func.now())
    total_amount = Column(Float)
    status = Column(String, default="completed") # draft, confirmed, producing, shipped, invoiced, completed

    customer = relationship("Customer")
    product = relationship("Product")

# Alias for backward compatibility if needed
Order = SalesOrder

# --- FINANCE ---

class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True, index=True)
    order_type = Column(String) # sales, purchase
    related_order_id = Column(Integer)
    invoice_number = Column(String, unique=True)
    issue_date = Column(DateTime, server_default=func.now())
    total_amount = Column(Float)
    currency = Column(String)
    is_paid = Column(Boolean, default=False)
