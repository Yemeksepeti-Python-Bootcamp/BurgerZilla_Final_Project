from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from .service import RestaurantService
from .dto import RestaurantDto

api = RestaurantDto.api #restaurant namespace
restaurant=RestaurantDto.restaurant
product=RestaurantDto.product
order=RestaurantDto.order
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
        return RestaurantService.create_restaurant(user_id,data)

@api.route("/<int:restaurant_id>/products")
class RestaurantProducts(Resource):
    @api.doc("Get products of a specific restaurant",responses={200:"Success",500:"Internal Server Error"})
    @jwt_required()
    def get(self,restaurant_id):
        """
        Get all products of a specific restaurant"""
        return RestaurantService.get_all_products(restaurant_id)

    @api.doc("Create a new product",responses={200:"Success",500:"Internal Server Error"})
    @api.expect(product)
    @jwt_required()
    def post(self,restaurant_id):
        """
        Create a new product of a specific restaurant"""
        data = request.get_json()
        return RestaurantService.create_product(restaurant_id,data)

@api.route("/<int:restaurant_id>/products/<int:product_id>")
class RestaurantProducts(Resource):
    @api.doc("Get specific product from specific restaurant",responses={200:"Success",500:"Internal Server Error"})
    @jwt_required()
    def get(self,restaurant_id,product_id):
        """
        Get all products of a specific restaurant"""
        return RestaurantService.get_product(restaurant_id,product_id)
    
    @api.doc("Update a specific product",responses={200:"Success",500:"Internal Server Error"})
    @api.expect(product)
    @jwt_required()
    def put(self,restaurant_id,product_id):
        """
        Update a specific product of a specific restaurant"""
        data = request.get_json()
        return RestaurantService.update_product(restaurant_id,product_id,data)

##############################################################################################
# API/RESTAURANT/ORDER
##############################################################################################

@api.route("/<int:restaurant_id>/orders/<int:order_id>")
class RestaurantOrders(Resource):
    @api.doc("Get specific order from specific restaurant",responses={200:"Success",500:"Internal Server Error"})
    @jwt_required()
    def get(self,restaurant_id,order_id):
        """
        Get all orders of a specific restaurant
        """
        return RestaurantService.get_order(restaurant_id,order_id)

    @api.doc("Update a status of an order",responses={200:"Success",500:"Internal Server Error"})
    #@api.expect(order)
    @jwt_required()
    def put(self,restaurant_id,order_id):
        """
        Update a specific order of a specific restaurant
        """
        data = request.get_json()
        return RestaurantService.update_order(restaurant_id,order_id,data)

@api.route("/<int:restaurant_id>/orders")
class RestaurantOrders(Resource):
    @api.doc("Get all orders of a specific restaurant",responses={200:"Success",500:"Internal Server Error"})
    #@jwt_required() 
    def get(self,restaurant_id):
        """
        Get all orders of a specific restaurant
        """
        return RestaurantService.get_all_orders(restaurant_id)

    @api.doc("Create a new order",responses={200:"Success",500:"Internal Server Error"})
    @api.expect(order)
    @jwt_required()
    def post(self,restaurant_id):
        """
        Create a new product of a specific restaurant"""
        data = request.get_json()
        return RestaurantService.create_order(restaurant_id,data)
    