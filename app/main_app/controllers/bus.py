from flask_restx import Resource
from flask import request
from app.main_app.models.bus import Bus  # Adjust the import as per your structure
from app.main_app.models.bus_type import BusType
from app.main_app import db
from app.main_app.dto.bus import busdto  # Adjust import to your DTO file

fetch_buses_blueprint = busdto.fetch_buses_api
add_bus_blueprint = busdto.add_bus_api
# update_bus_blueprint = busdto.update_bus_api
delete_bus_blueprint = busdto.delete_bus_api



# Fetching buses
@fetch_buses_blueprint.route('', methods=['GET'])
class FetchBuses(Resource):
    def get(self):
        # Join the Bus and BusType tables to fetch the bus_type_name instead of bus_type_id
        buses = db.session.query(
            Bus.bus_no,
            Bus.seats,
            BusType.bus_type_name
        ).join(BusType, Bus.bus_type_id == BusType.bus_type_id).all()

        if not buses:
            return {'message': 'No buses found', 'buses': []}, 200

        bus_list = [{
            'bus_no': bus.bus_no,
            'bus_type_name': bus.bus_type_name,
            'seats': bus.seats
        } for bus in buses]

        return {'message': 'Buses fetched successfully', 'buses': bus_list}, 200


# Add bus
@add_bus_blueprint.route('', methods=['POST'])
class AddBus(Resource):
    def post(self):
        data = request.get_json()

        if 'bus_no' not in data or 'bus_type_id' not in data or 'seats' not in data:
            return {'message': 'Missing required fields'}, 400

        existing_bus = Bus.query.filter_by(bus_no=data['bus_no']).first()
        if existing_bus:
            return {'message': 'Bus with this bus number already exists'}, 400

        new_bus = Bus(
            bus_no=data['bus_no'],
            bus_type_id=data['bus_type_id'],
            seats=data['seats']
        )

        try:
            db.session.add(new_bus)
            db.session.commit()
            return {'message': 'Bus added successfully'}, 201
        except Exception as e:
            db.session.rollback()
            return {'message': f'Failed to add bus: {str(e)}'}, 500


# Delete bus by bus number
@delete_bus_blueprint.route('/<string:bus_no>', methods=['DELETE'])
class DeleteBusByNumber(Resource):
    def delete(self, bus_no):
        # Fetch the bus by bus_no
        bus = Bus.query.filter_by(bus_no=bus_no).first()
        
        if not bus:
            return {'message': 'Bus not found'}, 404
        
        # Delete the bus
        db.session.delete(bus)
        db.session.commit()

        return {'message': 'Bus deleted successfully'}, 200
