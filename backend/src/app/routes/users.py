from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from datetime import datetime

users_bp = Blueprint('users', __name__)


# ============================================================
# GET CURRENT USER PROFILE
# ============================================================
@users_bp.route('/me', methods=['GET'])
@jwt_required()
def get_me():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict()), 200


# ============================================================
# UPDATE PROFILE
# ============================================================
@users_bp.route('/me', methods=['PATCH'])
@jwt_required()
def update_me():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    data = request.get_json()

    if 'username' in data:
        existing = User.query.filter_by(username=data['username']).first()
        if existing and existing.id != user_id:
            return jsonify({'error': 'Username already taken'}), 409
        user.username = data['username']

    if 'avatar_url' in data:
        user.avatar_url = data['avatar_url']

    db.session.commit()
    return jsonify({'message': 'Profile updated', 'user': user.to_dict()}), 200


# ============================================================
# SEARCH USERS (for inviting to workspaces)
# ============================================================
@users_bp.route('/search', methods=['GET'])
@jwt_required()
def search_users():
    query = request.args.get('q', '')
    if len(query) < 2:
        return jsonify({'error': 'Query too short'}), 400

    users = User.query.filter(
        (User.username.ilike(f'%{query}%')) | (User.email.ilike(f'%{query}%'))
    ).limit(10).all()

    return jsonify([u.to_dict() for u in users]), 200


# ============================================================
# UPDATE LAST SEEN
# ============================================================
@users_bp.route('/me/seen', methods=['POST'])
@jwt_required()
def update_last_seen():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    user.last_seen = datetime.utcnow()
    db.session.commit()
    return jsonify({'message': 'Last seen updated'}), 200
