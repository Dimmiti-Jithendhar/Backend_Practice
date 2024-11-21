from flask_restx import Resource
from flask import request
from app.main_app.models.available_buses import AvailableBuses  # Adjust import as per your structure
from app.main_app.models.bus import Bus  # Adjust import as per your structure
from app.main_app.models.routes import Route  # Adjust import as per your structure
from app.main_app.models.places import Place
from app.main_app.models.bus_type import BusType
from app.main_app.models.operators import Operator
from app.main_app.models.bus_operators import BusOperator
from app.main_app.models.bus_features import BusFeature
from app.main_app.models.bus_type import BusType
from app.main_app.models.features import Feature

from app.main_app.models.users import User
from app.main_app.models.booking import Booking  # Ensure Booking is imported
from app.main_app import db, socketio
from app.main_app.models.notifications import Notification
from app.main_app.dto.available_buses import availablebusesdto  # Adjust the DTO import as necessary
from sqlalchemy import not_

from datetime import datetime, timedelta
from flask import request, jsonify
from datetime import datetime, timedelta

# API blueprints
fetch_available_buses_blueprint = availablebusesdto.fetch_available_buses_api
fetch_available_bus_blueprint = availablebusesdto.fetch_available_bus_api
fetch_available_seats_blueprint = availablebusesdto.fetch_available_seats_api

fetch_available_buses_by_users_blueprint = availablebusesdto.fetch_available_buses_by_users_api
add_available_bus_blueprint = availablebusesdto.add_available_bus_api
update_available_bus_blueprint = availablebusesdto.update_available_bus_api
delete_available_bus_blueprint = availablebusesdto.delete_available_bus_api

book_ticket_blueprint = availablebusesdto.book_ticket_api
cancel_ticket_blueprint = availablebusesdto.cancel_ticket_api
history_blueprint = availablebusesdto.history_api
admin_pl_blueprint = availablebusesdto.admin_pl_api
booking_history_blueprint = availablebusesdto.booking_history_api
default_revenue_blueprint = availablebusesdto.default_revenue_api
custom_revenue_blueprint = availablebusesdto.custom_revenue_api
routes_revenue_blueprint = availablebusesdto.routes_revenue_api
notifications_blueprint = availablebusesdto.notifications_api


# Fetch all available buses
# Fetch all available buses


# Helper functions
def get_place_by_id(place_id):
    """Fetch a place by its ID."""
    return Place.query.get(place_id)

def get_place_by_name(place_name):
    """Fetch a place by its name."""
    return Place.query.filter_by(name=place_name).first()

def get_bus_by_id(bus_id):
    """Fetch a bus by its ID."""
    return Bus.query.get(bus_id)

def get_bus_by_number(bus_no):
    """Fetch a bus by its number."""
    return Bus.query.filter_by(bus_no=bus_no).first()

def get_route_by_ids(source_id, destination_id):
    """Fetch a route by source and destination place IDs."""
    return Route.query.filter_by(source=source_id, destination=destination_id).first()

def get_operator_by_bus_id(bus_id):
    """Fetch an operator by bus ID."""
    bus_operator = db.session.query(BusOperator).filter_by(bus_id=bus_id).first()
    if bus_operator:
        return Operator.query.get(bus_operator.operator_id)
    return None



#fetch all the available buses 
@fetch_available_buses_blueprint.route('', methods=['GET'])
class FetchAvailableBuses(Resource):
    def get(self):
        current_datetime = datetime.now()
        available_buses = AvailableBuses.query.filter(
            (AvailableBuses.deleted.is_(None)) | (AvailableBuses.deleted != True)
                ).all()
        if not available_buses:
            return {'message': 'No available buses found.'}, 404

        available_buses_data = []
        for available_bus in available_buses:
            bus = get_bus_by_id(available_bus.bus_id)
            route = get_route_by_ids(available_bus.route_id, available_bus.route_id)  # Reuse the helper
            operator = get_operator_by_bus_id(bus.bus_id) if bus else None

            # Fetch the operator from the bus_operator junction table
            # bus_operator = db.session.query(BusOperator).filter_by(bus_id=bus.bus_id).first()  # Assuming you have a BusOperator model
            # operator = None
            # if bus_operator:
            #     operator = Operator.query.get(bus_operator.operator_id)
            
            # Fetch the place names using the source and destination IDs
            source_place = get_place_by_id(route.source) if route else None
            destination_place = get_place_by_id(route.destination) if route else None 

            available_buses_data.append({
                'available_buses_id': available_bus.available_buses_id,
                'bus_id': bus.bus_id,
                'bus_no': bus.bus_no,
                'route_from': source_place.name if source_place else 'Unknown',  # Fetch the place name or default to 'Unknown'
                'route_to': destination_place.name if destination_place else 'Unknown',  # Fetch the place name or default to 'Unknown'
                'date': available_bus.date.isoformat(),  # Convert date to string
                'time': available_bus.time.isoformat(),  # Convert time to string
                'seats': bus.seats,
                'available_seats': len(available_bus.available_seats),  # Fetch available seats
                'operator_name': operator.operator_name if operator else 'No operator available',  # Operator name or default message
                'operator_rating': operator.operator_rating if operator else 'No rating available', # Fetch operator rating
                'fare': available_bus.fare 

            })

        return {
            'message': 'Available buses fetched successfully.',
            'available_buses': available_buses_data
        }, 200

