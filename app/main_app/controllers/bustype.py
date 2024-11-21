from flask_restx import Resource
from app.main_app.models.bus_type import BusType  # Adjust the import as per your structure
from app.main_app import db
from app.main_app.dto.bus_type import bustypedto  # Adjust import to your DTO file

fetch_bus_types_blueprint = bustypedto.fetch_bus_types_api

# Fetching bus types
@fetch_bus_types_blueprint.route('', methods=['GET'])
class FetchBusTypes(Resource):
    def get(self):
        bus_types = BusType.query.all()

        if not bus_types:
            return {'message': 'No bus types found', 'bus_types': []}, 200

        bus_type_list = [{
            'bus_type_id': bus_type.bus_type_id,
            'bus_type_name': bus_type.bus_type_name
        } for bus_type in bus_types]

        return {'message': 'Bus types fetched successfully', 'bus_types': bus_type_list}, 200
