from flask_restx import Namespace

class admindto:
    adminapi = Namespace('admin', description="Admin and user related operations")