@fetch_available_bus_blueprint.route('', methods=['GET'])
class FilterAvailableBuses(Resource):
    def get(self):
        # Get query parameters, defaulting to None if not provided
        bus_number = request.args.get('bus_number')
        date = request.args.get('date')
        from_location = request.args.get('from_route')
        to_location = request.args.get('to_route')

        # Start with the base query
        query = AvailableBuses.query.filter(
            (AvailableBuses.deleted.is_(None)) | (AvailableBuses.deleted != True)
        )

        # Apply filters conditionally if they are provided in the query params
        if date:
            query = query.filter(AvailableBuses.date == date)
        if bus_number:
            query = query.join(Bus).filter(Bus.bus_no == bus_number)
        
        # If from_location is provided, look up the place ID
        if from_location and to_location:
            source_place = get_place_by_name(from_location)
            destination_place = get_place_by_name(to_location)
            if not source_place or not destination_place:
                return {'message': 'One or both locations not found in the database.'}, 404
            route = get_route_by_ids(source_place.place_id, destination_place.place_id)
            if not route:
                return {'message': 'No route found between the specified locations.'}, 404

            # Start with the base query for available buses on the found route
            query = AvailableBuses.query.filter(
                AvailableBuses.route_id == route.route_id,
                (AvailableBuses.deleted.is_(None)) | (AvailableBuses.deleted != True)
            )
            
        # Execute the query
        available_buses = query.all()

        if not available_buses:
            return {'message': 'No available buses found with the specified filters.'}, 404

        # Process the results as in the original endpoint
        available_buses_data = []
        for available_bus in available_buses:
            bus = get_bus_by_id(available_bus.bus_id)
            route = get_route_by_ids(available_bus.route_id, available_bus.route_id) if bus else None
            operator = get_operator_by_bus_id(bus.bus_id) if bus else None

            # Fetch the place names using the source and destination IDs
            source_place = get_place_by_id(route.source) if route else None
            destination_place = get_place_by_id(route.destination) if route else None

            available_buses_data.append({
                'available_buses_id': available_bus.available_buses_id,
                'bus_id': bus.bus_id,
                'bus_no': bus.bus_no,
                'route_from': source_place.name if source_place else 'Unknown',
                'route_to': destination_place.name if destination_place else 'Unknown',
                'date': available_bus.date.isoformat(),
                'time': available_bus.time.isoformat(),
                'seats': bus.seats,
                'available_seats': len(available_bus.available_seats),
                'operator_name': operator.operator_name if operator else 'No operator available',
                'operator_rating': operator.operator_rating if operator else 'No rating available',
                'fare': available_bus.fare
            })

        return {
            'message': 'Filtered buses successfully.',
            'available_buses': available_buses_data
        }, 200


#fetch particular bus
@fetch_available_seats_blueprint.route('/<int:bus_id>/<string:date>/<string:bus_no>/', methods=['GET'])  # Fetch data for a specific bus and date
class FetchAvailableSeats(Resource):
    def get(self, bus_id, date,bus_no):
        # Fetch the bus based on the bus_id
        bus = get_bus_by_id(bus_id)
        if not bus:
            return {'message': 'Bus not found.'}, 404

        # Fetch the available bus based on both bus_id and date
        available_bus = AvailableBuses.query.filter_by(bus_id=bus_id, date=date,bus_number=bus_no).first()
        if not available_bus:
            return {'message': 'No available seats found for this bus on the specified date.'}, 404

        # Assuming available_seats is an array of seat numbers
        return {
            'totalSeats': bus.seats,
            'availableSeats': available_bus.available_seats  # Return available seat numbers for the specific bus and date
        }, 200




# Add a new available bus
@add_available_bus_blueprint.route('', methods=['POST'])
class AddAvailableBus(Resource):
    def post(self):
        data = request.get_json()
        print(data)

        # Check for required fields
        if 'bus_number' not in data or 'from' not in data or 'to' not in data or 'date' not in data or 'time' not in data or 'fare' not in data:
            return {'message': 'Missing required fields: bus_number, from, to, date, time, or fare'}, 400

        # Fetch the bus ID using bus_number
        bus = Bus.query.filter_by(bus_no=data['bus_number']).first()
        if not bus:
            return {'message': 'Bus number not found'}, 404

        # Fetch the route ID using the "from" and "to" places
        source_place = Place.query.filter_by(name=data['from']).first()
        destination_place = Place.query.filter_by(name=data['to']).first()
        if not source_place or not destination_place:
            return {'message': 'Invalid source or destination place name'}, 400

        route = Route.query.filter_by(source=source_place.place_id, destination=destination_place.place_id).first()
        if not route:
            return {'message': 'Route not found for the specified source and destination'}, 404
        # Check if the bus is already available for the same bus_number and date (any route)
        existing_bus = AvailableBuses.query.filter_by(
            bus_number=data['bus_number'],  # Check against bus_number
            date=data['date'],  # Only check for the same date
            deleted=True
        ).first()
        if existing_bus:
            return {'message': 'This bus number is already assigned to another route on the specified date. Please add another bus number.'}, 400

        # Check if the bus is already available for the same route and date
        existing_bus = AvailableBuses.query.filter_by(
            bus_number=data['bus_number'],  # Check against bus_number
            route_id=route.route_id,
            date=data['date']
        ).first()
        if existing_bus:
            return {'message': 'This bus number is already available for the specified route and date.'}, 400

        # Create the list of available seats
        available_seats = list(range(1, bus.seats + 1))

        # Create a new AvailableBuses record
        new_available_bus = AvailableBuses(
            bus_id=bus.bus_id,
            route_id=route.route_id,
            date=data['date'],
            time=data['time'],
            fare=data['fare'],
            available_seats=available_seats,
            bus_number=data['bus_number']  # Set the bus_number from the input data
        )
        
        db.session.add(new_available_bus)
        db.session.commit()

        return {'message': 'Available bus added successfully', 'available_buses_id': new_available_bus.available_buses_id}, 201

