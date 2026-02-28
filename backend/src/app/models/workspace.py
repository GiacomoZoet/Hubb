from app import db
from datetime import datetime

class Workspace(db.Model):
    __tablename__ = 'workspaces'

    id         = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name       = db.Column(db.String(100), nullable=False)
    slug       = db.Column(db.String(100), nullable=False, unique=True)
    owner_id   = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    channels = db.relationship('Channel', backref='workspace', lazy=True)
    members  = db.relationship('WorkspaceMember', backref='workspace', lazy=True)

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
