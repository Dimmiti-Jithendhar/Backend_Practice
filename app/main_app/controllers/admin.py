from flask_restx import Resource, Namespace
from flask import request, jsonify, session
from app.main_app.models.admin import Admin
from app.main_app import db
from app.main_app.models.users import User
from werkzeug.security import check_password_hash, generate_password_hash
import uuid
from app.main_app.dto.admin import admindto


admin_ns = admindto.adminapi 

#resource is a base class provided by flask_restful that simplifies creation of rest api

# Admin registration
@admin_ns.route('/add_admin')
class AdminSignup(Resource):
    def post(self):
        data = request.get_json()
        if not data.get('email') or not data.get('password'):
            return {'message': 'Email and password are required'}, 400

        existing_admin = Admin.query.filter_by(email=data['email']).first()
        if existing_admin:
            return {'message': 'Admin already exists'}, 400

        try:
            new_admin = Admin(
                email=data['email'],
                password=generate_password_hash(data['password'])
            )
            db.session.add(new_admin)
            db.session.commit()

            return {'message': 'Admin created successfully'}, 201
        except Exception as e:
            db.session.rollback()
            print("Error:", str(e))
            return {'message': f'Error occurred: {str(e)}'}, 500

# Add a user
@admin_ns.route('/add_user')
class AddUser(Resource):
    def post(self):
        data = request.get_json()

        required_fields = ['first_name', 'last_name', 'email', 'mobile', 'gender', 'password']
        if not all(field in data for field in required_fields):
            return {'message': 'Missing required fields'}, 400

        user = User.query.filter_by(email=data['email']).first()
        if user:
            return {'message': 'User already exists'}, 400

        new_user = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            mobile=data['mobile'],
            email=data['email'],
            gender=data['gender'],
            password=generate_password_hash(data['password'])
        )

        db.session.add(new_user)
        db.session.commit()

        return {'message': 'User added successfully'}, 201

# # Update a user (Admin use)
# @admin_ns.route('/user/update')
# class UpdateUser(Resource):
#     def put(self):
#         data = request.get_json()

#         required_fields = ['email', 'first_name', 'last_name', 'mobile', 'gender']
#         if not all(field in data for field in required_fields):
#             return {'message': 'Missing required fields'}, 400

#         current_email = data['email']
#         new_email = data.get('new_email')

#         user = User.query.filter_by(email=current_email).first()
#         if not user:
#             return {'message': 'User not found'}, 404

#         if new_email and new_email != current_email:
#             if User.query.filter_by(email=new_email).first():
#                 return {'message': 'New email is already in use'}, 400
#             user.email = new_email

#         user.first_name = data['first_name']
#         user.last_name = data['last_name']
#         user.mobile = data['mobile']
#         user.gender = data['gender']
#         user.password = generate_password_hash(data['password'])

#         db.session.commit()

#         return {'message': 'User details updated successfully'}, 200

# Update user details by the user
@admin_ns.route('/user/self-update')
class UserrUpdate(Resource):
    def put(self):
        data = request.get_json()

        current_email = data.get('email')
        new_email = data.get('new_email')
        new_password = data.get('new_password')
        current_password = data.get('password')

        if not current_email:
            return {'message': 'Email is required'}, 400

        user = User.query.filter_by(email=current_email).first()
        if not user:
            return {'message': 'User not found'}, 404

        if new_password and current_password:
            if not check_password_hash(user.password, current_password):
                return {'message': 'Current password is incorrect'}, 400
            user.password = generate_password_hash(new_password)

        if new_email and new_email != current_email:
            if User.query.filter_by(email=new_email).first():
                return {'message': 'New email is already in use'}, 400
            user.email = new_email

        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.mobile = data.get('mobile', user.mobile)
        user.gender = data.get('gender', user.gender)

        db.session.commit()

        return {'message': 'User details updated successfully'}, 200

# Get a specific user
# @admin_ns.route('/user/specific')
# class GetSpecificUser(Resource):
#     def get(self):
#         data = request.get_json()
#         email = data.get('email')
#         if not email:
#             return {"error": "Email is required"}, 400

