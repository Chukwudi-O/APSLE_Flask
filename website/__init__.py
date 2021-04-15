from flask import Flask,Blueprint, render_template, request

from .blueprints.Admin_Blueprint import Admin_Blueprint
from .blueprints.Authorize_Blueprint import Authorize_Blueprint
from .blueprints.Teacher_Blueprint import Teacher_Blueprint
from .blueprints.Student_Blueprint import Student_Blueprint
from .blueprints.Subject_Blueprint import Subject_Blueprint
from .SQL_Connector import SQL_Connector

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'apslev3isactuallyworking'
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = ''
    app.config['MYSQL_DB'] = 'apsle'
    app.config['UPLOAD_FOLDER'] = 'C:/Users/chukw/Documents/Flask/APSLE_V3/website/uploads/teacher_uploads'

    mysql = SQL_Connector()
    mysql.init_app(app)
    
    main = Blueprint('main',__name__)
    auth_blueprint = Authorize_Blueprint("auth",__name__,mysql)
    admin_blueprint = Admin_Blueprint("admin",__name__,mysql)
    teacher_blueprint = Teacher_Blueprint("teacher",__name__,mysql)
    student_blueprint = Student_Blueprint("student",__name__,mysql)
    subject_blueprint = Subject_Blueprint("subject",__name__,mysql,app.config['UPLOAD_FOLDER'])

    @main.route('/')
    def index():
        return render_template('index.html')

    app.register_blueprint(main)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(teacher_blueprint)
    app.register_blueprint(student_blueprint)
    app.register_blueprint(subject_blueprint)

    return app
