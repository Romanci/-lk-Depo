from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services.auth_service import get_password_hash
from app.models.erp_models import User, Product, BOM, WorkCenter, Routing, Employee, Supplier

def seed():
    db = SessionLocal()

    # 1. Admin User
    if not db.query(User).filter(User.username == "admin").first():
        admin = User(
            username="admin",
            hashed_password=get_password_hash("admin123"),
            full_name="İrfan Çelik",
            role="admin"
        )
        db.add(admin)

    # 2. Work Centers
    wc_assembly = WorkCenter(name="Montaj Hattı", description="Ünitelerin birleştirildiği ana hat", hourly_cost=50.0)
    wc_welding = WorkCenter(name="Kaynak Atölyesi", description="Şase ve kasa kaynak işlemleri", hourly_cost=60.0)
    wc_electric = WorkCenter(name="Elektrik Panosu Montaj", description="Elektrik ve otomasyon grubu", hourly_cost=55.0)
    db.add_all([wc_assembly, wc_welding, wc_electric])
    db.flush()

    # 3. Employees
    e1 = Employee(full_name="Ahmet Usta", department="Üretim", skills="welding,assembly", hourly_rate=25.0, performance_score=95.0)
    e2 = Employee(full_name="Mehmet Teknisyen", department="Elektrik", skills="electric,automation", hourly_rate=28.0, performance_score=88.0)
    db.add_all([e1, e2])

    # 4. Suppliers
    s1 = Supplier(name="Global Motor A.Ş.", contact_info="info@globalmotor.com", category="motor", reliability_score=98.0)
    s2 = Supplier(name="Pnömatik Dünyası", contact_info="sales@pnomatik.com", category="pneumatic", reliability_score=85.0)
    db.add_all([s1, s2])

    # 5. Products
    p_line = Product(name="Bazlama Pişirme Hattı", sku="LINE-BAZ-01", category="final_product", production_type="in_house", unit_price=250000.0)
    p_oven = Product(name="Pişirme Fırını Ünitesi", sku="UNIT-OVN-01", category="unit", production_type="in_house", unit_price=80000.0)
    p_motor_group = Product(name="Tahrik Motor Grubu", sku="MOD-MTR-01", category="module", production_type="in_house", unit_price=15000.0)
    p_motor = Product(name="0.75kW AC Motor", sku="PART-MTR-75", category="raw_material", production_type="purchased", unit_price=2500.0, stock_quantity=10)
    p_stainless = Product(name="Paslanmaz Sac 2mm", sku="RAW-SS-02", category="raw_material", production_type="purchased", unit_price=450.0, stock_quantity=100)

    db.add_all([p_line, p_oven, p_motor_group, p_motor, p_stainless])
    db.flush()

    # 6. BOM (Hiyerarşi) - Corrected field names
    bom1 = BOM(product_id=p_line.id, material_id=p_oven.id, quantity_required=1.0)
    bom2 = BOM(product_id=p_oven.id, material_id=p_motor_group.id, quantity_required=2.0)
    bom3 = BOM(product_id=p_oven.id, material_id=p_stainless.id, quantity_required=20.0)
    bom4 = BOM(product_id=p_motor_group.id, material_id=p_motor.id, quantity_required=1.0)

    db.add_all([bom1, bom2, bom3, bom4])

    # 7. Routing
    r1 = Routing(product_id=p_oven.id, sequence=1, work_center_id=wc_welding.id, operation_name="Kasa Kaynak", estimated_duration_minutes=120)
    r2 = Routing(product_id=p_oven.id, sequence=2, work_center_id=wc_assembly.id, operation_name="Genel Montaj", estimated_duration_minutes=240)
    db.add_all([r1, r2])

    db.commit()
    db.close()
    print("Endüstriyel Seed verileri (v02-fixed) başarıyla eklendi.")

if __name__ == "__main__":
    seed()
