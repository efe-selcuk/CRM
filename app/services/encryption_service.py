from cryptography.fernet import Fernet

# Anahtar oluştur (bunu güvenli bir yerde saklayın ve geri yükleme için kullanın)
def generate_key():
    return Fernet.generate_key()

# Anahtarı yükle
def load_key(key: bytes):
    return Fernet(key)

# Veriyi şifreleme
def encrypt_data(key: bytes, data: bytes) -> bytes:
    cipher_suite = load_key(key)
    return cipher_suite.encrypt(data)

# Veriyi çözme
def decrypt_data(key: bytes, encrypted_data: bytes) -> bytes:
    cipher_suite = load_key(key)
    return cipher_suite.decrypt(encrypted_data)
