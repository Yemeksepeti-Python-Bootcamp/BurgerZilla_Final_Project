from app import db

class UserType(db.Model):
    __tablename__ = 'user_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)   
    users = db.relationship('User', backref='user_types', lazy='dynamic') 
    def __repr__(self):
        return '<UserType {}>'.format(self.name)

    @staticmethod #BURAYI SONRADAN SİLEBİLİRİM run.py de çağırdığım  yerle birlikte
    def inital_insert():        
        if UserType.query.first() is None:
            restoran=UserType(id=0,name='Restaurant')
            user=UserType(id=1,name='User')
            db.session.add(restoran)
            db.session.add(user)
            db.session.commit()
            
