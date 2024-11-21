from flask import Blueprint
from flask_restx import Api, Resource, fields
from app.main_app.controllers.users import user_namespace
# from app.main_app.controllers.users import(signup_blueprint,login_blueprint,user_blueprint,update_blueprint,delete_blueprint,userlist_blueprint,user_detail_blueprint)
from app.main_app.controllers.admin import admin_ns
# from app.main_app.controllers.admin import(admin_blueprint,add_blueprint,adminlogin_blueprint,adduser_blueprint,updateuser_blueprint,deleteuser_blueprint,getspecificuser_blueprint,userrupdate_blueprint,userupdate_blueprint)
from app.main_app.controllers.places import place_namespace
#from app.main_app.controllers.places import(fetch_places_blueprint,add_place_blueprint,delete_place_blueprint,update_place_blueprint)
from app.main_app.controllers.routes import route_namespace
# from app.main_app.controllers.routes import(add_route_blueprint,delete_route_blueprint,fetch_routes_blueprint,update_route_blueprint)
from app.main_app.controllers.bus_features import bus_features_namespace
# from app.main_app.controllers.bus_features import(add_bus_features_blueprint,fetch_bus_features_blueprint,update_bus_features_blueprint,delete_bus_features_blueprint)
from app.main_app.controllers.operators import(add_operator_blueprint,fetch_operators_blueprint,update_operator_blueprint,delete_operator_blueprint)
from app.main_app.controllers.bus import(add_bus_blueprint,fetch_buses_blueprint,delete_bus_blueprint)
from app.main_app.controllers.bustype import(fetch_bus_types_blueprint)
from app.main_app.controllers.bus_operators import(fetch_bus_operators_blueprint,add_bus_operator_blueprint,delete_bus_operator_blueprint,update_bus_operator_blueprint)
from app.main_app.controllers.available_buses import (fetch_available_seats_blueprint,fetch_available_buses_blueprint,fetch_available_bus_blueprint,add_available_bus_blueprint,update_available_bus_blueprint,delete_available_bus_blueprint,fetch_available_buses_by_users_blueprint,book_ticket_blueprint,cancel_ticket_blueprint,history_blueprint,admin_pl_blueprint,booking_history_blueprint,default_revenue_blueprint,custom_revenue_blueprint,routes_revenue_blueprint,notifications_blueprint)
from app.main_app.controllers.otp import(sendotp_blueprint,verifyotp_blueprint,reset_password_blueprint)
blueprint=Blueprint('api',__name__)
api=Api(blueprint,version='1.0',title='jithu',description='API for user management')

api.add_namespace(user_namespace, path='/user')

# api.add_namespace(signup_blueprint)
# api.add_namespace(login_blueprint)
# api.add_namespace(user_blueprint)
# api.add_namespace(update_blueprint)
# api.add_namespace(delete_blueprint)
# api.add_namespace(userlist_blueprint)
# api.add_namespace(user_detail_blueprint)


api.add_namespace(admin_ns,path = '/admin')


# api.add_namespace(admin_blueprint)
# api.add_namespace(add_blueprint)
# api.add_namespace(adminlogin_blueprint)
# api.add_namespace(adduser_blueprint)  # add namespace for admin login and add user blueprint
# api.add_namespace(updateuser_blueprint)  # add namespace for admin login and add user blueprint
# api.add_namespace(userupdate_blueprint)  # add namespace for admin login and add user blueprint
# api.add_namespace(getspecificuser_blueprint)
# api.add_namespace(deleteuser_blueprint)
# api.add_namespace(userrupdate_blueprint)

api.add_namespace(place_namespace,path='/places')
# api.add_namespace(fetch_places_blueprint)
# api.add_namespace(add_place_blueprint)  # add namespace for add place blueprint
# api.add_namespace(delete_place_blueprint)
# api.add_namespace(update_place_blueprint)

api.add_namespace(route_namespace,path = '/routes')
# api.add_namespace(add_route_blueprint)
# api.add_namespace(delete_route_blueprint)
# api.add_namespace(update_route_blueprint)
# api.add_namespace(fetch_routes_blueprint)

api.add_namespace(bus_features_namespace,path = '/busfeatures')

# api.add_namespace(add_bus_features_blueprint)
# api.add_namespace(fetch_bus_features_blueprint)
# api.add_namespace(update_bus_features_blueprint)
# api.add_namespace(delete_bus_features_blueprint)


api.add_namespace(add_operator_blueprint)
api.add_namespace(fetch_operators_blueprint)
api.add_namespace(update_operator_blueprint)
api.add_namespace(delete_operator_blueprint)


api.add_namespace(add_bus_blueprint)
api.add_namespace(fetch_buses_blueprint)
api.add_namespace(delete_bus_blueprint)


api.add_namespace(fetch_bus_types_blueprint)


api.add_namespace(fetch_bus_operators_blueprint)
api.add_namespace(add_bus_operator_blueprint)
api.add_namespace(delete_bus_operator_blueprint)
api.add_namespace(update_bus_operator_blueprint)


api.add_namespace(fetch_available_seats_blueprint)
api.add_namespace(fetch_available_buses_blueprint)
api.add_namespace(fetch_available_bus_blueprint)
api.add_namespace(add_available_bus_blueprint)
api.add_namespace(update_available_bus_blueprint)
api.add_namespace(delete_available_bus_blueprint)
api.add_namespace(fetch_available_buses_by_users_blueprint)
api.add_namespace(book_ticket_blueprint)
api.add_namespace(cancel_ticket_blueprint)
api.add_namespace(history_blueprint)
api.add_namespace(admin_pl_blueprint)
api.add_namespace(booking_history_blueprint)
api.add_namespace(default_revenue_blueprint)
api.add_namespace(custom_revenue_blueprint)
api.add_namespace(routes_revenue_blueprint)
api.add_namespace(notifications_blueprint)





api.add_namespace(sendotp_blueprint)
api.add_namespace(verifyotp_blueprint)
api.add_namespace(reset_password_blueprint)

