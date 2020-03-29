import re
import os


def menu():
    # 输出菜单
    print('''
    ╔———————学生信息管理系统————————╗
    │                                              │
    │   =============== 功能菜单 ===============   │
    │                                              │
    │   1 录入学生信息                             │
    │   2 查找学生信息                             │
    │   3 删除学生信息                             │
    │   4 修改学生信息                             │
    │   5 排序                                     │
    │   6 统计学生总人数                           │
    │   7 显示所有学生信息                         │
    │   0 退出系统                                 │
    │  ==========================================  │
    │  说明：通过数字或↑↓方向键选择菜单          │
    ╚———————————————————————╝
    ''')


class StudentSystem(object):
    def __init__(self):
        self.filename = "students.txt"

    def __save(self, studentList):
        try:
            student_txt = open(self.filename, "a")  # 追加模式
        except:
            student_txt = open(self.filename, 'w')  # create a new file
        for info in studentList:
            student_txt.write(str(info) + "\n")
        student_txt.close()

    def __show_student(self, studentList):
        if not studentList:
            print("(o@.@o) 无数据信息 (o@.@o) \n")
            return
        format_title = "{:^6}{:^12}\t{:^8}\t{:^10}\t{:^10}\t{:^10}"
        print(format_title.format("ID", "名字", "英语成绩", "Python成绩", "C语言成绩", "总成绩"))
        format_data = "{:^6}{:^12}\t{:^12}\t{:^12}\t{:^12}\t{:^12}"
        for info in studentList:
            print(format_data.format(info.get("id"), info.get("name"), str(info.get("english")),
                                     str(info.get("python")),
                                     str(info.get("c")),
                                     str(info.get("english") + info.get("python") + info.get("c")).center(12)))

    def show(self):
        student_new = []
        if os.path.exists(self.filename):  # 判断文件是否存在
            with open(self.filename, 'r') as rfile:  # 打开文件
                student_old = rfile.readlines()  # 读取全部内容
            for list in student_old:
                student_new.append(eval(list))  # 将找到的学生信息保存到列表中
            if student_new:
                self.__show_student(student_new)
            else:
                print("datebase is none student info \n")
        else:
            print("暂未保存数据信息...")

    def insert(self):
        studentList = []
        mark = True
        while (mark):
            id = input("please input student id(example 1001): ")
            if not id: break
            name = input("please input student name: ")
            if not name: break
            try:
                english = int(input("please input english score: "))
                python = int(input("please input python score: "))
                c = int(input("please input C score "))
            except:
                print("输入无效，不是整型数值．．．．重新录入信息")
                continue
            student = {"id": id, "name": name, "english": english, "python": python, "c": c}  # 将输入的学生信息保存到字典
            studentList.append(student)
            input_mark = input("If continue add student info(y/n): ")
            mark = True if input_mark.lower() == "y" else False
        self.__save(studentList)
        print("having finished inputing and storing student info")

    def search(self):
        mark = True
        student_query = []
        name, id = "", ""
        if not os.path.isfile(self.filename):
            print("Not storing student info yet \n")
            return
        while (mark):
            mode = int(input("Search by ID, Please input 1; Searched by name, Please input 2: "))
            if mode == 1:
                id = input("input student id: ")
            elif mode == 2:
                name = input("input student name: ")
            else:
                print("Input error, Please reenter \n")
                self.search()
            with open(self.filename, 'r') as file:
                student_info = file.readlines()
                for list in student_info:
                    info = dict(eval(list))
                    print("id={}, current_id = {}, equal={}".format(id, name is not "", info["id"] == id))
                    if id is not "":
                        if info["id"] == id:
                            student_query.append(info)
                    elif name is not "":
                        if info["name"] == name:
                            student_query.append(info)
                self.__show_student(student_query)
                student_query.clear()
                input_mark = input("If continue search student(y/n): ")
                mark = True if input_mark.lower() == "y" else False

    def delet(self):
        mark = True
        if not os.path.isfile(self.filename):
            print("Student info is not stored yet \n ")
            return
        with open(self.filename, 'r') as file:
            studens_old = file.readlines()

        while mark:
            id  = input("Please input student id: ")
            ifdel = False
            with open(self.filename, 'w') as file:
                for student_info in studens_old:
                    student_info = dict(eval(student_info))
                    print("students_info={}, type={}".format(student_info, type(student_info)))
                    if student_info["id"] != id:
                        file.write(str(student_info)+"\n")
                    else:
                        ifdel = True
                if ifdel:
                    print("ID为 %s 的学生信息已经被删除..." % id)
                else:
                    print("没有找到ID为 %s 的学生信息..." % id)
            self.show()
            input_mark = input("if continue delete student info(y/n):")
            mark = True if input_mark.lower() == 'y' else False

    def modify(self):
        mark = True
        while(mark):
            if os.path.isfile(self.filename):
                with open(self.filename,"r") as mfile:
                    old_students = mfile.readlines()
                self.show()
            else:
                old_students = ""
                print("The database does not store student information \n")
            studentid = input("请输入要修改的学生ID：")
            with open(self.filename, "w") as mfile:
                for student in old_students:
                    each_student = dict(eval(student))
                    if each_student["id"] ==studentid:
                        while True:
                            try:
                                each_student["name"] = input("请输入姓名：")
                                each_student["english"] = int(input("请输入英语成绩："))
                                each_student["python"] = int(input("请输入Python成绩："))
                                each_student["c"] = int(input("请输入C语言成绩："))
                            except:
                                print("您的输入有误，请重新输入。")
                            else:
                                break  # 跳出循环
                        mfile.write(str(each_student)+"\n")
                    else:
                        mfile.write(student)
            mark = input("是否继续修改其他学生信息？（y/n）：")
            if mark == "y":
                self.modify()  # 重新执行修改操作

    def sort(self):
        if os.path.isfile(self.filename):
            with open(self.filename, "r") as file:
                old_students = file.readlines()
                new_student = []
            for student in old_students:

                new_student.append(dict(eval(student)))
        else:
            print("No student info in database \n")
            return
        ascORdesc = input("请选择（0升序；1降序）：")
        if ascORdesc == "0":  # 按升序排序
            ascORdescBool = False  # 标记变量，为False表示升序排序
        elif ascORdesc == "1":  # 按降序排序
            ascORdescBool = True  # 标记变量，为True表示降序排序
        else:
            print("您的输入有误，请重新输入！")
            self.sort()
        mode = input("请选择排序方式（1按英语成绩排序；2按Python成绩排序；3按C语言成绩排序；0按总成绩排序）：")
        if mode == "1":
            new_student.sort(key=lambda x: x["english"], reverse=ascORdescBool)
        elif mode == "2":
            new_student.sort(key=lambda x: x["python"], reverse=ascORdescBool)
        elif mode =="3":
            new_student.sort(key=lambda x: x["x"], reverse=ascORdescBool)
        elif mode =="0":
            new_student.sort(key=lambda x:x["english"]+x["python"]+x["c"], reverse=ascORdescBool)
        else:
            print("您的输入有误，请重新输入！")
            self.sort()
        self.__show_student(new_student)  # 显示排序结果

    def total(self):
        if os.path.exists(self.filename):  # 判断文件是否存在
            with open(self.filename, 'r') as rfile:  # 打开文件
                student_old = rfile.readlines()  # 读取全部内容
                if student_old:
                    print("一共有 %d 名学生！" % len(student_old))
                else:
                    print("还没有录入学生信息！")
        else:
            print("暂未保存数据信息...")

def main():
    student_system = StudentSystem()
    control = True

    while (control):
        menu()
        option = input("Please chose:")
        option_int = int(re.sub("\D", "", option))
        print(option_int)
        if option_int == 0:
            print("You have exited the student system\n")
            control = False
        elif option_int == 1:
            student_system.insert()
        elif option_int == 2:
            student_system.search()
        elif option_int == 3:
            student_system.delet()
        elif option_int ==4:
            student_system.modify()
        elif option_int == 5:
            student_system.sort()
        elif option_int ==6:
            student_system.total()
        elif option_int == 7:
            student_system.show()


if __name__ == "__main__":
    main()
