from sqlalchemy.orm import Session
from app.models.erp_models import Employee, Supplier, Product, Routing, WorkOrder
import numpy as np

def recommend_employee_for_task(db: Session, routing_id: int):
    """
    Belirli bir operasyon için en uygun personeli önerir.
    Kriterler: Beceri eşleşmesi, performans skoru ve iş yükü (basitleştirilmiş).
    """
    routing = db.query(Routing).filter(Routing.id == routing_id).first()
    if not routing:
        return None

    required_skill = routing.operation_name.lower()
    employees = db.query(Employee).all()

    scored_employees = []
    for emp in employees:
        score = emp.performance_score
        # Beceri eşleşmesi kontrolü (basit string arama)
        skill_match = 0
        emp_skills = emp.skills.lower().split(',')
        for s in emp_skills:
            if s in required_skill or required_skill in s:
                skill_match = 50 # Bonus puan
                break

        total_score = score + skill_match
        scored_employees.append({
            "employee_id": emp.id,
            "full_name": emp.full_name,
            "score": total_score,
            "skills": emp.skills
        })

    # Skora göre sırala
    scored_employees.sort(key=lambda x: x['score'], reverse=True)
    return scored_employees[0] if scored_employees else None

def recommend_supplier_for_product(db: Session, product_id: int):
    """
    Satın alınacak bir ürün için en iyi tedarikçiyi önerir.
    Kriterler: Tedarikçi kategorisi ve güvenilirlik puanı.
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product or product.production_type != "purchased":
        return None

    suppliers = db.query(Supplier).filter(Supplier.category == product.category).all()
    if not suppliers:
        # Kategori bazlı bulamazsa tümünü getir (basitleştirme)
        suppliers = db.query(Supplier).all()

    scored_suppliers = sorted(suppliers, key=lambda x: x.reliability_score, reverse=True)

    if scored_suppliers:
        best = scored_suppliers[0]
        return {
            "supplier_id": best.id,
            "name": best.name,
            "reliability_score": best.reliability_score
        }
    return None

def predict_production_delay(db: Session, work_order_id: int):
    """
    AI tabanlı gecikme tahmini (Mock - Gelecekte gerçek verilerle eğitilecek).
    """
    return {
        "work_order_id": work_order_id,
        "estimated_delay_days": np.random.choice([0, 1, 2, 3], p=[0.7, 0.15, 0.1, 0.05]),
        "reason": "Hammadde tedarik gecikmesi ihtimali"
    }
