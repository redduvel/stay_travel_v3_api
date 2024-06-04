# /app/api/hotels/routes.py
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from ...services.database import mongo
from ...services.utils import *
from bson.objectid import ObjectId
from flask_jwt_extended import get_jwt_identity, jwt_required

favorites_blueprint = Blueprint('favorites', __name__)

@favorites_blueprint.route('/', methods=['GET'])
@jwt_required()
def get_favorites():
    user_id = get_jwt_identity()
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    
    if not user or 'featured_hotels' not in user:
        return jsonify({'msg': 'Нет избранных отелей'}), 404
    
    favorite_hotel_ids = user.get('featured_hotels', [])
    
    favorite_hotels = list(mongo.db.hotels.find({'_id': {'$in': [ObjectId(hotel_id) for hotel_id in favorite_hotel_ids]}}))
    
    hotels = []
    for hotel in favorite_hotels:
        features_id = hotel['features']
        features = [mongo.db.features.find_one({'_id': ObjectId(id)}) for id in features_id]
        hotel['features'] = [serialize_document(feature) for feature in features]
        hotel['features'] = remove_duplicates(hotel['features'])
        hotels.append(hotel)


    return jsonify([serialize_document(hotel) for hotel in hotels]), 200


@favorites_blueprint.route('/add/<hotel_id>', methods=['POST'])
@jwt_required()
def add_hotel_to_featured_hotels(hotel_id):
    user_id = get_jwt_identity()
    result = mongo.db.users.update_one(
        {'_id': ObjectId(user_id)},
        {'$addToSet': {'featured_hotels': ObjectId(hotel_id)}}
    )
    print(result)
    
    if result.modified_count > 0:
        return {'msg': 'Отель успешно добавлен в избранные.'}, 200
    else:
        return {'msg': 'Отель уже находится в избранных.'}, 200


@favorites_blueprint.route('/remove/<hotel_id>', methods=['DELETE'])
@jwt_required()
def remove_hotel_from_featured_hotels(hotel_id):
    user_id = get_jwt_identity()
    
    result = mongo.db.users.update_one(
        {'_id': ObjectId(user_id)},
        {'$pull': {'featured_hotels': hotel_id}}
    )
    
    if result.modified_count > 0:
        return {'msg': 'Отель успешно удален из избранных.'}, 200
    else:
        return {'msg': 'Отель не найден в избранных'}, 200
