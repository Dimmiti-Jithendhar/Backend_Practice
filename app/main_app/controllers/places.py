from flask_restx import Namespace, Resource
from flask import request
from app.main_app.models.places import Place  # Adjust the import as per your structure
from app.main_app import db
from app.main_app.dto.places import placesdto  # Adjust import to your DTO file

# Unified namespace for all place-related operations
place_namespace = placesdto.place_api

# Route to fetch all places
@place_namespace.route('')  #fetching places
class FetchPlaces(Resource):
    def get(self):
        places = Place.query.all()
        
        if not places:
            return {'message': 'No places found', 'places': []}, 200

        place_list = [{
            'place_id': place.place_id,
            'name': place.name
        } for place in places]

        return {'message': 'Places fetched successfully', 'places': place_list}, 200


# Route to add a new place
@place_namespace.route('/add')
class AddPlace(Resource):
    def post(self):
        data = request.get_json()
        
        if 'name' not in data:
            return {'message': 'Missing required fields'}, 400

        existing_place = Place.query.filter_by(name=data['name']).first()
        if existing_place:
            return {'message': 'Place already exists'}, 400
        
        new_place = Place(name=data['name'])
        
        db.session.add(new_place)
        db.session.commit()
        return {'message': 'Place added successfully'}, 201


# Route to update an existing place
@place_namespace.route('/update/<int:place_id>')
class UpdatePlace(Resource):
    def put(self, place_id):
        place = Place.query.get(place_id)
        if not place:
            return {'message': 'Place not found. Use another ID.'}, 404

        data = request.get_json()
        
        if 'name' not in data:
            return {'message': 'Missing required field: name'}, 400
        
        place.name = data['name']
        
        db.session.commit()
        return {'message': 'Place details updated successfully'}, 200


# Route to delete a place
@place_namespace.route('/delete/<int:place_id>')
class DeletePlace(Resource):
    def delete(self, place_id):
        place = Place.query.get(place_id)
        if not place:
            return {'message': 'Place not found'}, 404

        db.session.delete(place)
        db.session.commit()
        return {'message': 'Place deleted successfully'}, 200














# from flask_restx import Resource
# from flask import request, jsonify
# from app.main_app.models.places import Place  # Adjust the import as per your structure
# from app.main_app import db
# from app.main_app.dto.places import placesdto  # Adjust import to your DTO file


# fetch_places_blueprint = placesdto.fetch_places_api
# add_place_blueprint= placesdto.add_place_api
# update_place_blueprint = placesdto.update_place_api
# delete_place_blueprint = placesdto.delete_place_api



# #fetching places
# @fetch_places_blueprint.route('', methods=['GET'])
# class FetchPlaces(Resource):
#     def get(self):
#         # Query to fetch all places from the database
#         places = Place.query.all()
        
#         # If no places are found, return an empty list
#         if not places:
#             return {'message': 'No places found', 'places': []}, 200

#         # Serialize the place data
#         place_list = [{
#             'place_id': place.place_id,
#             'name': place.name
#         } for place in places]

#         # Return the place data in JSON format
#         return {'message': 'Places fetched successfully', 'places': place_list}, 200


# #add places

# @add_place_blueprint.route('', methods=['POST'])
# class AddPlace(Resource):
#     def post(self):
#         data = request.get_json()

#         # Check if required fields are present
#         if 'name' not in data:
#             return {'message': 'Missing required fields'}, 400

#         # Check if the place already exists
#         existing_place = Place.query.filter_by(name=data['name']).first()
#         if existing_place:
#             return {'message': 'Place already exists'}, 400
        
#         new_place = Place(name=data['name'])
        
#         db.session.add(new_place)
#         db.session.commit()
#         return {'message': 'Place added successfully'}, 201



# @update_place_blueprint.route('/<int:place_id>', methods=['PUT'])
# class UpdatePlace(Resource):
#     def put(self, place_id):
#         # Fetch the place from the database using the ID
#         place = Place.query.get(place_id)
#         if not place:
#             return {'message': 'Place not found use another id'}, 404

#         # Get the data from the request
#         data = request.get_json()

#         # Check if the new name is provided
#         if 'name' not in data:
#             return {'message': 'Missing required field: name'}, 400
        
#         place.name = data['name']
        
#         # Commit changes to the database
#         db.session.commit()
#         return {'message': 'Place details updated successfully'}, 200


# @delete_place_blueprint.route('/<int:place_id>', methods=['DELETE'])
# class DeletePlace(Resource):
#     def delete(self, place_id):
#         # Fetch the place from the database using the ID
#         place = Place.query.get(place_id)
#         if not place:
#             return {'message': 'Place not found'}, 404

#         # Delete the place
#         db.session.delete(place)
#         db.session.commit()
#         return {'message': 'Place deleted successfully'}, 200


