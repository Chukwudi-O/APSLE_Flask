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

        string = 'SELECT * from '+u_type+'logins'
        conn.execute(string)
        users = conn.fetchall()
        conn.close()

        for i in range(len(users)):
            if (users[i][1] == u_name and users[i][2] == p_word):
                if u_type == "admin":
                    self.current_user = Administrator(users[i][1],0,0)
                    return self.current_user
                elif u_type == "teacher":
                    self.current_user = Teacher(users[i][1],users[i][4],users[i][3])
                    return self.current_user
                elif u_type == "student":
                    self.current_user = Student(users[i][1],users[i][4],users[i][3])
                    return self.current_user
        return None

    def get_all_users(self):
        conn = self.get_conn_cursor()
        users = []

        string = "SELECT * FROM teacherlogins"
        conn.execute(string)
        teachers = conn.fetchall()
        for i in range(len(teachers)):
            user_name = teachers[i][1]
            user_info = [user_name,"Teacher",teachers[i][4],teachers[i][3]]
            users.append(user_info)

        string = "SELECT * FROM studentlogins"
        conn.execute(string)
        students = conn.fetchall()
        for i in range(len(students)):
            user_name = students[i][1]
            user_info = [user_name,"Student",students[i][4],students[i][3]]
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

        string = "INSERT INTO "+user_type+"logins(username,password,gradeNumber,classNumber) "
        string += "VALUES (%s,%s,%s,%s)"
        print(string)
        conn.execute(string,(user_name,pass_word,grade_number,class_number))
        self.my_sql.connection.commit()
        conn.close()

    def delete_user(self,u_name,u_type):
        conn = self.get_conn_cursor()

        string = "DELETE FROM "+u_type+"logins WHERE username=%s"

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
                            query = "UPDATE "+user_info[1]+"logins SET password = %s, gradeNumber = %s, classNumber = %s WHERE username = %s"
                            conn.execute(query,(new_info[0],new_info[2],new_info[3],user_info[0]))
                            self.my_sql.connection.commit()
                            conn.close()
                            return 1
                        else:
                            query = "UPDATE "+user_info[1]+"logins SET password = %s, gradeNumber = %s WHERE username = %s"
                            conn.execute(query,(new_info[0],new_info[2],user_info[0]))
                            self.my_sql.connection.commit()
                            conn.close()
                            return 1
                    else:
                        if new_info[3] != "":
                            query = "UPDATE "+user_info[1]+"logins SET password = %s, classNumber = %s WHERE username = %s"
                            conn.execute(query,(new_info[0],new_info[3],user_info[0]))
                            self.my_sql.connection.commit()
                            conn.close()
                            return 1
                        else:
                            query = "UPDATE "+user_info[1]+"logins SET password = %s WHERE username = %s"
                            conn.execute(query,(new_info[0],user_info[0]))
                            self.my_sql.connection.commit()
                            conn.close()
                            return 1
                else:
                    if new_info[2] != "":
                        if new_info[3] != "":
                            query = "UPDATE "+user_info[1]+"logins SET gradeNumber = %s, classNumber = %s WHERE username = %s"
                            conn.execute(query,(new_info[2],new_info[3],user_info[0]))
                            self.my_sql.connection.commit()
                            conn.close()
                            return 1
                        else:
                            query = "UPDATE "+user_info[1]+"logins SET gradeNumber = %s WHERE username = %s"
                            conn.execute(query,(new_info[2],user_info[0]))
                            self.my_sql.connection.commit()
                            conn.close()
                            return 1
                    else:
                        if new_info[3] != "":
                            query = "UPDATE "+user_info[1]+"logins SET classNumber = %s WHERE username = %s"
                            conn.execute(query,(new_info[3],user_info[0]))
                            self.my_sql.connection.commit()
                            conn.close()
                            return 1
        conn.close()
        return 0
