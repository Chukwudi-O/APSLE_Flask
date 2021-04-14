from flask import Blueprint, render_template, redirect, url_for, request


class Student_Blueprint(Blueprint):
    def __init__(self,name,kind,my_sql):
        Blueprint.__init__(self,name,kind)
        self.current_user = None
        self.mysql = my_sql

        @self.route("/student_home", methods=['GET','POST'])
        def student_home():
            if request.method == 'POST':
                return render_template("student_home.html")
            return render_template("student_home.html")
            