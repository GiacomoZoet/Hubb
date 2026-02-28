from app import db
from datetime import datetime

class Message(db.Model):
    __tablename__ = 'messages'

    id         = db.Column(db.Integer, primary_key=True, autoincrement=True)
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id', ondelete='CASCADE'), nullable=False)
    user_id    = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    content    = db.Column(db.Text, nullable=False)
    parent_id  = db.Column(db.Integer, db.ForeignKey('messages.id', ondelete='SET NULL'), default=None)
    is_edited  = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    replies     = db.relationship('Message', backref=db.backref('parent', remote_side='Message.id'), lazy=True)
    reactions   = db.relationship('Reaction', backref='message', lazy=True)
    attachments = db.relationship('Attachment', backref='message', lazy=True,
                                  primaryjoin="Message.id == Attachment.message_id")

    def to_dict(self):
        return {
            'id':         self.id,
            'channel_id': self.channel_id,
            'user_id':    self.user_id,
            'content':    self.content,
            'parent_id':  self.parent_id,
            'is_edited':  self.is_edited,
            'created_at': self.created_at.isoformat()
        }


class Reaction(db.Model):
    __tablename__ = 'reactions'

    id         = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message_id = db.Column(db.Integer, db.ForeignKey('messages.id', ondelete='CASCADE'), nullable=False)
    user_id    = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    emoji      = db.Column(db.String(10), nullable=False)

    __table_args__ = (db.UniqueConstraint('message_id', 'user_id', 'emoji', name='unique_reaction'),)
