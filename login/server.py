import json
import socket as sk
import threading as th
import pymysql

SERVER_HOST = 'localhost'
SERVER_PORT = 10001
BUFFER_SIZE = 1024
MAX_LISTEN = 16

# 定义首部格式
header = {
    "head": "int:2",  # 头部，长度为2
    "type": "int:2",  # 大类型标识，长度为2
    "subtype": "int:2",  # 小类型标识，长度为2
    "timestamp": "str:10",  # 时间戳，长度为10
    "length": "int:4",  # 正文长度，长度为4
    "redundancy": "int:4"  # 冗余位，长度为4
}

# 定义第一个报文的类型
message1 = {
    "head": "int:2",  # 头部，长度为2
    "type": "int:2",  # 大类型标识，长度为2
    "subtype": "int:2",  # 小类型标识，长度为2
    "timestamp": "str:10",  # 时间戳，长度为10
    "length": "int:4",  # 正文长度，长度为4
    "redundancy": "int:4",  # 冗余位，长度为4
    "username": "str",
    "password": "str"
}

# 定义第二个报文的类型
message2 = {
    "header": header,
    "name": "str",
    "student_id": "str",
    "chinese_score": "int",
    "math_score": "int",
    "english_score": "int",
}


def handle_client(connection, client_address):
    try:
        print("Connection from", client_address)

        # 接收数据
        data = connection.recv(1024)
        print("Received:", repr(data))

        # 解析数据
        message = json.loads(data.decode('utf-8'))
        if "username" in message and "password" in message:
            if message["subtype"] == "01":  # 管理员
                username = message["username"]
                password = message["password"]
                print("Received message 1: username=%s, password=%s" %
                      (username, password))
                admin_pass = None

                # 数据库操作 查询管理员表
                db = pymysql.connect(
                    host="127.0.0.1", user="root", passwd="", db="student")  # 打开数据库连接
                cursor = db.cursor()  # 使用cursor()方法获取操作游标
                sql = "SELECT * FROM user_login_k WHERE username = '%s' and type = 0" % (
                    message["username"])  # SQL 查询语句
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
                except:
                    print("Error: unable to fetch data")
                    # messagebox.showinfo('警告！', '用户名或密码不正确！')
                db.close()  # 关闭数据库连接

                print("正在登陆管理员管理界面")

                if message["password"] == admin_pass:
                    print(admin_pass)
                    connection.sendall("01".encode())
                else:
                    pass
            elif message["subtype"] == "02":  # 学生
                username = message["username"]
                password = message["password"]
                print("Received message 1: username=%s, password=%s" %
                      (username, password))
                stu_pass = None

                db = pymysql.connect(
                    host="127.0.0.1", user="root", passwd="", db="student")  # 打开数据库连接
                cursor = db.cursor()  # 使用cursor()方法获取操作游标
                sql = "SELECT * FROM user_login_k WHERE username = '%s' and type = 1" % (
                    message["username"])  # SQL 查询语句
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
                except:
                    print("Error: unable to fecth data")
                    # messagebox.showinfo('警告！', '用户名或密码不正确！')
                db.close()  # 关闭数据库连接

                print("正在登陆学生信息查看界面")

                if message["password"] == stu_pass:
                    print(stu_pass)
                    connection.sendall("01".encode())  # 进入学生信息查看界面
                    data = connection.recv(1024)
                    # 解析数据
                    message = json.loads(data.decode('utf-8'))

                else:
                    pass

        elif "header" in message and "name" in message and "student_id" in message and "chinese_score" in message:
            name = message["name"]
            student_id = message["student_id"]
            chinese_score = message["chinese_score"]
            math_score = message["math_score"] if "math_score" in message else None
            english_score = message["english_score"] if "english_score" in message else None
            print("Received message 2: name=%s, student_id=%s, chinese_score=%d, math_score=%s, english_score=%s"
                  % (name, student_id, chinese_score, math_score, english_score))
            # 处理第二个数据报文
        elif "student_id" in message and len(message) == 1:
            student_id = message["student_id"]
            print("1")
            # 数据库操作 查询学生成绩
            db = pymysql.connect(host="127.0.0.1", user="root",
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
                    connection.sendall(json.dumps(scores_dict).encode())
                else:
                    # 没有找到学生记录，发送空字典给客户端
                    connection.sendall(json.dumps({}).encode())
                    print("没有找到学生记录")
            except Exception as e:
                print("查询学生成绩时发生错误。错误消息：", e)
                # 数据库操作时发生错误，将错误信息发送给客户端
                connection.sendall(json.dumps({"error": str(e)}).encode())
            finally:
                db.close()  # 关闭数据库连接

        # 当前请求处理完毕后可以关闭连接
        connection.close()
        print(f"Closed connection: {client_address}")
    except Exception as e:
        print(f"Error occured on thread for {client_address}: {e}")
        connection.close()


if __name__ == '__main__':

    server_socket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(MAX_LISTEN)

    print(f"Server listening on {SERVER_HOST}:{SERVER_PORT}...")

    while True:
        connection, client_address = server_socket.accept()
        t = th.Thread(target=handle_client,
                             args=(connection, client_address))
        t.start()
