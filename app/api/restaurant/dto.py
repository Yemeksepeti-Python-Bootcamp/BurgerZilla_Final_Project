from flask_restx import Namespace, fields

class RestaurantDto:

    api = Namespace("restaurant", description="Restaurant related operations")

    restaurant = api.model("Restaurant",{
        "id": fields.Integer(readOnly=True, description="The unique identifier of a restaurant"),
        "name": fields.String(required=True, description="Restaurant name"),
        "userid": fields.Integer(required=True, description="Restaurant owner id")
    })

    product = api.model("Product",{
        
        "name": fields.String(required=True, description="Product name"),
        "price": fields.Float(required=True, description="Product price"),
        "description": fields.String(required=True, description="Product description"),
        "image": fields.String(required=True, description="Product image"),
        "restaurantid": fields.Integer(required=True, description="Product restaurant id")
    })

    order = api.model("Order",{
        "productid": fields.Integer(required=True, description="Product id"),
        "restaurantid": fields.Integer(required=True, description="Restaurant id"),
        "userid": fields.Integer(required=True, description="User id"),
        "orderstatus": fields.String(required=True, description="Order status"),
        "quantity": fields.Integer(required=True, description="Order quantity"),
        "address": fields.String(required=True, description="Order address"),
        "orderdate": fields.DateTime(required=True, description="Order date")
    })

    data_resp = api.model("Restaura data response",{
        "status":fields.Boolean,
        "message":fields.String,
        "restaurant":fields.Nested(restaurant)
    })

    data_list_resp = api.model('data_list_resp', {
        'status':fields.Boolean,
        'message':fields.String,
        'restaurants':fields.List(fields.Nested(restaurant))})