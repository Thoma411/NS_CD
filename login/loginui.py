import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkFont
from tkinter import *  # 图形界面库
from message_process import admin_on_login
from message_process import stu_on_login

# 主菜单


class StartPage:
    def __init__(self, parent_window):
        parent_window.update()
        parent_window.destroy()  # 销毁子界面

        self.window = Tk()  # 初始框的声明
        self.window.title('学生信息管理系统')
        # align_str = '%dx%d+%d+%d' % (800, 600, (x - 800) / 2, (y - 600) / 2)
        self.window.geometry('900x800')  # 这里的乘是小x

        label = Label(self.window, text="学生信息管理系统", width=24, height=2, fg='blue', font=("Verdana", 40))
        label.grid(row=0, column=2, columnspan=3, pady=50)  # pady=50 界面的长度

        btn1 = Button(self.window, text="管理员登陆", font=tkFont.Font(size=24),
                      command=lambda: AdminPage(self.window),
                      width=30,
                      height=2,
                      fg='blue', bg='green', activebackground='black',
                      activeforeground='white')  # .pack(padx=35,pady=2,side=LEFT,anchor=N)
        btn1.grid(row=1, column=2, columnspan=3, pady=20)
        btn2 = Button(self.window, text="学生登陆", font=tkFont.Font(size=24), command=lambda: StudentPage(self.window),
                      width=30,
                      height=2, fg='blue', bg='green', activebackground='black',
                      activeforeground='white')  # .grid(row = 1,column = 2) #.pack(padx=10,pady=2,side=TOP)
        btn2.grid(row=2, column=2, columnspan=3, pady=20)
        # btn3 = Button(self.window, text="关于", font=tkFont.Font(size=10), command=lambda: AboutPage(self.window),
        #               width=15,
        #               height=2,
        #               fg='white', bg='green', activebackground='black', activeforeground='white')
        # btn3.grid(row=3, column=1, columnspan=3, pady=20)
        btn4 = Button(self.window, text='退出系统', height=2, font=tkFont.Font(size=10), width=15,
                      command=self.window.destroy,
                      fg='black', bg='red', activebackground='black', activeforeground='white')
        btn4.grid(row=3, column=3, columnspan=3, pady=20)
        self.window.mainloop()  # 主消息循环

# 管理员登录界面


class AdminPage:
    def __init__(self, parent_window):
        parent_window.destroy()  # 销毁主界面
        self.admin_on_login = admin_on_login  # 登录回调函数
        self.window = tk.Tk()  # 初始框的声明
        self.window.title('管理员登陆页面')
        self.window.geometry('900x800')  # 这里的乘是小x

        label = Label(self.window, text="管理员登陆", width=24, height=1, fg='blue', font=("Verdana", 20))
        label.grid(row=0, column=5, columnspan=3, pady=70)  # pady=50 界面的长度
        label2 = Label(self.window, text='管理员账号：', fg='blue', font=tkFont.Font(size=18))
        label2.grid(row=1, column=3, columnspan=3, padx=15, pady=20)
        self.admin_username = tk.Entry(self.window, width=15, font=tkFont.Font(size=18), bg='Ivory')
        self.admin_username.grid(row=1, column=5, columnspan=3, padx=15, pady=20)

        label3 = Label(self.window, text='管理员密码：', fg='blue', font=tkFont.Font(size=18))
        label3.grid(row=2, column=3, columnspan=3, padx=15, pady=20)
        self.admin_pass = tk.Entry(self.window, width=15, font=tkFont.Font(size=18), bg='Ivory', show='*')
        self.admin_pass.grid(row=2, column=5, columnspan=3, padx=15, pady=20)

        btn1 = Button(self.window, text="登陆", width=20, font=tkFont.Font(size=15), command=self.login)
        btn1.grid(row=3, column=5, columnspan=3, padx=25, pady=20)

        btn2 = Button(self.window, text="返回首页", width=20, font=tkFont.Font(size=15), command=self.back)
        btn2.grid(row=4, column=2, columnspan=3, padx=25, pady=20)

        self.window.protocol("WM_DELETE_WINDOW", self.back)  # 捕捉右上角关闭点击
        self.window.mainloop()  # 进入消息循环

    def login(self):
        username = self.admin_username.get().strip()
        password = self.admin_pass.get().strip()

        tag = admin_on_login(username, password)

        if tag == 1:

            # AdminManage(self.window)  # 进入管理员操作界面
            InfoManage(self.window)
        else:
            messagebox.showinfo('警告！', '用户名或密码不正确！')

    def back(self):
        StartPage(self.window)  # 显示主窗口 销毁本窗口

# 信息管理界面


class InfoManage:
    def __init__(self, parent_window):
        parent_window.destroy()  # 销毁主界面

        self.window = tk.Tk()  # 初始框的声明
        self.window.title('信息管理')
        self.window.geometry('900x600')  # 这里的乘是小x

        label = tk.Label(self.window, text='信息管理', width=24, height=1, font=('Verdana', 20))
        label.grid(row=1, column=5, columnspan=3, padx=80, pady=30)  # pady=20 界面的长度

        # btn1 = Button(self.window, text="学生成绩管理", width=24, height=1, relief='raised', font=('Verdana', 20),
        #               command=lambda: AdminManage(self.window),
        #               fg='white', bg='green', activebackground='black',
        #               activeforeground='blue')
        # btn1.grid(row=2, column=5, columnspan=3, padx=80, pady=30)
        #
        # btn2 = Button(self.window, text="用户信息管理", width=30, height=1, relief='raised', font=('Verdana', 20),
        #               command=lambda: UserInfoManage(self.window),
        #               fg='white', bg='green', activebackground='black',
        #               activeforeground='blue')
        # btn2.grid(row=5, column=5, columnspan=3, padx=80, pady=30)
        #
        # btn3 = Button(self.window, text="考勤信息管理", width=36, height=1, relief='raised', font=('Verdana', 20),
        #               command=lambda: AttendanceInfoManage(self.window),
        #               fg='white', bg='green', activebackground='red',
        #               activeforeground='blue')
        # btn3.grid(row=8, column=5, columnspan=3, padx=80, pady=30)
        self.window.protocol("WM_DELETE_WINDOW", self.back)  # 捕捉右上角关闭点击
        self.window.mainloop()  # 进入消息循环

    def back(self):
        StartPage(self.window)  # 显示主窗口 销毁本窗口

