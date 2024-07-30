import random
from faker import Faker
from app import create_app, db
from app.models import Musteri, Urun, Satis, Firsat, Aktivite, Personel

fake = Faker('tr_TR')

product_names = [
    "iPhone 14 Pro Max", "Samsung Galaxy S23 Ultra", "MacBook Air M2", "Dell XPS 13", 
    "iPad Air 5", "Sony WH-1000XM5", "Canon EOS R6", "LG OLED65CX", 
    "Asus ROG Flow Z13", "Bose QuietComfort Earbuds", "GoPro HERO10", "Microsoft Surface Pro 8",
    "Samsung QLED 4K TV", "Apple Watch Series 8", "Fitbit Charge 5", "Sony PlayStation 5",
    "Xbox Series X", "Nintendo Switch OLED", "Jabra Elite 85t", "HP Spectre x360"
]

categories = [
    "Akilli Telefon", "Bilgisayar", "Tablet", "Kulaklik", 
    "Kamera", "Televizyon", "Bilgisayar Ekipmanlari", "Ses Sistemleri",
    "Oyun Konsolu", "Akilli Saat", "Fitness Tracker", "Aksesuar"
]

roles = ["admin", "satis temsilcisi", "musteri hizmetleri"]

def generate_simple_id(existing_ids):
    new_id = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=8))
    while new_id in existing_ids:
        new_id = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=8))
    existing_ids.add(new_id)
    return new_id

def generate_customers(n):
    existing_ids = set()
    existing_emails = set()
    for _ in range(n):
        while True:
            email = fake.email()
            if email not in existing_emails:
                existing_emails.add(email)
                break

        customer_id = generate_simple_id(existing_ids)
        customer = Musteri(
            id=customer_id,
            isim=fake.name(),
            email=email,
            telefon=fake.phone_number(),
            adres=fake.address(),
            alisveris_sikligi=round(random.uniform(1, 10), 2),
            sadakat_puani=round(random.uniform(0, 100), 2)
        )
        db.session.add(customer)
    db.session.commit()

def generate_products(n):
    existing_ids = set()
    for _ in range(n):
        product_id = generate_simple_id(existing_ids)
        product = Urun(
            id=product_id,
            ad=random.choice(product_names),
            kategori=random.choice(categories),
            fiyat=round(random.uniform(100, 3000), 2),
            stok_miktari=random.randint(1, 100)
        )
        db.session.add(product)
    db.session.commit()

def generate_sales(n):
    existing_ids = set()
    customers = Musteri.query.all()
    for _ in range(n):
        customer = random.choice(customers)
        sale_id = generate_simple_id(existing_ids)
        sale = Satis(
            id=sale_id,
            musteri_id=customer.id,
            tarih=fake.date_time_this_year(),
            toplam_tutar=round(random.uniform(100, 5000), 2)
        )
        db.session.add(sale)
    db.session.commit()

def generate_opportunities(n):
    existing_ids = set()
    products = Urun.query.all()
    used_product_ids = set()
    discounts = [25, 50, 70]

    for _ in range(n):
        if len(products) == len(used_product_ids):
            break

        product = random.choice([p for p in products if p.id not in used_product_ids])
        start_date = fake.date_time_this_year()
        end_date = fake.date_time_between(start_date=start_date)
        discount = random.choice(discounts)
        opportunity_id = generate_simple_id(existing_ids)
        opportunity = Firsat(
            id=opportunity_id,
            urun_id=product.id,
            indirim=discount,
            baslangic_tarihi=start_date,
            bitis_tarihi=end_date
        )
        used_product_ids.add(product.id)
        db.session.add(opportunity)
    db.session.commit()

def generate_activities(n):
    existing_ids = set()
    customers = Musteri.query.all()
    opportunities = Firsat.query.all()
    for _ in range(n):
        customer = random.choice(customers)
        activity_id = generate_simple_id(existing_ids)
        opportunity = random.choice(opportunities)
        activity = Aktivite(
            id=activity_id,
            musteri_id=customer.id,
            tarih=fake.date_time_this_year(),
            tur=random.choice(['Telefon Gorusemesi', 'E-posta']),
            not_=f"{opportunity.urun.ad} urunu su an %{opportunity.indirim} indirimde! Firsati kacirmayin."
        )
        db.session.add(activity)
    db.session.commit()

def generate_personnel(n):
    existing_emails = set()
    for _ in range(n):
        while True:
            email = fake.email()
            if email not in existing_emails:
                existing_emails.add(email)
                break

        personel = Personel(
            isim=fake.name(),
            email=email,
            rol=random.choice(roles)
        )
        personel.set_password('password')  # Şifreyi hashleyerek kaydediyoruz
        db.session.add(personel)
    db.session.commit()

def main():
    app = create_app()
    with app.app_context():
        db.create_all()
        generate_customers(100)
        generate_products(50)
        generate_sales(200)
        generate_opportunities(50)
        generate_activities(100)
        generate_personnel(10)  # 10 personel ekliyoruz

if __name__ == "__main__":
    main()
