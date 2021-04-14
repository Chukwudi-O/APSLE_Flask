from flask import Flask
from .views import Views

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'apslev3isactuallyworking'
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = ''
    app.config['MYSQL_DB'] = 'apsle'

    views = Views()
    views.mysql.init_app(app)

    app.register_blueprint(views.main)
    app.register_blueprint(views.auth)

    return app