# Update an available bus
@update_available_bus_blueprint.route('/<int:available_buses_id>', methods=['PUT'])
class UpdateAvailableBus(Resource):
    def put(self, available_buses_id):
        data = request.get_json()
        
        # Fetch the available bus entry by ID
        available_bus = AvailableBuses.query.get(available_buses_id)
        if not available_bus:
            return {'message': 'Available bus not found'}, 404

        # Update bus ID using bus_number if provided
        if 'bus_number' in data:
            bus = Bus.query.filter_by(bus_no=data['bus_number']).first()
            if not bus:
                return {'message': 'Bus not found with the specified bus number'}, 404
            available_bus.bus_id = bus.bus_id
            available_bus.bus_number = data['bus_number']

        # Update route ID using from and to places if provided
        if 'from' in data and 'to' in data:
            source_place = Place.query.filter_by(name=data['from']).first()
            destination_place = Place.query.filter_by(name=data['to']).first()
            if not source_place or not destination_place:
                return {'message': 'Invalid source or destination place name'}, 400

            route = Route.query.filter_by(source=source_place.place_id, destination=destination_place.place_id).first()
            if not route:
                return {'message': 'Route not found for the specified source and destination'}, 404
            available_bus.route_id = route.route_id

        # Update other fields if provided in the data
        if 'date' in data:
            available_bus.date = data['date']  # Ensure date format is correct

        if 'time' in data:
            available_bus.time = data['time']  # Ensure time format is correct

        if 'fare' in data:
            available_bus.fare = data['fare']  # Update fare
        db.session.commit()
        return {'message': 'Available bus updated successfully'}, 200

# Delete an available bus
@delete_available_bus_blueprint.route('/<int:available_buses_id>', methods=['DELETE'])
class DeleteAvailableBus(Resource):
    def delete(self, available_buses_id):
        # Fetch the available bus to be "deleted"
        available_bus = AvailableBuses.query.get(available_buses_id)
        if not available_bus:
            return {'message': 'Available bus not found'}, 404

        route = Route.query.filter_by(route_id=available_bus.route_id).first()
        print(route)
        if not route:
            return {'message': 'Route information not found for the specified bus.'}, 404
        # Fetch place names for origin and destination
        origin_place = Place.query.filter_by(place_id=route.source).first()
        destination_place = Place.query.filter_by(place_id=route.destination).first()
        print(origin_place,destination_place)

        if not origin_place or not destination_place:
            return {'message': 'Invalid origin or destination place.'}, 404

        origin_name = origin_place.name
        destination_name = destination_place.name

        # Fetch bookings related to this bus and its specific date
        bookings = Booking.query.filter_by(available_bus_id=available_buses_id, booking_date=available_bus.date).all()
        
        # Cancel each booking associated with this bus and add a notification for each canceled ticket
        for booking in bookings:
            booking.status = 'canceled'

            # Create a notification message for each booking
            notification_message = (
                f"Your ticket from {origin_name} to {destination_name} is canceled due to service maintenance. seats {booking.seat_no} "
                "Sorry for the inconvenience caused. Refund will be initiated shortly."
            )

            # Add the notification to the Notification table
            new_notification = Notification(
                user_id=booking.user_id,
                message=notification_message,
                type='admin-cancellation',
                status='unread'
            )
            db.session.add(new_notification)
        
        # Commit the cancellations and notifications
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error canceling tickets: {str(e)}'}, 500

        # Instead of deleting, set the bus's "deleted" flag to True
        available_bus.deleted = True
        
        # Commit the soft delete
        try:
            db.session.commit()
            return {'message': 'Available bus deleted successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error marking bus as deleted: {str(e)}'}, 500


