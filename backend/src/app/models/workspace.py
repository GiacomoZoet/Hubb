from app import db
from datetime import datetime

class Workspace(db.Model):
    __tablename__ = 'workspaces'

    id         = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name       = db.Column(db.String(100), nullable=False)
    slug       = db.Column(db.String(100), nullable=False, unique=True)
    owner_id   = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    channels = db.relationship('Channel', backref='workspace', lazy=True, passive_deletes=True)
    members  = db.relationship('WorkspaceMember', backref='workspace', lazy=True, passive_deletes=True)

    def to_dict(self):
        return {
            'id':         self.id,
            'name':       self.name,
            'slug':       self.slug,
            'owner_id':   self.owner_id,
            'created_at': self.created_at.isoformat()
        }


class WorkspaceMember(db.Model):
    __tablename__ = 'workspace_members'

    workspace_id = db.Column(db.Integer, db.ForeignKey('workspaces.id', ondelete='CASCADE'), primary_key=True)
    user_id      = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    role         = db.Column(db.Enum('owner', 'admin', 'member'), default='member')
    joined_at    = db.Column(db.DateTime, default=datetime.utcnow)


class WorkspaceInvitation(db.Model):
    __tablename__ = 'workspace_invitations'

    id           = db.Column(db.Integer, primary_key=True, autoincrement=True)
    workspace_id = db.Column(db.Integer, db.ForeignKey('workspaces.id', ondelete='CASCADE'), nullable=False)
    invited_by   = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user_id      = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    status       = db.Column(db.Enum('pending', 'accepted', 'declined'), default='pending')
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id':           self.id,
            'workspace_id': self.workspace_id,
            'invited_by':   self.invited_by,
            'user_id':      self.user_id,
            'status':       self.status,
            'created_at':   self.created_at.isoformat()
        }
