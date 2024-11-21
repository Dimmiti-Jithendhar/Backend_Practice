from flask_restx import Resource
from flask import request
from app.main_app.models.bus_operators import BusOperator  # Adjust import as per your structure
from app.main_app.models.bus import Bus  # Adjust import as per your structure
from app.main_app.models.operators import Operator  # Adjust import as per your structure
from app.main_app import db
from app.main_app.dto.bus_operators import busoperatorsdto  # Adjust the DTO import as necessary

# API blueprints
fetch_bus_operators_blueprint = busoperatorsdto.fetch_bus_operators_api
add_bus_operator_blueprint = busoperatorsdto.add_bus_operator_api
update_bus_operator_blueprint = busoperatorsdto.update_bus_operator_api
delete_bus_operator_blueprint = busoperatorsdto.delete_bus_operator_api

# Fetch all bus operators
@fetch_bus_operators_blueprint.route('', methods=['GET'])
class FetchBusOperators(Resource):
    def get(self):
        bus_operators = BusOperator.query.all()
        if not bus_operators:
            return {'message': 'No bus operators found.'}, 404

        bus_operators_data = []
        for bus_operator in bus_operators:
            bus = Bus.query.get(bus_operator.bus_id)
            operator = Operator.query.get(bus_operator.operator_id)
            bus_operators_data.append({
                'bus_operator_id': bus_operator.bus_operator_id,
                'bus_id': bus.bus_id,
                'bus_no': bus.bus_no,
                'operator_id': operator.operator_id,
                'operator_name': operator.operator_name,
                'operator_phn_no': operator.operator_phn_no
            })

        return {
            'message': 'Bus operators fetched successfully.',
            'bus_operators': bus_operators_data
        }, 200

# Add a new bus operator
@add_bus_operator_blueprint.route('', methods=['POST'])
class AddBusOperator(Resource):
    def post(self):
        data = request.get_json()

        if 'bus_id' not in data or 'operator_id' not in data:
            return {'message': 'Missing required fields: bus_id or operator_id'}, 400
         # Check if the BusOperator already exists
        existing_relation = BusOperator.query.filter_by(bus_id=data['bus_id'], operator_id=data['operator_id']).first()
        if existing_relation:
            return {'message': 'This bus already has the specified operator assigned.'}, 409
        # Create a new BusOperator
        bus = Bus.query.get(data['bus_id'])
        operator = Operator.query.get(data['operator_id'])
        if not bus:
            return {'message': 'Bus not found'}, 404
        if not operator:
            return {'message': 'Operator not found'}, 404

        new_bus_operator = BusOperator(bus_id=bus.bus_id, operator_id=operator.operator_id)
        db.session.add(new_bus_operator)
        db.session.commit()

        return {'message': 'Bus operator added successfully', 'bus_operator_id': new_bus_operator.bus_operator_id}, 201

# Update a bus operator
@update_bus_operator_blueprint.route('/<int:bus_operator_id>', methods=['PUT'])
class UpdateBusOperator(Resource):
    def put(self, bus_operator_id):
        data = request.get_json()
        bus_operator = BusOperator.query.get(bus_operator_id)
        if not bus_operator:
            return {'message': 'Bus operator not found'}, 404

        if 'bus_id' in data:
            bus = Bus.query.get(data['bus_id'])
            if not bus:
                return {'message': 'Bus not found'}, 404
            bus_operator.bus_id = bus.bus_id

        if 'operator_id' in data:
            operator = Operator.query.get(data['operator_id'])
            if not operator:
                return {'message': 'Operator not found'}, 404
            bus_operator.operator_id = operator.operator_id

        db.session.commit()
        return {'message': 'Bus operator updated successfully'}, 200

# Delete a bus operator
@delete_bus_operator_blueprint.route('/<int:bus_operator_id>', methods=['DELETE'])
class DeleteBusOperator(Resource):
    def delete(self, bus_operator_id):
        bus_operator = BusOperator.query.get(bus_operator_id)
        if not bus_operator:
            return {'message': 'Bus operator not found'}, 404

        db.session.delete(bus_operator)
        db.session.commit()
        return {'message': 'Bus operator deleted successfully'}, 200