from flask import request, jsonify
from datetime import datetime, timedelta
@fetch_available_buses_by_users_blueprint.route('', methods=['POST'])
class FetchAvailableBusesByUsers(Resource):
    def post(self):
        data = request.get_json()
        from_location = data.get('from')
        to_location = data.get('to')
        date_str = data.get('date')

        # Optional filters
        fare_min = data.get('fare_min')
        fare_max = data.get('fare_max')
        min_rating = data.get('min_rating')
        bus_type_filter = data.get('bus_type')  # e.g., "sleeper", "semi-sleeper", "seater", "luxury"
        amenities_filter = data.get('amenities')  # e.g., ["wifi", "AC", "Charging"]
        print(amenities_filter)
        if not from_location or not to_location or not date_str:
            return {'message': 'Missing required parameters: from, to, or date'}, 400

        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return {'message': 'Invalid date format. Expected format: YYYY-MM-DD'}, 400

        source_place = Place.query.filter_by(name=from_location).first()
        destination_place = Place.query.filter_by(name=to_location).first()

        if not source_place or not destination_place:
            return {'message': 'Source or destination place not found.'}, 404

        matching_routes = Route.query.filter_by(source=source_place.place_id, destination=destination_place.place_id).all()
        available_buses_data = []

        for route in matching_routes:
            available_buses = AvailableBuses.query.filter_by(route_id=route.route_id, date=date, deleted=False).all()
            for available_bus in available_buses:
                bus = Bus.query.get(available_bus.bus_id)
                if not bus:
                    continue

                # Apply bus type filter if provided
                bus_type = BusType.query.get(bus.bus_type_id)
                if not bus_type or (bus_type_filter and bus_type.bus_type_name.lower() != bus_type_filter.lower()):
                    continue

                # Apply operator rating filter if provided
                bus_operator = BusOperator.query.filter_by(bus_id=bus.bus_id).first()
                operator = Operator.query.get(bus_operator.operator_id) if bus_operator else None
                if min_rating and (not operator or operator.operator_rating < float(min_rating)):
                    continue

                # Apply fare range filter if provided
                if fare_min and available_bus.fare < float(fare_min):
                    continue
                if fare_max and available_bus.fare > float(fare_max):
                    continue

                # Fetch amenities for the bus type
                amenities = [
                    feature.feature_name 
                    for feature in Feature.query.join(BusFeature, Feature.feature_id == BusFeature.feature_id)
                    .filter(BusFeature.bus_type_id == bus_type.bus_type_id)
                    .all()
                ]

                # Apply amenities filter if provided
                if amenities_filter and not all(amenity.lower() in [a.lower() for a in amenities] for amenity in amenities_filter):
                    continue

                # Calculate arrival time based on duration
                starting_time = datetime.combine(available_bus.date, available_bus.time)
                duration_in_minutes = route.duration
                destination_time = starting_time + timedelta(minutes=duration_in_minutes)

                hours = duration_in_minutes // 60
                minutes = duration_in_minutes % 60

                available_buses_data.append({
                    'bus_type': bus_type.bus_type_name,
                    'bus_no': bus.bus_no,
                    'route_from': source_place.name,
                    'time': available_bus.time.isoformat(),
                    'duration': f"{hours}h {minutes}m",
                    'route_to': destination_place.name,
                    'destination_time': destination_time.time().isoformat(),
                    'fare': available_bus.fare,
                    'available_seats': len(available_bus.available_seats),
                    'distance': route.distance,
                    'rating': operator.operator_rating if operator else '3.5',
                    'operator_name': operator.operator_name if operator else 'Unknown',
                    'amenities': amenities,  # Assuming amenities are stored in the bus table
                })

        if not available_buses_data:
            return {'message': 'No available buses found for the specified date and route.'}, 404

        return ({
            'message': 'Available buses fetched successfully.',
            'available_buses': available_buses_data
        }), 200

@book_ticket_blueprint.route('', methods=['POST'])
class BookTicket(Resource):
    def post(self):
        data = request.get_json()

        bus_id = data.get('bus_id')
        user_id = data.get('user_id')  # Capture the user ID
        passenger_details = data.get('passenger_details')  # This should contain a list of dictionaries
        booking_date = data.get('date')  # The date for booking
        # bus_number = data.get('bus_number')

        # Validate input data
        if not bus_id or not user_id or not passenger_details or not booking_date:
            return {'message': 'Bus ID, User ID, passenger details, and booking date are required.'}, 400

        if not isinstance(passenger_details, list) or not passenger_details:
            return {'message': 'Passenger details must be a non-empty list.'}, 400

        # Validate each passenger's details (seat number, name, age, and gender)
        for passenger in passenger_details:
            if not all(key in passenger for key in ('seat_number', 'name', 'age', 'gender')):
                return {'message': 'Each passenger must have seat_number, name, age, and gender.'}, 400

        # Fetch the available bus on the selected date
        available_bus = AvailableBuses.query.filter_by(bus_id=bus_id, date=booking_date).first()
        if not available_bus:
            return {'message': 'Bus not found for the specified date.'}, 404
        # Fetch route information for the bus
        route = Route.query.filter_by(route_id=available_bus.route_id).first()
        print(route)
        if not route:
            return {'message': 'Route information not found for the specified bus.'}, 404
        # Fetch place names for origin and destination
        origin_place = Place.query.filter_by(place_id=route.source).first()
        destination_place = Place.query.filter_by(place_id=route.destination).first()
        print(origin_place,destination_place)

        if not origin_place or not destination_place:
            return {'message': 'Invalid origin or destination place.'}, 404

        origin_name = origin_place.name
        destination_name = destination_place.name

        # Extract all seat numbers from the passenger details
        selected_seats = [str(passenger['seat_number']) for passenger in passenger_details]  # Normalize to string

        # Normalize available seats to strings for comparison
        current_available_seats = [str(seat) for seat in available_bus.available_seats]

        # Check if the selected seats are available on this bus for this date
        if not all(seat in current_available_seats for seat in selected_seats):
            unavailable_seats = [seat for seat in selected_seats if seat not in current_available_seats]
            return {'message': 'One or more selected seats are not available.', 'unavailable_seats': unavailable_seats}, 400

        # Remove selected seats from available seats for this bus on the given date
        updated_seats = [seat for seat in current_available_seats if seat not in selected_seats]

        # Update the available seats in the database
        available_bus.available_seats = updated_seats

        try:
            # Calculate total fare
            fare_per_ticket = available_bus.fare  # Assuming fare is per ticket
            total_fare = fare_per_ticket * len(passenger_details)  # Multiply fare by number of passengers

            # Collect all seat numbers in an array
            seat_numbers = [passenger['seat_number'] for passenger in passenger_details]

            # Create a single booking entry with all seat numbers
            new_booking = Booking(
                user_id=user_id,
                available_bus_id=available_bus.available_buses_id,
                booking_date=booking_date,
                seat_no=seat_numbers,  # Store all seat numbers as an array
                total_fare=total_fare,  # Total fare for all passengers
                status='confirmed'  # Default status
            )
            db.session.add(new_booking)

            # Commit both the seat update and the new booking in one transaction
            # db.session.commit()

            # Send a notification after successful booking
            notification_message = f"Ticket booked successfully from {origin_name} to {destination_name} on {booking_date}"
            new_notification = Notification(
                user_id=user_id,
                message=notification_message,
                type='booking',
                status='unread'
            )
            db.session.add(new_notification)
            db.session.commit()

            # Emit the notification using SocketIO
            socketio.emit('notification', {
                'user_id': user_id,
                'message': notification_message
            }, room=f"user_{user_id}")

            return {'message': 'Ticket(s) booked successfully.', 'seats_booked': seat_numbers, 'total_fare': total_fare}, 201

        except Exception as e:
            # Rollback in case of error
            db.session.rollback()
            return {'message': f'Error processing the booking: {str(e)}'}, 500
