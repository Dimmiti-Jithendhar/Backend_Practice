from flask_socketio import SocketIO, join_room, emit
from app.main_app import app1

socketio = SocketIO(app1, cors_allowed_origins="*")

@socketio.on('connect')
def handle_connect():
    print("Client connected")

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

# When a user joins their unique chat room
@socketio.on('join_user')
def handle_join_user(data):
    user_id = data.get('user_id')
    room = f"user_{user_id}"  # Unique room for each user
    join_room(room)
    print(f"User {user_id} joined room {room}")

# When an admin joins a user's chat room
@socketio.on('join_admin')
def handle_join_admin(data):
    user_id = data.get('user_id')
    room = f"user_{user_id}"  # Admin joins the same room as the user
    join_room(room)
    print(f"Admin joined user {user_id}'s chat room {room}")
    emit('status', {'msg': f'Admin joined user {user_id}\'s chat'}, room=room)

# Handling a message sent by a user
@socketio.on('send_message')
def handle_send_message(data):
    user_id = data.get('user_id')
    room = f"user_{user_id}"  # Send to the user's room
    message = data.get('message')
    print(f"Message received from user {user_id}: {message}")
    emit('receive_message', {'msg': message}, room=room)  # Emitting to the room

# When user sends message to admin
@socketio.on('send_message_to_admin')
def handle_send_message_to_admin(data):
    emit('message_from_user', data, room='room')  # Send to the admin room

# Admin sends message to a user
@socketio.on('send_message_to_user')
def handle_send_message_to_user(data):
    user_id = data.get('user_id')
    room = f"user_{user_id}"
    message = data.get('message')
    print(f"Admin sends message to user {user_id}: {message}")
    emit('receive_message', {'msg': message, 'user': 'admin'}, room=room)  # Emit message to user room
