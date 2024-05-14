# /app/services/database.py
from flask_pymongo import PyMongo

mongo = PyMongo()

def init_db(app):
    """
    Инициализирует подключение к MongoDB.
    Аргументы:
        app: экземпляр Flask приложения.
    """
    mongo.init_app(app)

