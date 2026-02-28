from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.direct_message import DirectMessage
from app.models.user import User

dm_bp = Blueprint('dm', __name__)


# ============================================================
# SEND DIRECT MESSAGE
# ============================================================
@dm_bp.route('/<int:receiver_id>', methods=['POST'])
@jwt_required()
def send_dm(receiver_id):
    sender_id = int(get_jwt_identity())
    data = request.get_json()

    if sender_id == receiver_id:
        return jsonify({'error': 'Cannot message yourself'}), 400
    if not data.get('content'):
        return jsonify({'error': 'Content is required'}), 400
    if not User.query.get(receiver_id):
        return jsonify({'error': 'User not found'}), 404

    dm = DirectMessage(sender_id=sender_id, receiver_id=receiver_id, content=data['content'])
    db.session.add(dm)
    db.session.commit()
    return jsonify({'message': 'DM sent', 'data': dm.to_dict()}), 201


# ============================================================
# GET CONVERSATION BETWEEN TWO USERS
# ============================================================
@dm_bp.route('/<int:other_user_id>', methods=['GET'])
@jwt_required()
def get_conversation(other_user_id):
    user_id = int(get_jwt_identity())
    page = request.args.get('page', 1, type=int)

    messages = DirectMessage.query.filter(
        ((DirectMessage.sender_id == user_id) & (DirectMessage.receiver_id == other_user_id)) |
        ((DirectMessage.sender_id == other_user_id) & (DirectMessage.receiver_id == user_id))
    ).order_by(DirectMessage.created_at.desc())\
     .paginate(page=page, per_page=30, error_out=False)

    # Mark received messages as read
    DirectMessage.query.filter_by(
        sender_id=other_user_id, receiver_id=user_id, is_read=False
    ).update({'is_read': True})
    db.session.commit()

    return jsonify({
        'messages': [m.to_dict() for m in messages.items],
        'total': messages.total,
        'pages': messages.pages
    }), 200


# ============================================================
# GET ALL DM CONVERSATIONS (inbox)
# ============================================================
@dm_bp.route('/', methods=['GET'])
@jwt_required()
def get_inbox():
    user_id = int(get_jwt_identity())

    # Get distinct users this user has exchanged DMs with
    sent = db.session.query(DirectMessage.receiver_id).filter_by(sender_id=user_id)
    received = db.session.query(DirectMessage.sender_id).filter_by(receiver_id=user_id)
    contact_ids = {row[0] for row in sent.union(received).all()}

    result = []
    for contact_id in contact_ids:
        user = User.query.get(contact_id)
        unread = DirectMessage.query.filter_by(
            sender_id=contact_id, receiver_id=user_id, is_read=False
        ).count()
        result.append({**user.to_dict(), 'unread_count': unread})

    return jsonify(result), 200