# 学生登陆界面


class StudentPage:
    def __init__(self, parent_window):
        parent_window.destroy()  # 销毁主界面

        self.window = tk.Tk()  # 初始框的声明
        self.window.title('学生登陆')
        self.window.geometry('900x800')  # 这里的乘是小x

        label = tk.Label(self.window, text='学生登陆', width=24, height=1, fg='blue', font=('Verdana', 20))
        label.grid(row=0, column=5, columnspan=3, pady=50)  # pady=50 界面的长度

        label2 = Label(self.window, text='学生账号：', fg='blue', font=tkFont.Font(size=18))
        label2.grid(row=1, column=3, columnspan=3, padx=35, pady=20)
        self.student_id = tk.Entry(self.window, width=15, font=tkFont.Font(size=18), bg='Ivory')
        self.student_id.grid(row=1, column=5, columnspan=3, padx=15, pady=20)

        label3 = Label(self.window, text='学生密码：', fg='blue', font=tkFont.Font(size=18))
        label3.grid(row=2, column=3, columnspan=3, padx=35, pady=20)
        self.student_pass = tk.Entry(self.window, width=15, font=tkFont.Font(size=18), bg='Ivory', show='*')
        self.student_pass.grid(row=2, column=5, columnspan=3, padx=15, pady=20)

        btn1 = Button(self.window, text="登陆", width=20, font=tkFont.Font(size=15), command=self.login)
        btn1.grid(row=3, column=5, columnspan=3, padx=25, pady=20)
        btn2 = Button(self.window, text="返回首页", width=20, font=tkFont.Font(size=15), command=self.back)
        btn2.grid(row=4, column=2, columnspan=3, padx=25, pady=20)

        self.window.protocol("WM_DELETE_WINDOW", self.back)  # 捕捉右上角关闭点击
        self.window.mainloop()  # 进入消息循环

    def login(self):
        username = self.student_id.get().strip()
        password = self.student_pass.get().strip()
        tag = stu_on_login(username, password)

        if tag == 1:

            # AdminManage(self.window)  # 进入管理员操作界面
            StudentInfoManage(self.window, self.student_id.get())
        else:
            messagebox.showinfo('警告！', '用户名或密码不正确！')

    def back(self):
        StartPage(self.window)  # 显示主窗口 销毁本窗口

# 学生信息查询


class StudentInfoManage:
    def __init__(self, parent_window, student_id):
        parent_window.destroy()  # 销毁主界面

        self.window = tk.Tk()  # 初始框的声明
        self.window.title('学生信息查询')
        self.window.geometry('900x600')  # 这里的乘是小x

        self.student_id = student_id

        label = tk.Label(self.window, text='学生信息查询', width=24, height=1, font=('Verdana', 20))
        label.grid(row=1, column=8, columnspan=5, padx=80, pady=30)  # pady=20 界面的长度

        # btn1 = Button(self.window, text="学生成绩查询", width=24, height=1, relief='raised', font=('Verdana', 20),
        #               command=lambda: StudentGradeView(self.window, student_id),
        #               fg='white', bg='blue', activebackground='black',
        #               activeforeground='white')
        # btn1.grid(row=3, column=8, columnspan=5, padx=80, pady=30)
        #
        # btn2 = Button(self.window, text="考勤信息查询", width=24, height=1, relief='raised', font=('Verdana', 20),
        #               command=lambda: StudentAttendanceView(self.window, student_id),
        #               fg='white', bg='blue', activebackground='black',
        #               activeforeground='white')
        # btn2.grid(row=5, column=8, columnspan=5, padx=80, pady=30)

        self.window.protocol("WM_DELETE_WINDOW", self.back)  # 捕捉右上角关闭点击
        self.window.mainloop()  # 进入消息循环

    def back(self):
        StartPage(self.window)  # 显示主窗口 销毁本窗口


# class LoginUI:
#     def __init__(self, on_login):
#         self.on_login = on_login  # 登录回调函数
#         self.root = tk.Tk()
#         self.root.title("登录")
#
#         # 创建用户名Label和Entry
#         tk.Label(self.root, text="用户名").grid(row=0)
#         self.username_entry = tk.Entry(self.root)
#         self.username_entry.grid(row=0, column=1)
#
#         # 创建密码Label和Entry
#         tk.Label(self.root, text="密码").grid(row=1)
#         self.password_entry = tk.Entry(self.root, show="*")
#         self.password_entry.grid(row=1, column=1)
#
#         # 创建登录按钮
#         login_btn = tk.Button(self.root, text="登录", command=self.login)
#         login_btn.grid(row=2, column=0, columnspan=2, pady=10)
#
#     def run(self):
#         self.root.mainloop()
#
#     def login(self):
#         # 获取用户名和密码
#         username = self.username_entry.get().strip()
#         password = self.password_entry.get().strip()
#
#         self.on_login(username, password)