# @book_ticket_blueprint.route('', methods=['POST'])
# class BookTicket(Resource):
#     def post(self):
#         data = request.get_json()

#         bus_id = data.get('bus_id')
#         user_id = data.get('user_id')  # Capture the user ID
#         passenger_details = data.get('passenger_details')  # This should contain a list of dictionaries
#         booking_date = data.get('date')  # The date for booking

#         # Validate input data
#         if not bus_id or not user_id or not passenger_details or not booking_date:
#             return {'message': 'Bus ID, User ID, passenger details, and booking date are required.'}, 400

#         if not isinstance(passenger_details, list) or not passenger_details:
#             return {'message': 'Passenger details must be a non-empty list.'}, 400

#         # Validate each passenger's details (seat number, name, age, and gender)
#         for passenger in passenger_details:
#             if not all(key in passenger for key in ('seat_number', 'name', 'age', 'gender')):
#                 return {'message': 'Each passenger must have seat_number, name, age, and gender.'}, 400

#         # Fetch the available bus on the selected date
#         available_bus = AvailableBuses.query.filter_by(bus_id=bus_id, date=booking_date).first()
#         if not available_bus:
#             return {'message': 'Bus not found for the specified date.'}, 404

#         # Extract all seat numbers from the passenger details
#         selected_seats = [str(passenger['seat_number']) for passenger in passenger_details]  # Normalize to string

#         # Normalize available seats to strings for comparison
#         current_available_seats = [str(seat) for seat in available_bus.available_seats]

#         # Debugging: Print available seats before booking
#         print(f"Current available seats for bus {bus_id} on {booking_date}: {current_available_seats}")
#         print(f"Selected seats: {selected_seats}")

#         # Check if the selected seats are available on this bus for this date
#         if not all(seat in current_available_seats for seat in selected_seats):
#             unavailable_seats = [seat for seat in selected_seats if seat not in current_available_seats]
#             print(f"Unavailable seats: {unavailable_seats}")  # Debugging: Print unavailable seats
#             return {'message': 'One or more selected seats are not available.', 'unavailable_seats': unavailable_seats}, 400

#         # Remove selected seats from available seats for this bus on the given date
#         updated_seats = [seat for seat in current_available_seats if seat not in selected_seats]

#         # Debugging: Print available seats after booking
#         print(f"Updated available seats after booking for bus {bus_id} on {booking_date}: {updated_seats}")

#         # Update the available seats in the database
#         available_bus.available_seats = updated_seats

#         try:
#             # Calculate total fare
#             fare_per_ticket = available_bus.fare  # Assuming fare is per ticket
#             total_fare = fare_per_ticket * len(passenger_details)  # Multiply fare by number of passengers

#             # Collect all seat numbers in an array
#             seat_numbers = [passenger['seat_number'] for passenger in passenger_details]

#             # Create a single booking entry with all seat numbers
#             new_booking = Booking(
#                 user_id=user_id,
#                 available_bus_id=available_bus.available_buses_id,
#                 booking_date=booking_date,
#                 seat_no=seat_numbers,  # Store all seat numbers as an array
#                 total_fare=total_fare,  # Total fare for all passengers
#                 status='confirmed'  # Default status
#             )
#             db.session.add(new_booking)

#             # Commit both the seat update and the new booking in one transaction
#             db.session.commit()

#             return {'message': 'Ticket(s) booked successfully.', 'seats_booked': seat_numbers, 'total_fare': total_fare}, 201

#         except Exception as e:
#             # Rollback in case of error
#             db.session.rollback()
#             print(f"Error: {str(e)}")  # Debugging: Print error message
#             return {'message': f'Error processing the booking: {str(e)}'}, 500


from datetime import datetime, timedelta

