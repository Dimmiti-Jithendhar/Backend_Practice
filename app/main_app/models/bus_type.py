from app.main_app import db
from app.main_app import models


# Define BusType model
class BusType(db.Model):
    __tablename__ = 'bus_type'
    bus_type_id = db.Column(db.Integer, primary_key=True)
    bus_type_name = db.Column(db.String(50), unique=True, nullable=False)  # e.g., luxury, seater, sleeper

    def __repr__(self):
        return f'<BusType {self.bus_type_name}>'
        
        
        
        
  
def insert_bus_types():
    # New bus types to add
    bus_types_to_add = ['Luxury', 'Seater', 'Sleeper', 'Semi-Sleeper']
    
    for bus_type_name in bus_types_to_add:
        existing_bus_type = BusType.query.filter_by(bus_type_name=bus_type_name).first()
        if not existing_bus_type:  # Only add if it doesn't exist
            new_bus_type = BusType(bus_type_name=bus_type_name)
            db.session.add(new_bus_type)

    db.session.commit()
