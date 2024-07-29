from flask import Flask
from flask_jwt_extended import JWTManager
from config import Config
from models import db, Kullanıcı
from auth import auth_bp, limiter

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
jwt = JWTManager(app)
limiter.init_app(app)

app.register_blueprint(auth_bp, url_prefix='/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
