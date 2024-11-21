from app.main_app import db
from app.main_app import models
from app.main_app.models.bus import Bus

# Define BusOperator model
class BusOperator(db.Model):
    __tablename__ = 'bus_operator'  # Table name in the database

    # Primary key
    bus_operator_id = db.Column(db.Integer, primary_key=True)  
    
    # Foreign key to Bus
    bus_id = db.Column(db.Integer, db.ForeignKey('buses.bus_id'), nullable=False)  
    
    # Foreign key to Operator
    operator_id = db.Column(db.Integer, db.ForeignKey('operators.operator_id'), nullable=False)  

    # Relationships
    bus = db.relationship('Bus', backref=db.backref('bus_operators', lazy=True))  
    operators = db.relationship('Operator', backref=db.backref('bus_operators', lazy=True))  

    def __repr__(self):
        return f'<BusOperator bus_operator_id={self.bus_operator_id}, bus_id={self.bus_id}, operator_id={self.operator_id}>'
