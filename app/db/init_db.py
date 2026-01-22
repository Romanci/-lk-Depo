from app.db.session import engine, Base
from app.models.erp_models import Product, BOM, Order

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    print("Veritabanı tabloları oluşturuluyor...")
    init_db()
    print("Tablolar başarıyla oluşturuldu.")
