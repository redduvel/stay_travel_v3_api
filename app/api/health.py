#/app/api/health.py

from flask import Blueprint, jsonify

health_blueprint = Blueprint('health', __name__)

@health_blueprint.route('/ping', methods=['GET'])
def ping():
    return jsonify({'status': 'ok', 'message': 'Server is running'}), 200
