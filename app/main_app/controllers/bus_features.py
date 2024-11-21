from flask_restx import Resource
from flask import request
from app.main_app.models.bus_features import BusFeature  # Adjust import as per your structure
from app.main_app.models.bus_type import BusType        # Adjust import as per your structure
from app.main_app.models.features import Feature        # Adjust import as per your structure
from app.main_app import db
from app.main_app.dto.bus_features import busfeaturesdto  # Adjust the DTO import as necessary



bus_features_namespace = busfeaturesdto.bus_features_api

# Route to fetch all bus features
@bus_features_namespace.route('')
class FetchBusFeatures(Resource):
    def get(self):
        bus_types = BusType.query.all()
        if not bus_types:
            return {'message': 'No bus types found.'}, 404

        bus_features_data = []
        for bus_type in bus_types:
            bus_features = db.session.query(Feature).join(BusFeature).filter(BusFeature.bus_type_id == bus_type.bus_type_id).all()
            feature_list = [feature.feature_name for feature in bus_features]
            bus_features_data.append({
                'bus_type_name': bus_type.bus_type_name,
                'features': feature_list
            })

        return {'message': 'Bus features fetched successfully.', 'bus_features': bus_features_data}, 200


# Route to add new bus features
@bus_features_namespace.route('/add')
class AddBusFeatures(Resource):
    def post(self):
        data = request.get_json()

        if 'bus_type_name' not in data or 'feature_names' not in data:
            return {'message': 'Missing required fields: bus_type_name or feature_names'}, 400

        bus_type = BusType.query.filter_by(bus_type_name=data['bus_type_name']).first()
        if not bus_type:
            return {'message': 'Bus type not found'}, 404

        added_features = []
        for feature_name in data['feature_names']:
            feature = Feature.query.filter_by(feature_name=feature_name).first()
            if not feature:
                return {'message': f'Feature "{feature_name}" not found'}, 404

            existing_relation = BusFeature.query.filter_by(bus_type_id=bus_type.bus_type_id, feature_id=feature.feature_id).first()
            if existing_relation:
                continue

            new_relation = BusFeature(bus_type_id=bus_type.bus_type_id, feature_id=feature.feature_id)
            db.session.add(new_relation)
            added_features.append(feature_name)

        db.session.commit()

        if added_features:
            return {'message': 'Bus features added successfully', 'added_features': added_features}, 201
        else:
            return {'message': 'No new features added; they already exist.'}, 200


# Route to update existing bus features
@bus_features_namespace.route('/update/<string:bus_type_name>')
class UpdateBusFeature(Resource):
    def put(self, bus_type_name):
        data = request.get_json()
        
        bus_type = BusType.query.filter_by(bus_type_name=bus_type_name).first()
        if not bus_type:
            return {'message': 'Bus type not found'}, 404

        features = data.get('feature_names', [])
        updated_features = []

        for feature_name in features:
            feature = Feature.query.filter_by(feature_name=feature_name).first()
            if not feature:
                return {'message': f'Feature "{feature_name}" not found'}, 404

            existing_relation = BusFeature.query.filter_by(bus_type_id=bus_type.bus_type_id, feature_id=feature.feature_id).first()
            if existing_relation:
                continue

            new_relation = BusFeature(bus_type_id=bus_type.bus_type_id, feature_id=feature.feature_id)
            db.session.add(new_relation)
            updated_features.append(feature_name)

        db.session.commit()
        return {'message': 'Bus features updated successfully', 'updated_features': updated_features}, 200


# Route to delete bus features
@bus_features_namespace.route('/delete/<string:bus_type_name>')
class DeleteBusFeatures(Resource):
    def delete(self, bus_type_name):
        bus_type = BusType.query.filter_by(bus_type_name=bus_type_name).first()
        if not bus_type:
            return {'message': 'Bus type not found'}, 404

        data = request.get_json()
        if 'feature_names' not in data:
            return {'message': 'Missing required field: feature_names'}, 400

        deleted_features = []
        not_present_features = []

        for feature_name in data['feature_names']:
            feature = Feature.query.filter_by(feature_name=feature_name).first()
            if feature:
                bus_feature = BusFeature.query.filter_by(bus_type_id=bus_type.bus_type_id, feature_id=feature.feature_id).first()
                if bus_feature:
                    db.session.delete(bus_feature)
                    deleted_features.append(feature_name)
                else:
                    not_present_features.append(feature_name)
            else:
                not_present_features.append(feature_name)

        db.session.commit()

        response_message = 'Features deleted successfully' if deleted_features else 'No valid features were deleted.'

        return {
            'message': response_message,
            'deleted_features': deleted_features,
            'not_present_features': not_present_features
        }, 200






# fetch_bus_features_blueprint = busfeaturesdto.fetch_bus_features_api
# add_bus_features_blueprint = busfeaturesdto.add_bus_features_api
# update_bus_features_blueprint = busfeaturesdto.update_bus_features_api
# delete_bus_features_blueprint = busfeaturesdto.delete_bus_features_api

# @fetch_bus_features_blueprint.route('', methods=['GET'])
# class FetchBusFeatures(Resource):
#     def get(self):
#         # Fetch all bus types
#         bus_types = BusType.query.all()
#         if not bus_types:
#             return {'message': 'No bus types found.'}, 404

