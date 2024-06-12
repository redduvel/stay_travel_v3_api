# /app/api/messages/routes.py
import datetime
from flask import Blueprint, request, jsonify
from ...services.utils import serialize_document
from ...services.database import mongo
from bson.objectid import ObjectId
from flask_jwt_extended import jwt_required, get_jwt_identity


messages_blueprint = Blueprint('messages', __name__)


@messages_blueprint.route('/', methods=['GET'])
@jwt_required()
def get_messages():
    user_id = get_jwt_identity()
    
    messages = mongo.db.messages.find({"client_id": ObjectId(user_id)})
    result = [serialize_document(message) for message in messages]

    return jsonify(result), 200
    

@messages_blueprint.route('/', methods=['POST'])
@jwt_required()
def post_message():
    data = request.json
    data['client_id'] = ObjectId(data['client_id'])
    data['businessman_id'] = ObjectId(data['businessman_id'])
    data['created_at'] = datetime.datetime.now()
    data['isDeleted'] = False
    result = mongo.db.messages.insert_one(data)

    return jsonify({"result": True}), 200



