from app.main_app import db
import uuid

class OTP(db.Model):
    __tablename__ = 'otp'

    otp_id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    otp = db.Column(db.String(6), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, otp, email, expires_at):
        self.otp = otp
        self.email = email
        self.expires_at = expires_at

    def __repr__(self):
        return f'<OTP {self.otp} for {self.email}>'
