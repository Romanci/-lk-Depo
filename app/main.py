from datetime import timedelta
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.inventory_service import InventoryService
from app.services.mrp_service import MRPService
from app.ai.forecaster import get_ai_insight
from app.services.auth_service import (
    authenticate_user, create_access_token, get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES, get_password_hash
)
from app.models.erp_models import User
from app.schemas.erp_schemas import UserCreate

app = FastAPI(title="Factory ERP/MRP AI")

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
    return {"access_token": access_token, "token_type": "bearer", "role": user.role}

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
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully"}

@app.get("/")
def read_root():
    return {"message": "Welcome to AI-Powered Factory ERP/MRP System"}

@app.get("/inventory")
def get_inventory(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return InventoryService.get_stock_levels(db)

@app.post("/inventory/product")
def create_product(name: str, sku: str, unit_price: float, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role not in ["admin", "manager"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    return InventoryService.create_product(db, name, sku, unit_price)

@app.get("/mrp/requirements/{product_id}")
def get_mrp_requirements(product_id: int, quantity: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return MRPService.calculate_requirements(db, product_id, quantity)

@app.get("/ai/forecast/{product_id}")
def get_forecast(product_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_ai_insight(db, product_id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
