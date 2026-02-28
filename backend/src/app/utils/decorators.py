from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from app.models.workspace import WorkspaceMember

def workspace_member_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = int(get_jwt_identity())
        workspace_id = kwargs.get('workspace_id')
        member = WorkspaceMember.query.filter_by(
            workspace_id=workspace_id, user_id=user_id
        ).first()
        if not member:
            return jsonify({'error': 'Access denied — not a workspace member'}), 403
        return f(*args, **kwargs)
    return decorated_function

def workspace_admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = int(get_jwt_identity())
        workspace_id = kwargs.get('workspace_id')
        member = WorkspaceMember.query.filter_by(
            workspace_id=workspace_id, user_id=user_id
        ).first()
        if not member or member.role not in ('admin', 'owner'):
            return jsonify({'error': 'Access denied — admin required'}), 403
        return f(*args, **kwargs)
    return decorated_function

def channel_access_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from app.models.channel import Channel, ChannelMember
        user_id = int(get_jwt_identity())
        channel_id = kwargs.get('channel_id')
        channel = Channel.query.get(channel_id)
        if not channel:
            return jsonify({'error': 'Channel not found'}), 404
        if channel.is_private:
            member = ChannelMember.query.filter_by(
                channel_id=channel_id, user_id=user_id
            ).first()
            if not member:
                return jsonify({'error': 'Access denied — private channel'}), 403
        return f(*args, **kwargs)
    return decorated_function
