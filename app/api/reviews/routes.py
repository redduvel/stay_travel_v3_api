# /app/api/reviews/routes.py
from flask import Blueprint, request, jsonify
from ...services.utils import serialize_document
from ...services.database import mongo
from bson.objectid import ObjectId
from flask_jwt_extended import jwt_required, get_jwt_identity

reviews_blueprint = Blueprint('reviews', __name__)

@reviews_blueprint.route('/hotel/<hotel_id>', methods=['POST'])
@jwt_required()
def create_review(hotel_id):
    user_id = get_jwt_identity()
    data = request.json
    review = {
        'user_id': ObjectId(user_id),
        'hotel_id': ObjectId(hotel_id),
        'text': data['text'],
        'rating': data['rating']
    }
    mongo.db.reviews.insert_one(review)
    return jsonify({'message': 'Review added successfully'}), 201

@reviews_blueprint.route('/hotel/<hotel_id>', methods=['GET'])
def get_reviews(hotel_id):
    reviews = mongo.db.reviews.find({'hotel_id': ObjectId(hotel_id)})
    result = [serialize_document(review) for review in reviews]
    return jsonify(result), 200

@reviews_blueprint.route('/<review_id>', methods=['DELETE'])
@jwt_required()
def delete_review(review_id):
    user_id = get_jwt_identity()
    result = mongo.db.reviews.update_one(
        {'_id': ObjectId(review_id), 'user_id': ObjectId(user_id)},
        {'$set': {'isDeleted': True}}
    )
    if result.modified_count:
        return jsonify({'message': 'Review marked as deleted'}), 200
    else:
        return jsonify({'error': 'Review not found or permission denied'}), 404

@reviews_blueprint.route('/<review_id>', methods=['PUT'])
@jwt_required()
def update_review(review_id):
    user_id = get_jwt_identity()
    data = request.json
    result = mongo.db.reviews.update_one(
        {'_id': ObjectId(review_id), 'user_id': ObjectId(user_id)},
        {'$set': {'text': data['text'], 'rating': data['rating']}}
    )
    if result.modified_count:
        return jsonify({'message': 'Review updated successfully'}), 200
