from http.client import responses
from flask_restx import Resource
from flask_jwt_extended import jwt_required


from .service import UserService
from .dto import UserDto

api  = UserDto.api
data_resp = UserDto.data_resp
restaurant=UserDto.restaurant
product=UserDto.product
order=UserDto.order

@api.route("/<string:username>")
class UserGet(Resource):
    @api.doc("get user details by username",responses={
        200:("Success",data_resp),
        404:"User Not Found",
    })
    #@jwt_required()
    def get(self,username):
        """get user data"""
        return UserService.get_user_data(username)
    


@api.route("/<int:user_id>")
class UserOrders(Resource):
    @api.doc("Get all orders of a user",responses={200:"Success",500:"Internal Server Error"})
    #@jwt_required()
    def get(self,user_id):
        """
        Get all orders of a user"""
        return UserService.get_all_orders(user_id)

@api.route("/orders/<int:order_id>")
class UserOrder(Resource):
    @api.doc("Get a specific order",responses={200:"Success",500:"Internal Server Error"})
    #@jwt_required()
    def get(self,order_id):
        """
        Get a specific order"""
        return UserService.get_order_by_id(order_id)