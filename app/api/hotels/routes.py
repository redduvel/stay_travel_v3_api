# /app/api/hotels/routes.py
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from ...services.database import mongo
from ...services.utils import *
from bson.objectid import ObjectId
from flask_jwt_extended import get_jwt_identity, jwt_required

hotels_blueprint = Blueprint('hotels', __name__)

@hotels_blueprint.route('/', methods=['POST'])
@jwt_required()
def create_hotel(): 
    hotel_data = request.json
    hotel_data['owner_id'] = get_jwt_identity()
    hotel_data['created_at'] = datetime.datetime.now()
    hotel_data['isDeleted'] = False
    result = mongo.db.hotels.insert_one(hotel_data)
    return jsonify({'hotel_id': str(result.inserted_id)}), 201

@hotels_blueprint.route('/', methods=['GET'])
def get_hotels():
    page = int(request.args.get('page', 1)) 
    limit = int(request.args.get('limit', 10))
    show_deleted = request.args.get('show_deleted', 'false').lower()

    query_filter = {}
    if show_deleted == 'true':
        query_filter['isDeleted'] = True
    elif show_deleted == 'false':
        query_filter['isDeleted'] = False

    skip = (page - 1) * limit

    hotels_cursor = mongo.db.hotels.find(query_filter).skip(skip).limit(limit)
    
    hotels = []
    for hotel in hotels_cursor:
        features_id = hotel['features']
        features = [mongo.db.features.find_one({'_id': ObjectId(id)}) for id in features_id]
        hotel['features'] = [serialize_document(feature) for feature in features]
        hotel['features'] = remove_duplicates(hotel['features'])
        hotels.append(hotel)

    total = mongo.db.hotels.count_documents(query_filter) 

    return jsonify({
        'total': total,
        'page': page,
        'limit': limit,
        'hotels': [serialize_document(hotel) for hotel in hotels]
    }), 200

@hotels_blueprint.route('/<hotel_id>', methods=['GET'])
def get_hotel(hotel_id):
    hotel = mongo.db.hotels.find_one({'_id': ObjectId(hotel_id)})

    features_id = hotel['features']
    features = [mongo.db.features.find_one({'_id': ObjectId(id)}) for id in features_id]
    hotel['features'] = [serialize_document(feature) for feature in features]
    hotel['features'] = remove_duplicates(hotel['features'])

    if hotel:
        return jsonify(serialize_document(hotel)), 200
    else:
        return jsonify({'error': 'Hotel not found'}), 404

@hotels_blueprint.route('/<hotel_id>', methods=['PUT'])
@jwt_required()
def update_hotel(hotel_id):
    update_data = request.json
    result = mongo.db.hotels.update_one(
        {'_id': ObjectId(hotel_id)},
        {'$set': update_data}
    )
    if result.modified_count:
        return jsonify({'message': 'Hotel updated successfully'}), 200
    else:
        return jsonify({'error': 'Update failed'}), 400

@hotels_blueprint.route('/<hotel_id>', methods=['DELETE'])
@jwt_required()
def delete_hotel(hotel_id):
    update_result = mongo.db.hotels.update_one(
        {'_id': ObjectId(hotel_id)},
        {'$set': {'isDeleted': True}}
    )
    if update_result.modified_count:
        return jsonify({'message': 'Hotel marked as deleted'}), 200
    else:
        return jsonify({'error': 'Hotel not found'}), 404

@hotels_blueprint.route('/search', methods=['GET'])
def search_hotels():
    query = request.args.get('query', '')
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    show_deleted = request.args.get('show_deleted', 'false').lower()

    query_filter = {'$text': {'$search': query}}
    if show_deleted == 'true':
        query_filter['isDeleted'] = True
    elif show_deleted == 'false':
        query_filter['isDeleted'] = False

    skip = (page - 1) * limit

    hotels = mongo.db.hotels.find(query_filter).skip(skip).limit(limit)
    total = mongo.db.hotels.count_documents(query_filter) 

    return jsonify({
        'total': total,
        'page': page,
        'limit': limit,
        'hotels': [serialize_document(hotel) for hotel in hotels]
    }), 200

