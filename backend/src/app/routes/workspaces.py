from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.workspace import Workspace, WorkspaceMember
from app.models.user import User
from app.utils.decorators import workspace_member_required, workspace_admin_required
import re

workspaces_bp = Blueprint('workspaces', __name__)

def slugify(text):
    text = text.lower().strip()
    return re.sub(r'[\s_-]+', '-', re.sub(r'[^\w\s-]', '', text))


# ============================================================
# CREATE WORKSPACE
# ============================================================
@workspaces_bp.route('/', methods=['POST'])
@jwt_required()
def create_workspace():
    user_id = int(get_jwt_identity())
    data = request.get_json()

    if not data.get('name'):
        return jsonify({'error': 'Workspace name is required'}), 400

    slug = slugify(data['name'])

    # Ensure slug is unique
    if Workspace.query.filter_by(slug=slug).first():
        slug = f"{slug}-{user_id}"

    workspace = Workspace(name=data['name'], slug=slug, owner_id=user_id)
    db.session.add(workspace)
    db.session.flush()  # get workspace.id before commit

    # Add creator as owner in workspace_members
    member = WorkspaceMember(workspace_id=workspace.id, user_id=user_id, role='owner')
    db.session.add(member)
    db.session.commit()

    return jsonify({'message': 'Workspace created', 'workspace': workspace.to_dict()}), 201


# ============================================================
# LIST MY WORKSPACES
# ============================================================
@workspaces_bp.route('/', methods=['GET'])
@jwt_required()
def list_workspaces():
    user_id = int(get_jwt_identity())
    memberships = WorkspaceMember.query.filter_by(user_id=user_id).all()
    workspace_ids = [m.workspace_id for m in memberships]
    workspaces = Workspace.query.filter(Workspace.id.in_(workspace_ids)).all()
    return jsonify([w.to_dict() for w in workspaces]), 200


# ============================================================
# GET WORKSPACE BY SLUG
# ============================================================
@workspaces_bp.route('/<slug>', methods=['GET'])
@jwt_required()
def get_workspace(slug):
    user_id = int(get_jwt_identity())
    workspace = Workspace.query.filter_by(slug=slug).first()
    if not workspace:
        return jsonify({'error': 'Workspace not found'}), 404

    member = WorkspaceMember.query.filter_by(
        workspace_id=workspace.id, user_id=user_id
    ).first()
    if not member:
        return jsonify({'error': 'Access denied'}), 403

    return jsonify(workspace.to_dict()), 200


# ============================================================
# INVITE MEMBER TO WORKSPACE
# ============================================================
@workspaces_bp.route('/<int:workspace_id>/members', methods=['POST'])
@jwt_required()
@workspace_admin_required
def invite_member(workspace_id):
    data = request.get_json()

    user = User.query.filter_by(email=data.get('email')).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    existing = WorkspaceMember.query.filter_by(
        workspace_id=workspace_id, user_id=user.id
    ).first()
    if existing:
        return jsonify({'error': 'User is already a member'}), 409

    member = WorkspaceMember(
        workspace_id=workspace_id,
        user_id=user.id,
        role=data.get('role', 'member')
    )
    db.session.add(member)
    db.session.commit()

    return jsonify({'message': f'{user.username} added to workspace'}), 201


# ============================================================
# LIST WORKSPACE MEMBERS
# ============================================================
@workspaces_bp.route('/<int:workspace_id>/members', methods=['GET'])
@jwt_required()
@workspace_member_required
def list_members(workspace_id):
    members = WorkspaceMember.query.filter_by(workspace_id=workspace_id).all()
    result = []
    for m in members:
        user = User.query.get(m.user_id)
        result.append({**user.to_dict(), 'role': m.role})
    return jsonify(result), 200


# ============================================================
# UPDATE MEMBER ROLE
# ============================================================
@workspaces_bp.route('/<int:workspace_id>/members/<int:user_id>', methods=['PATCH'])
@jwt_required()
@workspace_admin_required
def update_member_role(workspace_id, user_id):
    data = request.get_json()
    member = WorkspaceMember.query.filter_by(
        workspace_id=workspace_id, user_id=user_id
    ).first()
    if not member:
        return jsonify({'error': 'Member not found'}), 404
    if data.get('role') not in ('admin', 'member'):
        return jsonify({'error': 'Invalid role'}), 400

    member.role = data['role']
    db.session.commit()
    return jsonify({'message': 'Role updated'}), 200


# ============================================================
# REMOVE MEMBER
# ============================================================
@workspaces_bp.route('/<int:workspace_id>/members/<int:user_id>', methods=['DELETE'])
@jwt_required()
@workspace_admin_required
def remove_member(workspace_id, user_id):
    member = WorkspaceMember.query.filter_by(
        workspace_id=workspace_id, user_id=user_id
    ).first()
    if not member:
        return jsonify({'error': 'Member not found'}), 404
    if member.role == 'owner':
        return jsonify({'error': 'Cannot remove the workspace owner'}), 403

    db.session.delete(member)
    db.session.commit()
    return jsonify({'message': 'Member removed'}), 200


# ============================================================
# DELETE WORKSPACE
# ============================================================
@workspaces_bp.route('/<int:workspace_id>', methods=['DELETE'])
@jwt_required()
def delete_workspace(workspace_id):
    user_id = int(get_jwt_identity())
    workspace = Workspace.query.get(workspace_id)
    if not workspace:
        return jsonify({'error': 'Workspace not found'}), 404
    if workspace.owner_id != user_id:
        return jsonify({'error': 'Only the owner can delete this workspace'}), 403

    db.session.delete(workspace)
    db.session.commit()
    return jsonify({'message': 'Workspace deleted'}), 200