# Cancel tickets 
@cancel_ticket_blueprint.route('', methods=['POST'])
class CancelTicket(Resource):
    def post(self):
        data = request.get_json()

        booking_number = data.get('booking_number')
        seats_to_cancel = data.get('seats_to_cancel')  # List of seat numbers to cancel

        # Validate input
        if not booking_number or not seats_to_cancel:
            return {'message': 'Booking number and seats to cancel are required.'}, 400

        if not isinstance(seats_to_cancel, list) or not seats_to_cancel:
            return {'message': 'Seats to cancel must be a non-empty list.'}, 400

        # Step 1: Find the booking
        booking = Booking.query.filter_by(booking_number=booking_number).first()

        if not booking:
            return {'message': 'Enter a valid Booking Number.'}, 404

        if booking.status == 'canceled':
            return {'message': 'This booking has already been canceled.'}, 400

        # Step 2: Fetch the available bus details for this booking
        available_bus = AvailableBuses.query.filter_by(
            available_buses_id=booking.available_bus_id
        ).first()

        if not available_bus:
            return {'message': 'Bus availability not found.'}, 404

        bus_departure_datetime = datetime.combine(available_bus.date, available_bus.time)
        current_datetime = datetime.now()
        time_difference = bus_departure_datetime - current_datetime

        route = Route.query.filter_by(route_id=available_bus.route_id).first()
        print(route)
        if not route:
            return {'message': 'Route information not found for the specified bus.'}, 404
        # Fetch place names for origin and destination
        origin_place = Place.query.filter_by(place_id=route.source).first()
        destination_place = Place.query.filter_by(place_id=route.destination).first()
        print(origin_place,destination_place)

        if not origin_place or not destination_place:
            return {'message': 'Invalid origin or destination place.'}, 404

        origin_name = origin_place.name
        destination_name = destination_place.name

        if time_difference <= timedelta(hours=2):
            return {'message': 'Cancellation is not possible now. Please cancel at least 2 hours before the departure.'}, 400

        # Step 4: Verify that seats to cancel are part of the original booking
        current_booked_seats = list(booking.seat_no)

        if not all(seat in current_booked_seats for seat in seats_to_cancel):
            invalid_seats = [seat for seat in seats_to_cancel if seat not in current_booked_seats]
            return {'message': f'Please check the seat numbers: {invalid_seats}'}, 400

        try:
            # Calculate seats remaining after cancellation
            remaining_seats = [seat for seat in current_booked_seats if seat not in seats_to_cancel]

            # Update booking status
            if not remaining_seats:
                booking.status = 'canceled'
            else:
                booking.seat_no = remaining_seats
                booking.status = 'confirmed'

            # Add canceled seats back to available seats
            current_available_seats = set(available_bus.available_seats)
            updated_available_seats = list(current_available_seats.union(seats_to_cancel))
            available_bus.available_seats = sorted(updated_available_seats)

            # Adjust fare
            fare_per_ticket = available_bus.fare
            booking.total_fare = fare_per_ticket * len(remaining_seats)

            # Commit the changes to the database
            db.session.commit()

            # Step 6: Create notification entry for the cancellation
            
            notification_message = (
                f"Ticket canceled successfully. Seat number(s) {seats_to_cancel} "
                f"from {origin_name} to {destination_name} on {available_bus.date}."
            )

            new_notification = Notification(
                user_id=booking.user_id,
                message=notification_message,
                type='cancellation',
                status='unread'
            )
            db.session.add(new_notification)
            db.session.commit()  # Commit notification

            return {
                'message': 'Ticket(s) canceled successfully.',
                'canceled_seats': seats_to_cancel,
                'remaining_seats': remaining_seats
            }, 200

        except Exception as e:
            db.session.rollback()
            print(f"Error: {str(e)}")
            return {'message': f'Error canceling the ticket: {str(e)}'}, 500





from datetime import datetime, timedelta
from pytz import timezone

@history_blueprint.route('', methods=['GET'])
class BookingHistory(Resource):
    def get(self):
        user_id = request.args.get('user_id')  # Get user_id from the query parameter

        # Fetch all bookings for this user from the Booking table
        bookings = Booking.query.filter_by(user_id=user_id).all()

        if not bookings:
            return {'message': 'No bookings found for this user.'}, 404

        booking_history = []

        for booking in bookings:
            available_bus_id = booking.available_bus_id
            booking_date = booking.booking_date

            # Fetch available bus details using available_bus_id
            available_bus = AvailableBuses.query.filter_by(available_buses_id=available_bus_id).first()

            if not available_bus:
                continue  # Skip this booking if bus details are not found

            # Extract route_id, fare, and time (starting time)
            route_id = available_bus.route_id
            fare = booking.total_fare  # Assuming total fare is stored in the booking
            departure_time = available_bus.time  # The bus starting time
            booking_date = available_bus.date

            # Fetch route details from Route table using route_id
            route = Route.query.filter_by(route_id=route_id).first()

            if not route:
                continue  # Skip if route not found

            from_place_id= route.source
            to_place_id = route.destination
            duration_in_minutes = route.duration  # Duration in minutes
            distance = route.distance

            # Fetch place names from Places table
            from_place = Place.query.filter_by(place_id=from_place_id).first()
            to_place = Place.query.filter_by(place_id=to_place_id).first()
            #upto here we were get the place ids from the route table 
            # so with that place id we are going to get place name it is in places table we are having only place id and name only here 

            from_place_name = from_place.name if from_place else "Unknown"
            to_place_name = to_place.name if to_place else "Unknown"

            # Calculate arrival time using departure time + duration
            starting_time = datetime.combine(booking_date, departure_time)
            destination_time = starting_time + timedelta(minutes=duration_in_minutes)

            # No need to format, just use the raw values
            departure_time_raw = departure_time.strftime('%H:%M:%S')  # Departure time already in 24-hour format
            arrival_time_raw = destination_time.strftime('%H:%M:%S')  # Arrival time in 24-hour format

            # Calculate number of persons
            bus = Bus.query.get(available_bus.bus_id)
            no_of_persons = len(booking.seat_no)
            bus_operator = BusOperator.query.filter_by(bus_id=bus.bus_id).first()
            operator = Operator.query.get(bus_operator.operator_id) if bus_operator else None
            # if min_rating and (not operator or operator.operator_rating < float(min_rating)):
            #         continue

            # Prepare the booking history entry
            booking_entry = {
                'uid': booking.user_id,
                'Ticket_id': booking.booking_number,
                'from': from_place_id,
                'to': to_place_id,
                'fare': fare,
                'no_of_persons': no_of_persons,
                'doj': booking_date.strftime('%Y-%m-%d'),  # Date of journey
                'distance': distance,
                'arrival_time': arrival_time_raw,
                'departure_time': departure_time_raw,
                'operator_name':operator.operator_name,
                'operator_phn_no':operator.operator_phn_no
            }

            booking_history.append(booking_entry)

        return {'booking_history': booking_history}, 200




