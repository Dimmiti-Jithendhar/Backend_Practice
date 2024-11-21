from app.main_app import db
import uuid
from werkzeug.security import generate_password_hash,check_password_hash


#create table based on all columns 

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))    
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    mobile = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Adjust length as needed

    def __init__(self, first_name, last_name, mobile, email, gender, password):
        self.first_name = first_name
        self.last_name = last_name
        self.mobile = mobile
        self.email = email
        self.gender = gender
        self.set_password(password)
    #use hashed password to store
    def set_password(self, password):
        self.password = generate_password_hash(password)
    #check hashed password
    def check_password(self, password):
        return check_password_hash(self.password, password)
    def __repr__(self):
        return f'<User {self.first_name} {self.last_name}>'




