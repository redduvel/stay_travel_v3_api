# /app/api/settings/routes.py
import datetime
from bson import ObjectId
from flask import Blueprint, request, jsonify
import bcrypt
from ...services.database import mongo
from ...services.utils import serialize_document
from flask_jwt_extended import jwt_required, get_jwt_identity

settings_blueprint = Blueprint('settings', __name__)

@settings_blueprint.route('/update', methods=['PUT'])
@jwt_required()
def update_user():
    user_id = get_jwt_identity()
    update_data = request.json

    mongo.db.users.update_one({'_id': ObjectId(user_id)}, {'$set': update_data})

    return jsonify({'message': 'Profile updated successfully'}), 200

@settings_blueprint.route('/update_password', methods=['PUT'])
@jwt_required()
def update_password():
    user_id = get_jwt_identity()
    old_password = request.json.get('old_password')
    new_password = request.json.get('new_password')
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})

    if not bcrypt.checkpw(old_password.encode(encoding="utf-8"), user['password']):
        return jsonify({'error': 'Invalid password'}), 401

    mongo.db.users.update_one(
        {'_id': user_id},
        {'$set': {'password': bcrypt.hashpw(new_password.encode(encoding="utf-8"),  bcrypt.gensalt())}}
    )
    user['set_password'] = datetime.datetime.now()

    return jsonify({'message': 'Password updated successfully'}), 200
