import datetime
import re
from bson import ObjectId

def identify_string(input_string):
    """
    Определяет, является ли входная строка электронной почтой или номером телефона.
    Аргументы:
        input_string (str): Строка для анализа.
    Возвращает:
        str: 'email', 'phone', или 'unknown' в зависимости от содержания строки.
    """
    email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    phone_pattern = r"^\+?[\d\s]{10,15}$"

    if re.match(email_pattern, input_string):
        return 'email'
    elif re.match(phone_pattern, input_string):
        return 'phone'
    else:
        return 'unknown'
    

def serialize_document(document):
    """
    Преобразует поля ObjectId в строки в словаре, предназначенном для сериализации.
    Аргументы:
        document (dict): Словарь, содержащий данные документа MongoDB.
    Возвращает:
        dict: Словарь с сериализованными полями ObjectId.
    """
    if document is None:
        return None
    serialized = {}
    for key, value in document.items():
        if isinstance(value, ObjectId):
            serialized[key] = str(value)  # Преобразование ObjectId в строку
        elif isinstance(value, datetime.datetime):
            serialized[key] = value.isoformat()  # Преобразование datetime в ISO формат
        else:
            serialized[key] = value
    return serialized

