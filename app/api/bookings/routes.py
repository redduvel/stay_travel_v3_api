# /app/api/bookings/routes.py
from flask import Blueprint, request, jsonify
from ...services.utils import serialize_document
from ...services.database import mongo
from bson.objectid import ObjectId
from flask_jwt_extended import jwt_required, get_jwt_identity
import datetime

bookings_blueprint = Blueprint('bookings', __name__)

@bookings_blueprint.route('/', methods=['POST'])
@jwt_required()
def create_booking():
    user_id = get_jwt_identity()
    data = request.json
    booking = {
        'user_id': ObjectId(user_id),
        'hotel_id': ObjectId(data['hotel_id']),
        'start_date': datetime.datetime.strptime(data['start_date'], '%Y-%m-%d'),
        'end_date': datetime.datetime.strptime(data['end_date'], '%Y-%m-%d'),
        'description': data.get('description', ''),
        'status': 'Ожидание',
        'isDeleted': False,
        'created_at': datetime.datetime.now()
    }
    result = mongo.db.bookings.insert_one(booking)
    return jsonify({'booking_id': str(result.inserted_id)}), 201


@bookings_blueprint.route('/<booking_id>', methods=['DELETE'])
@jwt_required()
def delete_booking(booking_id):
    result = mongo.db.bookings.update_one({'_id': ObjectId(booking_id)}, {'$set': {'isDeleted': True}})
    if result.modified_count:
        return jsonify({'message': 'Booking marked as deleted'}), 200
    else:
        return jsonify({'error': 'Booking not found'}), 404


@bookings_blueprint.route('/<booking_id>/status', methods=['PUT'])
@jwt_required()
def update_booking_status(booking_id):
    status = request.json.get('status')
    result = mongo.db.bookings.update_one({'_id': ObjectId(booking_id)}, {'$set': {'status': status}})
    if result.modified_count:
        return jsonify({'message': 'Booking status updated'}), 200
    else:
        return jsonify({'error': 'Booking not found'}), 404

@bookings_blueprint.route('/user', methods=['GET'])
@jwt_required()
def get_bookings_by_user():
    user_id = get_jwt_identity()
    bookings = mongo.db.bookings.find({'user_id': ObjectId(user_id), 'isDeleted': False})
    results = []
    for booking in bookings:
        hotel = mongo.db.hotels.find_one({'_id': booking['hotel_id']})
        booking_data = serialize_document(booking)
        booking_data['hotel'] = serialize_document(hotel)
        results.append(booking_data)
    
    return jsonify(results), 200

