from app.main_app import db
from app.main_app import models
from sqlalchemy.dialects.postgresql import ARRAY  # Import for using array type
from sqlalchemy import Boolean, Column

class AvailableBuses(db.Model):
    __tablename__ = 'available_buses'

    # Primary key
    available_buses_id = db.Column(db.Integer, primary_key=True)

    # Foreign key to Bus
    bus_id = db.Column(db.Integer, db.ForeignKey('buses.bus_id'), nullable=False)

    # Foreign key to Route
    route_id = db.Column(db.Integer, db.ForeignKey('routes.route_id'), nullable=False)

    # Date of the bus availability
    date = db.Column(db.Date, nullable=False)

    # Time in 24-hour format
    time = db.Column(db.Time, nullable=False)

    # Fare
    fare = db.Column(db.Float, nullable=False, default=0.0)

    # New column for storing available seats as an array of integers
    available_seats = db.Column(ARRAY(db.Integer), nullable=False)  # Using PostgreSQL ARRAY type

    # Soft delete flag
    deleted = db.Column(Boolean, default=False)

    # New column for bus number
    bus_number = db.Column(db.String, nullable=False)

    # Relationships
    bus = db.relationship('Bus', backref=db.backref('available_buses', lazy=True))
    route = db.relationship('Route', backref=db.backref('available_buses', lazy=True))

    def __repr__(self):
        return f'<AvailableBuses available_buses_id={self.available_buses_id}, bus_id={self.bus_id}, route_id={self.route_id}, date={self.date}, time={self.time}, fare={self.fare}, available_seats={self.available_seats}, bus_number={self.bus_number}>'























# from app.main_app import db
# from app.main_app import models
# from sqlalchemy.dialects.postgresql import ARRAY   # Import for using array type
# from sqlalchemy import Boolean, Column
# class AvailableBuses(db.Model):
#     __tablename__ = 'available_buses'

#     # Primary key
#     available_buses_id = db.Column(db.Integer, primary_key=True)

#     # Foreign key to Bus
#     bus_id = db.Column(db.Integer, db.ForeignKey('buses.bus_id'), nullable=False)

#     # Foreign key to Route
#     route_id = db.Column(db.Integer, db.ForeignKey('routes.route_id'), nullable=False)

#     # Date of the bus availability
#     date = db.Column(db.Date, nullable=False)

#     # Time in 24-hour format
#     time = db.Column(db.Time, nullable=False)

#     # Fare
#     fare = db.Column(db.Float, nullable=False, default=0.0)

#     # New column for storing available seats as an array of integers
#     available_seats = db.Column(ARRAY(db.Integer), nullable=False)  # Using PostgreSQL ARRAY type

#     deleted = db.Column(Boolean, default=False)
#     # Relationships
#     bus = db.relationship('Bus', backref=db.backref('available_buses', lazy=True))
#     route = db.relationship('Route', backref=db.backref('available_buses', lazy=True))

#     def __repr__(self):
#         return f'<AvailableBuses available_buses_id={self.available_buses_id}, bus_id={self.bus_id}, route_id={self.route_id}, date={self.date}, time={self.time}, fare={self.fare}, available_seats={self.available_seats}>'



































# from app.main_app import db
# from app.main_app import models


# class AvailableBuses(db.Model):
#     __tablename__ = 'available_buses'

#     # Primary key
#     available_buses_id = db.Column(db.Integer, primary_key=True)

#     # Foreign key to Bus
#     bus_id = db.Column(db.Integer, db.ForeignKey('buses.bus_id'), nullable=False)

#     # Foreign key to Route
#     route_id = db.Column(db.Integer, db.ForeignKey('routes.route_id'), nullable=False)

#     # Date of the bus availability
#     date = db.Column(db.Date, nullable=False)

#     # Time in 24-hour format
#     time = db.Column(db.Time, nullable=False)

#     # New fare column
#     fare = db.Column(db.Float, nullable=False, default=0.0)  # Add the fare column with a default value

#     # Relationships
#     bus = db.relationship('Bus', backref=db.backref('available_buses', lazy=True))
#     route = db.relationship('Route', backref=db.backref('available_buses', lazy=True))

#     def __repr__(self):
#         return f'<AvailableBuses available_buses_id={self.available_buses_id}, bus_id={self.bus_id}, route_id={self.route_id}, date={self.date}, time={self.time}, fare={self.fare}>'
