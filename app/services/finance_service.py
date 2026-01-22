from sqlalchemy.orm import Session
from app.models.erp_models import Invoice, SalesOrder
from datetime import datetime

class FinanceService:
    @staticmethod
    def get_exchange_rates():
        """
        Döviz kurlarını getirir.
        Gerçek senaryoda bir API'den (TCMB, Fixer vb.) çekilir.
        """
        return {
            "USD": 34.25,
            "EUR": 37.10,
            "GBP": 44.15,
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    @staticmethod
    def create_invoice_from_order(db: Session, order_id: int, order_type: str = "sales"):
        """
        Siparişi faturaya dönüştürür.
        """
        # Basitleştirilmiş fatura oluşturma mantığı
        if order_type == "sales":
            order = db.query(SalesOrder).filter(SalesOrder.id == order_id).first()
            if not order:
                return None

            invoice = Invoice(
                order_type="sales",
                related_order_id=order.id,
                invoice_number=f"INV-SAL-{order.id}-{datetime.now().strftime('%y%m%d%H%M')}",
                total_amount=order.total_amount,
                currency="TRY",
                is_paid=False
            )
            db.add(invoice)
            db.commit()
            db.refresh(invoice)
            return invoice
        return None

    @staticmethod
    def get_company_efficiency(db: Session):
        """
        Verimlilik Yönetimi (Personel, Tezgah vb.)
        Şu an için mock veriler döndürür.
        """
        return {
            "overall_efficiency": 82.5,
            "personnel_efficiency": 88.0,
            "work_center_efficiency": 76.5,
            "customer_satisfaction": 92.0,
            "supplier_reliability": 85.5
        }
