from app import db
from datetime import datetime

class DirectMessage(db.Model):
    __tablename__ = 'direct_messages'

    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sender_id   = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    content     = db.Column(db.Text, nullable=False)
    is_read     = db.Column(db.Boolean, default=False)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    attachments = db.relationship('Attachment', backref='direct_message', lazy=True,
                                  primaryjoin="DirectMessage.id == Attachment.dm_id")

    def to_dict(self):
        return {
            'id':          self.id,
            'sender_id':   self.sender_id,
            'receiver_id': self.receiver_id,
            'content':     self.content,
            'is_read':     self.is_read,
            'created_at':  self.created_at.isoformat()
        }


class Attachment(db.Model):
    __tablename__ = 'attachments'

    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message_id  = db.Column(db.Integer, db.ForeignKey('messages.id', ondelete='CASCADE'), default=None)
    dm_id       = db.Column(db.Integer, db.ForeignKey('direct_messages.id', ondelete='CASCADE'), default=None)
    file_url    = db.Column(db.String(500), nullable=False)
    file_name   = db.Column(db.String(255), nullable=False)
    file_type   = db.Column(db.String(50), nullable=False)
    file_size   = db.Column(db.Integer, nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
