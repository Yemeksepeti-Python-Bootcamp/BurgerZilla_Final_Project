from app import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    orderstatus = db.Column(db.String(64))
    quantity = db.Column(db.Integer, default=1)
    address = db.Column(db.String(64))
    orderdate = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Order {}>'.format(self.id)