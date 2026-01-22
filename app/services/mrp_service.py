from sqlalchemy.orm import Session
from app.models.erp_models import Product, BOM, Order

class MRPService:
    @staticmethod
    def calculate_requirements(db: Session, product_id: int, target_quantity: int):
        """
        Calculates how much raw material is needed for a specific production quantity.
        """
        bom_items = db.query(BOM).filter(BOM.product_id == product_id).all()
        requirements = []

        for item in bom_items:
            material = db.query(Product).filter(Product.id == item.material_id).first()
            needed_qty = item.quantity_required * target_quantity

            requirements.append({
                "material_id": item.material_id,
                "material_name": material.name,
                "needed_quantity": needed_qty,
                "current_stock": material.stock_quantity,
                "shortage": max(0, needed_qty - material.stock_quantity)
            })

        return requirements

    @staticmethod
    def create_production_order(db: Session, product_id: int, quantity: int):
        new_order = Order(product_id=product_id, quantity=quantity, status="pending")
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        return new_order
