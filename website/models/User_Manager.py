

class User_Manager:
    def __init__(self,mysql):
        self.my_sql = mysql
    
    def get_all_users(self):
        cursor = self.my_sql.connection.cursor()
        users = []

        string = "SELECT * FROM teacher_logins"
        cursor.execute(string)
        teachers = cursor.fetchall()
        for i in range(len(teachers)):
            user_name = teachers[i][3]
            user_info = [user_name,"Teacher",teachers[i][6],teachers[i][7]]
            users.append(user_info)

        string = "SELECT * FROM student_logins"
        cursor.execute(string)
        students = cursor.fetchall()
        for i in range(len(students)):
            user_name = students[i][3]
            user_info = [user_name,"Student",students[i][6],students[i][7]]
            users.append(user_info)

        cursor.close()
        return users

    def add_user(self,new_user):
        cursor = self.my_sql.connection.cursor()
        user_name = (new_user[0]+new_user[1]).lower()
        pass_word = new_user[2]
        user_type = new_user[3].lower()
        grade_number = new_user[4]
        class_number = new_user[5]
        gender = new_user[6]

        string = "INSERT INTO "+user_type+"_logins (first_name,last_name,username,password,gender,grade_number,class_number) "
        string += "VALUES (%s,%s,%s,%s,%s,%s,%s)"

        cursor.execute(string,(new_user[0],new_user[1],user_name,pass_word,gender,grade_number,class_number))
        self.my_sql.connection.commit()
        cursor.close()

    def delete_user(self,u_name,u_type):
        cursor = self.my_sql.connection.cursor()

        string = "DELETE FROM "+u_type+"_logins WHERE username=%s"

        cursor.execute(string,(u_name,))
        self.my_sql.connection.commit()
        cursor.close()

    def update_user(self,user_info,new_info):
        all_users = self.get_all_users()
        cursor = self.my_sql.connection.cursor()

        for i in range(len(all_users)):
            if all_users[i][0] == user_info[0] and all_users[i][1].lower() == user_info[1].lower():
                query=""
                if new_info[0] != "":
                    if new_info[2] != "":
                        if new_info[3] != "":
                            query = "UPDATE "+user_info[1]+"_logins SET password = %s, "
                            query += "grade_number = %s, class_number = %s WHERE username = %s"
                            cursor.execute(query,(new_info[0],new_info[2],new_info[3],user_info[0]))
                            self.my_sql.connection.commit()
                            cursor.close()
                            return 1
                        else:
                            query = "UPDATE "+user_info[1]+"_logins SET password = %s,"
                            query += " grade_number = %s WHERE username = %s"
                            cursor.execute(query,(new_info[0],new_info[2],user_info[0]))
                            self.my_sql.connection.commit()
                            cursor.close()
                            return 1
                    else:
                        if new_info[3] != "":
                            query = "UPDATE "+user_info[1]+"_logins SET password = %s,"
                            query += " class_number = %s WHERE username = %s"
                            cursor.execute(query,(new_info[0],new_info[3],user_info[0]))
                            self.my_sql.connection.commit()
                            cursor.close()
                            return 1
                        else:
                            query = "UPDATE "+user_info[1]+"_logins "
                            query += "SET password = %s WHERE username = %s"
                            cursor.execute(query,(new_info[0],user_info[0]))
                            self.my_sql.connection.commit()
                            cursor.close()
                            return 1
                else:
                    if new_info[2] != "":
                        if new_info[3] != "":
                            query = "UPDATE "+user_info[1]+"_logins SET grade_number = %s,"
                            query += " class_number = %s WHERE username = %s"
                            cursor.execute(query,(new_info[2],new_info[3],user_info[0]))
                            self.my_sql.connection.commit()
                            cursor.close()
                            return 1
                        else:
                            query = "UPDATE "+user_info[1]+"_logins "
                            query += "SET grade_number = %s WHERE username = %s"
                            cursor.execute(query,(new_info[2],user_info[0]))
                            self.my_sql.connection.commit()
                            cursor.close()
                            return 1
                    else:
                        if new_info[3] != "":
                            query = "UPDATE "+user_info[1]+"_logins "
                            query += "SET class_number = %s WHERE username = %s"
                            cursor.execute(query,(new_info[3],user_info[0]))
                            self.my_sql.connection.commit()
                            cursor.close()
                            return 1
        cursor.close()
        return 0