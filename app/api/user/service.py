from datetime import datetime
from flask import current_app
from app.models.schemas import RestaurantSchema
from app.utils import err_resp,internal_err_resp,message
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.restaurant import Restaurant
from app.models.product import Product
from app.models.order import Order
from app import db
from app.models.user import User

class UserService:
    @staticmethod
    def get_user_data(username): #örn bunu controllerda getbyusername için kullanıyoruz.
        """
        get user data"""
        if not (user := User.query.filter_by(username=username).first()):
            return err_resp("User Not Found","user_404",404)
        
        from .utils import load_data

        try:
            user_data = load_data(user)
            resp = message(True,"User data sent")
            resp["user"] = user_data
            return resp,200
        except Exception as e:
            print("Error User:",e)
            current_app.logger.error(e)
            return internal_err_resp()

    @staticmethod
    def get_all_orders(user_id):
        """
        Get all orders of a specific user
        
        """
        if not(orders := Order.query.filter_by(userid=user_id)):
            return err_resp("orders not found","orders_404",404)
        from .utils import load_order_data
        try:
            orders_data = [load_order_data(order) for order in orders]
            if len(orders_data)==0:
                resp=message(True,"User has no orders yet")
            else:
                resp=message(True,"Orders loaded successfully")
            resp["orders"]=orders_data
            return resp,200
        except Exception as e:
            current_app.logger.error(e)
            return internal_err_resp()
    
    @staticmethod
    def get_order_by_id(order_id):
        """
        Get a specific order
        
        """
        if not(order := Order.query.filter_by(id=order_id).first()):
            return err_resp("order not found","order_404",404)
        from .utils import load_order_data
        try:
            order_data = load_order_data(order)
            resp=message(True,"Order loaded successfully")
            resp["order"]=order_data
            return resp,200
        except Exception as e:
            current_app.logger.error(e)
            return internal_err_resp()
