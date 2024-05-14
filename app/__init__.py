# app/__init__.py

from flask import Flask
from app.config.config import Config
from app.services.database import init_db
from flask_jwt_extended import JWTManager

from app.api.settings.routes import settings_blueprint
from app.api.auth.routes import auth_blueprint
from app.api.hotels.routes import hotels_blueprint
from app.api.bookings.routes import bookings_blueprint
from app.api.health import health_blueprint
from app.api.reviews.routes import reviews_blueprint

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    jwt = JWTManager(app)
    init_db(app)

    # Регистрация blueprints
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(settings_blueprint, url_prefix='/settings')
    app.register_blueprint(hotels_blueprint, url_prefix='/hotels')
    app.register_blueprint(bookings_blueprint, url_prefix='/bookings')
    app.register_blueprint(reviews_blueprint, url_prefix='/reviews')
    app.register_blueprint(health_blueprint)


    return app
