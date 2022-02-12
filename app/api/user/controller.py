from http.client import responses
from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required


from .service import UserService
from .dto import UserDto

api  = UserDto.api
data_resp = UserDto.data_resp
restaurant=UserDto.restaurant
product=UserDto.product
order=UserDto.order

@api.route("/")
class UserGet(Resource):
    @api.doc("get user details by username",responses={
        200:("Success",data_resp),
        404:"User Not Found",
    })
    @jwt_required()
    def get(self):
        """get user data"""
        return UserService.get_user_data()

@api.route("/orders")
class UserOrder(Resource):
    @api.doc("Create a new order",responses={200:"Success",500:"Internal Server Error"})
    @api.expect(order)
    @jwt_required()
    def post(self):
        """
        Create a new order"""
        data = request.get_json()
        return UserService.create_order(data)

    @api.doc("Get all orders of a user",responses={200:"Success",500:"Internal Server Error"})
    @jwt_required()
    def get(self):
        """
        Get all orders of a user"""
        return UserService.get_all_orders()

@api.route("/orders/<int:order_id>")
class UserOrder(Resource):
    @api.doc("Get a specific order",responses={200:"Success",500:"Internal Server Error"})
    @jwt_required()
    def get(self,order_id):
        """
        Get a specific order"""
        return UserService.get_order_by_id(order_id)
    
    @api.doc("Update a specific order",responses={200:"Success",500:"Internal Server Error"})
    @api.expect(order)
    @jwt_required()
    def put(self,order_id):
        """
        Update a specific order"""
        data = request.get_json()
        return UserService.update_order(order_id,data)

@api.route("/orders/cancel/<int:order_id>")
class CancelOrder(Resource):
    @api.doc("Cancel an order",responses={200:"Success",500:"Internal Server Error"})
    @api.expect(order)
    @jwt_required()
    def put(self,order_id):
        """
        Cancel an order"""
        return UserService.cancel_order(order_id)