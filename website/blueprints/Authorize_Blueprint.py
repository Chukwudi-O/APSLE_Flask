from flask import Blueprint, render_template, redirect, url_for, request

class Authorize_Blueprint(Blueprint):
    def __init__(self,name,kind,my_sql):
        Blueprint.__init__(self,name,kind)
        self.current_user = None
        self.mysql = my_sql
            
        @self.route('/login',methods=['GET','POST'])
        def login_post():
            if request.method == "POST":
                usern = request.form['user']
                passw = request.form['pass']

                if (usern == '' or passw == ''):
                    return render_template("login.html")

                if self.mysql.check_credentials(usern,passw,"admin") != None:
                    self.current_user = self.mysql.check_credentials(usern,passw,"admin")
                    return redirect(url_for('admin.admin_home'))
                elif self.mysql.check_credentials(usern,passw,"teacher") != None:
                    self.current_user = self.mysql.check_credentials(usern,passw,"teacher")
                    return redirect(url_for('main.teacher_home'))
                elif self.mysql.check_credentials(usern,passw,"student") != None:
                    self.current_user = self.mysql.check_credentials(usern,passw,"student")
                    return redirect(url_for('main.student_home'))
                return render_template("login.html")
            return render_template('login.html')

        @self.route('/register',methods=['GET','POST'])
        def register():
            return render_template('register.html')