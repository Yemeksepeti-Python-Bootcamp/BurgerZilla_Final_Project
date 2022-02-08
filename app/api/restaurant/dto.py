from flask_restx import Namespace, fields

class RestaurantDto:

    api = Namespace("restaurant", description="Restaurant related operations")

    restaurant = api.model("Restaurant",{
        "id": fields.Integer(readOnly=True, description="The unique identifier of a restaurant"),
        "name": fields.String(required=True, description="Restaurant name"),
        "userid": fields.Integer(required=True, description="Restaurant owner id")
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