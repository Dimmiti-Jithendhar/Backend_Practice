
from flask_restx import Namespace, Resource
from flask import request, jsonify
from app.main_app.models.places import Place
from app.main_app.models.routes import Route

from app.main_app import db
from app.main_app.dto.routes import routesdto

route_namespace = routesdto.routes_api  # Unified namespace for all route-related operations

# Helper function to get place ID by name
def get_place_id_by_name(place_name):
    place = Place.query.filter_by(name=place_name).first()
    return place.place_id if place else None

# Route to add a new route
@route_namespace.route('/add')
class AddRoute(Resource):
    def post(self):
        data = request.get_json()
        required_fields = ['source', 'destination', 'duration', 'distance']
        
        if not all(field in data for field in required_fields):
            return {'message': 'Missing required fields'}, 400

        if data['source'] == data['destination']:
            return {'message': 'Source and destination cannot be the same'}, 400

        source_place_id = get_place_id_by_name(data['source'])
        destination_place_id = get_place_id_by_name(data['destination'])

        if not source_place_id or not destination_place_id:
            return {'message': 'Invalid source or destination place name'}, 400

        existing_route = Route.query.filter_by(source=source_place_id, destination=destination_place_id).first()
        if existing_route:
            return {'message': 'Route already exists'}, 400

        new_route = Route(
            source=source_place_id,
            destination=destination_place_id,
            duration=data['duration'],
            distance=data['distance']
        )
        
        db.session.add(new_route)
        db.session.commit()
        return {'message': 'Route added successfully'}, 201

# Route to update an existing route
@route_namespace.route('/update/<int:route_id>')
class UpdateRoute(Resource):
    def put(self, route_id):
        route = Route.query.get(route_id)
        if not route:
            return {'message': 'Route not found'}, 404

        data = request.get_json()
        if 'source' in data and 'destination' in data and data['source'] == data['destination']:
            return {'message': 'Source and destination cannot be the same'}, 400

        if 'source' in data:
            source_place_id = get_place_id_by_name(data['source'])
            if not source_place_id:
                return {'message': 'Invalid source place name'}, 400
            route.source = source_place_id

        if 'destination' in data:
            destination_place_id = get_place_id_by_name(data['destination'])
            if not destination_place_id:
                return {'message': 'Invalid destination place name'}, 400
            route.destination = destination_place_id

        route.duration = data.get('duration', route.duration)
        route.distance = data.get('distance', route.distance)

        db.session.commit()
        return {'message': 'Route updated successfully'}, 200

# Route to delete a route
@route_namespace.route('/delete/<int:route_id>')
class DeleteRoute(Resource):
    def delete(self, route_id):
        route = Route.query.get(route_id)
        if not route:
            return {'message': 'Route not found'}, 404

        db.session.delete(route)
        db.session.commit()
        return {'message': 'Route deleted successfully'}, 200

# Route to fetch all routes
@route_namespace.route('')
class FetchRoutes(Resource):
    def get(self):
        routes = Route.query.all()
        if not routes:
            return {'message': 'No routes found', 'routes': []}, 200

        route_list = [{
            'route_id': route.route_id,
            'source': Place.query.get(route.source).name if route.source else None,
            'destination': Place.query.get(route.destination).name if route.destination else None,
            'duration': route.duration,
            'distance': route.distance
        } for route in routes]

        return {'message': 'Routes fetched successfully', 'routes': route_list}, 200































# from flask_restx import Resource
# from flask import request, jsonify
# from app.main_app.models.routes import Route  # Adjust the import as per your structure
# from app.main_app import db
# from app.main_app.models.places import Place 
# from app.main_app.dto.routes import routesdto  # Adjust import to your DTO file


# fetch_routes_blueprint = routesdto.fetch_routes_api
# add_route_blueprint = routesdto.add_route_api
# update_route_blueprint = routesdto.update_route_api
# delete_route_blueprint = routesdto.delete_route_api