#######################################################################
@admin_pl_blueprint.route('', methods=['GET'])
class AdminBusUsersDetails(Resource):
    def get(self):
        # Get bus_number and date from query parameters
        bus_no = request.args.get('bus_number')
        journey_date = request.args.get('date')
        # print(bus_no,journey_date)
        # Validate inputs
        if not bus_no or not journey_date:
            return {'message': 'Bus number and date are required.'}, 400

        # Parse the date to a Python date object
        try:
            journey_date = datetime.strptime(journey_date, '%d-%m-%Y').date()
        except ValueError:
            return {'message': 'Invalid date format. Use DD-MM-YYYY.'}, 400
        # print(journey_date)
        # Fetch the bus_id from the Buses table based on the bus_number
        bus = Bus.query.filter_by(bus_no=bus_no).first()

        if not bus:
            
            return {'message': 'Bus not found with the given bus number.'}, 404

        bus_id = bus.bus_id

        # Fetch the available bus entry from AvailableBuses using bus_id and journey_date
        available_bus = AvailableBuses.query.filter_by(bus_id=bus_id, date=journey_date).first()
        print(available_bus)
        if not available_bus:
            return {'message': 'No bus found for the given bus number and date.'}, 404

        available_bus_id = available_bus.available_buses_id
        total_seats = available_bus.available_seats  # Assuming there is a total_seats field
        print(available_bus_id,total_seats)
        # Fetch all bookings for this bus on the specified date
        bookings = Booking.query.filter_by(available_bus_id=available_bus_id).all()

        if not bookings:
            return {'message': 'No bookings found for this bus on the given date.'}, 404

        # Prepare the user booking details list
        user_bookings = []
        booked_seats = 0

        for booking in bookings:
            user_id = booking.user_id
            seats_booked = len(booking.seat_no)  # Assuming seat_no is a list of booked seats
            fare = booking.total_fare

            # Fetch user details from the User table
            user = User.query.filter_by(id=user_id).first()
            user_name = user.first_name if user else "Unknown"  # Assuming 'name' exists in the User table

            # Add the total number of booked seats
            booked_seats += seats_booked

            # Prepare user booking entry
            booking_entry = {
                'uname': user_name,
                'seats_booked': booking.seat_no,  # List of booked seats
                'fare': fare,
            }

            user_bookings.append(booking_entry)

        # Calculate the remaining available seats
        available_seats = len(available_bus.available_seats)

        # Return the response
        return {
            'bus_number': bus_no,
            'date': journey_date.strftime('%Y-%m-%d'),
            'available_seats': available_seats,
            'bookings': user_bookings
            
        }, 200



###################################################
#booking history -- past and upcoming 

@booking_history_blueprint.route('', methods=['GET'])
class BookingHistory(Resource):
    def get(self):
        user_id = request.args.get('user_id')

        if not user_id:
            return {'message': 'User ID is required.'}, 400

        # 2. Get today's date 
        today = datetime.today().date()

        # 3. Fetch bookings for the user
        bookings = Booking.query.filter_by(user_id=user_id).all()

        if not bookings:
            return {'message': 'No Bookings Found'}, 404

        upcoming_bookings = []  # Consistent naming
        past_bookings = []      # Consistent naming

        # 4. Loop through bookings and filter based on the date 
        for booking in bookings:
            journey_date = booking.booking_date
            
            # 5. Fetch details from the available bus
            available_bus = AvailableBuses.query.filter_by(available_buses_id=booking.available_bus_id).first()
            if not available_bus:
                continue  # Skip if no available bus is found

            # 6. Fetch the bus and route details
            bus = Bus.query.filter_by(bus_id=available_bus.bus_id).first()
            route = Route.query.filter_by(route_id=available_bus.route_id).first()

            if not bus or not route:
                continue  # Skip if bus or route is not found
            bus = Bus.query.get(available_bus.bus_id)
        
            bus_operator = BusOperator.query.filter_by(bus_id=bus.bus_id).first()
            operator = Operator.query.get(bus_operator.operator_id) if bus_operator else None
            # 7. Fetch place details using place_id from the Route table
            from_place_id= route.source
            to_place_id = route.destination
            from_place = Place.query.filter_by(place_id=from_place_id).first()  # Assuming 'from_place_id'
            to_place = Place.query.filter_by(place_id=to_place_id).first()      # Assuming 'to_place_id'
            from_place_name = from_place.name if from_place else "Unknown"
            to_place_name = to_place.name if to_place else "Unknown"

            # If place information is not found, continue with the next iteration
            if not from_place or not to_place:
                continue

            # Prepare booking details
            booking_details = {
                'booking_number': booking.booking_number,
                'bus_number': bus.bus_no,
                'fare': booking.total_fare,
                'seats': booking.seat_no,
                'date_of_journey': str(booking.booking_date),
                'from': from_place_name,
                'to': to_place_name,
                'Starting_time' : str(available_bus.time),
                'status' : booking.status,
                'operator_name':operator.operator_name,
                'operator_phn_no':operator.operator_phn_no
            }

            # 9. Categorize bookings as upcoming or past
            if journey_date >= today:
                upcoming_bookings.append(booking_details)
            else:
                past_bookings.append(booking_details)

        # 10. Debug logging
        

        # 11. Return the results
        return {
            'upcoming_bookings': upcoming_bookings,
            'past_bookings': past_bookings
        }, 200

