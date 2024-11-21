from app.main_app import db
from app.main_app import models

class Route(db.Model):
    __tablename__ = 'routes'
    route_id = db.Column(db.Integer, primary_key=True)  # Primary key
    source = db.Column(db.Integer, db.ForeignKey('places.place_id'), nullable=False)
    destination = db.Column(db.Integer, db.ForeignKey('places.place_id'), nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # duration in minutes
    distance = db.Column(db.Float, nullable=False)  # distance in kilometers

    # Unique constraint to ensure source-destination pairs are unique
    __table_args__ = (db.UniqueConstraint('source', 'destination', name='uix_source_destination'),)

    source_place = db.relationship('Place', foreign_keys=[source])
    destination_place = db.relationship('Place', foreign_keys=[destination])

    def __repr__(self):
        return f'<Route {self.route_id}: {self.source} -> {self.destination}>'
