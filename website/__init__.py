from flask import Flask
from .views import mysql, auth, main

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'apslev3isactuallyworking'
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = ''
    app.config['MYSQL_DB'] = 'apsle'

    mysql.init_app(app)

    app.register_blueprint(auth)
    app.register_blueprint(main)

    return app
