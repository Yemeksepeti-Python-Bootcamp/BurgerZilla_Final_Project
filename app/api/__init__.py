#api aslında auth olduktan sonra gidilecek endpointler adresler :)
from flask_restx import Api
from flask import Blueprint

from .user.controller import api as user_ns
from .restaurant.controller import api as restaurant_ns

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api_bp = Blueprint("api", __name__)
api = Api(api_bp, version="1.", title="API", description="API",authorizations=authorizations, security='Bearer Auth')


api.add_namespace(user_ns)
api.add_namespace(restaurant_ns)