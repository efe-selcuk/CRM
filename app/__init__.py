from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
jwt = JWTManager()
limiter = Limiter(key_func=get_remote_address)

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)

    # Blueprint'leri burada içe aktarın
    from app.routes.product_routes import product_bp
    from app.routes.customer_routes import customer_bp
    from app.routes.sales_routes import sales_bp
    from app.routes.opportunity_routes import opportunity_bp
    from app.routes.activity_routes import activity_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.admin_routes import admin_bp

    app.register_blueprint(product_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(sales_bp)
    app.register_blueprint(opportunity_bp)
    app.register_blueprint(activity_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    return app
