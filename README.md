# AI-Powered Factory ERP/MRP System (v01)

This project is a modular ERP (Enterprise Resource Planning) and MRP (Material Requirements Planning) system designed for factories. It features AI-powered demand forecasting to optimize inventory levels and production planning.

## Features
- **Auth System**: Secure login and registration with JWT tokens and role-based access control (Admin, Manager, Operator).
- **Inventory Management**: Track products, stock levels, and SKUs.
- **MRP (Material Requirements Planning)**: Automatically calculate material requirements based on Bill of Materials (BOM).
- **AI Forecasting**: Linear regression-based demand forecasting for smarter inventory planning.
- **Modern Frontend**: A simple and responsive dashboard built with Tailwind CSS.

## Technology Stack
- **Backend**: Python 3.12, FastAPI, SQLAlchemy (SQLite)
- **AI/ML**: Scikit-learn, Pandas
- **Frontend**: HTML5, JavaScript, Tailwind CSS
- **Testing**: Pytest, Playwright

---

# Yapay Zeka Destekli Fabrika ERP/MRP Sistemi (v01)

Bu proje, fabrikalar için tasarlanmış modüler bir ERP (Kurumsal Kaynak Planlaması) ve MRP (Malzeme İhtiyaç Planlaması) sistemidir. Stok seviyelerini ve üretim planlamasını optimize etmek için yapay zeka tabanlı talep tahmini içerir.

## Özellikler
- **Kimlik Doğrulama**: JWT token'ları ve rol tabanlı erişim kontrolü (Admin, Yönetici, Operatör) ile güvenli giriş ve kayıt.
- **Stok Yönetimi**: Ürünleri, stok seviyelerini ve SKU'ları takip edin.
- **MRP (Malzeme İhtiyaç Planlaması)**: Ürün Ağacı (BOM) bazlı otomatik malzeme gereksinimi hesaplama.
- **Yapay Zeka Tahmini**: Daha akıllı stok planlaması için doğrusal regresyon tabanlı talep tahmini.
- **Modern Arayüz**: Tailwind CSS ile oluşturulmuş basit ve duyarlı bir kontrol paneli.

## Teknoloji Yığını
- **Backend**: Python 3.12, FastAPI, SQLAlchemy (SQLite)
- **AI/ML**: Scikit-learn, Pandas
- **Frontend**: HTML5, JavaScript, Tailwind CSS
- **Test**: Pytest, Playwright

## Kurulum / Installation
1. Bağımlılıkları yükleyin / Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Veritabanını hazırlayın / Initialize database:
   ```bash
   python app/db/init_db.py
   python app/db/seed.py
   ```
3. Sunucuyu başlatın / Start server:
   ```bash
   python app/main.py
   ```
4. Tarayıcıda `frontend/index.html` dosyasını açın / Open `frontend/index.html` in your browser.
