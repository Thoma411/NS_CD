import socket as sk
import threading as th
import pymysql
from MsgFieldDef import *


SERVER_HOST = '0.0.0.0'
DB_HOST = '127.0.0.1'
SERVER_PORT = 10001
BUFFER_SIZE = 1024
MAX_LISTEN = 16


# 管理员登陆连接数据库
def sql_login_adm(username):
    db = pymysql.connect(
        host=DB_HOST, user="root", passwd="", db="student")  # 打开数据库连接
    cursor = db.cursor()  # 使用cursor()方法获取操作游标
    sql = "SELECT * FROM user_login_k WHERE username = '%s' and type = 0" % (
        username)  # SQL 查询语句
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            admin_id = row[0]
            admin_pass = row[1]
            # 打印结果
            print("admin_id=%s,admin_pass=%s" %
                  (admin_id, admin_pass))
            print("正在登陆管理员管理界面")
            return admin_pass
    except:
        print("Error: unable to fetch data")
        # messagebox.showinfo('警告！', '用户名或密码不正确！')
    db.close()  # 关闭数据库连接


# 学生登录连接数据库
def sql_login_stu(username):
    db = pymysql.connect(
        host=DB_HOST, user="root", passwd="", db="student")  # 打开数据库连接
    cursor = db.cursor()  # 使用cursor()方法获取操作游标
    sql = "SELECT * FROM user_login_k WHERE username = '%s' and type = 1" % (
        username)  # SQL 查询语句
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            stu_id = row[0]
            stu_pass = row[1]
            stu_type = row[2]
            # 打印结果
            print("stu_id=%s,stu_pass=%s,stu_type=%s" %
                  (stu_id, stu_pass, stu_type))
            return stu_pass
    except:
        print("Error: unable to fecth data")
        # messagebox.showinfo('警告！', '用户名或密码不正确！')
    db.close()  # 关闭数据库连接

    print("正在登陆学生信息查看界面")


# 学生成绩查询连接数据库
def sql_search_stu(student_id):
    db = pymysql.connect(host=DB_HOST, user="root",
                         passwd="", db="student")  # 打开数据库连接
    cursor = db.cursor()  # 使用cursor()方法获取操作游标
    sql = "SELECT name, gender, age, c_grade, m_grade, e_grade FROM student_k WHERE id='%s'" % student_id  # SQL 查询语句
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        if len(results) > 0:
            # 取第一个结果
            result = results[0]
            # 构建成绩字典
            scores_dict = {
                'NAME': result[0],
                'GEND': result[1],
                'AGE': result[2],
                'MARK_C': result[3],
                'MARK_M': result[4],
                'MARK_E': result[5]
            }
            # 发送成绩字典数据给客户端
            # connection.sendall(dict2str(scores_dict).encode())
            return scores_dict
        else:
            # 没有找到学生记录，发送空字典给客户端
            # connection.sendall(dict2str({}).encode())
            return {}
            print("没有找到学生记录")
    except Exception as e:
        print("查询学生成绩时发生错误。错误消息：", e)
        # 数据库操作时发生错误，将错误信息发送给客户端
        connection.sendall(dict2str({"error": str(e)}).encode())
    finally:
        db.close()  # 关闭数据库连接


# 管理员查询连接数据库
def sql_search_adm():
    db = pymysql.connect(host="127.0.0.1", user="root", passwd="", db="student")
    cursor = db.cursor()  # 使用cursor()方法获取操作游标
    sql = "SELECT * FROM student_k"  # SQL 查询语句

    student_list = []  # 创建一个空列表用于存储学生信息的字典

    try:
        cursor.execute(sql)  # 执行SQL语句
        results = cursor.fetchall()  # 获取所有记录列表

        for row in results:
            # 将每个学生信息存储到一个字典中
            stu_dict = {
                "id": row[0],
                "name": row[1],
                "gender": row[2],
                "age": row[3],
                "c_grade": row[4],
                "m_grade": row[5],
                "e_grade": row[6]
            }

            student_list.append(stu_dict) # 将学生信息的字典添加到列表中
 # 将学生信息的字典添加到列表中
        students_all_dict = {}  # 创建一个字典用于保存所有学生的信息， 其中键值是每个学生的id
        for student in student_list:
            id = student['id']
            students_all_dict[id] = student
        print('学生成绩的所有字典db：',students_all_dict)
        return students_all_dict
    except Exception as e:  # 捕获异常
        print("查询学生成绩时发生错误。错误消息：", e)
        # 数据库操作时发生错误，将错误信息发送给客户端
        connection.sendall(dict2str({"error": str(e)}).encode())

    db.close()  # 关闭数据库连接
    return student_list  # 返回学生信息的列表


# 管理员修改学生信息
def sql_del_stu(stu_id):
    # res = messagebox.askyesnocancel('警告！', '是否删除所选数据？')
    # if res == True:
    #     print(self.row_info[0])  # 鼠标选中的学号
    #     print(self.tree.selection()[0])  # 行号
    #     print(self.tree.get_children())  # 所有行
    # 打开数据库连接
    db = pymysql.connect(host="127.0.0.1", user="root", passwd="", db="student")
    cursor = db.cursor()  # 使用cursor()方法获取操作游标
    sql = "DELETE FROM student_k WHERE id = '%s'" % (stu_id)  # SQL 插入语句
    try:
        cursor.execute(sql)  # 执行sql语句
        db.commit()  # 提交到数据库执行
        # messagebox.showinfo('提示！', '删除成功！')
        return 1
    except:
        db.rollback()  # 发生错误时回滚
        # messagebox.showinfo('警告！', '删除失败，数据库连接失败！')
        return 0
    db.close()  # 关闭数据库连接


