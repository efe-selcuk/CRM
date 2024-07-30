import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

db = SQLAlchemy()
jwt = JWTManager()
limiter = Limiter(key_func=get_remote_address)

def create_app():
    app = Flask(__name__)
    
    # Load configuration from environment variables
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)

    # Register blueprints
    from app.routes.product_routes import product_bp
    from app.routes.customer_routes import customer_bp
    from app.routes.sales_routes import sales_bp
    from app.routes.opportunity_routes import opportunity_bp
    from app.routes.activity_routes import activity_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.admin_routes import admin_bp
    from app.routes.satis_tahmini_routes import satis_tahmini_bp
    from app.routes.email_routes import email_bp

    app.register_blueprint(product_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(sales_bp)
    app.register_blueprint(opportunity_bp)
    app.register_blueprint(activity_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(satis_tahmini_bp)
    app.register_blueprint(email_bp)

    return app
