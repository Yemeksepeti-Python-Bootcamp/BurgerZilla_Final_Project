source env/bin/activate
flask db init
flask db migrate
flask db upgrade
flask insertdb
flask run --host=0.0.0.0