from flask import Blueprint, render_template, redirect, url_for, request


class Admin_Blueprint(Blueprint):
    def __init__(self,name,kind,my_sql):
        Blueprint.__init__(self,name,kind)
        self.current_user = None
        self.mysql = my_sql

        @self.route("/admin_home", methods=['GET','POST'])
        def admin_home():
            self.current_user = self.mysql.current_user
            if request.method == 'POST':
                return redirect(url_for("admin.manage_users"))

            return render_template("admin_home.html",user_name=self.current_user.user_name)

        @self.route("/manage_users",methods=['GET','POST'])
        def manage_users():
            del_msg,add_msg,edit_msg = "","",""
            all_users = self.mysql.get_all_users()
            
            if request.method == 'POST':
                if request.form["form_type"] == "add_users":
                    pass_word = request.form.get("p_word")
                    c_pass_word = request.form.get("c_p_word")
                    if (c_pass_word != pass_word):
                        add_msg = "Please ensure both passwords are correct"
                        return render_template("manage_users.html",len=len(all_users),all_users=all_users,delete_message=del_msg,add_message=add_msg,edit_message=edit_msg)

                    grade_number = request.form.get("g_num")
                    class_number = request.form.get("c_num")
                    if (int(grade_number) >= 7 or int(class_number) >= 7):
                        add_msg = "Please ensure class number and grade number are less than 7"
                        return render_template("manage_users.html",len=len(all_users),all_users=all_users,delete_message=del_msg,add_message=add_msg,edit_message=edit_msg)
                    
                    first_name = request.form.get("f_name")
                    last_name = request.form.get("l_name")
                    user_type = request.form["user_type"]
                    #gender = request.form["gender"]

                    new_user_info = [first_name,last_name,pass_word,user_type,str(grade_number),str(class_number)]
                    self.mysql.add_user(new_user_info)
                    add_msg = "User \'"+first_name.lower()+last_name.lower()+"\' has been added successfully"
                elif request.form["form_type"] == "edit_users":
                    user_info = [request.form.get("user_name"),request.form.get("user_type")]
                    new_info = [request.form.get("new_password"),request.form.get("c_new_password"),request.form.get("new_grade"),request.form.get("new_class")]

                    if new_info[0] != "" and new_info[0] != new_info[1]:
                        edit_msg = "Please ensure both password and confirm password are identical."
                        return render_template("manage_users.html",len=len(all_users),all_users=all_users,delete_message=del_msg,add_message=add_msg,edit_message=edit_msg)
                    
                    edit = self.mysql.update_user(user_info,new_info)

                    if edit == 0:
                        edit_msg = "Update has failed, "+user_info[0]+" was not updated."
                    else:
                        edit_msg = "Update was successful, "+user_info[0]+"'s info was changed."
                elif request.form["form_type"] == "delete_users":
                    user_name = request.form.get("user_name")
                    user_type = request.form.get("user_type")
                    self.mysql.delete_user(user_name,user_type)
                    del_msg = "User "+user_name+" was deleted successfully"
                
            all_users = self.mysql.get_all_users()
            return render_template("manage_users.html",len=len(all_users),all_users=all_users,delete_message=del_msg,add_message=add_msg,edit_message=edit_msg)
            
        