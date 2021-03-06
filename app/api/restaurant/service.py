from datetime import datetime
from flask import current_app
from .utils import load_data, load_order_data, load_product_data
from app.models.schemas import RestaurantSchema
from app.utils import err_resp,internal_err_resp,message
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.restaurant import Restaurant
from app.models.product import Product
from app.models.order import Order
from app import db


class RestaurantService:
    @staticmethod
    def get_restaurant(restaurant_id):
        """
        get a restaurant by id"""
        current_user=get_jwt_identity()
        if not(restaurant := Restaurant.query.get(restaurant_id)):
            return err_resp("restaurant not found","restaurant404",400)
        if current_user != restaurant.userid:
            return err_resp("You are not authorized to see restaurant orders","YoureNotRestaurantOwner 401",401)     
        try:            
            restaurant_data = load_data(restaurant)
            resp=message(True,"Restaurant loaded successfully")
            resp["restaurant"]=restaurant_data
            return resp,200
        except Exception as e:
            current_app.logger.error(e)
            return internal_err_resp()

    @staticmethod
    def delete_restaurant(restaurant_id):    
        """
        Delete a restaurant by id"""
        if not (restaurant := Restaurant.query.get(restaurant_id)):
            return err_resp("restaurant not found","restaurant404",400)
        try:
            db.session.delete(restaurant)
            db.session.commit()
            deleted_restaurant_data=load_data(restaurant)
            resp=message(True,"Restaurant deleted successfully")
            resp["restaurant"]=deleted_restaurant_data
            return resp,200
        except Exception as e:
            current_app.logger.error(e)
            return internal_err_resp()

    @staticmethod
    def create_restaurant(restaurant_data):
        """
        Create a new restaurant"""
        try:
            from .utils import load_data
            current_user = get_jwt_identity()
            restaurant = Restaurant(name=restaurant_data["name"],userid=current_user)
            db.session.add(restaurant)
            db.session.commit()
            created_restaurant_data=load_data(restaurant)
            resp=message(True,"Restaurant created successfully")
            resp["restaurant"]=created_restaurant_data
            return resp,200
        except Exception as e:
            current_app.logger.error(e)
            return internal_err_resp()

    @staticmethod
    def update_restaurant(restaurant_id,restaurant_data):
        """
        update a restaurant by id"""
        if not (restaurant:=Restaurant.query.get(restaurant_id)):
            return err_resp("restaurant not found","restaurant404",400)
        try:
            Restaurant.query.filter_by(id=restaurant_id).update(restaurant_data)
            db.session.commit()
            created_restaurant_data=load_data(restaurant)
            resp=message(True,"Restaurant updated successfully")
            resp["restaurant"]=created_restaurant_data
            return resp,200
        except Exception as e:
            current_app.logger.error(e)
            return internal_err_resp()
        
    @staticmethod
    def get_all_restaurants():
        """
        Get aLL restaurants by owner id"""
        current_user = get_jwt_identity()
        if not(restaurants := Restaurant.query.filter_by(userid=current_user)):
            return err_resp(message="restaurants not found",status=400)
        from .utils import load_data
        try:
            restaurants_data = [load_data(restaurant) for restaurant in restaurants]
            resp=message(True,"Restaurants loaded successfully")
            resp["restaurants"]=restaurants_data
            return resp,200
        except Exception as e:
            current_app.logger.error(e)
            return internal_err_resp()

    @staticmethod
    def get_all_products(restaurant_id): #bir restoranin t??m ??r??nlerini getirir
        """
        Get all products of a specific restaurant
        
        """
        if not(products := Product.query.filter_by(restaurant_id=restaurant_id)):
            return err_resp(message="products not found",status=400)
        from .utils import load_product_data
        try:
            products_data = [load_product_data(product) for product in products]
            resp=message(True,"Products loaded successfully")
            resp["products"]=products_data
            return resp,200
        except Exception as e:
            current_app.logger.error(e)
            return internal_err_resp()
    
    @staticmethod
    def get_product(restaurant_id,product_id):
        """
        Get a product of a specific restaurant
        
        """
        if not(product := Product.query.filter_by(restaurant_id=restaurant_id,id=product_id).first()):
            return err_resp("product not found","productnotfound",400)
        from .utils import load_product_data
        try:
            product_data = load_product_data(product)
            resp=message(True,"Product loaded successfully")
            resp["product"]=product_data
            return resp,200
        except Exception as e:
            current_app.logger.error(e)
            return internal_err_resp()
    
    @staticmethod
    def create_product(restaurant_id,product_data):
        """
        Create a new product"""
        try:            
            current_user = get_jwt_identity()
            if not(restaurant := Restaurant.query.get(restaurant_id)):
                return err_resp("Restaurant not found","restaurant404",400)
            if current_user != restaurant.userid:
                return err_resp("You are not authorized to create product","YoureNotRestaurantOwner 401",401)
            product = Product(name=product_data["name"],price=product_data["price"],description=product_data["description"],image=product_data["image"],restaurant_id=restaurant_id)
            db.session.add(product)
            db.session.commit()
            created_product_data=load_product_data(product)
            resp=message(True,"Product created successfully")
            resp["product"]=created_product_data
            return resp,200
        except Exception as e:
            current_app.logger.error(e)
            return internal_err_resp()

    @staticmethod
    def create_order(restaurant_id,order_data):
        """
        Create a new order"""
        try:            
            current_user = get_jwt_identity()
            order = Order(userid=current_user,restaurant_id=restaurant_id,
            product_id=order_data["product_id"],orderstatus="NEW",orderdate=datetime.utcnow())
            db.session.add(order)
            db.session.commit()
            created_order_data=load_order_data(order)
            resp=message(True,"Product created successfully")
            resp["order"]=created_order_data
            return resp,200
        except Exception as e:
            current_app.logger.error(e)
            return internal_err_resp()

    @staticmethod
    def get_order(restaurant_id,order_id):
        """
        Get an order of a specific restaurant
        
        """
        current_user=get_jwt_identity()
        if not(restaurant := Restaurant.query.get(restaurant_id)):
            return err_resp("restaurant not found","restaurant404",400)
        if current_user != restaurant.userid:
            return err_resp("You are not authorized to see restaurant orders","YoureNotRestaurantOwner 401",401)  
        if not(order := Order.query.filter_by(restaurant_id=restaurant_id,id=order_id).first()):
            return err_resp("This order not found in given restaurant","OrderNotFound 404",404)
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
    def get_all_orders(restaurant_id):
        """
        Get all orders of a specific restaurant
        
        """
        current_user=get_jwt_identity()
        if not(restaurant := Restaurant.query.get(restaurant_id)):
            return err_resp("restaurant not found","restaurant404",400)
        if current_user != restaurant.userid:
            return err_resp("You are not authorized to see restaurant orders","YoureNotRestaurantOwner 401",401)            
        if not(orders := Order.query.filter_by(restaurant_id=restaurant_id)):
            return err_resp("orders not found","order404",400)
        from .utils import load_order_data
        try:
            orders_data = [load_order_data(order) for order in orders]
            if len(orders_data)==0:
                resp=message(True,"Restaurant has no orders yet")
            else:
                resp=message(True,"Orders loaded successfully")
            resp["orders"]=orders_data
            return resp,200
        except Exception as e:
            current_app.logger.error(e)
            return internal_err_resp()

    @staticmethod
    def update_order(restaurant_id,order_id,order_data):
        """
        Update an order of a specific restaurant
        
        """
        current_user=get_jwt_identity()
        if not(restaurant := Restaurant.query.get(restaurant_id)):
            return err_resp("restaurant not found","restaurant404",400)
        if current_user != restaurant.userid:
            return err_resp("You are not authorized to change restaurant orders","YoureNotRestaurantOwner 401",401)  
        if not(order := Order.query.filter_by(restaurant_id=restaurant_id,id=order_id).first()):
            return err_resp("This order not found in given restaurant","OrderNotFound 404",404)
        try:
            order_status = order_data["orderstatus"]
            Order.query.filter_by(id=order_id).update({"orderstatus":order_status})
            db.session.commit()
            updated_order_data=load_order_data(order)
            resp=message(True,"Order updated successfully")
            resp["order"]=updated_order_data
            return resp,200
        except Exception as e:
            current_app.logger.error(e)
            return internal_err_resp()

    @staticmethod
    def update_product(restaurant_id,product_id,product_data):
        """
        Update a product of a specific restaurant
        
        """
        #product_data = {key:value for (key,value) in product_data.items()}
        if not(product := Product.query.filter_by(restaurant_id=restaurant_id,id=product_id).first()):
            return err_resp(message="product not found",status=400)
        try:
            Product.query.filter_by(id=product_id).update(product_data)
            db.session.commit()
            updated_product_data=load_product_data(product)
            resp=message(True,"Product updated successfully")
            resp["product"]=updated_product_data
            return resp,200
        except Exception as e:
            current_app.logger.error(e)
            return internal_err_resp()

    @staticmethod
    def delete_product(restaurant_id,product_id):
        """
        Delete a product of a specific restaurant
        
        """
        if not(product := Product.query.filter_by(restaurant_id=restaurant_id,id=product_id).first()):
            return err_resp(message="product or restaurant not found",status=400)
        try:
            db.session.delete(product)
            db.session.commit()
            deleted_product_data=load_data(product)
            resp=message(True,"product deleted successfully")
            resp["product"]=deleted_product_data
            return resp,200
        except Exception as e:
            current_app.logger.error(e)
            return internal_err_resp()