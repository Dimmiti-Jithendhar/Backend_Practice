from flask_restx import Namespace

class routesdto:

    routes_api = Namespace('routes', description="API for managing routes")


    # fetch_routes_api = Namespace('fetch_routes', description="API for fetching all routes")
    # add_route_api = Namespace('add_route', description="API for adding a new route")
    # update_route_api = Namespace('update_route', description="API for updating route details")
    # # get_specific_place_api = Namespace('getspecificplace', description="API for getting specific place details")
    # delete_route_api = Namespace('delete_route', description="API for deleting a route")
