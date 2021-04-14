from flask import Blueprint, render_template, redirect, url_for, request
from .SQL_Connector import SQL_Connector
#from .classes.Users import *

class Views:
    

    def __init__(self):
        self.auth = Blueprint('auth',__name__)
        self.main = Blueprint('main',__name__)
        self.mysql = SQL_Connector()
        #self.current_user = None
    
        @self.auth.route('/login',methods=['GET'])
        def login():
            return render_template('login.html')

        @self.auth.route('/login',methods=['POST'])
        def login_post():
            usern = request.form['user']
            passw = request.form['pass']

            if (usern == '' or passw == ''):
                return render_template("login.html")

            if self.mysql.check_credentials(usern,passw,"admin"):
                return redirect(url_for('main.admin_home'))
            elif self.mysql.check_credentials(usern,passw,"teacher"):
                return redirect(url_for('main.teacher_home'))
            elif self.mysql.check_credentials(usern,passw,"student"):
                return redirect(url_for('main.student_home'))

            return render_template("login.html")

        @self.auth.route('/register',methods=['GET'])
        def register():
            return render_template('register.html')

        #@auth.route('/register', methods=['POST'])
        #def register_post():

        @self.auth.route('/logout')
        def logout():
            return redirect(url_for('main.index'))

        @self.main.route("/admin_home", methods=['GET','POST'])
        def admin_home():
            if request.method == 'GET':
                return render_template("admin_home.html")
            else:
                return redirect(url_for("main.manage_users"))

        @self.main.route("/manage_users",methods=['GET','POST'])
        def manage_users():
            all_users = self.mysql.get_all_users()
            del_msg = ""
            add_msg = ""
            if request.method == 'GET':
                return render_template("manage_users.html",len=len(all_users),all_users=all_users,delete_message=del_msg,add_message=add_msg)
    
            if request.form.get("form_type") == "add_users":
                pass_word = request.form.get("p_word")
                c_pass_word = request.form.get("c_p_word")
                if (c_pass_word != pass_word):
                    add_msg = "Please ensure both passwords are correct"
                    return render_template("manage_users.html",len=len(all_users),all_users=all_users,delete_message=del_msg,add_message=add_msg)

                grade_number = request.form.get("g_num")
                class_number = request.form.get("c_num")
                if (int(grade_number) >= 7 or int(class_number) >= 7):
                    add_msg = "Please ensure class number and grade number are less than 7"
                    return render_template("manage_users.html",len=len(all_users),all_users=all_users,delete_message=del_msg,add_message=add_msg)
                
                first_name = request.form.get("f_name")
                last_name = request.form.get("l_name")
                user_type = request.form["user_type"]
                #gender = request.form["gender"]

                new_user_info = [first_name,last_name,pass_word,user_type,str(grade_number),str(class_number)]
                self.mysql.add_user(new_user_info)
                all_users = self.mysql.get_all_users()
                add_msg = "User \'"+first_name.lower()+last_name.lower()+"\' has been added successfully"
            elif request.form.get("form_type") == "delete_users":
                user_name = request.form.get("user_name")
                user_type = request.form.get("user_type")
                self.mysql.delete_user(user_name,user_type)
                all_users = self.mysql.get_all_users()
                del_msg = "User "+user_name+" was deleted successfully"
            elif request.form.get("form_type") == "edit_users":
                user_info = [request.form.get("user_name"),request.form.get("user_type")]
                #new_user_info = [request.form.get(""),]
            return render_template("manage_users.html",len=len(all_users),all_users=all_users,delete_message=del_msg,add_message=add_msg)

        @self.main.route("/teacher_home", methods=['GET','POST'])
        def teacher_home():
            if request.method == 'GET':
                return render_template("teacher_home.html")
            else:
                print("Form submitted")

        @self.main.route("/student_home", methods=['GET','POST'])
        def student_home():
            if request.method == 'GET':
                return render_template("student_home.html")
            else:
                print("Form submitted")

        @self.main.route('/')
        def index():
            return render_template('index.html')
