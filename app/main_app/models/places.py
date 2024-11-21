from app.main_app import db
from app.main_app import models

class Place(db.Model):
    __tablename__ = 'places'

    place_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Place {self.name}>'






