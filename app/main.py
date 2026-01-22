from datetime import timedelta
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db.session import get_db
from app.services.inventory_service import InventoryService
from app.services.mrp_service import MRPService
from app.services.finance_service import FinanceService
from app.ai.forecaster import get_ai_insight
from app.ai.decision_support import recommend_employee_for_task, recommend_supplier_for_product
from app.services.auth_service import (
    authenticate_user, create_access_token, get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES, get_password_hash
)
from app.models.erp_models import User, Employee, Supplier, Product
from app.schemas.erp_schemas import UserCreate, ProductCreate

app = FastAPI(title="Industrial ERP/MRP AI - v02")

# CORS middleware for Frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "role": user.role, "full_name": user.full_name}

@app.post("/register")
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        username=user_data.username,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
        role=user_data.role
    )
    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    return {"message": "User created successfully"}

@app.get("/")
def read_root():
    return {"message": "Welcome to AI-Powered Factory ERP/MRP System"}

@app.get("/inventory")
def get_inventory(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return InventoryService.get_stock_levels(db)

@app.post("/inventory/product")
def create_product(product: ProductCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    return InventoryService.create_product(
        db,
        product.name,
        product.sku,
        product.unit_price,
        product.reorder_level
    )

@app.get("/mrp/requirements/{product_id}")
def get_detailed_requirements(product_id: int, quantity: float = 1.0, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return MRPService.calculate_full_requirements(db, product_id, quantity)

@app.get("/mrp/routing/{product_id}")
def get_routing(product_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return MRPService.get_production_plan(db, product_id)

@app.get("/ai/forecast/{product_id}")
def get_forecast(product_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_ai_insight(db, product_id)

@app.get("/ai/recommend/employee/{routing_id}")
def get_employee_recommendation(routing_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can access AI recommendations")
    return recommend_employee_for_task(db, routing_id)

@app.get("/ai/recommend/supplier/{product_id}")
def get_supplier_recommendation(product_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return recommend_supplier_for_product(db, product_id)

@app.get("/employees")
def list_employees(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Employee).all()

@app.get("/suppliers")
def list_suppliers(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Supplier).all()

@app.get("/finance/rates")
def get_rates(current_user: User = Depends(get_current_user)):
    return FinanceService.get_exchange_rates()

@app.get("/analytics/efficiency")
def get_efficiency(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return FinanceService.get_company_efficiency(db)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
