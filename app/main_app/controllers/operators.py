from flask_restx import Resource
from flask import request
from app.main_app.models.operators import Operator  # Adjust the import as per your structure
from app.main_app import db
from app.main_app.dto.operators import operatorsdto  # Adjust import to your DTO file

fetch_operators_blueprint = operatorsdto.fetch_operators_api
add_operator_blueprint = operatorsdto.add_operator_api
update_operator_blueprint = operatorsdto.update_operator_api
delete_operator_blueprint = operatorsdto.delete_operator_api

# Fetching operators
@fetch_operators_blueprint.route('', methods=['GET'])
class FetchOperators(Resource):
    def get(self):
        operators = Operator.query.all()
        
        if not operators:
            return {'message': 'No operators found', 'operators': []}, 200

        operator_list = [{
            'operator_id': operator.operator_id,
            'operator_name': operator.operator_name,
            'operator_phn_no': operator.operator_phn_no,
            'operator_email': operator.operator_email,
            'operator_rating': operator.operator_rating
        } for operator in operators]

        return {'message': 'Operators fetched successfully', 'operators': operator_list}, 200

# Add operator
@add_operator_blueprint.route('', methods=['POST'])
class AddOperator(Resource):
    def post(self):
        data = request.get_json()

        if 'operator_name' not in data or 'operator_phn_no' not in data or 'operator_email' not in data:
            return {'message': 'Missing required fields'}, 400

        existing_operator = Operator.query.filter_by(operator_phn_no=data['operator_phn_no']).first()
        if existing_operator:
            return {'message': 'Operator with this phone number already exists'}, 400

        new_operator = Operator(
            operator_name=data['operator_name'],
            operator_phn_no=data['operator_phn_no'],
            operator_email=data['operator_email'],
            operator_rating=data.get('operator_rating')  # Optional field
        )
        
        db.session.add(new_operator)
        db.session.commit()
        return {'message': 'Operator added successfully'}, 201


@update_operator_blueprint.route('/<int:operator_id>', methods=['PUT'])
class UpdateOperatorById(Resource):
    def put(self, operator_id):
        operator = Operator.query.get(operator_id)
        if not operator:
            return {'message': 'Operator not found'}, 404

        data = request.get_json()

        if 'operator_name' not in data and 'operator_phn_no' not in data and 'operator_email' not in data:
            return {'message': 'At least one field must be provided for update'}, 400

        # Update operator name if provided
        if 'operator_name' in data:
            operator.operator_name = data['operator_name']

        # Update operator phone number if provided and ensure it's unique
        if 'operator_phn_no' in data:
            new_phone_no = data['operator_phn_no']
            if new_phone_no != operator.operator_phn_no:
                existing_operator = Operator.query.filter_by(operator_phn_no=new_phone_no).first()
                if existing_operator and existing_operator.operator_id != operator.operator_id:
                    return {'message': 'Phone number already in use by another operator'}, 400
                operator.operator_phn_no = new_phone_no

        # Update operator email if provided and ensure it's unique
        if 'operator_email' in data:
            new_email = data['operator_email']
            if new_email != operator.operator_email:
                existing_operator = Operator.query.filter_by(operator_email=new_email).first()
                if existing_operator and existing_operator.operator_id != operator.operator_id:
                    return {'message': 'Email already in use by another operator'}, 400
                operator.operator_email = new_email

        # Update operator rating if provided
        operator.operator_rating = data.get('operator_rating', operator.operator_rating)  # Optional update

        # Commit the changes to the database
        db.session.commit()

        return {'message': 'Operator details updated successfully'}, 200

@delete_operator_blueprint.route('/<int:operator_id>', methods=['DELETE'])
class DeleteOperatorByName(Resource):
    def delete(self, operator_id):
        # Fetch the operator by id
        operator = Operator.query.filter_by(operator_id=operator_id).first()
        if not operator:
            return {'message': 'Operator not found'}, 404

        # Delete the operator
        db.session.delete(operator)
        db.session.commit()

        return {'message': 'Operator deleted successfully'}, 200



