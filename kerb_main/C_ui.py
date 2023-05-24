import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkFont
# from MsgFieldDef import *
import C_Tclient as cc
from tkinter import *

# K_CV = cc.DKEY_C
# Vsock = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
# #Vsock.connect((V_IP, V_PORT))


class StartPage:  # 主菜单
    def __init__(self, parent_window):
        parent_window.update()
        parent_window.destroy()  # 销毁子界面
        self.window = tk.Tk()  # 初始框的声明
        self.window.title('学生信息管理系统')
        # align_str = '%dx%d+%d+%d' % (800, 600, (x - 800) / 2, (y - 600) / 2)
        self.window.geometry('900x800')  # 这里的乘是小x

        label = tk.Label(self.window, text="学生信息管理系统", width=24,
                         height=2, fg='blue', font=("Verdana", 40))
        label.grid(row=0, column=2, columnspan=3, pady=50)  # pady=50 界面的长度

        btn1 = tk.Button(self.window, text="管理员登陆", font=tkFont.Font(size=24),
                         command=lambda: AdminPage(self.window),
                         width=30,
                         height=2,
                         fg='blue', bg='green', activebackground='black',
                         activeforeground='white')  # .pack(padx=35,pady=2,side=LEFT,anchor=N)
        btn1.grid(row=1, column=2, columnspan=3, pady=20)
        btn2 = tk.Button(self.window, text="学生登陆", font=tkFont.Font(size=24),
                         command=lambda: StudentPage(self.window),
                         width=30,
                         height=2, fg='blue', bg='green', activebackground='black',
                         activeforeground='white')  # .grid(row = 1,column = 2) #.pack(padx=10,pady=2,side=TOP)
        btn2.grid(row=2, column=2, columnspan=3, pady=20)
        # btn3 = Button(self.window, text="关于", font=tkFont.Font(size=10), command=lambda: AboutPage(self.window),
        #               width=15,
        #               height=2,
        #               fg='white', bg='green', activebackground='black', activeforeground='white')
        # btn3.grid(row=3, column=1, columnspan=3, pady=20)
        btn4 = tk.Button(self.window, text='退出系统', height=2, font=tkFont.Font(size=10), width=15,
                         command=self.window.destroy,
                         fg='black', bg='red', activebackground='black', activeforeground='white')
        btn4.grid(row=3, column=3, columnspan=3, pady=20)
        self.window.mainloop()  # 主消息循环


class AdminPage:  # 管理员登录界面
    def __init__(self, parent_window):
        parent_window.destroy()  # 销毁主界面
        self.admin_on_login = cc.admin_on_login  # 登录回调函数
        self.window = tk.Tk()  # 初始框的声明
        self.window.title('管理员登录页面')
        self.window.geometry('900x800')  # 这里的乘是小x
        label = tk.Label(self.window, text="管理员登录", width=24,
                         height=1, fg='blue', font=("Verdana", 20))
        label.grid(row=0, column=5, columnspan=3, pady=70)  # pady=50 界面的长度
        label2 = tk.Label(self.window, text='管理员账号：',
                          fg='blue', font=tkFont.Font(size=18))
        label2.grid(row=1, column=3, columnspan=3, padx=15, pady=20)
        self.admin_username = tk.Entry(
            self.window, width=15, font=tkFont.Font(size=18), bg='Ivory')
        self.admin_username.grid(
            row=1, column=5, columnspan=3, padx=15, pady=20)
        label3 = tk.Label(self.window, text='管理员密码：',
                          fg='blue', font=tkFont.Font(size=18))
        label3.grid(row=2, column=3, columnspan=3, padx=15, pady=20)
        self.admin_pass = tk.Entry(
            self.window, width=15, font=tkFont.Font(size=18), bg='Ivory', show='*')
        self.admin_pass.grid(row=2, column=5, columnspan=3, padx=15, pady=20)
        btn1 = tk.Button(self.window, text="登录", width=20,
                         font=tkFont.Font(size=15), command=self.login)
        btn1.grid(row=3, column=5, columnspan=3, padx=25, pady=20)

        btn2 = tk.Button(self.window, text="返回首页", width=20,
                         font=tkFont.Font(size=15), command=self.back)
        btn2.grid(row=4, column=2, columnspan=3, padx=25, pady=20)

        self.window.protocol("WM_DELETE_WINDOW", self.back)  # 捕捉右上角关闭点击
        self.window.mainloop()  # 进入消息循环

    def login(self):
        username = self.admin_username.get().strip()
        password = self.admin_pass.get().strip()
        global K_CV, C_PKEY_V  # *声明K_CV为共享密钥
        tag, k_cv, C_PKEY_V = cc.admin_on_login(
            username, password)  # *返回PK_V 保存为全局变量供后续验证
        K_CV = k_cv
        if tag == cc.LOG_ACC:
            # AdminManage(self.window)  # 进入管理员操作界面
            InfoManage(self.window)
        else:
            messagebox.showinfo('警告！', '用户名或密码不正确！')

    def back(self):
        StartPage(self.window)  # 显示主窗口 销毁本窗口


