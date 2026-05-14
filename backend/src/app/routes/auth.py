from flask import Blueprint, request, jsonify, make_response, current_app
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity,
    set_access_cookies, set_refresh_cookies,
    unset_jwt_cookies
)
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from app import db
from app.models.user import User, RefreshToken
from app.models.workspace import WorkspaceMember
from app.utils.email import send_confirmation_email
from datetime import datetime, timedelta
import bcrypt

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    required = ['username', 'email', 'password']
    if not all(field in data for field in required):
        return jsonify({'error': 'Missing required fields'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already in use'}), 409
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already taken'}), 409

    try:
        send_confirmation_email(data['email'])
    except Exception:
        return jsonify({'error': 'Failed to send confirmation email. Check mail settings.'}), 500

    hashed = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    user = User(
        username=data['username'],
        email=data['email'],
        password=hashed.decode('utf-8'),
        confirmed=False
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'Check your email to confirm your account'}), 201


@auth_bp.route('/confirm/<token>', methods=['GET'])
def confirm_email(token):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = s.loads(token, salt='email-confirm', max_age=86400)
    except SignatureExpired:
        return jsonify({'error': 'Confirmation link has expired'}), 400
    except BadSignature:
        return jsonify({'error': 'Confirmation link is invalid'}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    if user.confirmed:
        return jsonify({'message': 'Email already confirmed'}), 200

    user.confirmed = True
    db.session.commit()
    return jsonify({'message': 'Email confirmed successfully'}), 200


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

    if not user.confirmed:
        return jsonify({'error': 'Please confirm your email before logging in'}), 403

    identity = str(user.id)
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

    rt = RefreshToken(
        user_id=user.id,
        token=refresh_token,
        expires_at=datetime.utcnow() + timedelta(days=30)
    )
    db.session.add(rt)
    user.last_seen = datetime.utcnow()
    db.session.commit()

    response = make_response(jsonify({'message': 'Login successful', 'user': user.to_dict()}))
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    return response, 200


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
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


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    user_id = get_jwt_identity()
    refresh_token_str = request.cookies.get('refresh_token_cookie')
    if refresh_token_str:
        rt = RefreshToken.query.filter_by(token=refresh_token_str, user_id=user_id).first()
        if rt:
            rt.revoked = True
            db.session.commit()

    response = make_response(jsonify({'message': 'Logged out'}))
    unset_jwt_cookies(response)
    return response, 200
