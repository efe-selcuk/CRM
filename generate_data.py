import random
from faker import Faker
from uuid import uuid4
from werkzeug.security import generate_password_hash
from app import app, db, Müşteri, Fırsat, Aktivite, Kullanıcı

fake = Faker('tr_TR')

def generate_customers(n):
    with app.app_context():
        for _ in range(n):
            customer = Müşteri(
                id=str(uuid4()),  # UUID ile benzersiz ID'ler oluşturuyoruz
                isim=fake.name(),
                email=fake.email(),
                telefon=fake.phone_number(),
                adres=fake.address(),
                şirket=fake.company()
            )
            db.session.add(customer)
        db.session.commit()

def generate_opportunities(n):
    with app.app_context():
        customers = Müşteri.query.all()
        for _ in range(n):
            customer = random.choice(customers)
            opportunity = Fırsat(
                id=str(uuid4()),  # UUID ile benzersiz ID'ler oluşturuyoruz
                müşteri_id=customer.id,
                başlangıç_tarihi=fake.date_time_this_year(),
                bitiş_tarihi=fake.date_time_this_year(),
                aşama=random.choice(['Teklif', 'Kapanış', 'Geri Çekilme']),
                toplam_tutar=round(random.uniform(1000, 10000), 2),  # Daha basit tutar aralığı
                açıklama=fake.sentence()  # Kısa açıklama
            )
            db.session.add(opportunity)
        db.session.commit()

def generate_activities(n):
    with app.app_context():
        customers = Müşteri.query.all()
        for _ in range(n):
            customer = random.choice(customers)
            activity = Aktivite(
                id=str(uuid4()),  # UUID ile benzersiz ID'ler oluşturuyoruz
                müşteri_id=customer.id,
                tarih=fake.date_time_this_year(),
                tür=random.choice(['Toplantı', 'Telefon Görüşmesi', 'E-posta']),
                not_=fake.sentence(),  # Kısa not
                sonuç=random.choice(['Başarılı', 'Başarısız'])
            )
            db.session.add(activity)
        db.session.commit()

def generate_users(n):
    with app.app_context():
        for _ in range(n):
            password = fake.password()  # Faker ile basit bir şifre üretiyoruz
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')  # Geçerli bir hashleme yöntemi kullanıyoruz
            user = Kullanıcı(
                id=str(uuid4()),  # UUID ile benzersiz ID'ler oluşturuyoruz
                isim=fake.name(),
                email=fake.email(),
                şifre=hashed_password,  # Hash'lenmiş şifreyi kaydediyoruz
                rol=random.choice(['Admin', 'Satış Temsilcisi', 'Müşteri Hizmetleri'])
            )
            db.session.add(user)
        db.session.commit()

def main():
    with app.app_context():
        db.create_all()  # Veritabanı tablolarını oluşturur
        generate_customers(10)
        generate_opportunities(10)
        generate_activities(10)
        generate_users(5)

if __name__ == "__main__":
    main()
