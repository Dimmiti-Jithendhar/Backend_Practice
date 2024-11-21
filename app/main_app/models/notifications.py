from datetime import datetime
from app.main_app import db
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(UUID(as_uuid=True), nullable=False)  # This will handle UUIDs
    message = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(50), default="unread")
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    type = db.Column(db.String(50), nullable=False)

    def __init__(self, user_id, message, type,status="unread"):
        self.user_id = user_id
        self.message = message
        self.type = type
        self.status = status