# 管理员增加学生信息
def sql_add_stu(stu_id, stu_dict):
    # if str(self.var_id.get()) in self.id:
    #     messagebox.showinfo('警告！', '该学生已存在！')
    # else:
    if stu_id != '' and stu_dict['NAME'] != '' and stu_dict['GENDER'] != '' and stu_dict['AGE'] != '' \
            and stu_dict['MARK_C'] != '' and stu_dict['MARK_M'] != '' and stu_dict['MARK_E'] != '':
        # 打开数据库连接
        db = pymysql.connect(host="127.0.0.1", user="root", passwd="", db="student")
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        sql = "INSERT INTO student_stu_dict['NAME']k(id, name, gender, age ,c_grade, m_grade, e_grade, total ,ave ) \
				       VALUES ('%s', '%s', '%s', '%s','%s','%s','%s','%s','%s')" % \
              (stu_id, stu_dict['NAME'], stu_dict['GENDER'], stu_dict['AGE'],
               stu_dict['MARK_C'], stu_dict['MARK_M'], stu_dict['MARK_E'],
               float(stu_dict['MARK_C']) + float(stu_dict['MARK_M']) + float(stu_dict['MARK_E']),
               (float(stu_dict['MARK_C']) + float(stu_dict['MARK_M']) + float(
                   stu_dict['MARK_E'])) / 3
               )  # SQL 插入语句
        try:
            cursor.execute(sql)  # 执行sql语句
            db.commit()  # 提交到数据库执行
        except:
            db.rollback()  # 发生错误时回滚
            # messagebox.showinfo('警告！', '数据库连接失败！')
        db.close()  # 关闭数据库连接


# 管理员更新学生信息
def sql_update_stu(stu_id, stu_dict):
    # res = messagebox.askyesnocancel('警告！', '是否更新所填数据？')
    # if res == True:
    #     if self.var_id.get() == self.row_info[0]:  # 如果所填学号 与 所选学号一致
    #         # 打开数据库连接
    db = pymysql.connect(host="127.0.0.1", user="root", passwd="", db="student")
    cursor = db.cursor()  # 使用cursor()方法获取操作游标
    sql = "UPDATE student_k SET name = '%s', gender = '%s', age = '%s',c_grade = '%s', m_grade = '%s', e_grade = '%s' , total = '%s', ave = '%s'  \
				 WHERE id = '%s'" % (
        stu_dict['NAME'], stu_dict['GENDER'], stu_dict['AGE'],
        stu_dict['MARK_C'], stu_dict['MARK_M'], stu_dict['MARK_E'],
        float(stu_dict['MARK_C']) + float(stu_dict['MARK_M']) + float(stu_dict['MARK_E']),
        (float(stu_dict['MARK_C']) + float(stu_dict['MARK_M']) + float(stu_dict['MARK_E'])) / 3,
        stu_id)  # SQL 插入语句

    try:
        cursor.execute(sql)  # 执行sql语句
        db.commit()  # 提交到数据库执行
        # messagebox.showinfo('提示！', '更新成功！')
    except:
        db.rollback()  # 发生错误时回滚
        # messagebox.showinfo('警告！', '更新失败，数据库连接失败！')
    db.close()  # 关闭数据库连





def handle_client(connection, client_address):
    try:
        print("Connection from", client_address)

        # 接收数据
        data = connection.recv(1024)
        print("Received:", repr(data), type(data))

        # 解析数据
        message = str2dict(data.decode('utf-8'))
        print(message)
        if "username" in message and "password" in message:
            if message["INTYPE"] == 10:  # 管理员
                username = message["username"]
                password = message["password"]
                print("Received message 1: username=%s, password=%s" %
                      (username, password))
                # 数据库操作 查询管理员表
                admin_pass = sql_login_adm(username)

                if message["password"] == admin_pass:
                    print(admin_pass)
                    connection.sendall("01".encode())
                else:
                    pass
            elif message["INTYPE"] == 11:  # 学生
                username = message["username"]
                password = message["password"]
                print("Received message 1: username=%s, password=%s" %
                      (username, password))
                stu_pass = sql_login_stu(username)
                if message["password"] == stu_pass:
                    print(stu_pass)
                    connection.sendall("01".encode())  # 进入学生信息查看界面
                    data = connection.recv(1024)
                    # 解析数据
                    message = str2dict(data.decode('utf-8'))

                else:
                    pass

        elif "student_id" in message and len(message) == 1:
            student_id = message["student_id"]
            sql_search_stu(student_id)
            print("1")
            # 数据库操作 查询学生成绩

        # 当前请求处理完毕后可以关闭连接
        # connection.close()
        print(f"Closed connection: {client_address}")
    except Exception as e:
        print(f"Error occurred on thread for {client_address}: {e}")
        # connection.close()


if __name__ == '__main__':

    server_socket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    server_socket.bind(('', SERVER_PORT))
    server_socket.listen(MAX_LISTEN)

    print(f"Server listening on {SERVER_HOST}:{SERVER_PORT}...")

    while True:
        connection, client_address = server_socket.accept()
        t = th.Thread(target=handle_client,
                      args=(connection, client_address))
        t.start()
