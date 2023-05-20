import json
import socket as sk
import threading as th
import pymysql
from MsgFieldDef import *


SERVER_HOST = '0.0.0.0'
DB_HOST = '192.168.137.60'
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
                "name": result[0],
                "gender": result[1],
                "age": result[2],
                "chinese_score": result[3],
                "math_score": result[4],
                "english_score": result[5]
            }
            # 发送成绩字典数据给客户端
            connection.sendall(dict2str(scores_dict).encode())
        else:
            # 没有找到学生记录，发送空字典给客户端
            connection.sendall(dict2str({}).encode())
            print("没有找到学生记录")
    except Exception as e:
        print("查询学生成绩时发生错误。错误消息：", e)
        # 数据库操作时发生错误，将错误信息发送给客户端
        connection.sendall(dict2str({"error": str(e)}).encode())
    finally:
        db.close()  # 关闭数据库连接


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
