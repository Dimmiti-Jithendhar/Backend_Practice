from app.main_app import db
from app.main_app import models



class Bus(db.Model):
    __tablename__ = 'buses'
    
    bus_id = db.Column(db.Integer, primary_key=True)
    bus_no = db.Column(db.String(50), unique=True, nullable=False)
    bus_type_id = db.Column(db.Integer, db.ForeignKey('bus_type.bus_type_id'), nullable=False)
    seats = db.Column(db.Integer, nullable=False)  # Capacity
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # Relationship to bus type (assuming there's a BusType model)
    bus_type = db.relationship('BusType', backref='buses')
