from flask import Blueprint, render_template, redirect, url_for, request


class Student_Blueprint(Blueprint):
    def __init__(self,name,kind,c_checker):
        Blueprint.__init__(self,name,kind)
        self.current_user = None
        self.cred_check = c_checker

        @self.route("/student_home", methods=['GET','POST'])
        def student_home():
            self.current_user = self.cred_check.current_user
            return render_template("student_home.html")
