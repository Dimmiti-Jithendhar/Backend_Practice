from flask_restx import Namespace

class busdto:
    add_bus_api = Namespace('add_bus', description="API for adding a bus")
    fetch_buses_api=Namespace('fetch_buses',description="API for fetching a bus")
    delete_bus_api=Namespace('delete_bus',description="API for delete a bus")
