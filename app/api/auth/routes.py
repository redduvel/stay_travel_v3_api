# /app/api/auth/routes.py
from flask_jwt_extended import create_access_token
import jwt
import datetime
from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from ...services.utils import serialize_document, identify_string
from ...services.database import mongo

auth_blueprint = Blueprint('auth', __name__)

def create_token(user_id):
    expires = datetime.timedelta(hours=128)
    access_token = create_access_token(identity=str(user_id), expires_delta=expires)
    return access_token

@auth_blueprint.route('/login', methods=['POST'])
def login():
    emailOrNumber = request.json.get('emailOrNumber')
    password = request.json.get('password')
    input_type = identify_string(emailOrNumber)

    if input_type == 'email':
        user = mongo.db.users.find_one({'email': emailOrNumber})
    elif input_type == 'phone':
        user = mongo.db.users.find_one({'number': emailOrNumber})
    else:
        return jsonify({'error': 'Invalid email or phone number format'}), 400

    if user and check_password_hash(user['password'], password):
        token = create_token(user['_id'])
        user_data = serialize_document(user)
        user_data['token'] = token
        return jsonify(user_data), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.json
    emailOrNumber = request.json.get('emailOrNumber')
    password = request.json.get('password')
    input_type = identify_string(emailOrNumber)

    user_data = {'password': generate_password_hash(password)}
    if input_type == 'email':
        if mongo.db.users.find_one({'email': emailOrNumber}):
            return jsonify({'error': 'Email already exists'}), 409
        user_data['email'] = emailOrNumber
    elif input_type == 'phone':
        if mongo.db.users.find_one({'number': emailOrNumber}):
            return jsonify({'error': 'Phone number already exists'}), 409
        user_data['number'] = emailOrNumber
    else:
        return jsonify({'error': 'Invalid email or phone number format'}), 400

    user_data['created_at'] = datetime.datetime.now()
    user_data['isDeleted'] = False
    
    user_id = mongo.db.users.insert_one(user_data).inserted_id
    user = mongo.db.users.find_one({'_id': user_id})

    token = create_token(user['_id'])
    user_data = serialize_document(user)
    user_data['token'] = token


    return jsonify(user_data), 200

