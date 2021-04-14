from flask_mysqldb import MySQL

class SQL_Connector:
    def __init__(self):
        self.my_sql = MySQL()

    def get_conn_cursor(self):
        return self.my_sql.connection.cursor()

    def init_app(self,app):
        self.my_sql.init_app(app)

    def check_credentials(self,u_name,p_word,u_type):
        conn = self.get_conn_cursor()

        string = 'SELECT * from '+u_type+'logins'
        conn.execute(string)
        users = conn.fetchall()

        for i in range(len(users)):
            if (users[i][1] == u_name and users[i][2] == p_word):
                conn.close()
                #self.current_user = Administrator(admins[i][1],0,0)
                return True
        
        conn.close()
        return False

    def get_all_users(self):
        conn = self.get_conn_cursor()
        users = []

        string = "SELECT * FROM teacherlogins"
        conn.execute(string)
        teachers = conn.fetchall()
        for i in range(len(teachers)):
            user_name = teachers[i][1]
            #i_1 = user_name.index("\'")
            #i_2 = user_name.index("\'",i_1+1)
            user_info = [user_name,"Teacher",teachers[i][4],teachers[i][3]]
            users.append(user_info)

        string = "SELECT * FROM studentlogins"
        conn.execute(string)
        students = conn.fetchall()
        for i in range(len(students)):
            user_name = students[i][1]
            #i_1 = user_name.index("\'")
            #i_2 = user_name.index("\'",i_1+1)
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
