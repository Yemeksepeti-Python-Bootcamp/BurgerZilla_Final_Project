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
    def get_user_data(): #örn bunu controllerda getbyusername için kullanıyoruz.
        """
        get user data"""
        user_id = get_jwt_identity()
        if not (user := User.query.filter_by(id=user_id).first()):
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
    def get_all_orders():
        """
        Get all orders of a specific user
        
        """
        user_id=get_jwt_identity()
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
        user_id=get_jwt_identity()
        if not(order := Order.query.filter_by(id=order_id).first()):
            return err_resp("Order not found","order_404",404)
        if order.userid!=user_id:
            return err_resp("This order is not yours.","order_404",404)
        from .utils import load_order_data
        try:
            order_data = load_order_data(order)
            resp=message(True,"Order loaded successfully")
            resp["order"]=order_data
            return resp,200
        except Exception as e:
            current_app.logger.error(e)
            return internal_err_resp()
    
    @staticmethod
    def create_order(data):
        """
        Create a new order
        
        """
        user_id=get_jwt_identity()
        if not(product := Product.query.filter_by(id=data["product_id"]).first()):
            return err_resp("product not found","product_404",404)
        try:
            from .utils import load_product_data
            product_data=load_product_data(product)
            if product_data["restaurant_id"]!=data["restaurant_id"]:
                return err_resp("Given restaurant does not have this product","product_404",404)
            order = Order(userid=user_id,restaurant_id=data["restaurant_id"],
            product_id=data["product_id"],quantity=data["quantity"],orderstatus="NEW",orderdate=datetime.utcnow())
            db.session.add(order)
            db.session.commit()
            return message(True,"Order created successfully")
        except Exception as e:
            current_app.logger.error(e)
            return internal_err_resp()

    @staticmethod
    def update_order(order_id,order_data):
        """
        Update a specific order
        
        """
        try:
            user_id=get_jwt_identity()
            if not(order := Order.query.filter_by(id=order_id).first()):
                return err_resp("order not found","order_404",404)
            if order.userid!=user_id:
                return err_resp("You can only update your orders","order_404",404)
            if order.orderstatus=="NEW": #orderin statusu
                    Order.query.filter_by(id=order_id).update(order_data)
                    db.session.commit()
                    return message(True,"Order cancelled successfully")
            else:
                return err_resp("You can only update orders with status 'NEW'","order_404",404)
        except Exception as e:
            current_app.logger.error(e)
            return internal_err_resp()

    @staticmethod
    def cancel_order(order_id):
        """
        Update a specific order
        
        """
        try:
            user_id=get_jwt_identity()
            if not(order := Order.query.filter_by(id=order_id).first()):
                return err_resp("order not found","order_404",404)
            if order.userid!=user_id:
                return err_resp("You can only cancel your orders","order_404",404)
            if order.orderstatus=="NEW": #orderin statusu                
                    Order.query.filter_by(id=order_id).update({"orderstatus":"CANCELLED"})
                    db.session.commit()
                    return message(True,"Order cancelled successfully")
            else:
                return err_resp("You can only cancel orders status with 'NEW'","order_404",404)
        except Exception as e:
            current_app.logger.error(e)
            return internal_err_resp()