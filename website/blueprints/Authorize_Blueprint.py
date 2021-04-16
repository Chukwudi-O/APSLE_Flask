from flask import Blueprint, render_template, redirect, url_for, request

class Authorize_Blueprint(Blueprint):
    def __init__(self,name,kind,c_checker):
        Blueprint.__init__(self,name,kind)
        self.current_user = None
        self.cred_check = c_checker
            
        @self.route('/login',methods=['GET','POST'])
        def login():
            if request.method == "POST":
                usern = request.form['user']
                passw = request.form['pass']

                if (usern == '' or passw == ''):
                    return render_template("login.html")

                if self.cred_check.check_credentials(usern,passw,"admin") is not None:
                    self.current_user = self.cred_check.check_credentials(usern,passw,"admin")
                    return redirect(url_for('admin.admin_home'))
                elif self.cred_check.check_credentials(usern,passw,"teacher") is not None:
                    self.current_user = self.cred_check.check_credentials(usern,passw,"teacher")
                    return redirect(url_for('teacher.teacher_home'))
                elif self.cred_check.check_credentials(usern,passw,"student") is not None:
                    self.current_user = self.cred_check.check_credentials(usern,passw,"student")
                    return redirect(url_for('student.student_home'))
                return render_template("login.html")
            return render_template('login.html')

        @self.route('/register',methods=['GET','POST'])
        def register():
            return render_template('register.html')