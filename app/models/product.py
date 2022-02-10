from app import db


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=False)    
    price = db.Column(db.Float)
    description = db.Column(db.String(140))
    image = db.Column(db.String(140))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    orders = db.relationship('Order', backref='product', lazy='dynamic')
    
    def __repr__(self):
        return '<Product {}>'.format(self.name)