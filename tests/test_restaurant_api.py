import json
from pkgutil import get_data
from re import A

from flask_jwt_extended import create_access_token

from app import db
from app.models.restaurant import Restaurant

from utils.base import BaseTestCase

def get_restaurant_data(self,accestoken,restaurant_id):
    return self.client.get(
        f"/api/restaurant/{restaurant_id}",
        headers={"Authorization": "Bearer " + accestoken},
    )

def get_restaurants_data(self,accestoken):
    return self.client.get(
        f"/api/restaurant/user",
        headers={"Authorization": "Bearer " + accestoken},
    )

def post_restaurant_data(self,accestoken,restaurant_data):
    return self.client.post(
        f"/api/restaurant",
        data=json.dumps(restaurant_data),
        content_type="application/json",
        headers={"Authorization": "Bearer " + accestoken},
    )

def put_restaurant_data(self,accesstoken,restaurant_data,restaurant_id):
    return self.client.put(
        f"/api/restaurant/{restaurant_id}",
        data=json.dumps(restaurant_data),
        content_type="application/json",
        headers={"Authorization": "Bearer " + accesstoken},
    )

def delete_restaurant_data(self,accesstoken,restaurant_id):
    return self.client.delete(
        f"/api/restaurant/{restaurant_id}",
        headers={"Authorization": "Bearer " + accesstoken},
    )

class TestRestaurantBlueprint(BaseTestCase):
    def test_restaurant_get(self):
        """
        Test for getting a restaurant
        """
        r = Restaurant(name="TestRestaurant1",userid=1)
        db.session.add(r)
        db.session.commit()
        
        access_token = create_access_token(identity=1)

        restaurant_resp = get_restaurant_data(self,access_token,r.id)
        restaurant_data = json.loads(restaurant_resp.data.decode())

        self.assertTrue(restaurant_data.status == 200)
        self.assertTrue(restaurant_data["restaurant"]['name'] == 'TestRestaurant1')
        self.assertTrue(restaurant_data["restaurant"]['userid'] == 1)

        data_404_resp = get_restaurant_data(self,access_token,1)
        self.assertEquals(data_404_resp.status_code, 400)