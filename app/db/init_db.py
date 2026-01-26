from app.db.session import engine, Base
from app.models.erp_models import (
    User, Product, BOM, WorkCenter, Routing,
    WorkOrder, Employee, Supplier, Customer, SalesOrder, Invoice
)

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    print("Endüstriyel Veritabanı tabloları oluşturuluyor...")
    init_db()
    print("Tüm tablolar başarıyla oluşturuldu.")
