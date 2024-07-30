import random
from faker import Faker
from app import app, db, Müşteri, Ürün, Satış, Fırsat, Aktivite

fake = Faker('tr_TR')

# Daha fazla ürün ve kategori
product_names = [
    "iPhone 14 Pro Max", "Samsung Galaxy S23 Ultra", "MacBook Air M2", "Dell XPS 13", 
    "iPad Air 5", "Sony WH-1000XM5", "Canon EOS R6", "LG OLED65CX", 
    "Asus ROG Flow Z13", "Bose QuietComfort Earbuds", "GoPro HERO10", "Microsoft Surface Pro 8",
    "Samsung QLED 4K TV", "Apple Watch Series 8", "Fitbit Charge 5", "Sony PlayStation 5",
    "Xbox Series X", "Nintendo Switch OLED", "Jabra Elite 85t", "HP Spectre x360"
]

categories = [
    "Akıllı Telefon", "Bilgisayar", "Tablet", "Kulaklık", 
    "Kamera", "Televizyon", "Bilgisayar Ekipmanları", "Ses Sistemleri",
    "Oyun Konsolu", "Akıllı Saat", "Fitness Tracker", "Aksesuar"
]

def generate_simple_id(existing_ids):
    new_id = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=8))
    while new_id in existing_ids:
        new_id = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=8))
    existing_ids.add(new_id)
    return new_id

def generate_customers(n):
    with app.app_context():
        existing_ids = set()
        existing_emails = set()
        for _ in range(n):
            while True:
                email = fake.email()
                if email not in existing_emails:
                    existing_emails.add(email)
                    break

            customer_id = generate_simple_id(existing_ids)
            customer = Müşteri(
                id=customer_id,
                isim=fake.name(),
                email=email,
                telefon=fake.phone_number(),
                adres=fake.address(),
                alışveriş_sıklığı=round(random.uniform(1, 10), 2),
                sadakat_puanı=round(random.uniform(0, 100), 2)
            )
            db.session.add(customer)
        db.session.commit()

def generate_products(n):
    with app.app_context():
        existing_ids = set()
        for _ in range(n):
            product_id = generate_simple_id(existing_ids)
            product = Ürün(
                id=product_id,
                ad=random.choice(product_names),
                kategori=random.choice(categories),
                fiyat=round(random.uniform(100, 3000), 2),
                stok_miktarı=random.randint(1, 100)
            )
            db.session.add(product)
        db.session.commit()

def generate_sales(n):
    with app.app_context():
        existing_ids = set()
        customers = Müşteri.query.all()
        for _ in range(n):
            customer = random.choice(customers)
            sale_id = generate_simple_id(existing_ids)
            sale = Satış(
                id=sale_id,
                müşteri_id=customer.id,
                tarih=fake.date_time_this_year(),
                toplam_tutar=round(random.uniform(100, 5000), 2)
            )
            db.session.add(sale)
        db.session.commit()

def generate_opportunities(n):
    with app.app_context():
        existing_ids = set()
        products = Ürün.query.all()
        used_product_ids = set()
        discounts = [25, 50, 70]  # İndirim oranları

        for _ in range(n):
            if len(products) == len(used_product_ids):
                break

            product = random.choice([p for p in products if p.id not in used_product_ids])
            start_date = fake.date_time_this_year()
            end_date = fake.date_time_between(start_date=start_date)
            discount = random.choice(discounts)
            opportunity_id = generate_simple_id(existing_ids)
            opportunity = Fırsat(
                id=opportunity_id,
                ürün_id=product.id,
                indirim=discount,
                başlangıç_tarihi=start_date,
                bitiş_tarihi=end_date
            )
            used_product_ids.add(product.id)
            db.session.add(opportunity)
        db.session.commit()

def generate_activities(n):
    with app.app_context():
        existing_ids = set()
        customers = Müşteri.query.all()
        opportunities = Fırsat.query.all()  # Fırsatları almak için query
        for _ in range(n):
            customer = random.choice(customers)
            activity_id = generate_simple_id(existing_ids)
            opportunity = random.choice(opportunities)
            activity = Aktivite(
                id=activity_id,
                müşteri_id=customer.id,
                tarih=fake.date_time_this_year(),
                tür=random.choice(['Telefon Görüşmesi', 'E-posta']),
                not_=f"{opportunity.ürün.ad} ürünü şu an %{opportunity.indirim} indirimde! Fırsatı kaçırmayın."  # Güncellenmiş not
            )
            db.session.add(activity)
        db.session.commit()

def main():
    with app.app_context():
        db.create_all()
        generate_customers(100)
        generate_products(50)
        generate_sales(200)
        generate_opportunities(50)
        generate_activities(100)

if __name__ == "__main__":
    main()
