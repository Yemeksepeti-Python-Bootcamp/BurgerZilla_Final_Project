from flask_restx import Namespace, fields

class UserDto:

    api = Namespace("user", description="User related operations")

    user = api.model("User object", {
        "email":fields.String,
        "name":fields.String,
        "username":fields.String,
        "usertype_id":fields.Integer
    })

    data_resp = api.model("User data response",{
        "status":fields.Boolean,
        "message":fields.String,
        "user":fields.Nested(user)
    })

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
        "orderdate": fields.DateTime(required=True, description="Order date")
    })