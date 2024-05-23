# /app/api/hotels/routes.py
from flask import Blueprint, request, jsonify
from ...services.database import mongo
from ...services.utils import *
from bson.objectid import ObjectId
from flask_jwt_extended import jwt_required

features_blueprint = Blueprint('features', __name__)

@features_blueprint.route('/', methods=['POST'])
@jwt_required
def create_feature():
    feature_date = request.json
    feature_date['created_at'] = datetime.datetime.now()
    feature_date['isDeleted'] = False
    result = mongo.db.features.insert_one(feature_date)
    return jsonify({'feature_id': str(result.inserted_id)}), 201

@features_blueprint.route('/', methods=['GET'])
def get_features():
    result = mongo.db.features.find()
    result = serialize_cursor(result)

    return jsonify(result), 200

@features_blueprint.route('/<feature_id>', methods=['GET'])
def get_feature(feature_id):
    feature = mongo.db.features.find_one({'_id': ObjectId(feature_id)})
    if feature:
        return jsonify(serialize_document(feature)), 200
    else:
        return jsonify({'error': 'Feature not found'}), 404
    
