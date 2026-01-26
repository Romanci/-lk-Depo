import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.session import Base
from app.services.inventory_service import InventoryService
from app.models.erp_models import Product

# Test veritabanı kurulumu
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_create_product(db):
    product = InventoryService.create_product(db, "Test Product", "SKU123", 100.0, "raw_material", "purchased")
    assert product.name == "Test Product"
    assert product.sku == "SKU123"
    assert product.stock_quantity == 0.0

def test_update_stock(db):
    product = InventoryService.create_product(db, "Stock Item", "SKU456", 50.0, "raw_material", "purchased")
    InventoryService.update_stock(db, product.id, 20)
    assert product.stock_quantity == 20.0
