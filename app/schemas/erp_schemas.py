from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# --- AUTH & USER ---
class UserCreate(BaseModel):
    username: str
    password: str
    full_name: str
    role: Optional[str] = "operator"

class UserOut(BaseModel):
    id: int
    username: str
    full_name: str
    role: str
    class Config:
        from_attributes = True

# --- PRODUCT & BOM ---
class BOMBase(BaseModel):
    child_id: int
    quantity_required: float

class ProductCreate(BaseModel):
    name: str
    sku: str
    description: Optional[str] = None
    unit_price: float
    currency: Optional[str] = "TRY"
    category: str # raw_material, sub_assembly, final_product, unit, module
    production_type: str # in_house, purchased, outsourced
    reorder_level: Optional[float] = 10.0

class ProductOut(BaseModel):
    id: int
    name: str
    sku: str
    stock_quantity: float
    unit_price: float
    currency: str
    category: str
    class Config:
        from_attributes = True

# --- PRODUCTION ---
class WorkCenterCreate(BaseModel):
    name: str
    description: str
    hourly_cost: float

class RoutingCreate(BaseModel):
    sequence: int
    work_center_id: int
    operation_name: str
    estimated_duration_minutes: float

class WorkOrderCreate(BaseModel):
    product_id: int
    quantity: float
    start_date: datetime

# --- HR ---
class EmployeeCreate(BaseModel):
    full_name: str
    department: str
    skills: str
    hourly_rate: float

# --- SUPPLY CHAIN ---
class SupplierCreate(BaseModel):
    name: str
    contact_info: str
    category: str

class CustomerCreate(BaseModel):
    company_name: str
    contact_person: str
    email: str
    phone: str
