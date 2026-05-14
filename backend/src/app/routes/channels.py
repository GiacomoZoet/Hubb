from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.channel import Channel, ChannelMember
from app.models.user import User
from app.utils.decorators import workspace_member_required, workspace_admin_required, channel_access_required

channels_bp = Blueprint('channels', __name__)


# ============================================================
# CREATE CHANNEL
# ============================================================
@channels_bp.route('/<int:workspace_id>/channels', methods=['POST'])
@jwt_required()
@workspace_member_required
def create_channel(workspace_id):
    user_id = int(get_jwt_identity())
    data = request.get_json()

    if not data.get('name'):
        return jsonify({'error': 'Channel name is required'}), 400

    channel = Channel(
        workspace_id=workspace_id,
        name=data['name'],
        description=data.get('description'),
        is_private=data.get('is_private', False),
        created_by=user_id
    )
    db.session.add(channel)
    db.session.flush()

    # If private, add creator as first member
    if channel.is_private:
        db.session.add(ChannelMember(channel_id=channel.id, user_id=user_id))

    db.session.commit()
    return jsonify({'message': 'Channel created', 'channel': channel.to_dict()}), 201


# ============================================================
# LIST CHANNELS IN WORKSPACE
# ============================================================
@channels_bp.route('/<int:workspace_id>/channels', methods=['GET'])
@jwt_required()
@workspace_member_required
def list_channels(workspace_id):
    user_id = int(get_jwt_identity())
    all_channels = Channel.query.filter_by(workspace_id=workspace_id).all()

    result = []
    for c in all_channels:
        if not c.is_private:
            result.append(c.to_dict())
        else:
            # Only include private channels the user is a member of
            is_member = ChannelMember.query.filter_by(
                channel_id=c.id, user_id=user_id
            ).first()
            if is_member:
                result.append(c.to_dict())

    return jsonify(result), 200


# ============================================================
# ADD MEMBER TO PRIVATE CHANNEL
# ============================================================
@channels_bp.route('/channel/<int:channel_id>/members', methods=['POST'])
@jwt_required()
def add_channel_member(channel_id):
    data = request.get_json()
    user = User.query.filter_by(email=data.get('email')).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    existing = ChannelMember.query.filter_by(channel_id=channel_id, user_id=user.id).first()
    if existing:
        return jsonify({'error': 'User already in channel'}), 409

    db.session.add(ChannelMember(channel_id=channel_id, user_id=user.id))
    db.session.commit()
    return jsonify({'message': f'{user.username} added to channel'}), 201


# ============================================================
# DELETE CHANNEL
# ============================================================
@channels_bp.route('/channel/<int:channel_id>', methods=['DELETE'])
@jwt_required()
def delete_channel(channel_id):
    user_id = int(get_jwt_identity())
    channel = Channel.query.get(channel_id)
    if not channel:
        return jsonify({'error': 'Channel not found'}), 404
    if channel.created_by != user_id:
        return jsonify({'error': 'Only the channel creator can delete it'}), 403

    db.session.delete(channel)
    db.session.commit()
    return jsonify({'message': 'Channel deleted'}), 200
