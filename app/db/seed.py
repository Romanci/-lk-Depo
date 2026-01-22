import os
import sys
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services.auth_service import get_password_hash
from app.models.erp_models import User, Product, BOM

def seed():
    db = SessionLocal()
    # Create Admin User
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin:
        admin = User(
            username="admin",
            hashed_password=get_password_hash("admin123"),
            full_name="Admin User",
            role="admin"
        )
        db.add(admin)

    # Create Sample Products
    if not db.query(Product).first():
        p1 = Product(name="Elektrikli Motor (Bitmiş Ürün)", sku="MTR-FIN", unit_price=1500.0, stock_quantity=10.0)
        p2 = Product(name="Motor Gövdesi", sku="MTR-001", unit_price=500.0, stock_quantity=100.0)
        p3 = Product(name="Rulman", sku="RLM-002", unit_price=20.0, stock_quantity=500.0)
        db.add_all([p1, p2, p3])
        db.flush()

        # Create BOM (Bill of Materials)
        # 1 Elektrikli Motor = 1 Gövde + 2 Rulman
        bom1 = BOM(product_id=p1.id, material_id=p2.id, quantity_required=1.0)
        bom2 = BOM(product_id=p1.id, material_id=p3.id, quantity_required=2.0)
        db.add_all([bom1, bom2])

    db.commit()
    db.close()
    print("Seed verileri eklendi (Admin: admin / admin123)")

if __name__ == "__main__":
    seed()
