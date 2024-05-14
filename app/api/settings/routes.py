# /app/api/settings/routes.py
from bson import ObjectId
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from ...services.database import mongo
from ...services.utils import serialize_document
from flask_jwt_extended import jwt_required, get_jwt_identity

settings_blueprint = Blueprint('settings', __name__)

@settings_blueprint.route('/update', methods=['PUT'])
@jwt_required()
def update_user():
    user_id = get_jwt_identity()
    update_data = request.json
    # Удалите поля, которые нельзя обновлять напрямую
    update_data.pop('password', None)  # Предотвратить обновление пароля через этот метод

    mongo.db.users.update_one({'_id': ObjectId(user_id)}, {'$set': update_data})
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    return jsonify(serialize_document(user)), 200

@settings_blueprint.route('/update_password', methods=['PUT'])
@jwt_required()
def update_password():
    user_id = get_jwt_identity()
    old_password = request.json.get('old_password')
    new_password = request.json.get('new_password')
    user = mongo.db.users.find_one({'_id': ObjectId(user_id)})

    print(type(user['password']), type(old_password))
    if not check_password_hash(user['password'], old_password):
        return jsonify({'error': 'Invalid password'}), 401

    mongo.db.users.update_one(
        {'_id': user_id},
        {'$set': {'password': generate_password_hash(new_password)}}
    )
    return jsonify({'message': 'Password updated successfully'}), 200
