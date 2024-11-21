from app.main_app import db
import random
import string
from datetime import datetime
from sqlalchemy.dialects.postgresql import ARRAY

class Booking(db.Model):
    __tablename__ = 'booking_table'

    # Primary key
    booking_id = db.Column(db.Integer, primary_key=True)

    # Foreign key to User
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    # Foreign key to Available Buses
    available_bus_id = db.Column(db.Integer, db.ForeignKey('available_buses.available_buses_id'), nullable=False)

    # Booking date
    booking_date = db.Column(db.Date, nullable=False)

    # Seat numbers stored as an array
    seat_no = db.Column(ARRAY(db.Integer), nullable=False)  # Change to ARRAY type

    # Total fare
    total_fare = db.Column(db.Float, nullable=False)

    # Status of the booking (e.g., confirmed, canceled)
    status = db.Column(db.String(50), nullable=False, default='confirmed')

    # Booking number (unique 8-digit code)
    booking_number = db.Column(db.String(8), unique=True, nullable=False)

    # Timestamps for creation and update
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = db.relationship('User', backref=db.backref('bookings', lazy=True))
    available_bus = db.relationship('AvailableBuses', backref=db.backref('bookings', lazy=True))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.booking_number = self.generate_unique_booking_number()  # Generate unique booking number on creation

    @staticmethod
    def generate_unique_booking_number():
        """Generate a unique 8-digit booking number."""
        while True:
            booking_number = ''.join(random.choices(string.digits, k=8))
            if not Booking.query.filter_by(booking_number=booking_number).first():
                return booking_number  # Return if it's unique

    def __repr__(self):
        return (f'<Booking booking_id={self.booking_id}, user_id={self.user_id}, '
                f'available_bus_id={self.available_bus_id}, booking_date={self.booking_date}, '
                f'seat_no={self.seat_no}, total_fare={self.total_fare}, '
                f'status={self.status}, booking_number={self.booking_number}, '
                f'created_at={self.created_at}, updated_at={self.updated_at}>')




























# from app.main_app import db
# import random
# import string
# from datetime import datetime
# from sqlalchemy.dialects.postgresql import ARRAY


# class Booking(db.Model):
#     __tablename__ = 'booking_table'

#     # Primary key
#     booking_id = db.Column(db.Integer, primary_key=True)

#     # Foreign key to User
#     user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

#     # Foreign key to Available Buses
#     available_bus_id = db.Column(db.Integer, db.ForeignKey('available_buses.available_buses_id'), nullable=False)

#     # Booking date
#     booking_date = db.Column(db.Date, nullable=False)

#     # Seat numbers stored as an array
#     seat_no = db.Column(ARRAY(db.Integer), nullable=False)  # Change to ARRAY type

#     # Total fare
#     total_fare = db.Column(db.Float, nullable=False)

#     # Status of the booking (e.g., confirmed, canceled)
#     status = db.Column(db.String(50), nullable=False, default='confirmed')

#     # Booking number (unique 8-digit code)
#     booking_number = db.Column(db.String(8), unique=True, nullable=False)

#     # Timestamps for creation and update
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

#     # Relationships
#     user = db.relationship('User', backref=db.backref('bookings', lazy=True))
#     available_bus = db.relationship('AvailableBuses', backref=db.backref('bookings', lazy=True))

#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.booking_number = self.generate_unique_booking_number()  # Generate unique booking number on creation

#     @staticmethod
#     def generate_unique_booking_number():
#         """Generate a unique 8-digit booking number."""
#         while True:
#             booking_number = ''.join(random.choices(string.digits, k=8))
#             if not Booking.query.filter_by(booking_number=booking_number).first():
#                 return booking_number  # Return if it's unique

#     def __repr__(self):
#         return (f'<Booking booking_id={self.booking_id}, user_id={self.user_id}, '
#                 f'available_bus_id={self.available_bus_id}, booking_date={self.booking_date}, '
#                 f'seat_no={self.seat_no}, total_fare={self.total_fare}, '
#                 f'status={self.status}, booking_number={self.booking_number}, '
#                 f'created_at={self.created_at}, updated_at={self.updated_at}>')
