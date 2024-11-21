from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO

db=SQLAlchemy()
ma=Marshmallow()
jwt = JWTManager()
socketio = SocketIO(cors_allowed_origins="*")





def mydb():
    app=Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:Djithu%40326@127.0.0.1/project'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    app.config['SECRET_KEY'] = 'Jithu'
    app.config['JWT_ALGORITHM'] = 'HS256'
    app.config['JWT_SECRET_KEY'] = '9493187822'
    # app.config['SQLALCHEMY_ECHO'] = True  # Enable debug SQL logging
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    socketio.init_app(app)
    return app