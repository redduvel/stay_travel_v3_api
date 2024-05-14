# /app/api/bookings/models.py
from bson import ObjectId
import datetime

class Booking:
    def __init__(self, user_id, hotel_id, start_date, end_date, description='', status='Ожидание', isDeleted=False):
        self.user_id = ObjectId(user_id)
        self.hotel_id = ObjectId(hotel_id)
        self.created_at = datetime.datetime.now()
        self.start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        self.end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        self.description = description
        self.status = status
        self.isDeleted = isDeleted

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'hotel_id': self.hotel_id,
            'created_at': self.created_at,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'description': self.description,
            'status': self.status,
            'isDeleted': self.isDeleted
        }
