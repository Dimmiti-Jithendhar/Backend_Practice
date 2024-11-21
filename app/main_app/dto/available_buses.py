from flask_restx import Namespace
#dto -- data transfer object
class availablebusesdto:
    fetch_available_seats_api = Namespace('fetch_available_seats',description="API for fetching particular bus")
    fetch_available_buses_api = Namespace('fetch_available_buses', description="API for fetching available buses")
    fetch_available_bus_api = Namespace('fetch_available_bus',description = "API for fetching the avaialable bus based on query params")
    fetch_available_buses_by_users_api=Namespace('fetch_available_buses_by_users', description="API for fetching available buses by users")
    add_available_bus_api = Namespace('add_available_bus', description="API for adding a available buses")
    delete_available_bus_api = Namespace('delete_available_bus', description="API for deleting a available buses")
    update_available_bus_api = Namespace('update_available_bus', description="API for updating a available buses")
    book_ticket_api = Namespace('book_ticket',description="API for booking a ticket")
    cancel_ticket_api = Namespace('cancel_ticket',description="API for cancelling a ticket")
    history_api = Namespace('booking_history',description="API for Booking history")
    admin_pl_api = Namespace('admin_pl',description = "API for admin getting passengers list ")
    booking_history_api = Namespace('booking_history_up',description = "API for past and upcoming bookings")
    default_revenue_api = Namespace('default_revenue', description = "API for getting the default revenue for months and years and till now")
    custom_revenue_api = Namespace('custom_revenue',description = "API for getting the revenue generated in between the dates " )
    routes_revenue_api = Namespace('routes_revenue', description = "API for getting the revenue generated on the routes")
    notifications_api = Namespace('notifications',description = 'API for user notifications ')












#Controllers implement the logic for routing and HTTP methods (like GET, POST, PUT, DELETE).
#The purpose of the DTO is to provide a standardized way to handle the input/output for the API operations. It acts as an intermediary between the controller and the actual models 
#DTO's provides the Automatically generate the Swagger/OpenAPI documentation for the APIs.

#data = request.get_json()
# Extracts the JSON payload sent in the HTTP request body and stores it in the variable data.




