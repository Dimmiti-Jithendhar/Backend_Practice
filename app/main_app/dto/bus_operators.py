from flask_restx import Namespace

class busoperatorsdto:
    fetch_bus_operators_api = Namespace('fetch_bus_operators', description="API for fetching bus operators")
    add_bus_operator_api=Namespace('add_bus_operator',description="API for adding bus operator")
    update_bus_operator_api=Namespace('update_bus_operator',description="API for updating bus operator")
    delete_bus_operator_api=Namespace('delete_bus_operator',description="API for deleting bus operator")
    

