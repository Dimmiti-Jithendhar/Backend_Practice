from flask_restx import Namespace, Resource
from flask import request, jsonify
from app.main_app.models.users import User
from app.main_app.models.admin import Admin
from app.main_app import db
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from app.main_app.dto.users import userdto
import re
user_namespace = userdto.userapi  # Unified namespace for all user-related operations

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

PASSWORD_REGEX = re.compile(
    r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
)
# Define all user-related routes within the userapi namespace
@user_namespace.route('/signup')
class Signup(Resource):
    def post(self):
        data = request.get_json()
        
        # Check for required fields
        required_fields = ['first_name', 'last_name', 'email', 'mobile', 'gender', 'password']
        if not all(field in data for field in required_fields):
            return {'message': 'Missing required fields'}, 400

        if not EMAIL_REGEX.match(data['email']):
            return {'message': 'Invalid email format'}, 400

        # Check if email already exists
        if User.query.filter_by(email=data['email']).first():
            return {'message': 'Email already exists'}, 400

        if not (data['mobile'].isdigit() and len(data['mobile']) == 10):
            return {'message': 'Mobile number must be exactly 10 digits'}, 400

        # Check if mobile number already exists
        if User.query.filter_by(mobile=data['mobile']).first():
            return {'message': 'Phone number already exists'}, 400

        # Validate password complexity
        if not PASSWORD_REGEX.match(data['password']):
            return {
                'message': 'Password must be at least 8 characters long, contain one lowercase letter, '
                           'one uppercase letter, one digit, and one special character.'
            }, 400

        # Create new user with hashed password
        new_user = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            mobile=data['mobile'],
            email=data['email'],
            gender=data['gender'],
            password=data['password']  # Password hashing is handled in the User model
        )

        db.session.add(new_user)
        db.session.commit()

        return {'message': 'User added successfully'}, 201
@user_namespace.route('/check_email')
class CheckEmail(Resource):
    def post(self):
        data = request.get_json()
        email_exists = bool(User.query.filter_by(email=data['email']).first())
        return {'exists': email_exists}, 200

@user_namespace.route('/check_mobile')
class CheckMobile(Resource):
    def post(self):
        data = request.get_json()
        mobile_exists = bool(User.query.filter_by(mobile=data['mobile']).first())
        return {'exists': mobile_exists}, 200


@user_namespace.route('/login')
class Login(Resource):
    def post(self):
        data = request.get_json()
        
        # Check if email or password is missing in the request
        if not data.get('email') or not data.get('password'):
            return {'message': 'Missing email or password'}, 400

        # Check if the email exists in the Admin table
        admin = Admin.query.filter_by(email=data['email']).first()
        if admin and check_password_hash(admin.password, data['password']):
            # Generate access token with additional claims for admin
            access_token = create_access_token(
                identity={'id': admin.id},
                additional_claims={
                    'role': 'admin',
                    'email': admin.email,
                    # Add other claims for admin if needed
                },
                fresh=True
            )
            return {
                'message': 'Admin login successful',
                'role': 'admin',
                'token': access_token
            }, 200

        # If not found in Admin table, check in User table
        user = User.query.filter_by(email=data['email']).first()
        if user and check_password_hash(user.password, data['password']):
            # Generate access token with additional claims for user
            access_token = create_access_token(
                identity={'id': user.id},
                additional_claims={
                    'role': 'user',
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'gender': user.gender,
                    'mobile': user.mobile,
                    'id': user.id
                },
                fresh=True
            )
            return {
                'message': 'User login successful',
                'role': 'user',
                'token': access_token
            }, 200

        # If no match found in either table, return invalid credentials
        return {'message': 'Invalid credentials'}, 401

@user_namespace.route('/update')
class UpdateUser(Resource):
    def put(self):
        data = request.get_json()
        user = User.query.get(data['id'])  # Assuming 'id' is passed in the payload for simplicity
        if not user:
            return {'message': 'User not found'}, 404

        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.mobile = data.get('mobile', user.mobile)
        user.email = data.get('email', user.email)

        if 'password' in data and check_password_hash(user.password, data['current_password']):
            user.password = data['password']

        db.session.commit()
        return {'message': 'User updated successfully'}, 200

@user_namespace.route('/list')
class UserList(Resource):
    def get(self):
        users = User.query.all()
        user_list = [{
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'mobile': user.mobile,
            'email': user.email,
            'gender': user.gender
        } for user in users]
        x=len(users)
        print(x)
        return {'message': 'Users fetched successfully', 'users': user_list,'totalUsers': x}, 200






