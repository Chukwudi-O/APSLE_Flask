from flask import Blueprint, render_template, redirect, url_for, request


class Teacher_Blueprint(Blueprint):
    def __init__(self,name,kind,my_sql):
        Blueprint.__init__(self,name,kind)
        self.current_user = None
        self.mysql = my_sql

        @self.route("/teacher_home", methods=['GET','POST'])
        def teacher_home():
            if request.method == 'POST':
                return render_template("teacher_home.html")
            return render_template("teacher_home.html")
