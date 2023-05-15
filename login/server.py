import json
import socket
import pymysql

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

# 创建TCP/IP套接字并开始监听端口
server_address = ('localhost', 10006)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(server_address)
sock.listen(1)

while True:
    print("Waiting for a connection...")
    # 等待连接
    connection, client_address = sock.accept()
    try:
        print("Connection from", client_address)
        # 接收数据
        data = connection.recv(1024)
        print("Received:", repr(data))
        # data = b""  # 初始化空的byte字符串
        #
        # # 持续接收数据，直到读取完整个请求
        # while True:
        #     received_data = connection.recv(1024)
        #     if not received_data:
        #         break  # 客户端关闭连接
        #     data += received_data

        # 解析数据
        message = json.loads(data.decode('utf-8'))
        if "username" in message and "password" in message:
            if message["subtype"] == "01":  # 管理员
                username = message["username"]
                password = message["password"]
                print("Received message 1: username=%s, password=%s" % (username, password))
                admin_pass = None

                # 数据库操作 查询管理员表
                db = pymysql.connect(host="127.0.0.1", user="root", passwd="", db="student")  # 打开数据库连接
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
                        print("admin_id=%s,admin_pass=%s" % (admin_id, admin_pass))
                except:
                    print("Error: unable to fecth data")
                    # messagebox.showinfo('警告！', '用户名或密码不正确！')
                db.close()  # 关闭数据库连接

                print("正在登陆管理员管理界面")

                if message["password"] == admin_pass:
                    print(admin_pass)
                    connection.sendall("01".encode())
                    # AdminManage(self.window)  # 进入管理员操作界面
                    # InfoManage(self.window)
                else:
                    pass
            elif message["subtype"] == "02":  # 学生
                username = message["username"]
                password = message["password"]
                print("Received message 1: username=%s, password=%s" % (username, password))
                stu_pass = None

                db = pymysql.connect(host="127.0.0.1", user="root", passwd="", db="student")  # 打开数据库连接
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
                        print("stu_id=%s,stu_pass=%s,stu_type=%s" % (stu_id, stu_pass, stu_type))
                except:
                    print("Error: unable to fecth data")
                    # messagebox.showinfo('警告！', '用户名或密码不正确！')
                db.close()  # 关闭数据库连接

                print("正在登陆学生信息查看界面")

                if message["password"] == stu_pass:
                    print(stu_pass)
                    connection.sendall("01".encode())  # 进入学生信息查看界面
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
        else:
            print("Unknown message type")

    finally:
        # 关闭连接
        connection.close()
