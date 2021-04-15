import os
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.utils import secure_filename

class Subject_Blueprint(Blueprint):
    def __init__(self,name,kind,my_sql,config):
        Blueprint.__init__(self,name,kind)
        self.current_user = None
        self.mysql = my_sql
        self.upload_folder = config

        @self.route("/maths", methods=['GET','POST'])
        def maths():
            self.current_user = self.mysql.current_user

            if request.method == "POST":
                if request.form['form_type'] == "upload":
                    file = request.files['file']
                    if file.filename == "":
                        flash('No file selected')
                        return redirect(request.url)
                    
                    upload_name = request.form['material_name']
                    upload_description = request.form['material_description']
                    upload_type = request.form['material_type']
                    file_name = secure_filename(file.filename)
                    upload_info = [upload_name,upload_description,"MATH",upload_type,file_name]
                    self.mysql.upload_file(upload_info)
                    file.save(os.path.join(self.upload_folder+"teacher_uploads",file_name))
                    return redirect(request.url)
                elif request.form['form_type'] == 'delete':
                    if request.form['mat_type'] == 'assignments':
                        mat_id = request.form['assignment_id']
                    else:
                        mat_id = request.form['notes_id']
                    self.mysql.delete_material(mat_id)
                elif request.form['form_type'] == 'submission':
                    file = request.files['file']
                    assignment_id = request.form['assignment_id']
                    file_name = secure_filename(file.filename)
                    file.save(os.path.join(self.upload_folder+"student_submissions",file_name))
                    sub_info = [file_name,"MATH","submission",assignment_id]
                    self.mysql.upload_file(sub_info)

            subject_notes = self.mysql.get_subject_info("MATH","lecture_notes",self.current_user.grade_number,self.current_user.class_number)
            subject_assignments = self.mysql.get_subject_info("MATH","assignment",self.current_user.grade_number,self.current_user.class_number)      
            return render_template("subject.html",subject="Mathematics",user=self.current_user,notes=subject_notes,
            assignments=subject_assignments,notes_len=len(subject_notes),assignments_len=len(subject_assignments))
        
        @self.route("/english", methods=['GET','POST'])
        def english():
            self.current_user = self.mysql.current_user

            if request.method == "POST":
                if request.form['form_type'] == "upload":
                    file = request.files['file']
                    if file.filename == "":
                        flash('No file selected')
                        return redirect(request.url)
                    
                    upload_name = request.form['material_name']
                    upload_description = request.form['material_description']
                    upload_type = request.form['material_type']
                    file_name = secure_filename(file.filename)
                    upload_info = [upload_name,upload_description,"ENGLISH",upload_type,file_name]
                    self.mysql.upload_file(upload_info)
                    file.save(os.path.join(self.upload_folder,file_name))
                    return redirect(request.url)
                elif request.form['form_type'] == 'delete':
                    mat_name = request.form['name']
                    mat_type = request.form['type']
                    self.mysql.delete_material(mat_name,mat_type)
                elif request.form['form_type'] == 'submission':
                    file = request.files['file']
                    assignment_id = request.form['assignment_id']
                    file_name = secure_filename(file.filename)
                    file.save(os.path.join(self.upload_folder+"student_submissions",file_name))
                    sub_info = [file_name,"ENGLISH","submission",assignment_id]
                    self.mysql.upload_file(sub_info)

            subject_notes = self.mysql.get_subject_info("ENGLISH","lecture_notes",self.current_user.grade_number,self.current_user.class_number)
            subject_assignments = self.mysql.get_subject_info("ENGLISH","assignment",self.current_user.grade_number,self.current_user.class_number)
            return render_template("subject.html",subject="English",user=self.current_user,notes=subject_notes,
            assignments=subject_assignments,notes_len=len(subject_notes),assignments_len=len(subject_assignments))
        
        @self.route("/science", methods=['GET','POST'])
        def science():
            self.current_user = self.mysql.current_user

            if request.method == "POST":
                if request.form['form_type'] == "upload":
                    file = request.files['file']
                    if file.filename == "":
                        flash('No file selected')
                        return redirect(request.url)
                    
                    upload_name = request.form['material_name']
                    upload_description = request.form['material_description']
                    upload_type = request.form['material_type']
                    file_name = secure_filename(file.filename)
                    upload_info = [upload_name,upload_description,"SCIENCE",upload_type,file_name]
                    self.mysql.upload_file(upload_info)
                    file.save(os.path.join(self.upload_folder,file_name))
                    return redirect(request.url)
                elif request.form['form_type'] == 'delete':
                    mat_name = request.form['name']
                    mat_type = request.form['type']
                    self.mysql.delete_material(mat_name,mat_type)
                elif request.form['form_type'] == 'submission':
                    file = request.files['file']
                    assignment_id = request.form['assignment_id']
                    file_name = secure_filename(file.filename)
                    file.save(os.path.join(self.upload_folder+"student_submissions",file_name))
                    sub_info = [file_name,"SCIENCE","submission",assignment_id]
                    self.mysql.upload_file(sub_info)

            subject_notes = self.mysql.get_subject_info("SCIENCE","lecture_notes",self.current_user.grade_number,self.current_user.class_number)
            subject_assignments = self.mysql.get_subject_info("SCIENCE","assignment",self.current_user.grade_number,self.current_user.class_number)
            return render_template("subject.html",subject="Science",user=self.current_user,notes=subject_notes,
            assignments=subject_assignments,notes_len=len(subject_notes),assignments_len=len(subject_assignments))