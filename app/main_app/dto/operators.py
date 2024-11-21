from flask_restx import Namespace

class operatorsdto:
    add_operator_api = Namespace('add_operator', description="API for adding an operator")
    fetch_operators_api=Namespace('fetch_operators',description="API for fetching an operators")
    update_operator_api=Namespace('update_operator',description="API for updating an operator")
    delete_operator_api=Namespace('delete_operator',description="API for deleting an operator")