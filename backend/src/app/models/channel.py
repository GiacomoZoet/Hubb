from app import db
from datetime import datetime

class Channel(db.Model):
    __tablename__ = 'channels'

    id           = db.Column(db.Integer, primary_key=True, autoincrement=True)
    workspace_id = db.Column(db.Integer, db.ForeignKey('workspaces.id', ondelete='CASCADE'), nullable=False)
    name         = db.Column(db.String(100), nullable=False)
    description  = db.Column(db.String(255), default=None)
    is_private   = db.Column(db.Boolean, default=False)
    created_by   = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), default=None)
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)

    messages = db.relationship('Message', backref='channel', lazy=True)
    members  = db.relationship('ChannelMember', backref='channel', lazy=True)

    def to_dict(self):
        return {
            'id':           self.id,
            'workspace_id': self.workspace_id,
            'name':         self.name,
            'description':  self.description,
            'is_private':   self.is_private,
            'created_by':   self.created_by,
            'created_at':   self.created_at.isoformat()
        }


class ChannelMember(db.Model):
    __tablename__ = 'channel_members'

    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id', ondelete='CASCADE'), primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
