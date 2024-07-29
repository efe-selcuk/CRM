from faker import Faker
from uuid import uuid4
import random
from app import app, db
from models import Müşteri, Ürün, Satış, Fırsat, Aktivite

fake = Faker('tr_TR')

def generate_customers(n):
    with app.app_context():
        for _ in range(n):
            customer = Müşteri(
                id=str(uuid4()),
                isim=fake.name(),
                email=fake.email(),
                telefon=fake.phone_number(),
                adres=fake.address(),
                alışveriş_sıklığı=random.randint(1, 12),  # Tam sayı
                sadakat_puanı=random.randint(0, 1000)    # Tam sayı
            )
            db.session.add(customer)
        db.session.commit()

def generate_products(n):
    with app.app_context():
        categories = ['Gıda', 'İçecek', 'Temizlik', 'Kişisel Bakım']
        for _ in range(n):
            product = Ürün(
                id=str(uuid4()),
                ad=fake.word(),
                kategori=random.choice(categories),
                fiyat=round(random.uniform(1.0, 100.0), 2),  # İki ondalıklı basamak
                stok_miktarı=random.randint(0, 100)  # Tam sayı
            )
            db.session.add(product)
        db.session.commit()

def generate_sales(n):
    with app.app_context():
        customers = Müşteri.query.all()
        for _ in range(n):
            customer = random.choice(customers)
            sale = Satış(
                id=str(uuid4()),
                müşteri_id=customer.id,
                tarih=fake.date_time_this_year(),
                toplam_tutar=round(random.uniform(10.0, 500.0), 2)  # İki ondalıklı basamak
            )
            db.session.add(sale)
        db.session.commit()

def generate_opportunities(n):
    with app.app_context():
        products = Ürün.query.all()
        for _ in range(n):
            product = random.choice(products)
            opportunity = Fırsat(
                id=str(uuid4()),
                ürün_id=product.id,
                indirim=round(random.uniform(5.0, 50.0), 2),  # İki ondalıklı basamak
                başlangıç_tarihi=fake.date_time_this_year(),
                bitiş_tarihi=fake.date_time_this_year()
            )
            db.session.add(opportunity)
        db.session.commit()

def generate_activities(n):
    with app.app_context():
        customers = Müşteri.query.all()
        for _ in range(n):
            customer = random.choice(customers)
            activity = Aktivite(
                id=str(uuid4()),
                müşteri_id=customer.id,
                tarih=fake.date_time_this_year(),
                tür=random.choice(['Toplantı', 'Telefon Görüşmesi', 'E-posta']),
                not_=fake.sentence(),
            )
            db.session.add(activity)
        db.session.commit()

def main():
    with app.app_context():
        db.create_all()
        generate_customers(10)
        generate_products(10)
        generate_sales(10)
        generate_opportunities(10)
        generate_activities(10)

if __name__ == "__main__":
    main()
