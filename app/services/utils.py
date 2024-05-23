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

    def serialize_value(value):
        if isinstance(value, ObjectId):
            return str(value)  # Преобразование ObjectId в строку
        elif isinstance(value, datetime.datetime):
            return value.isoformat()  # Преобразование datetime в ISO формат
        elif isinstance(value, list):
            return [serialize_value(item) for item in value]  # Рекурсивное преобразование элементов списка
        elif isinstance(value, dict):
            return serialize_document(value)  # Рекурсивное преобразование вложенных словарей
        else:
            return value

    serialized = {}
    for key, value in document.items():
        serialized[key] = serialize_value(value)

    return serialized

def serialize_cursor(cursor):
    """
    Преобразует документы в курсоре в сериализованный список.
    Аргументы:
        cursor (Cursor): Курсор MongoDB.
    Возвращает:
        list: Список сериализованных документов.
    """
    return [serialize_document(doc) for doc in cursor]

def remove_duplicates(service_list):
    seen = set()
    unique_services = []
    for service in service_list:
        if service[0] not in seen:
            unique_services.append(service)
            seen.add(service[0])
    return unique_services