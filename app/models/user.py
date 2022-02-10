from datetime import datetime
from app import db, bcrypt

# Alias common DB names
Column = db.Column
Model = db.Model
relationship = db.relationship
DEFAULT_USERTYPE = 0
class User(Model):
    """ User model for storing user related data """

    id = Column(db.Integer, primary_key=True)
    email = Column(db.String(64), unique=True, index=True)
    username = Column(db.String(15), unique=True, index=True)
    name = Column(db.String(64))
    password_hash = Column(db.String(128))
    usertype_id = Column(db.Integer, db.ForeignKey('user_types.id'), default=DEFAULT_USERTYPE)
    restaurants=relationship('Restaurant', backref='user', lazy='dynamic')
    orders=relationship('Order', backref='user', lazy='dynamic')
    
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"