#         user = User.query.filter_by(email=email).first()
#         if user:
#             return {
#                 'firstName': user.first_name,
#                 'lastName': user.last_name,
#                 'email': user.email,
#                 'mobile': user.mobile,
#                 'gender': user.gender
#             }, 200
#         else:
#             return {"error": "User not found"}, 404

@admin_ns.route('/user/specific')
class GetSpecificUser(Resource):
    def get(self):
        # Retrieve email from query parameters
        email = request.args.get('email')
        if not email:
            return {"error": "Email is required"}, 400

        # Fetch user details from the database using the provided email
        user = User.query.filter_by(email=email).first()
        
        if user:
            # Return user details
            return {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'mobile': user.mobile,
                'gender': user.gender
            }, 200
        else:
            return {"error": "User not found"}, 404
# Delete a user
@admin_ns.route('/delete_user')
class DeleteUser(Resource):
    def delete(self):
        data = request.get_json()

        if 'mobile' not in data:
            return {'message': 'Mobile number is required'}, 400

        user = User.query.filter_by(mobile=data['mobile']).first()
        if not user:
            return {'message': 'User not found'}, 404

        db.session.delete(user)
        db.session.commit()

        return {'message': 'User deleted successfully'}, 200



































































# from flask_restx import Resource
# from flask import request, jsonify, session
# from app.main_app.models.admin import Admin
# from app.main_app import db
# from app.main_app.dto.admin import admindto
# import uuid
# from app.main_app.models.users import User
# from werkzeug.security import check_password_hash, generate_password_hash

# admin_blueprint = admindto.fetchapi  
# add_blueprint= admindto.addapi
# adminlogin_blueprint=admindto.logapi
# adduser_blueprint =admindto.adduserapi
# updateuser_blueprint=admindto.updateuserapi
# userupdate_blueprint=admindto.updateuserapi
# getspecificuser_blueprint=admindto.getspecificuserapi
# deleteuser_blueprint=admindto.deleteuserapi
# userrupdate_blueprint=admindto.userrupdateapi



# @admin_blueprint.route('', methods=['GET'])
# #fetching
# class UserList(Resource):
#     def get(self):
#         # Ensure admin is logged in
#         if 'admin_id' not in session:
#             return {'message': 'Admin not logged in'}, 401

#         # Fetch all users
#         users = User.query.all()  # Fetch all users from the User model
#         users_data = [{
#             'first_name': user.first_name,
#             'last_name': user.last_name,
#             'mobile': user.mobile,
#             'email': user.email,
#             'gender': user.gender
#         } for user in users]

#         return jsonify(users_data)



# #admin register
# # from werkzeug.security import generate_password_hash,check_password_hash
# @add_blueprint.route('', methods=['POST'])
# class AdminSignup(Resource):
#     def post(self):
#         data = request.get_json()
#         if not data.get('email') or not data.get('password'):
#             return {'message': 'Email and password are required'}, 400

#         existing_admin = Admin.query.filter_by(email=data['email']).first()
#         if existing_admin:
#             return {'message': 'Admin already exists'}, 400

#         try:
#             new_admin = Admin(
#                 email=data['email'],
#                 password=data['password']
#             )
#             db.session.add(new_admin)
#             db.session.commit()

#             return {'message': 'Admin created successfully'}, 201

#         except Exception as e:
#             db.session.rollback()
#             print("Error:", str(e))
#             return {'message': f'Error occurred: {str(e)}'}, 500


# #add an user to user table 
# from flask import Blueprint, request
# @adduser_blueprint.route('', methods=['POST'])
# class AddUser(Resource):
#     def post(self):
#         data = request.get_json()

#         # Manual validation: Check if all required fields are present
#         required_fields = ['first_name', 'last_name', 'email', 'mobile', 'gender', 'password']
#         if not all(field in data for field in required_fields):
#             return {'message': 'Missing required fields'}, 400

#         # Check if the user already exists
#         user = User.query.filter_by(email=data['email']).first()
#         if user:
#             return {'message': 'User already exists'}, 400

#         # Create a new user
#         new_user = User(
#             first_name=data['first_name'],
#             last_name=data['last_name'],
#             mobile=data['mobile'],
#             email=data['email'],
#             gender=data['gender'],
#             password=data['password']
#         )

