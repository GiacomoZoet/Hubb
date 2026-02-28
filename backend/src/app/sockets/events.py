from flask_socketio import join_room, leave_room, emit
from flask_jwt_extended import decode_token
from app import socketio, db
from app.models.message import Message
from app.models.user import User
from datetime import datetime


def get_user_from_token(token):
    try:
        decoded = decode_token(token)
        return int(decoded['sub'])
    except Exception:
        return None


# ============================================================
# CONNECTION
# ============================================================
@socketio.on('connect')
def handle_connect(auth):
    token = auth.get('token') if auth else None
    user_id = get_user_from_token(token) if token else None
    if not user_id:
        return False  # Reject connection
    user = User.query.get(user_id)
    if user:
        user.last_seen = None  # None = currently online
        db.session.commit()
    emit('connected', {'message': 'Connected successfully'})


# ============================================================
# DISCONNECTION
# ============================================================
@socketio.on('disconnect')
def handle_disconnect():
    pass  # Update last_seen via REST /api/users/me/seen on frontend


# ============================================================
# JOIN CHANNEL ROOM
# ============================================================
@socketio.on('join_room')
def handle_join(data):
    channel_id = data.get('channel_id')
    if channel_id:
        join_room(f'channel_{channel_id}')
        emit('room_joined', {'channel_id': channel_id})


# ============================================================
# LEAVE CHANNEL ROOM
# ============================================================
@socketio.on('leave_room')
def handle_leave(data):
    channel_id = data.get('channel_id')
    if channel_id:
        leave_room(f'channel_{channel_id}')


# ============================================================
# NEW MESSAGE (real-time broadcast)
# ============================================================
@socketio.on('send_message')
def handle_message(data):
    token = data.get('token')
    user_id = get_user_from_token(token)
    if not user_id:
        return

    channel_id = data.get('channel_id')
    content = data.get('content')
    parent_id = data.get('parent_id')

    if not channel_id or not content:
        return

    message = Message(
        channel_id=channel_id,
        user_id=user_id,
        content=content,
        parent_id=parent_id
    )
    db.session.add(message)
    db.session.commit()

    user = User.query.get(user_id)

    # Broadcast to everyone in the channel room
    emit('new_message', {
        **message.to_dict(),
        'username': user.username,
        'avatar_url': user.avatar_url
    }, room=f'channel_{channel_id}')


# ============================================================
# TYPING INDICATOR
# ============================================================
@socketio.on('typing')
def handle_typing(data):
    token = data.get('token')
    user_id = get_user_from_token(token)
    if not user_id:
        return

    user = User.query.get(user_id)
    channel_id = data.get('channel_id')

    emit('user_typing', {
        'user_id': user_id,
        'username': user.username,
        'channel_id': channel_id
    }, room=f'channel_{channel_id}', include_self=False)
