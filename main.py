from app.main_app import mydb, socketio
from flask_cors import CORS
from app import blueprint
from app.main_app import db
from flask import Flask
from flask_migrate import Migrate
from app.main_app.models.places import Place
from app.main_app.models.routes import Route
from app.main_app.models.bus_type import BusType, insert_bus_types
from app.main_app.models.features import Feature, insert_features
from app.main_app.models.bus_features import BusFeature
from app.main_app.models.operators import Operator
from app.main_app.models.bus import Bus
from app.main_app.models.notifications import Notification
from app.main_app.models.bus_operators import BusOperator
from app.main_app.models.available_buses import AvailableBuses
from app.main_app.models.booking import Booking
from flask_socketio import SocketIO, join_room, leave_room, send, emit
from app.main_app.models.otp import OTP


app1 = mydb()  # Initializes the Flask app instance.
CORS(app1)  # Enables CORS for the app to allow requests from different origins.
app1.register_blueprint(blueprint)  # Registers your blueprint, allowing you to modularize your routes.
app1.app_context().push()

migrate = Migrate(app1, db)
# Initialize SocketIO with the Flask app
socketio = SocketIO(app1, cors_allowed_origins="*")

# Store active user rooms
# user_rooms = {}

# Create the tables after Place model is imported
with app1.app_context():
    db.create_all()
    


# # Define WebSocket events
# @socketio.on('connect')
# def handle_connect():
#     print("Client connected")

# @socketio.on('disconnect')
# def handle_disconnect():
#     print("Client disconnected")

# When a user joins the chat
# @socketio.on('join_user')
# def handle_join_user(data):
#     user_id = data['user_id']
#     room = f"user_{user_id}"
#     join_room(room)
#     user_rooms[user_id] = room
#     emit('status', {'msg': f'User {user_id} joined the chat'}, room=room)

# # When the admin joins the chat
# @socketio.on('join_admin')
# def handle_join_admin():
#     room = 'admin'
#     join_room(room)
#     emit('status', {'msg': 'Admin has joined the chat'}, room=room)

# When a user sends a message to the admin
# @socketio.on('user_message')
# def handle_user_message(data):
#     user_id = data['user_id']
#     message = data['message']
#     room = user_rooms.get(user_id)

#     if room:
#         # Send the message to the admin room
#         emit('admin_message', {'user_id': user_id, 'message': message}, room='admin')
#         # Notify the user that the message was sent
#         emit('status', {'msg': 'Message sent to admin'}, room=room)

# When the admin sends a reply to a specific user
# @socketio.on('admin_reply')
# def handle_admin_reply(data):
#     user_id = data['user_id']
#     message = data['message']
#     room = user_rooms.get(user_id)

#     if room:
#         # Send the admin's message to the specific user's room
#         emit('user_message', {'user_id': 'admin', 'message': message}, room=room)

if __name__ == '__main__':
    socketio.run(app1, debug=True)









'''
from app.main_app import mydb
from flask_cors import CORS
from app import blueprint
from app.main_app import db
from app.main_app.models.places import Place  # Import the Place model explicitly
from app.main_app.models.routes import Route
from app.main_app.models.bus_type import BusType,insert_bus_types
from app.main_app.models.features import Feature,insert_features
from app.main_app.models.bus_features import BusFeature
from app.main_app.models.operators import Operator
from app.main_app.models.bus import Bus
from app.main_app.models.bus_operators import BusOperator
from app.main_app.models.available_buses import AvailableBuses
from app.main_app.models.booking import Booking


app1 = mydb()   #Initializes the Flask app instance.
CORS(app1)    #Enables CORS for the app to allow requests from different origins.
app1.register_blueprint(blueprint)   #egisters your blueprint, allowing you to modularize your routes.
app1.app_context().push()

# Enable SQLAlchemy debug mode to see SQL queries
# app1.config['SQLALCHEMY_ECHO'] = True

# Create the tables after Place model is imported
with app1.app_context():

    db.create_all()  # This will create the 'places' table
    #insert_bus_types()
    #insert_features()

if __name__ == '__main__':
    app1.run(debug=True)


'''