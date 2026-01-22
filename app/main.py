from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.inventory_service import InventoryService
from app.services.mrp_service import MRPService
from app.ai.forecaster import get_ai_insight

app = FastAPI(title="Factory ERP/MRP AI")

@app.get("/")
def read_root():
    return {"message": "Welcome to AI-Powered Factory ERP/MRP System"}

@app.get("/inventory")
def get_inventory(db: Session = Depends(get_db)):
    return InventoryService.get_stock_levels(db)

@app.post("/inventory/product")
def create_product(name: str, sku: str, unit_price: float, db: Session = Depends(get_db)):
    return InventoryService.create_product(db, name, sku, unit_price)

@app.get("/mrp/requirements/{product_id}")
def get_mrp_requirements(product_id: int, quantity: int, db: Session = Depends(get_db)):
    return MRPService.calculate_requirements(db, product_id, quantity)

@app.get("/ai/forecast/{product_id}")
def get_forecast(product_id: int, db: Session = Depends(get_db)):
    return get_ai_insight(db, product_id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
