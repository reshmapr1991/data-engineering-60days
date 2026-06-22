class University:
    def __init__(self,uni_name):
        self.uni_name=uni_name
    def show_detail(self):
        print(f"Name of university is {self.uni_name}")


class Course(University):
    def __init__(self,uni_name,c_name):
        University.__init__(self, uni_name)
        self.c_name = c_name

    def show_detail(self):
        print(f"Name of university is {self.uni_name} and course is {self.c_name}")

class Branch(University):
    def __init__(self, uni_name, b_name):
        University.__init__(self, uni_name)
        self.b_name = b_name

    def show_detail(self):
        print(f"Name of Branch is {self.b_name}")

class Student(Course,Branch):
    def __init__(self,uni_name,s_name,c_name,b_name):
        University.__init__(self, uni_name)
        Course.__init__(self,uni_name,c_name)
        Branch.__init__(self,uni_name,b_name)
        self.s_name = s_name

    def show_detail(self):
        print("i am student")


class Faculty(Branch):
    def __init__(self, uni_name,f_name,b_name):
        Branch.__init__(self, b_name)
        self.f_name = f_name

    def show_detail(self):
        print(f"Name of Faculty is {self.f_name}")

u1 = University('mku')
c1 = Course('mku','BTECH')
b1 = Branch('mku','CSE')
student_1 = Student('mku','kai','CSE','cse')
student_1.show_detail()
University.show_detail(student_1)
Course.show_detail(student_1)
Branch.show_detail(student_1)

