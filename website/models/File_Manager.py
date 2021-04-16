import datetime

class File_Manager:
    def __init__(self,mysql,c_checker):
        self.my_sql = mysql
        self.cred_check = c_checker
        self.current_user = None


    def upload_file(self,upload_info):
        self.current_user = self.cred_check.current_user
        cursor = self.my_sql.connection.cursor()
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

        cursor.execute(query,info)
        self.my_sql.connection.commit()
        cursor.close()
    
    def delete_material(self,mat_id):
        self.current_user = self.cred_check.current_user
        cursor = self.my_sql.connection.cursor()
        if self.current_user.user_type == "Teacher" or self.current_user.user_type == "Admin":
            query = "DELETE FROM teacher_uploads WHERE id = %s"
            cursor.execute(query,mat_id)
            self.my_sql.connection.commit()
        cursor.close()

    def get_subject_info(self,subject,type_u,grade_n,class_n):
        cursor = self.my_sql.connection.cursor()
        query = "SELECT * FROM teacher_uploads WHERE grade_number = %s AND class_number = %s"
        cursor.execute(query,(grade_n,class_n))

        results = cursor.fetchall()
        out =[]

        for res in results:
            if res[6] == subject and res[9] == type_u:
                temp = [res[1],res[2],res[3],res[4],res[0]]
                out.append(temp)

        cursor.close()
        return out