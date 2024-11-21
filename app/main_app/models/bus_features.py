from app.main_app import db
from app.main_app import models


# Define BusFeature model (Junction Table between BusType and Feature)
class BusFeature(db.Model):
    __tablename__ = 'bus_feature'
    bus_feature_id = db.Column(db.Integer, primary_key=True)  # Primary key
    bus_type_id = db.Column(db.Integer, db.ForeignKey('bus_type.bus_type_id'), nullable=False)  # Foreign key to BusType
    feature_id = db.Column(db.Integer, db.ForeignKey('features.feature_id'), nullable=False)  # Foreign key to Feature

    # Relationships
    bus_type = db.relationship('BusType', backref=db.backref('bus_features', lazy=True))
    feature = db.relationship('Feature', backref=db.backref('bus_features', lazy=True))

    def __repr__(self):
        return f'<BusFeature bus_type_id={self.bus_type_id}, feature_id={self.feature_id}>'