# # Function to get place ID from name
# def get_place_id_by_name(place_name):
#     place = Place.query.filter_by(name=place_name).first()
#     print(place)
#     return place.place_id if place else None

# # Add Route
# @add_route_blueprint.route('', methods=['POST'])
# class AddRoute(Resource):
#     def post(self):
#         data = request.get_json()
#         required_fields = ['source', 'destination', 'duration', 'distance']
        
#         if not all(field in data for field in required_fields):
#             return {'message': 'Missing required fields'}, 400

#         if data['source'] == data['destination']:
#             return {'message': 'Source and destination cannot be the same'}, 400

#         source_place_id = get_place_id_by_name(data['source'])
#         destination_place_id = get_place_id_by_name(data['destination'])

#         if not source_place_id:
#             return {'message': 'Invalid source place name'}, 400

#         if not destination_place_id:
#             return {'message': 'Invalid destination place name'}, 400

#         existing_route = Route.query.filter_by(source=source_place_id, destination=destination_place_id).first()
#         if existing_route:
#             return {'message': 'Route already exists'}, 400

#         new_route = Route(
#             source=source_place_id,
#             destination=destination_place_id,
#             duration=data['duration'],
#             distance=data['distance']
#         )
        
#         db.session.add(new_route)
#         db.session.commit()
#         return {'message': 'Route added successfully'}, 201

# ##       o     k
        
# @delete_route_blueprint.route('/<int:route_id>', methods=['DELETE'])
# class DeleteRoute(Resource):
#     def delete(self, route_id):
#         # Fetch the route from the database using the route_id
#         route = Route.query.get(route_id)
#         if not route:
#             return {'message': 'Route not found'}, 404

#         # Delete the route
#         db.session.delete(route)
#         db.session.commit()
#         return {'message': 'Route deleted successfully'}, 200


# ##      o       k 


# @update_route_blueprint.route('/<int:route_id>', methods=['PUT'])
# class UpdateRoute(Resource):
#     def put(self, route_id):
#         # Fetch the route from the database using the route_id
#         route = Route.query.get(route_id)
#         if not route:
#             return {'message': 'Route not found'}, 404

#         # Get the data from the request
#         data = request.get_json()
#         # Check if source and destination are the same
#         if 'source' in data and 'destination' in data:
#             if data['source'] == data['destination']:
#                 return {'message': 'Source and destination cannot be the same'}, 400

#         # Update the route details
#         if 'source' in data:
#             source_place = Place.query.filter_by(name=data['source']).first()
#             if not source_place:
#                 return {'message': 'Invalid source place name'}, 400
#             route.source = source_place.place_id  # Update source ID based on place name

#         if 'destination' in data:
#             destination_place = Place.query.filter_by(name=data['destination']).first()
#             if not destination_place:
#                 return {'message': 'Invalid destination place name'}, 400
#             route.destination = destination_place.place_id
#         if 'duration' in data:
#             route.duration = data['duration']
#         if 'distance' in data:
#             route.distance = data['distance']

#         # Commit changes to the database
#         db.session.commit()
#         return {'message': 'Route updated successfully'}, 200

# @fetch_routes_blueprint.route('', methods=['GET'])
# class FetchRoutes(Resource):
#     def get(self):
#         # Fetch all routes from the database
#         routes = Route.query.all()
#         print(len(routes))
#         # If no routes are found, return an empty list
#         if not routes:
#             return {'message': 'No routes found', 'routes': []}, 200

#         # Serialize the route data
#         route_list = [{
#             'route_id': route.route_id,
#             'source': Place.query.get(route.source).name if route.source else None,  # Fetch place name
#             'destination': Place.query.get(route.destination).name if route.destination else None,  # Fetch place name
#             'duration': route.duration,
#             'distance': route.distance
#         } for route in routes]

#         # Return the route data in JSON format
#         return {'message': 'Routes fetched successfully', 'routes': route_list}, 200