#         # Add the new user to the database
#         db.session.add(new_user)
#         db.session.commit()

#         return {'message': 'User added successfully'}, 201


# #update the details 
# #this has created before which is used by admin
# @updateuser_blueprint.route('', methods=['PUT'])
# class UpdateUser(Resource):
#     def put(self):
#         data = request.get_json()

#         # Validate required fields
#         required_fields = ['email', 'first_name', 'last_name', 'mobile', 'gender']
#         if not all(field in data for field in required_fields):
#             return {'message': 'Missing required fields'}, 400

#         current_email = data['email']
#         new_email = data.get('new_email')  # Use new_email if provided, otherwise it will be None

#         # Find the user by the current email
#         user = User.query.filter_by(email=current_email).first()
#         if not user:
#             return {'message': 'User not found'}, 404

#         # Check if the new email is provided and if it's different from the current email
#         if new_email and new_email != current_email:
#             if User.query.filter_by(email=new_email).first():
#                 return {'message': 'New email is already in use'}, 400
#             user.email = new_email

#         # Update user details
#         user.first_name = data['first_name']
#         user.last_name = data['last_name']
#         user.mobile = data['mobile']
#         user.gender = data['gender']
#         user.password = data['password']  # Ensure password is hashed if required

#         # Commit changes to the database
#         db.session.commit()

#         return {'message': 'User details updated successfully'}, 200

# # update user details update by user only 
# @userrupdate_blueprint.route('', methods=['PUT'])
# class UserrUpdate(Resource):
#     def put(self):
#         data = request.get_json()

#         current_email = data.get('email')
#         new_email = data.get('new_email')  # Optional new email field
#         new_password = data.get('new_password')  # Optional new password field
#         current_password = data.get('password')  # User's current password

#         # Check if the current email is provided
#         if not current_email:
#             return {'message': 'Email is required'}, 400

#         # Find the user by the current email
#         user = User.query.filter_by(email=current_email).first()
#         if not user:
#             return {'message': 'User not found'}, 404

#         # Validate password if the user wants to change their password
#         if new_password and current_password:
#             if not check_password_hash(user.password, current_password):
#                 return {'message': 'Current password is incorrect'}, 400
#             user.password = generate_password_hash(new_password)  # Update with new password

#         # Check if the new email is provided and if it's different from the current email
#         if new_email and new_email != current_email:
#             if User.query.filter_by(email=new_email).first():
#                 return {'message': 'New email is already in use'}, 400
#             user.email = new_email  # Update email

#         # Update other user details only if provided (these fields are optional)
#         user.first_name = data.get('first_name', user.first_name)
#         user.last_name = data.get('last_name', user.last_name)
#         user.mobile = data.get('mobile', user.mobile)
#         user.gender = data.get('gender', user.gender)

#         # Commit the changes to the database
#         db.session.commit()

#         return {'message': 'User details updated successfully'}, 200

# from sqlalchemy.orm import sessionmaker


# #getting specific user
# @getspecificuser_blueprint.route('',methods=['GET'])
# class GetSpecificUser(Resource):

#     def get(self):
#         data= request.get_json()
#         email = data['email']
#         if not email:
#             return {"error": "Email is required"}, 400
        
#         # Fetch user details from database using email
#         user = User.query.filter_by(email=email).first()
        
#         if user:
#             # Return user details
#             return {
#                 'firstName': user.first_name,
#                 'lastName': user.last_name,
#                 'email': user.email,
#                 'mobile': user.mobile,
#                 'gender': user.gender
#             }, 200
#         else:
#             return {"error": "User not found"}, 404




# @deleteuser_blueprint.route('',methods=['DELETE'])
# class DeleteUser(Resource):
#     def delete(self):
#         data = request.get_json()

#         # Validate required field
#         if 'mobile' not in data:
#             return {'message': 'Mobile number is required'}, 400

#         # Find the user by mobile number
#         user = User.query.filter_by(mobile=data['mobile']).first()
#         if not user:
#             return {'message': 'User not found'}, 404

#         # Delete the user
#         db.session.delete(user)
#         db.session.commit()

#         return {'message': 'User deleted successfully'}, 200
