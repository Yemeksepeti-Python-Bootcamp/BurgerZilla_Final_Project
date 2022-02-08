from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from .service import RestaurantService
from .dto import RestaurantDto

api = RestaurantDto.api #restaurant namespace
restaurant=RestaurantDto.restaurant
data_resp=RestaurantDto.data_resp
data_list_resp=RestaurantDto.data_list_resp

@api.route('/<int:restaurant_id>')
class Restaurant(Resource):
    @api.doc('get specific restaurant',responses={
        200:('Success',data_resp),
        400:'Invalid Restaurant ID',
    })
    @jwt_required()
    def get(self,restaurant_id):
        """ get specific restaurant """
        return RestaurantService.get_by_id(restaurant_id)
    
    @api.doc("Delete a specific restaurant",responses={
        200:"Success"})
    @jwt_required()
    def delete(self,restaurant_id):
        """ Delete a specific restaurant"""
        return RestaurantService.delete_by_id(restaurant_id)

    @api.doc("Update a specific restaurant",responses={200:"Success"})
    @api.expect(restaurant)
    @jwt_required()
    def put(self,restaurant_id):
        """ Update a specific restaurant"""
        data = request.get_json()
        return RestaurantService.update_by_id(restaurant_id,data)

@api.route("/user/<int:user_id>")
class RestaurantList(Resource):
    @api.doc("Get restaurant by owner id",responses={200:"Success",500:"Internal Server Error"})
    @jwt_required()
    def get(self,user_id):
        """
        Get all restaurants of a specific user"""
        return RestaurantService.get_all(user_id)


    @api.doc("Create a new restaurant",responses={200:"Success",500:"Internal Server Error"})
    @api.expect(restaurant)
    @jwt_required()
    def post(self,user_id):
        """
        Create a new restaurant whose owner is the user_id"""
        data = request.get_json()
        return RestaurantService.create(user_id,data)