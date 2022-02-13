import os

from dotenv import load_dotenv
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

import click
from  flask_migrate import Migrate
from app import create_app, db
from app.models.restaurant import Restaurant
from app.models.usertype import UserType
from app.models.user import User
from app.models.product import Product



app = create_app(os.getenv("FLASK_CONFIG") or "default")

migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Restaurant=Restaurant)


@app.cli.command()
@click.argument("test_names", nargs=-1)
def test(test_names):
    """ Run unit tests """
    import unittest

    if test_names:
        """ Run specific unit tests.
        Example:
        $ flask test tests.test_auth_api tests.test_user_model ...
        """
        tests = unittest.TestLoader().loadTestsFromNames(test_names)

    else:
        tests = unittest.TestLoader().discover("tests", pattern="test*.py")

    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0

    # Return 1 if tests failed, won't reach here if succeeded.
    return 1

@app.cli.command()
def insertdb():
    # initial data insertions
    if UserType.query.first() is None:
        usertypes=[
            UserType(id=0,name='Restaurant'),
            UserType(id=1,name='User')
            ]
        db.session.bulk_save_objects(usertypes)
        db.session.commit()
        users=[
            User(username="ugurozy",name="Uğur Özyalı",email="ugurozy@musteri.nett",password="123",usertype_id=0),
            User(username="ezelozy",name="Ezel Özyalı",email="ezelozy@musteri.nett",password="123",usertype_id=0),
            User(username="omerk",name="Ömer Kandor",email="omerk@restoran.nett",password="123",usertype_id=1),
            User(username="tuncd",name="Tunç Dimdal",email="tuncd@restoran.nett",password="123",usertype_id=1)
            ] 
        db.session.bulk_save_objects(users)
        db.session.commit()
        restaurants=[
            Restaurant(name="Dombili Burger",userid=3),
            Restaurant(name="Dublemumble",userid=4)
        ]
        db.session.bulk_save_objects(restaurants)
        db.session.commit()
        products=[
            Product(name="Bombili",price=30,description="Meşhur dombili burger, özel soslu, sarmısaklı ve soğanlı",image="x-txmt-filehandle://job/Preview/resource/dombili1.jpg",restaurant_id=1),
            Product(name="Duble Peynirli",price=50,description="Çift katlı, mozerella ve çedarla bezenmiş dombili burger",image="x-txmt-filehandle://job/Preview/resource/dombili2.jpg",restaurant_id=1),
            Product(name="Aç doyuran",price=75,description="Üç katlı, zeytin soslu,özel ketçap ve tatlı mayonezli burger ve patates",image="x-txmt-filehandle://job/Preview/resource/dombili3.jpg",restaurant_id=1),
            Product(name="Tekkatlı",price=25,description="Bol domatesli, özel muble soslu",image="x-txmt-filehandle://job/Preview/resource/dublemuble1.jpg",restaurant_id=2),
            Product(name="Dublemuble",price=45,description="Çift katlı, beyaz peynir + kaşar peynir soslu, duble hamburger",image="x-txmt-filehandle://job/Preview/resource/dublemuble2.jpg",restaurant_id=2),
            Product(name="Delüks",price=70,description="Özel dublemuble burger, patates ve eritme peynirle birlikte",image="x-txmt-filehandle://job/Preview/resource/dublemuble3.jpg",restaurant_id=2)
        ]
        db.session.bulk_save_objects(products)
        db.session.commit()


