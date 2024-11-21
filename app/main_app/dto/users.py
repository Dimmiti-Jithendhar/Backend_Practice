from flask_restx import Namespace

class userdto:
    userapi = Namespace('user', description="User operations")  # Single namespace for user-related endpoints