class StudentPage:  # 学生登录界面
    def __init__(self, parent_window):
        parent_window.destroy()  # 销毁主界面
        self.window = tk.Tk()  # 初始框的声明
        self.window.title('学生登录')
        self.window.geometry('900x800')  # 这里的乘是小x
        label = tk.Label(self.window, text='学生登录', width=24,
                         height=1, fg='blue', font=('Verdana', 20))
        label.grid(row=0, column=5, columnspan=3, pady=50)  # pady=50 界面的长度
        label2 = tk.Label(self.window, text='学生账号：',
                          fg='blue', font=tkFont.Font(size=18))
        label2.grid(row=1, column=3, columnspan=3, padx=35, pady=20)
        self.student_id = tk.Entry(
            self.window, width=15, font=tkFont.Font(size=18), bg='Ivory')
        self.student_id.grid(row=1, column=5, columnspan=3, padx=15, pady=20)
        label3 = tk.Label(self.window, text='学生密码：',
                          fg='blue', font=tkFont.Font(size=18))
        label3.grid(row=2, column=3, columnspan=3, padx=35, pady=20)
        self.student_pass = tk.Entry(
            self.window, width=15, font=tkFont.Font(size=18), bg='Ivory', show='*')
        self.student_pass.grid(row=2, column=5, columnspan=3, padx=15, pady=20)
        btn1 = tk.Button(self.window, text="登录", width=20,
                         font=tkFont.Font(size=15), command=self.login)
        btn1.grid(row=3, column=5, columnspan=3, padx=25, pady=20)
        btn2 = tk.Button(self.window, text="返回首页", width=20,
                         font=tkFont.Font(size=15), command=self.back)
        btn2.grid(row=4, column=2, columnspan=3, padx=25, pady=20)

        self.window.protocol("WM_DELETE_WINDOW", self.back)  # 捕捉右上角关闭点击
        self.window.mainloop()  # 进入消息循环

    def login(self):
        username = self.student_id.get().strip()
        password = self.student_pass.get().strip()
        global K_CV, C_PKEY_V  # *声明K_CV为共享密钥
        tag, k_cv, C_PKEY_V = cc.stu_on_login(username, password)
        K_CV = k_cv
        if tag == cc.LOG_ACC:
            # AdminManage(self.window)  # 进入学生操作界面
            StudentInfoManage(self.window, self.student_id.get())
        else:
            messagebox.showinfo('警告！', '用户名或密码不正确！')

    def back(self):
        StartPage(self.window)  # 显示主窗口 销毁本窗口


class InfoManage:  # 信息管理界面
    def __init__(self, parent_window):
        parent_window.destroy()  # 销毁主界面
        self.window = tk.Tk()  # 初始框的声明
        self.window.title('信息管理')
        self.window.geometry('900x600')  # 这里的乘是小x
        label = tk.Label(self.window, text='信息管理', width=24,
                         height=1, font=('Verdana', 20))
        label.grid(row=1, column=5, columnspan=3,
                   padx=80, pady=30)  # pady=20 界面的长度
        btn1 = Button(self.window, text="学生成绩管理", width=24, height=1, relief='raised', font=('Verdana', 20),
                      command=lambda: AdminManage(self.window),
                      fg='white', bg='green', activebackground='black',
                      activeforeground='blue')
        btn1.grid(row=2, column=5, columnspan=3, padx=80, pady=30)
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


