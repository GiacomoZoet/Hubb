from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username    = db.Column(db.String(50), nullable=False, unique=True)
    email       = db.Column(db.String(100), nullable=False, unique=True)
    password    = db.Column(db.String(255), nullable=False)
    avatar_url  = db.Column(db.String(500), default=None)
    is_active   = db.Column(db.Boolean, default=True)
    last_seen   = db.Column(db.DateTime, default=None)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    workspaces     = db.relationship('Workspace', backref='owner', lazy=True)
    refresh_tokens = db.relationship('RefreshToken', backref='user', lazy=True)

    def to_dict(self):
        return {
            'id':         self.id,
            'username':   self.username,
            'email':      self.email,
            'avatar_url': self.avatar_url,
            'last_seen':  self.last_seen.isoformat() if self.last_seen else None,
            'created_at': self.created_at.isoformat()
        }


class RefreshToken(db.Model):
    __tablename__ = 'refresh_tokens'

    id         = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id    = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    token      = db.Column(db.String(500), nullable=False, unique=True)
    expires_at = db.Column(db.DateTime, nullable=False)
    revoked    = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
