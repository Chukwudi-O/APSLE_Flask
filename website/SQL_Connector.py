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
                    self.current_user = Administrator(users[i][1],0,0)
                    return self.current_user
                elif u_type == "teacher":
                    self.current_user = Teacher(users[i][1],users[i][6],users[i][7])
                    return self.current_user
                elif u_type == "student":
                    self.current_user = Student(users[i][1],users[i][6],users[i][7])
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

        string = "INSERT INTO "+user_type+"logins (first_name,last_name,username,password,gender,grade_number,class_number) "
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
        if upload_info[3] == "lecture_notes" or upload_info[3] == "assignment":
            query = "INSERT into teacheruploads (`file_name`,`file_extension`,`input_name`,`file_description`,"
            query += "`date_uploaded`,`subject`,`grade_number`,`class_number`,`type_of_upload`,`uploaded_by`)"
            query += " VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

            conn = self.get_conn_cursor()
            dot = upload_info[4].rfind(".")
            file_name = upload_info[4][:dot]
            file_extension = upload_info[4][dot+1:].lower()
            date_now = datetime.datetime.now()
            info = (file_name,file_extension, upload_info[0], upload_info[1], date_now,upload_info[2],self.current_user.grade_number,
                    self.current_user.class_number,upload_info[3],self.current_user.user_name)
            
            conn.execute(query,info)
            self.my_sql.connection.commit()
            conn.close()

    def get_subject_info(self,subject,type_u,grade_n,class_n):
        conn = self.get_conn_cursor()
        query = "SELECT * FROM teacheruploads WHERE grade_number = %s AND class_number = %s"
        conn.execute(query,(grade_n,class_n))

        results = conn.fetchall()
        out =[]

        for res in results:
            if res[6] == subject and res[9] == type_u:
                temp = [res[1],res[2],res[3],res[4]]
                out.append(temp)

        conn.close()
        return out
    
    def delete_material(self,m_name,m_type):
        conn = self.get_conn_cursor()
        query = "DELETE FROM teacheruploads WHERE input_name = %s AND type_of_upload = %s"
        conn.execute(query,(m_name,m_type))
        self.my_sql.connection.commit()
        conn.close()