class StudentInfoManage:  # 学生信息查询
    def __init__(self, parent_window, student_id):
        parent_window.destroy()  # 销毁主界面

        self.window = tk.Tk()  # 初始框的声明
        self.window.title('学生信息查询')
        self.window.geometry('900x600')  # 这里的乘是小x

        self.student_id = student_id

        label = tk.Label(self.window, text='学生信息查询', width=24,
                         height=1, font=('Verdana', 20))
        label.grid(row=1, column=8, columnspan=5,
                   padx=80, pady=30)  # pady=20 界面的长度

        btn1 = tk.Button(self.window, text="学生成绩查询", width=24, height=1, relief='raised', font=('Verdana', 20),
                         command=lambda: StudentGradeView(
                             self.window, student_id),
                         fg='white', bg='blue', activebackground='black',
                         activeforeground='white')
        btn1.grid(row=3, column=8, columnspan=5, padx=80, pady=30)

        # btn2 = Button(self.window, text="考勤信息查询", width=24, height=1, relief='raised', font=('Verdana', 20),
        #               command=lambda: StudentAttendanceView(self.window, student_id),
        #               fg='white', bg='blue', activebackground='black',
        #               activeforeground='white')
        # btn2.grid(row=5, column=8, columnspan=5, padx=80, pady=30)

        self.window.protocol("WM_DELETE_WINDOW", self.back)  # 捕捉右上角关闭点击
        self.window.mainloop()  # 进入消息循环

    def back(self):
        StartPage(self.window)  # 显示主窗口 销毁本窗口


class StudentGradeView:  # 学生成绩信息查看界面
    def __init__(self, parent_window, student_id):
        parent_window.destroy()  # 销毁主界面

        self.window = tk.Tk()  # 初始框的声明
        self.window.title('学生成绩信息查看界面')
        self.student_id = student_id
        self.frame_center = tk.Frame(width=1100, height=400)
        # 定义下方中心列表区域
        self.columns = ("学号", "姓名", "性别", "年龄", "语文成绩",
                        "数学成绩", "英语成绩", "总分", "平均分")
        self.tree = ttk.Treeview(
            self.frame_center, show="headings", height=18, columns=self.columns)
        self.vbar = ttk.Scrollbar(
            self.frame_center, orient=tk.VERTICAL, command=self.tree.yview)
        # 定义树形结构与滚动条
        self.tree.configure(yscrollcommand=self.vbar.set)

        # 表格的标题
        self.tree.column("学号", width=150, anchor='center')  # 表示列,不显示
        self.tree.column("姓名", width=150, anchor='center')
        self.tree.column("性别", width=100, anchor='center')
        self.tree.column("年龄", width=100, anchor='center')
        self.tree.column("语文成绩", width=150, anchor='center')  # 表示列,不显示
        self.tree.column("数学成绩", width=150, anchor='center')
        self.tree.column("英语成绩", width=100, anchor='center')
        self.tree.column("总分", width=100, anchor='center')
        self.tree.column("平均分", width=100, anchor='center')
        # 调用方法获取表格内容插入
        self.tree.grid(row=0, column=0, sticky=tk.NSEW)
        self.vbar.grid(row=0, column=1, sticky=tk.NS)

        self.id = []
        self.name = []
        self.gender = []
        self.age = []
        self.c_grade = []
        self.m_grade = []
        self.e_grade = []
        self.total = []
        self.ave = []
        print("xx")
        # 打开数据库连接
        stu_dict = cc.query_student_score(student_id, K_CV)
        self.id.append(student_id)
        self.name.append(stu_dict['NAME'])
        self.gender.append(stu_dict['GEND'])
        self.age.append(stu_dict['AGE'])
        self.c_grade.append(stu_dict['MARK_C'])
        self.m_grade.append(stu_dict['MARK_M'])
        self.e_grade.append(stu_dict['MARK_E'])
        grade_total = stu_dict['MARK_C'] + \
            stu_dict['MARK_M'] + stu_dict['MARK_E']
        grade_ave = grade_total / 3
        self.total.append(grade_total)
        self.ave.append(grade_ave)
        # print(self.id)
        # print(self.name)
        # print(self.gender)
        # print(self.age)

        print("test***********************")
        for i in range(min(len(self.id), len(self.name), len(self.gender), len(self.age),
                           len(self.c_grade), len(self.m_grade), len(
            self.e_grade), len(self.total), len(self.ave)
        )):  # 写入数据
            self.tree.insert('', i, values=(self.id[i], self.name[i], self.gender[i], self.age[i],
                                            self.c_grade[i], self.m_grade[i], self.e_grade[i],
                                            self.total[i], self.ave[i]))

        for col in self.columns:  # 绑定函数，使表头可排序
            self.tree.heading(col, text=col,
                              command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))

        self.frame_center.grid(row=1, column=0, columnspan=2, padx=4, pady=5)

        self.frame_center.grid_propagate(0)

        self.frame_center.tkraise()  # 开始显示主菜单

        self.window.protocol("WM_DELETE_WINDOW", self.back)  # 捕捉右上角关闭点击
        self.window.mainloop()  # 进入消息循环

    def back(self):
        StudentInfoManage(self.window, self.student_id)  # 显示主窗口 销毁本窗口

    def tree_sort_column(self, tv, col, reverse):  # Treeview、列名、排列方式
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)  # 排序方式
        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):  # 根据排序后索引移动
            tv.move(k, '', index)
        tv.heading(col, command=lambda: self.tree_sort_column(
            tv, col, not reverse))  # 重写标题，使之成为再点倒序的标题


