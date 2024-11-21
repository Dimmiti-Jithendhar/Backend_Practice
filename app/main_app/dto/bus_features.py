from flask_restx import Namespace

class busfeaturesdto:
    bus_features_api = Namespace('busfeatures', description="API for managing the bus features")
    # fetch_bus_features_api = Namespace('fetch_bus_features', description="API for fetching bus features")
    # add_bus_features_api = Namespace('add_bus_features', description="API for adding a feature")
    # update_bus_features_api = Namespace('update_bus_features', description="API for updating feature details")
    # # get_specific_place_api = Namespace('getspecificplace', description="API for getting specific place details")
    # delete_bus_features_api = Namespace('delete_bus_features', description="API for deleting a feature")
