from app import db
from app.models.restaurant import Restaurant
from app.models.schemas import RestaurantSchema

from tests.utils.base import BaseTestCase

class TestRestaurantModel(BaseTestCase):
    def test_create_restaurant(self):
        # is restaurant id generated?
        r = Restaurant(name="TestRestaurant1",userid=1)
        db.session.add(r)
        db.session.commit()
        self.assertTrue(r.id > 0)
    
    def test_update_restaurant(self):
        # is updating properly?
        r= Restaurant(name="TestRestaurant2",userid=1)
        db.session.add(r)
        db.session.commit()
        r.name = "TestRestaurant2_updated"
        db.session.commit()
        self.assertTrue(r.name == "TestRestaurant2_updated")


    def test_delete_restaurant(self):
        # is deleting properly?
        r = Restaurant(name="TestRestaurant3",userid=1)
        db.session.add(r)
        db.session.commit()
        db.session.delete(r)
        db.session.commit()
        res = Restaurant.query.filter_by(name="TestRestaurant3").first()        
        self.assertTrue(res is None)


    def test_schema(self):
        # R = Restaurant(userid=1)
        r= Restaurant(name="TestRestaurant4",userid=1)
        r_dump = RestaurantSchema().dump(r)
        self.assertTrue(r_dump["name"] == "TestRestaurant4")