######################### REVENUE #########################
# Get default revenue data
@default_revenue_blueprint.route('', methods=['GET'])
class DefaultRevenue(Resource):
    def get(self):
        # Define start and end dates for this year
        this_year_start = datetime(datetime.now().year, 1, 1)
        this_year_end = datetime(datetime.now().year + 1, 1, 1)

        # Calculate revenue for this year based on date range and status
        this_year_revenue = Booking.query.filter(
            Booking.booking_date >= this_year_start,
            Booking.booking_date < this_year_end,
            Booking.status == 'confirmed'
        ).with_entities(db.func.sum(Booking.total_fare)).scalar()

        # Define start and end dates for this month
        this_month_start = datetime(datetime.now().year, datetime.now().month, 1)
        next_month = datetime.now().month + 1 if datetime.now().month < 12 else 1
        next_month_year = datetime.now().year if next_month > 1 else datetime.now().year + 1
        this_month_end = datetime(next_month_year, next_month, 1)

        # Calculate revenue for this month based on date range and status
        this_month_revenue = Booking.query.filter(
            Booking.booking_date >= this_month_start,
            Booking.booking_date < this_month_end,
            Booking.status == 'confirmed'
        ).with_entities(db.func.sum(Booking.total_fare)).scalar()

        # Calculate overall revenue for confirmed bookings only
        overall_revenue = Booking.query.filter(
            Booking.status == 'confirmed'
        ).with_entities(db.func.sum(Booking.total_fare)).scalar()

        return {
            'this_year_revenue': this_year_revenue or 0,
            'this_month_revenue': this_month_revenue or 0,
            'overall_revenue': overall_revenue or 0
        }, 200
# Get revenue data for a custom date range
@custom_revenue_blueprint.route('', methods=['GET'])
class CustomRevenue(Resource):
    def get(self):
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        if not start_date or not end_date:
            return {'message': 'Start date and end date are required.'}, 400

        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        revenue_data = Booking.query.filter(
            Booking.booking_date >= start_date,
            Booking.booking_date <= end_date,
            Booking.status == 'confirmed'
        ).all()

        total_revenue = sum(booking.total_fare for booking in revenue_data)

        return {'total_revenue': total_revenue}, 200

@routes_revenue_blueprint.route('', methods=['GET'])
class PlaceBasedRevenue(Resource):
    def get(self):
        place_name_1 = request.args.get('place_name_1')
        place_name_2 = request.args.get('place_name_2')

        # Validate input
        if not (place_name_1 and place_name_2):
            return {'message': 'Two place names are required.'}, 400

        # 1. Fetch place IDs for the given place names
        place_1 = Place.query.filter_by(name=place_name_1).first()
        place_2 = Place.query.filter_by(name=place_name_2).first()
        print(place_1,place_2)
        if not (place_1 and place_2):
            return {'message': 'One or both of the specified places not found.'}, 404

        # 2. Fetch route IDs where source and destination match the place IDs
        routes = Route.query.filter(
            ((Route.source == place_1.place_id) & (Route.destination == place_2.place_id)) 
            # ((Route.source == place_2.place_id) & (Route.destination == place_1.place_id))
        )
        print(routes)
        if not routes:
            return {'message': 'No routes found between the specified places.'}, 404

        route_ids = [route.route_id for route in routes]
        print(route_ids)


        # 3. Fetch available bus IDs based on the route IDs
        available_buses = AvailableBuses.query.filter(AvailableBuses.route_id.in_(route_ids)).all()
        #print(available_buses)
        if not available_buses:
            return {'message': 'No available buses found for the specified routes.'}, 404

        available_buses_ids = [bus.available_buses_id for bus in available_buses]

        # 4. Calculate total revenue for confirmed bookings related to these available buses
        revenue_data = Booking.query.filter(
            Booking.available_bus_id.in_(available_buses_ids),
            Booking.status == 'confirmed'
        ).all()
        print(revenue_data)
        total_revenue = sum(booking.total_fare for booking in revenue_data)

        return {'total_revenue': total_revenue}, 200



@notifications_blueprint.route('', methods=['GET'])
class Notifications(Resource):
    def get(self):
        # Fetch user ID from query parameters
        user_id = request.args.get('user_id')

        # Check if user_id is provided
        if not user_id:
            return {'message': 'User ID is required.'}, 400

        # Build query to fetch notifications for the specified user
        query = Notification.query.filter_by(user_id=user_id)

        # Fetch notifications from the database, ordered by timestamp descending
        notifications = query.order_by(Notification.timestamp.desc()).all()

        # Format response
        response = [
            {
                'id': notification.id,
                'message': notification.message,
                'timestamp': notification.timestamp.isoformat() if notification.timestamp else None
            } for notification in notifications
        ]

        return jsonify(response)
