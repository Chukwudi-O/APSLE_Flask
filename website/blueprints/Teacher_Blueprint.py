from flask import Blueprint, render_template, redirect, url_for, request


class Teacher_Blueprint(Blueprint):
    def __init__(self,name,kind,c_checker):
        Blueprint.__init__(self,name,kind)
        self.current_user = None
        self.cred_check = c_checker

        @self.route("/teacher_home", methods=['GET','POST'])
        def teacher_home():
            self.current_user = self.cred_check.current_user
            return render_template("teacher_home.html",current_user=self.current_user)

        @self.route("/manage_tests", methods=['GET','POST'])
        def manage_tests():
            if request.method == "POST":
                pass
            return render_template("manage_tests.html")
