from app import db

class UserType(db.Model):
    __tablename__ = 'user_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)   
    users = db.relationship('User', backref='user_types', lazy='dynamic') 
    def __repr__(self):
        return '<UserType {}>'.format(self.name)