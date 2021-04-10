class User:
    def __init__(self,uname,gNum,cNum):
        self.user_name = uname
        self.grade_number = gNum
        self.class_number = cNum

    def set_grade(self,new_grade):
        self.grade_number = new_grade

    def set_class(self,new_class):
        self.class_number = new_class

class Administrator(User):
    def __init__(self,uname,gNum,cNum):
        User.__init__(self,uname,gNum,cNum)

class Teacher(User):
    def __init__(self,uname,gNum,cNum):
        User.__init__(self,uname,gNum,cNum)

class Student(User):
    def __init__(self,uname,gNum,cNum):
        User.__init__(self,uname,gNum,cNum)