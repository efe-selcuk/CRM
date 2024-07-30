from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)

    # Blueprint'leri ekle
    from app.routes.product_routes import product_bp
    from app.routes.customer_routes import customer_bp
    from app.routes.sales_routes import sales_bp
    from app.routes.opportunity_routes import opportunity_bp
    from app.routes.activity_routes import activity_bp

    app.register_blueprint(product_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(sales_bp)
    app.register_blueprint(opportunity_bp)
    app.register_blueprint(activity_bp)

    return app
