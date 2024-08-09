import random
from faker import Faker
from app import create_app, db
from app.models import Musteri, Urun, Satis, Firsat, Aktivite, Personel, Kategori

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

def generate_simple_id(existing_ids):
    new_id = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=8))
    while new_id in existing_ids:
        new_id = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=8))
    existing_ids.add(new_id)
    return new_id

def generate_customers(n):
    app = create_app()
    with app.app_context():
        existing_emails = set()
        for _ in range(n):
            while True:
                email = fake.email()
                if email not in existing_emails:
                    existing_emails.add(email)
                    break

            customer_id = generate_simple_id(existing_emails)
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

def generate_categories():
    app = create_app()
    with app.app_context():
        existing_categories = {cat.ad for cat in Kategori.query.all()}
        for category_name in categories:
            if category_name not in existing_categories:
                category = Kategori(ad=category_name)
                db.session.add(category)
        db.session.commit()

def generate_products(n):
    app = create_app()
    with app.app_context():
        existing_product_names = set()
        existing_ids = set()
        category_ids = [cat.id for cat in Kategori.query.all()]  # Kategori ID'lerini al
        
        if not category_ids:
            raise ValueError("No categories available to assign to products. Please generate categories first.")

        for _ in range(n):
            name = random.choice(product_names)
            if name not in existing_product_names:
                existing_product_names.add(name)
                category_id = random.choice(category_ids)  # Kategori ID'lerini kullan
                product_id = generate_simple_id(existing_ids)
                product = Urun(
                    id=product_id,
                    ad=name,
                    fiyat=round(random.uniform(100, 3000), 2),
                    stok_miktari=random.randint(1, 100),
                    kategori_id=category_id
                )
                db.session.add(product)
        db.session.commit()

def generate_sales(n):
    app = create_app()
    with app.app_context():
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
    app = create_app()
    with app.app_context():
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
    app = create_app()
    with app.app_context():
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
                tur=random.choice(['Telefon Görüşmesi', 'E-posta']),
                not_=f"{opportunity.urun.ad} ürünü şu an %{opportunity.indirim} indirimde! Fırsatı kaçırmayın."
            )
            db.session.add(activity)
        db.session.commit()

def generate_personel(n):
    app = create_app()
    with app.app_context():
        existing_ids = set()
        for _ in range(n):
            personel_id = generate_simple_id(existing_ids)
            personel = Personel(
                id=personel_id,
                isim=fake.name(),
                email=fake.email(),
                rol=random.choice(['Admin', 'Satis Temsilcisi', 'Musteri Hizmetleri'])
            )
            personel.set_password('password')  # Varsayılan şifre
            db.session.add(personel)
        db.session.commit()

def main():
    app = create_app()
    with app.app_context():
        db.create_all()
        generate_categories()  # Kategorileri oluştur
        generate_customers(100)
        generate_products(50)
        generate_sales(200)
        generate_opportunities(50)
        generate_activities(100)
        generate_personel(10)  # Örnek olarak 10 personel ekliyoruz

if __name__ == "__main__":
    main()