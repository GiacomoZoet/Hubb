from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.message import Message, Reaction
from app.models.channel import Channel, ChannelMember
from app.utils.decorators import channel_access_required

messages_bp = Blueprint('messages', __name__)


# ============================================================
# GET MESSAGES IN CHANNEL (paginated)
# ============================================================
@messages_bp.route('/<int:channel_id>', methods=['GET'])
@jwt_required()
@channel_access_required
def get_messages(channel_id):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 30, type=int)

    messages = Message.query.filter_by(channel_id=channel_id, parent_id=None)\
        .order_by(Message.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'messages': [m.to_dict() for m in messages.items],
        'total': messages.total,
        'pages': messages.pages,
        'current_page': messages.page
    }), 200


# ============================================================
# GET THREAD REPLIES
# ============================================================
@messages_bp.route('/<int:channel_id>/thread/<int:parent_id>', methods=['GET'])
@jwt_required()
@channel_access_required
def get_thread(channel_id, parent_id):
    replies = Message.query.filter_by(channel_id=channel_id, parent_id=parent_id)\
        .order_by(Message.created_at.asc()).all()
    return jsonify([r.to_dict() for r in replies]), 200


# ============================================================
# SEND MESSAGE
# ============================================================
@messages_bp.route('/<int:channel_id>', methods=['POST'])
@jwt_required()
@channel_access_required
def send_message(channel_id):
    user_id = int(get_jwt_identity())
    data = request.get_json()

    if not data.get('content'):
        return jsonify({'error': 'Message content is required'}), 400

    message = Message(
        channel_id=channel_id,
        user_id=user_id,
        content=data['content'],
        parent_id=data.get('parent_id')  # None = top-level, set = thread reply
    )
    db.session.add(message)
    db.session.commit()

    return jsonify({'message': 'Message sent', 'data': message.to_dict()}), 201


# ============================================================
# EDIT MESSAGE
# ============================================================
@messages_bp.route('/<int:channel_id>/<int:message_id>', methods=['PATCH'])
@jwt_required()
@channel_access_required
def edit_message(channel_id, message_id):
    user_id = int(get_jwt_identity())
    message = Message.query.get(message_id)

    if not message:
        return jsonify({'error': 'Message not found'}), 404
    if message.user_id != user_id:
        return jsonify({'error': 'You can only edit your own messages'}), 403

    data = request.get_json()
    if not data.get('content'):
        return jsonify({'error': 'Content is required'}), 400

    message.content = data['content']
    message.is_edited = True
    db.session.commit()

    return jsonify({'message': 'Message updated', 'data': message.to_dict()}), 200


# ============================================================
# DELETE MESSAGE
# ============================================================
@messages_bp.route('/<int:channel_id>/<int:message_id>', methods=['DELETE'])
@jwt_required()
@channel_access_required
def delete_message(channel_id, message_id):
    user_id = int(get_jwt_identity())
    message = Message.query.get(message_id)

    if not message:
        return jsonify({'error': 'Message not found'}), 404
    if message.user_id != user_id:
        return jsonify({'error': 'You can only delete your own messages'}), 403

    db.session.delete(message)
    db.session.commit()
    return jsonify({'message': 'Message deleted'}), 200


# ============================================================
# SEARCH MESSAGES (FULLTEXT)
# ============================================================
@messages_bp.route('/search', methods=['GET'])
@jwt_required()
def search_messages():
    query = request.args.get('q', '')
    channel_id = request.args.get('channel_id', type=int)

    if not query or len(query) < 2:
        return jsonify({'error': 'Query too short'}), 400

    sql = """
        SELECT * FROM messages
        WHERE MATCH(content) AGAINST(:query IN BOOLEAN MODE)
    """

    params = {'query': query}

    if channel_id:
        sql += " AND channel_id = :channel_id"
        params['channel_id'] = channel_id

    sql += " LIMIT 20"

    results = db.session.execute(db.text(sql), params).fetchall()

    return jsonify([{
        'id':         row.id,
        'channel_id': row.channel_id,
        'user_id':    row.user_id,
        'content':    row.content,
        'parent_id':  row.parent_id,
        'is_edited':  row.is_edited,
        'created_at': row.created_at.isoformat()
    } for row in results]), 200


# ============================================================
# ADD REACTION
# ============================================================
@messages_bp.route('/<int:channel_id>/<int:message_id>/reactions', methods=['POST'])
@jwt_required()
@channel_access_required
def add_reaction(channel_id, message_id):
    user_id = int(get_jwt_identity())
    data = request.get_json()

    if not data.get('emoji'):
        return jsonify({'error': 'Emoji is required'}), 400

    existing = Reaction.query.filter_by(
        message_id=message_id, user_id=user_id, emoji=data['emoji']
    ).first()
    if existing:
        # Toggle off if already reacted
        db.session.delete(existing)
        db.session.commit()
        return jsonify({'message': 'Reaction removed'}), 200

    reaction = Reaction(message_id=message_id, user_id=user_id, emoji=data['emoji'])
    db.session.add(reaction)
    db.session.commit()
    return jsonify({'message': 'Reaction added'}), 201
