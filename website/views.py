from flask import Blueprint, render_template, redirect, url_for, request
from flask_mysqldb import MySQL

mysql = MySQL()
auth = Blueprint('auth',__name__)

@auth.route('/login')
def login():
    return render_template('login.html',methods=['GET'])

@auth.route('/login',methods=['POST'])
def login_post():
    usern = request.form['user']
    passw = request.form['pass']

    if (usern == '' or passw == ''):
        return render_template("login.html")
    
    conn = mysql.connection.cursor()

    string = 'SELECT * from adminlogins'
    conn.execute(string)
    admins = conn.fetchall()

    string = 'SELECT * from teacherlogins'
    conn.execute(string)
    teachers = conn.fetchall()

    string = 'SELECT * from studentlogins'
    conn.execute(string)
    students = conn.fetchall()

    for i in range(len(admins)):
        if (admins[i][1] == usern and admins[i][2] == passw):
            conn.close()
            return render_template("admin_home.html")
        elif (teachers[i][1] == usern and teachers[i][2] == passw):
            conn.close()
            return render_template("teacher_home.html")
        elif (students[i][1] == usern and students[i][2] == passw):
            conn.close()
            return render_template("student_home.html")
    return render_template("login.html")

@auth.route('/register',methods=['GET'])
def register():
    return render_template('register.html')

#@auth.route('/register', methods=['POST'])
#def register_post():

@auth.route('/logout')
def logout():
    return redirect(url_for('main.index'))

main = Blueprint('main',__name__)

@main.route('/')
def index():
    return render_template('index.html')
