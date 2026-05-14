from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity,
    set_access_cookies, set_refresh_cookies,
    unset_jwt_cookies
)
from app import db
from app.models.user import User, RefreshToken
from app.models.workspace import WorkspaceMember
from datetime import datetime, timedelta
import bcrypt
import uuid

auth_bp = Blueprint('auth', __name__)


# ============================================================
# REGISTER
# ============================================================
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Validate required fields
    required = ['username', 'email', 'password']
    if not all(field in data for field in required):
        return jsonify({'error': 'Missing required fields'}), 400

    # Check for duplicates
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already in use'}), 409
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already taken'}), 409

    # Hash password
    hashed = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

    user = User(
        username=data['username'],
        email=data['email'],
        password=hashed.decode('utf-8')
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User created', 'user': user.to_dict()}), 201


# ============================================================
# LOGIN
# ============================================================
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password required'}), 400

    user = User.query.filter_by(email=data['email']).first()

    if not user or not bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
        return jsonify({'error': 'Invalid credentials'}), 401

    if not user.is_active:
        return jsonify({'error': 'Account is disabled'}), 403

    # Build JWT identity — this is what gets embedded in the token
    identity = str(user.id)

    # Build additional claims (workspace roles)
    memberships = WorkspaceMember.query.filter_by(user_id=user.id).all()
    additional_claims = {
        'username': user.username,
        'email': user.email,
        'workspaces': [
            {'id': m.workspace_id, 'role': m.role}
            for m in memberships
        ]
    }

    access_token  = create_access_token(identity=identity, additional_claims=additional_claims)
    refresh_token = create_refresh_token(identity=identity)

    # Store refresh token in DB
    rt = RefreshToken(
        user_id=user.id,
        token=refresh_token,
        expires_at=datetime.utcnow() + timedelta(days=30)
    )
    db.session.add(rt)

    # Update last_seen
    user.last_seen = datetime.utcnow()
    db.session.commit()

    # Set tokens in httpOnly cookies
    response = make_response(jsonify({'message': 'Login successful', 'user': user.to_dict()}))
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)

    return response, 200


# ============================================================
# REFRESH
# ============================================================
@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()

    # Check token is in DB and not revoked
    refresh_token_str = request.cookies.get('refresh_token_cookie')
    rt = RefreshToken.query.filter_by(token=refresh_token_str, user_id=user_id, revoked=False).first()

    if not rt or rt.expires_at < datetime.utcnow():
        return jsonify({'error': 'Invalid or expired refresh token'}), 401

    user = User.query.get(user_id)
    memberships = WorkspaceMember.query.filter_by(user_id=user_id).all()

    additional_claims = {
        'username': user.username,
        'email': user.email,
        'workspaces': [
            {'id': m.workspace_id, 'role': m.role}
            for m in memberships
        ]
    }

    new_access_token = create_access_token(identity=user_id, additional_claims=additional_claims)

    response = make_response(jsonify({'message': 'Token refreshed'}))
    set_access_cookies(response, new_access_token)

    return response, 200


# ============================================================
# LOGOUT
# ============================================================
@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    user_id = get_jwt_identity()

    # Revoke the refresh token in DB
    refresh_token_str = request.cookies.get('refresh_token_cookie')
    if refresh_token_str:
        rt = RefreshToken.query.filter_by(token=refresh_token_str, user_id=user_id).first()
        if rt:
            rt.revoked = True
            db.session.commit()

    response = make_response(jsonify({'message': 'Logged out'}))
    unset_jwt_cookies(response)

    return response, 200
