from classes.Users import Administrator,Teacher,Student

class Credential_Checker:
    def __init__(self,mysql):
        self.my_sql = mysql
        self.current_user = None
    
    def check_credentials(self,u_name,p_word,u_type):
        cursor = self.my_sql.connection.cursor()

        string = 'SELECT * from '+u_type+'_logins'
        cursor.execute(string)
        users = cursor.fetchall()
        cursor.close()

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

    