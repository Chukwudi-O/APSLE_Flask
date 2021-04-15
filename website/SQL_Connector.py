import datetime
from flask_mysqldb import MySQL
from .classes.Users import Administrator,Teacher,Student

class SQL_Connector:
    def __init__(self):
        self.my_sql = MySQL()
        self.current_user = None

    def get_conn_cursor(self):
        return self.my_sql.connection.cursor()

    def init_app(self,app):
        self.my_sql.init_app(app)

    def check_credentials(self,u_name,p_word,u_type):
        conn = self.get_conn_cursor()

        string = 'SELECT * from '+u_type+'_logins'
        conn.execute(string)
        users = conn.fetchall()
        conn.close()

        for i in range(len(users)):
            if (users[i][3] == u_name and users[i][4] == p_word):
                if u_type == "admin":
                    self.current_user = Administrator(users[i][3],0,0)
                    return self.current_user
                elif u_type == "teacher":
                    self.current_user = Teacher(users[i][3],users[i][6],users[i][7])
                    return self.current_user
                elif u_type == "student":
                    self.current_user = Student(users[i][3],users[i][6],users[i][7])
                    return self.current_user
        return None

    def get_all_users(self):
        conn = self.get_conn_cursor()
        users = []

        string = "SELECT * FROM teacher_logins"
        conn.execute(string)
        teachers = conn.fetchall()
        for i in range(len(teachers)):
            user_name = teachers[i][1]
            user_info = [user_name,"Teacher",teachers[i][6],teachers[i][7]]
            users.append(user_info)

        string = "SELECT * FROM student_logins"
        conn.execute(string)
        students = conn.fetchall()
        for i in range(len(students)):
            user_name = students[i][1]
            user_info = [user_name,"Student",students[i][6],students[i][7]]
            users.append(user_info)

        conn.close()
        return users

    def add_user(self,new_user):
        conn = self.get_conn_cursor()
        user_name = (new_user[0]+new_user[1]).lower()
        pass_word = new_user[2]
        user_type = new_user[3].lower()
        grade_number = new_user[4]
        class_number = new_user[5]
        gender = new_user[6]

        string = "INSERT INTO "+user_type+"_logins (first_name,last_name,username,password,gender,grade_number,class_number) "
        string += "VALUES (%s,%s,%s,%s,%s,%s,%s)"
        print(string)
        conn.execute(string,(new_user[0],new_user[1],user_name,pass_word,gender,grade_number,class_number))
        self.my_sql.connection.commit()
        conn.close()

    def delete_user(self,u_name,u_type):
        conn = self.get_conn_cursor()

        string = "DELETE FROM "+u_type+"_logins WHERE username=%s"

        conn.execute(string,(u_name,))
        self.my_sql.connection.commit()
        conn.close()

    def update_user(self,user_info,new_info):
        all_users = self.get_all_users()
        conn = self.get_conn_cursor()

        for i in range(len(all_users)):
            if all_users[i][0] == user_info[0] and all_users[i][1].lower() == user_info[1].lower():
                query=""
                if new_info[0] != "":
                    if new_info[2] != "":
                        if new_info[3] != "":
                            query = "UPDATE "+user_info[1]+"_logins SET password = %s, "
                            query += "grade_number = %s, class_number = %s WHERE username = %s"
                            conn.execute(query,(new_info[0],new_info[2],new_info[3],user_info[0]))
                            self.my_sql.connection.commit()
                            conn.close()
                            return 1
                        else:
                            query = "UPDATE "+user_info[1]+"_logins SET password = %s,"
                            query += " grade_number = %s WHERE username = %s"
                            conn.execute(query,(new_info[0],new_info[2],user_info[0]))
                            self.my_sql.connection.commit()
                            conn.close()
                            return 1
                    else:
                        if new_info[3] != "":
                            query = "UPDATE "+user_info[1]+"_logins SET password = %s,"
                            query += " class_number = %s WHERE username = %s"
                            conn.execute(query,(new_info[0],new_info[3],user_info[0]))
                            self.my_sql.connection.commit()
                            conn.close()
                            return 1
                        else:
                            query = "UPDATE "+user_info[1]+"_logins "
                            query += "SET password = %s WHERE username = %s"
                            conn.execute(query,(new_info[0],user_info[0]))
                            self.my_sql.connection.commit()
                            conn.close()
                            return 1
                else:
                    if new_info[2] != "":
                        if new_info[3] != "":
                            query = "UPDATE "+user_info[1]+"_logins SET grade_number = %s,"
                            query += " class_number = %s WHERE username = %s"
                            conn.execute(query,(new_info[2],new_info[3],user_info[0]))
                            self.my_sql.connection.commit()
                            conn.close()
                            return 1
                        else:
                            query = "UPDATE "+user_info[1]+"_logins "
                            query += "SET grade_number = %s WHERE username = %s"
                            conn.execute(query,(new_info[2],user_info[0]))
                            self.my_sql.connection.commit()
                            conn.close()
                            return 1
                    else:
                        if new_info[3] != "":
                            query = "UPDATE "+user_info[1]+"_logins "
                            query += "SET class_number = %s WHERE username = %s"
                            conn.execute(query,(new_info[3],user_info[0]))
                            self.my_sql.connection.commit()
                            conn.close()
                            return 1
        conn.close()
        return 0

    def upload_file(self,upload_info):
        conn = self.get_conn_cursor()
        date_now = datetime.datetime.now()
        if self.current_user.user_type == "Teacher" or self.current_user.user_type == "Admin":
            query = "INSERT into teacher_uploads (`file_name`,`file_extension`,`input_name`,`file_description`,"
            query += "`date_uploaded`,`subject`,`grade_number`,`class_number`,`type_of_upload`,`uploaded_by`)"
            query += " VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

            dot = upload_info[4].rfind(".")
            file_name = upload_info[4][:dot]
            file_extension = upload_info[4][dot+1:].lower()
            info = (file_name,file_extension, upload_info[0], upload_info[1], date_now,upload_info[2],self.current_user.grade_number,
                    self.current_user.class_number,upload_info[3],self.current_user.user_name)
        elif self.current_user.user_type == "Student":
            query = "INSERT INTO student_submissions (`file_name`,`file_extension`,`date_uploaded`,`subject`,"
            query += "`grade_number`,`class_number`,`uploaded_by`,`assignment_id`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            
            dot = upload_info[0].rfind(".")
            file_name = upload_info[0][:dot]
            file_extension = upload_info[0][dot+1:].lower()
            info = (file_name,file_extension,date_now,upload_info[1],self.current_user.grade_number,
                    self.current_user.class_number,self.current_user.user_name,upload_info[3])

        conn.execute(query,info)
        self.my_sql.connection.commit()
        conn.close()

    def get_subject_info(self,subject,type_u,grade_n,class_n):
        conn = self.get_conn_cursor()
        query = "SELECT * FROM teacher_uploads WHERE grade_number = %s AND class_number = %s"
        conn.execute(query,(grade_n,class_n))

        results = conn.fetchall()
        out =[]

        for res in results:
            if res[6] == subject and res[9] == type_u:
                temp = [res[1],res[2],res[3],res[4],res[0]]
                out.append(temp)

        conn.close()
        return out
    
    def delete_material(self,mat_id):
        conn = self.get_conn_cursor()
        if self.current_user.user_type == "Teacher" or self.current_user.user_type == "Admin":
            query = "DELETE FROM teacher_uploads WHERE id = %s"
            conn.execute(query,mat_id)
            self.my_sql.connection.commit()
        conn.close()