class AdminManage:
    def __init__(self, parent_window):
        parent_window.destroy()  # 销毁主界面

        self.window = tk.Tk()  # 初始框的声明
        self.window.title('管理员操作界面')

        self.frame_left_top = tk.Frame(width=300, height=400)
        self.frame_right_top = tk.Frame(width=200, height=250)
        self.frame_center = tk.Frame(width=1100, height=400)
        self.frame_bottom = tk.Frame(width=650, height=50)

        # 定义下方中心列表区域
        self.columns = ("学号", "姓名", "性别", "年龄", "语文成绩",
                        "数学成绩", "英语成绩", "总分", "平均分")
        self.tree = ttk.Treeview(
            self.frame_center, show="headings", height=18, columns=self.columns)
        self.vbar = ttk.Scrollbar(
            self.frame_center, orient=VERTICAL, command=self.tree.yview)
        # 定义树形结构与滚动条
        self.tree.configure(yscrollcommand=self.vbar.set)

        # 表格的标题
        self.tree.column("学号", width=150, anchor='center')  # 表示列,不显示
        self.tree.column("姓名", width=150, anchor='center')
        self.tree.column("性别", width=100, anchor='center')
        self.tree.column("年龄", width=100, anchor='center')
        self.tree.column("语文成绩", width=150, anchor='center')  # 表示列,不显示
        self.tree.column("数学成绩", width=150, anchor='center')
        self.tree.column("英语成绩", width=100, anchor='center')
        self.tree.column("总分", width=100, anchor='center')
        self.tree.column("平均分", width=100, anchor='center')
        # 调用方法获取表格内容插入
        self.tree.grid(row=0, column=0, sticky=NSEW)
        self.vbar.grid(row=0, column=1, sticky=NS)

        self.id = []
        self.name = []
        self.gender = []
        self.age = []
        self.c_grade = []
        self.m_grade = []
        self.e_grade = []
        self.total = []
        self.ave = []
        # global K_CV
        qry = 1

        stu_all_dict = cc.query_admin_stuscore(qry, K_CV)
        print('abcccc', stu_all_dict)
        for key in stu_all_dict.keys():
            self.id.append(stu_all_dict[key]['id'])
            self.name.append(stu_all_dict[key]['name'])
            self.gender.append(stu_all_dict[key]['gender'])
            self.age.append(stu_all_dict[key]['age'])
            self.c_grade.append(stu_all_dict[key]['c_grade'])
            self.m_grade.append(stu_all_dict[key]['m_grade'])
            self.e_grade.append(stu_all_dict[key]['e_grade'])
            total = stu_all_dict[key]['c_grade'] + \
                stu_all_dict[key]['m_grade'] + stu_all_dict[key]['e_grade']
            self.total.append(total)
            ave = (total / 3)
            self.ave.append(ave)
        print("查询学生字典成功！")
        for i in range(min(len(self.id), len(self.name), len(self.gender), len(self.age),
                           len(self.c_grade), len(self.m_grade), len(
            self.e_grade), len(self.total), len(self.ave)
        )):  # 写入数据
            self.tree.insert('', i, values=(self.id[i], self.name[i], self.gender[i], self.age[i],
                                            self.c_grade[i], self.m_grade[i], self.e_grade[i], self.total[i],
                                            self.ave[i]
                                            ))

        for col in self.columns:  # 绑定函数，使表头可排序
            self.tree.heading(col, text=col,
                              command=lambda _col=col: self.tree_sort_column(self.tree, _col, False))

        # 定义顶部区域
        # 定义左上方区域
        self.top_title = Label(self.frame_left_top,
                               text="学生信息:", font=('Verdana', 20))
        self.top_title.grid(row=0, column=0, columnspan=2,
                            sticky=NSEW, padx=50, pady=10)

        self.left_top_frame = tk.Frame(self.frame_left_top)
        self.var_id = StringVar()  # 声明学号
        self.var_name = StringVar()  # 声明姓名
        self.var_gender = StringVar()  # 声明性别
        self.var_age = StringVar()  # 声明年龄
        self.var_c_grade = StringVar()  # 声明语文成绩
        self.var_m_grade = StringVar()  # 声明数学成绩
        self.var_e_grade = StringVar()  # 声明英语成绩
        self.var_total = StringVar()  # 声明总分
        self.var_ave = StringVar()  # 声明平均分
        # 学号
        self.right_top_id_label = Label(
            self.frame_left_top, text="学号：", font=('Verdana', 15))
        self.right_top_id_entry = Entry(
            self.frame_left_top, textvariable=self.var_id, font=('Verdana', 15))
        self.right_top_id_label.grid(row=1, column=0)  # 位置设置
        self.right_top_id_entry.grid(row=1, column=1)
        # 姓名
        self.right_top_name_label = Label(
            self.frame_left_top, text="姓名：", font=('Verdana', 15))
        self.right_top_name_entry = Entry(
            self.frame_left_top, textvariable=self.var_name, font=('Verdana', 15))
        self.right_top_name_label.grid(row=2, column=0)  # 位置设置
        self.right_top_name_entry.grid(row=2, column=1)
        # 性别
        self.right_top_gender_label = Label(
            self.frame_left_top, text="性别：", font=('Verdana', 15))
        self.right_top_gender_entry = Entry(self.frame_left_top, textvariable=self.var_gender,
                                            font=('Verdana', 15))
        self.right_top_gender_label.grid(row=3, column=0)  # 位置设置
        self.right_top_gender_entry.grid(row=3, column=1)
        # 年龄
        self.right_top_gender_label = Label(
            self.frame_left_top, text="年龄：", font=('Verdana', 15))
        self.right_top_gender_entry = Entry(self.frame_left_top, textvariable=self.var_age,
                                            font=('Verdana', 15))
        self.right_top_gender_label.grid(row=4, column=0)  # 位置设置
        self.right_top_gender_entry.grid(row=4, column=1)

        # 语文成绩
        self.right_top_c_grade_label = Label(
            self.frame_left_top, text="语文成绩：", font=('Verdana', 15))
        self.right_top_c_grade_entry = Entry(self.frame_left_top, textvariable=self.var_c_grade,
                                             font=('Verdana', 15))
        self.right_top_c_grade_label.grid(row=5, column=0)  # 位置设置
        self.right_top_c_grade_entry.grid(row=5, column=1)

        # 数学成绩
        self.right_top_m_grade_label = Label(
            self.frame_left_top, text="数学成绩：", font=('Verdana', 15))
        self.right_top_m_grade_entry = Entry(self.frame_left_top, textvariable=self.var_m_grade,
                                             font=('Verdana', 15))
        self.right_top_m_grade_label.grid(row=6, column=0)  # 位置设置
        self.right_top_m_grade_entry.grid(row=6, column=1)

        # 英语成绩
        self.right_top_e_grade_label = Label(
            self.frame_left_top, text="英语成绩：", font=('Verdana', 15))
        self.right_top_e_grade_entry = Entry(self.frame_left_top, textvariable=self.var_e_grade,
                                             font=('Verdana', 15))
        self.right_top_e_grade_label.grid(row=7, column=0)  # 位置设置
        self.right_top_e_grade_entry.grid(row=7, column=1)

        # 定义右上方区域
        self.right_top_title = Label(
            self.frame_right_top, text="操作：", font=('Verdana', 20))

        self.tree.bind('<Button-1>', self.click)  # 左键获取位置
        self.right_top_button1 = ttk.Button(
            self.frame_right_top, text='新建学生信息', width=20, command=self.new_row)
        self.right_top_button2 = ttk.Button(self.frame_right_top, text='更新选中学生信息', width=20,
                                            command=self.updata_row)
        self.right_top_button3 = ttk.Button(self.frame_right_top, text='删除选中学生信息', width=20,
                                            command=self.del_row)
        self.right_top_button4 = ttk.Button(self.frame_right_top, text='清空', width=20,
                                            command=self.clear)
        # 位置设置
        self.right_top_title.grid(row=0, column=0, pady=10)
        self.right_top_button1.grid(row=1, column=0, padx=20, pady=10)
        self.right_top_button2.grid(row=2, column=0, padx=20, pady=10)
        self.right_top_button3.grid(row=3, column=0, padx=20, pady=10)
        self.right_top_button4.grid(row=4, column=0, padx=20, pady=10)
        # 整体区域定位
        self.frame_left_top.grid(row=0, column=0, padx=2, pady=5)
        self.frame_right_top.grid(row=0, column=1, padx=30, pady=40)
        self.frame_center.grid(row=1, column=0, columnspan=2, padx=4, pady=5)
        self.frame_bottom.grid(row=2, column=0, columnspan=2)

        self.frame_left_top.grid_propagate(0)
        self.frame_right_top.grid_propagate(0)
        self.frame_center.grid_propagate(0)
        self.frame_bottom.grid_propagate(0)

        self.frame_left_top.tkraise()  # 开始显示主菜单
        self.frame_right_top.tkraise()  # 开始显示主菜单
        self.frame_center.tkraise()  # 开始显示主菜单
        self.frame_bottom.tkraise()  # 开始显示主菜单

        self.window.protocol("WM_DELETE_WINDOW", self.back)  # 捕捉右上角关闭点击
        self.window.mainloop()  # 进入消息循环

    def back(self):
        InfoManage(self.window)  # 显示主窗口 销毁本窗口

    def click(self, event):
        self.col = self.tree.identify_column(event.x)  # 列
        self.row = self.tree.identify_row(event.y)  # 行

        print(self.col)
        print(self.row)
        self.row_info = self.tree.item(self.row, "values")
        self.var_id.set(self.row_info[0])
        self.var_name.set(self.row_info[1])
        self.var_gender.set(self.row_info[2])
        self.var_age.set(self.row_info[3])
        self.var_c_grade.set(self.row_info[4])
        self.var_m_grade.set(self.row_info[5])
        self.var_e_grade.set(self.row_info[6])
        self.var_total.set(self.row_info[7])
        self.var_ave.set(self.row_info[8])

        self.right_top_id_entry = Entry(self.frame_left_top, state='disabled', textvariable=self.var_id,
                                        font=('Verdana', 15))

        print('')

    def tree_sort_column(self, tv, col, reverse):  # Treeview、列名、排列方式
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)  # 排序方式
        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):  # 根据排序后索引移动
            tv.move(k, '', index)
        tv.heading(col, command=lambda: self.tree_sort_column(
            tv, col, not reverse))  # 重写标题，使之成为再点倒序的标题

    def clear(self):
        self.var_id.set('')
        self.var_name.set('')
        self.var_gender.set('')
        self.var_age.set('')
        self.var_c_grade.set('')
        self.var_m_grade.set('')
        self.var_e_grade.set('')
        self.var_total.set('')
        self.var_ave.set('')

    def new_row(self):
        print('123')
        print(self.var_id.get())
        print(self.id)
        if str(self.var_id.get()) in self.id:
            messagebox.showinfo('警告！', '该学生已存在！')
        else:
            if self.var_id.get() != '' and self.var_name.get() != '' and self.var_gender.get() != '' and self.var_age.get() != '' \
                    and self.var_c_grade.get() != '' and self.var_m_grade.get() != '' and self.var_e_grade.get() != '':
                stu_dict = {
                    'ID': self.var_id.get(),  # 学号
                    'NAME': self.var_name.get(),  # 姓名
                    'GEND': self.var_gender.get(),  # 性别
                    'AGE': self.var_age.get(),
                    'MARK_C': self.var_c_grade.get(),  # 语文成绩
                    'MARK_M': self.var_m_grade.get(),  # 数学成绩
                    'MARK_E': self.var_e_grade.get()  # 英语成绩
                }

                cc.add_admin_stuscore(stu_dict, K_CV)
                # cc.C_D_Send()
                print("添加学生成功")
                self.id.append(self.var_id.get())
                self.name.append(self.var_name.get())
                self.gender.append(self.var_gender.get())
                self.age.append(self.var_age.get())
                self.c_grade.append(self.var_c_grade.get())
                self.m_grade.append(self.var_m_grade.get())
                self.e_grade.append(self.var_e_grade.get())
                self.total.append(self.var_total.get())
                self.ave.append(self.var_ave.get())
                self.tree.insert('', len(self.id) - 1, values=(
                    self.id[len(self.id) - 1], self.name[len(self.id) -
                                                         1], self.gender[len(self.id) - 1],
                    self.age[len(self.id) - 1], self.c_grade[len(self.id) -
                                                             1], self.m_grade[len(self.id) - 1],
                    self.e_grade[len(self.id) - 1], self.total[len(self.id) - 1], self.ave[len(self.id) - 1],))
                self.tree.update()
                messagebox.showinfo('提示！', '插入成功！')
            else:
                messagebox.showinfo('警告！', '请填写学生数据')

    def del_row(self):
        res = messagebox.askyesnocancel('警告！', '是否删除所选数据？')
        if res == True:
            print(self.row_info[0])  # 鼠标选中的学号
            print(self.tree.selection()[0])  # 行号
            print(self.tree.get_children())  # 所有行

            id_index = self.id.index(self.row_info[0])
            cc.del_admin_stuscore(self.id[id_index], K_CV)
            print(id_index)
            del self.id[id_index]
            del self.name[id_index]
            del self.gender[id_index]
            del self.age[id_index]
            del self.c_grade[id_index]
            del self.m_grade[id_index]
            del self.e_grade[id_index]
            del self.total[id_index]
            del self.ave[id_index]

            print(self.id)
            self.tree.delete(self.tree.selection()[0])  # 删除所选行
            print(self.tree.get_children())

    def updata_row(self):
        res = messagebox.askyesnocancel('警告！', '是否更新所填数据？')
        if res == True:
            if self.var_id.get() == self.row_info[0]:  # 如果所填学号 与 所选学号一致
                # 打开数据库连接
                stu_dict = {
                    'ID': self.var_id.get(),  # 学号
                    'NAME': self.var_name.get(),  # 姓名
                    'GEND': self.var_gender.get(),  # 性别
                    'AGE': self.var_age.get(),
                    'MARK_C': self.var_c_grade.get(),  # 语文成绩
                    'MARK_M': self.var_m_grade.get(),  # 数学成绩
                    'MARK_E': self.var_e_grade.get()  # 英语成绩
                }
                id_index = self.id.index(self.row_info[0])
                cc.update_admin_stuscore(stu_dict, K_CV)
                self.name[id_index] = self.var_name.get()
                self.gender[id_index] = self.var_gender.get()
                self.age[id_index] = self.var_age.get()
                self.c_grade[id_index] = self.var_c_grade.get()
                self.m_grade[id_index] = self.var_m_grade.get()
                self.e_grade[id_index] = self.var_e_grade.get()
                self.total[id_index] = self.var_total.get()
                self.ave[id_index] = self.var_ave.get()

                self.tree.item(self.tree.selection()[0], values=(
                    self.var_id.get(), self.var_name.get(), self.var_gender.get(),
                    self.var_age.get(), self.var_c_grade.get(
                    ), self.var_m_grade.get(), self.var_e_grade.get(),
                    float(self.var_c_grade.get()) + float(self.var_m_grade.get()
                                                          ) + float(self.var_e_grade.get()),
                    (float(self.var_c_grade.get()) + float(self.var_m_grade.get()
                                                           ) + float(self.var_e_grade.get())) / 3
                ))  # 修改对于行信息
            else:
                messagebox.showinfo('警告！', '不能修改学生学号！')
