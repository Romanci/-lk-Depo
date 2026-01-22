from sqlalchemy.orm import Session
from app.models.erp_models import Product, BOM, SalesOrder, Routing
from typing import List, Dict

class MRPService:
    @staticmethod
    def calculate_full_requirements(db: Session, product_id: int, quantity: float) -> List[Dict]:
        """
        Hiyerarşik BOM yapısını kullanarak tüm alt bileşen ihtiyaçlarını hesaplar.
        """
        requirements = []

        def explode_bom(pid: int, qty: float):
            bom_items = db.query(BOM).filter(BOM.product_id == pid).all()
            for item in bom_items:
                total_needed = item.quantity_required * qty
                child_product = db.query(Product).filter(Product.id == item.material_id).first()

                # Mevcut stok kontrolü
                shortage = max(0, total_needed - child_product.stock_quantity)

                requirements.append({
                    "product_id": child_product.id,
                    "name": child_product.name,
                    "sku": child_product.sku,
                    "needed": total_needed,
                    "in_stock": child_product.stock_quantity,
                    "shortage": shortage,
                    "category": child_product.category,
                    "production_type": child_product.production_type
                })

                # Eğer alt bileşen de üretilen bir şeyse (sub_assembly, module vb.), onu da patlat
                if child_product.production_type == "in_house":
                    explode_bom(child_product.id, total_needed)

        explode_bom(product_id, quantity)
        return requirements

    @staticmethod
    def get_production_plan(db: Session, product_id: int):
        """
        Ürün rotasına (Routing) göre üretim adımlarını getirir.
        """
        routings = db.query(Routing).filter(Routing.product_id == product_id).order_by(Routing.sequence).all()
        plan = []
        for r in routings:
            plan.append({
                "sequence": r.sequence,
                "operation": r.operation_name,
                "work_center": r.work_center.name,
                "duration_mins": r.estimated_duration_minutes
            })
        return plan
