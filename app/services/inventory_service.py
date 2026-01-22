from sqlalchemy.orm import Session
from app.models.erp_models import Product

class InventoryService:
    @staticmethod
    def get_stock_levels(db: Session):
        return db.query(Product).all()

    @staticmethod
    def update_stock(db: Session, product_id: int, quantity_change: float):
        product = db.query(Product).filter(Product.id == product_id).first()
        if product:
            product.stock_quantity += quantity_change
            db.commit()
            db.refresh(product)
        return product

    @staticmethod
    def create_product(db: Session, name: str, sku: str, unit_price: float, reorder_level: float = 10.0):
        new_product = Product(name=name, sku=sku, unit_price=unit_price, reorder_level=reorder_level)
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product
