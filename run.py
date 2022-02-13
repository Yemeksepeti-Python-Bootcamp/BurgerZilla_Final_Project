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



app = create_app(os.getenv("FLASK_CONFIG") or "default")

migrate = Migrate(app, db)
# with app.app_context():
#     UserType.inital_insert()
#
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