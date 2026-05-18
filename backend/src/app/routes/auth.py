from flask import Blueprint, request, jsonify, current_app
from app.utils.email import send_confirmation_email, send_reset_email
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity
)
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from app import db
from app.models.user import User, RefreshToken
from app.models.workspace import WorkspaceMember
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
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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

    return jsonify({
        'message': 'Login successful',
        'user': user.to_dict(),
        'access_token': access_token,
        'refresh_token': refresh_token
    }), 200


@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')
    if not email:
        return jsonify({'error': 'Email is required'}), 400

    user = User.query.filter_by(email=email).first()
    if user:
        try:
            send_reset_email(email)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return jsonify({'message': 'If that email exists, a reset link has been sent'}), 200


@auth_bp.route('/reset-password/<token>', methods=['POST'])
def reset_password(token):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = s.loads(token, salt='password-reset', max_age=3600)
    except SignatureExpired:
        return jsonify({'error': 'Reset link has expired'}), 400
    except BadSignature:
        return jsonify({'error': 'Reset link is invalid'}), 400

    data = request.get_json()
    password = data.get('password')
    if not password:
        return jsonify({'error': 'Password is required'}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user.password = hashed.decode('utf-8')
    db.session.commit()

    return jsonify({'message': 'Password updated'}), 200


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    refresh_token_str = request.headers.get('Authorization', '').replace('Bearer ', '')
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
    return jsonify({'access_token': new_access_token}), 200


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    refresh_token_str = data.get('refresh_token')
    if refresh_token_str:
        rt = RefreshToken.query.filter_by(token=refresh_token_str, user_id=user_id).first()
        if rt:
            rt.revoked = True
            db.session.commit()
    return jsonify({'message': 'Logged out'}), 200