#         bus_features_data = []

#         for bus_type in bus_types:
#             # Query the features associated with this bus type
#             bus_features = db.session.query(Feature).join(BusFeature).filter(BusFeature.bus_type_id == bus_type.bus_type_id).all()

#             # Serialize the feature data
#             feature_list = [feature.feature_name for feature in bus_features]
#             bus_features_data.append({
#                 'bus_type_name': bus_type.bus_type_name,
#                 'features': feature_list
#             })

#         # Return the feature data in JSON format
#         return {
#             'message': 'Bus features fetched successfully.',
#             'bus_features': bus_features_data
#         }, 200

# # Add a new bus feature (using names)
# @add_bus_features_blueprint.route('', methods=['POST'])
# class AddBusFeatures(Resource):
#     def post(self):
#         data = request.get_json()

#         # Check if required fields are present (bus_type_name, feature_names)
#         if 'bus_type_name' not in data or 'feature_names' not in data:
#             return {'message': 'Missing required fields: bus_type_name or feature_names'}, 400

#         # Fetch the bus type by its name
#         bus_type = BusType.query.filter_by(bus_type_name=data['bus_type_name']).first()
#         if not bus_type:
#             return {'message': 'Bus type not found'}, 404

#         # Initialize a list to keep track of added features
#         added_features = []

#         # Iterate over the list of feature names and add them to the junction table
#         for feature_name in data['feature_names']:
#             # Fetch each feature by its name
#             feature = Feature.query.filter_by(feature_name=feature_name).first()

#             if not feature:
#                 return {'message': f'Feature "{feature_name}" not found'}, 404

#             # Check if the bus feature relationship already exists
#             existing_bus_feature = BusFeature.query.filter_by(bus_type_id=bus_type.bus_type_id, feature_id=feature.feature_id).first()

#             if existing_bus_feature:
#                 # Feature already exists for this bus type, skip adding
#                 continue
            
#             # Create a new bus feature relationship
#             new_bus_feature = BusFeature(bus_type_id=bus_type.bus_type_id, feature_id=feature.feature_id)
#             db.session.add(new_bus_feature)
#             added_features.append(feature_name)  # Track added features

#         # Commit all new relationships to the database
#         db.session.commit()

#         if added_features:
#             return {'message': 'Bus features added successfully', 'added_features': added_features}, 201
#         else:
#             return {'message': 'No new features added; they already exist.'}, 200


# @update_bus_features_blueprint.route('/<string:bus_type_name>', methods=['PUT'])
# class UpdateBusFeature(Resource):
#     def put(self, bus_type_name):
#         data = request.get_json()

#         # Check if bus type exists
#         bus_type = BusType.query.filter_by(bus_type_name=bus_type_name).first()
#         if not bus_type:
#             return {'message': 'Bus type not found'}, 404

#         features = data.get('feature_names', [])
#         updated_features = []

#         for feature_name in features:
#             feature = Feature.query.filter_by(feature_name=feature_name).first()
#             if not feature:
#                 return {'message': f'Feature "{feature_name}" not found'}, 404
            
#             # Check if the bus type-feature relation already exists
#             existing_relation = BusFeature.query.filter_by(bus_type_id=bus_type.bus_type_id, feature_id=feature.feature_id).first()
#             if existing_relation:
#                 continue  # Skip if the relation already exists
            
#             new_relation = BusFeature(bus_type_id=bus_type.bus_type_id, feature_id=feature.feature_id)
#             db.session.add(new_relation)
#             updated_features.append(feature_name)

#         db.session.commit()
#         return {'message': 'Bus features updated successfully', 'updated_features': updated_features}, 200


# # Define the delete bus features endpoint
# @delete_bus_features_blueprint.route('/<string:bus_type_name>', methods=['DELETE'])
# class DeleteBusFeatures(Resource):
#     def delete(self, bus_type_name):
#         # Fetch the bus type by name
#         bus_type = BusType.query.filter_by(bus_type_name=bus_type_name).first()
#         if not bus_type:
#             return {'message': 'Bus type not found'}, 404
        
#         data = request.get_json()
#         if 'feature_names' not in data:
#             return {'message': 'Missing required field: feature_names'}, 400

#         # Initialize lists to keep track of deleted and non-existent features
#         deleted_features = []
#         not_present_features = []

#         # Iterate over feature names and attempt to delete them
#         for feature_name in data['feature_names']:
#             feature = Feature.query.filter_by(feature_name=feature_name).first()
#             if feature:
#                 bus_feature = BusFeature.query.filter_by(bus_type_id=bus_type.bus_type_id, feature_id=feature.feature_id).first()
#                 if bus_feature:
#                     db.session.delete(bus_feature)
#                     deleted_features.append(feature_name)
#                 else:
#                     not_present_features.append(feature_name)  # Feature not linked to the bus type
#             else:
#                 not_present_features.append(feature_name)  # Feature does not exist at all

#         db.session.commit()

#         # Create a message based on what happened
#         response_message = 'Features deleted successfully'
#         if not deleted_features:
#             response_message = 'No valid features were deleted.'
        
#         return {
#             'message': response_message,
#             'deleted_features': deleted_features,
#             'not_present_features': not_present_features
#         }, 200


