from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
jwt=JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    app.url_map.strict_slashes = False

    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # Import blueprints
    from app.main_routes import main        # renamed from routes.py
    from app.routes.auth_routes import auth_bp
    from app.routes.product_routes import product_bp

    # Register blueprints
    app.register_blueprint(main)
    app.register_blueprint(auth_bp)
    app.register_blueprint(product_bp)

    return app
