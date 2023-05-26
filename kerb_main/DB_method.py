'''
Author: sccccc1 & Luckyhao266
Date: 2023-05-10 20:22:14
LastEditTime: 2023-05-22 20:33:53
Description: 
'''
import socket as sk
import threading as th
import pymysql
from MsgFieldDef import *

SERVER_HOST = '0.0.0.0'
DB_HOST = '127.0.0.1'
SERVER_PORT = 10001
MAX_SIZE = 2048
MAX_LISTEN = 16


def sql_login_adm(usrname):  # 管理员登录连接数据库
    db = pymysql.connect(host=DB_HOST, user="root",
                         passwd="", db="student")
    cursor = db.cursor()  # 使用cursor()方法获取操作游标
    sql = "SELECT * FROM admin_login_k WHERE username = '%s' and type = 0" % usrname  # SQL 查询语句
    try:
        cursor.execute(sql)
        results = cursor.fetchall()  # 获取所有记录列表
        for row in results:
            adm_id = row[0]
            adm_pwd = row[1]
            print(f'admin_id: {adm_id}, admin_pass: {adm_pwd}')
            print('[DB] 正在登录管理员管理界面')
            return adm_pwd
    except:
        print("[DB] Error: unable to fetch data")
        # messagebox.showinfo('警告！', '用户名或密码不正确！')
    db.close()


def sql_login_stu(usrname):  # 学生登录连接数据库
    db = pymysql.connect(host=DB_HOST, user="root",
                         passwd="", db="student")
    cursor = db.cursor()  # 使用cursor()方法获取操作游标
    sql = "SELECT * FROM user_login_k WHERE username = '%s' and type = 1" % usrname  # SQL 查询语句
    try:
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            stu_id = row[0]
            stu_pass = row[1]
            stu_type = row[2]
            print(f'sid: {stu_id}, stu_pwd: {stu_pass}, stu_type: {stu_type}')
            return stu_pass
    except:
        print("[DB] Error: unable to fecth data")
        # messagebox.showinfo('警告！', '用户名或密码不正确！')
    db.close()
    print("[DB] 正在登录学生信息查看界面")


def sql_search_stu(sid):  # 学生成绩查询连接数据库
    db = pymysql.connect(host=DB_HOST, user="root",
                         passwd="", db="student")
    cursor = db.cursor()  # 使用cursor()方法获取操作游标
    sql = "SELECT name, gender, age, c_grade, m_grade, e_grade FROM student_k WHERE id='%s'" % sid  # SQL 查询语句
    try:
        cursor.execute(sql)
        results = cursor.fetchall()  # 获取所有记录列表
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
            print("[DB] 没有找到学生记录")
            return {}
    except Exception as e:
        print("[DB] 查询学生成绩时发生错误。错误消息：", e)
        # 数据库操作时发生错误，将错误信息发送给客户端
        connection.sendall(dict2str({"error": str(e)}).encode())
    finally:
        db.close()


def sql_search_adm():  # 管理员查询连接数据库
    db = pymysql.connect(host=DB_HOST, user="root", passwd="", db="student")
    cursor = db.cursor()  # 使用cursor()方法获取操作游标
    sql = "SELECT * FROM student_k"  # SQL 查询语句
    stu_list = []  # 创建一个空列表用于存储学生信息的字典
    try:
        cursor.execute(sql)  # 执行SQL语句
        results = cursor.fetchall()  # 获取所有记录列表
        for row in results:  # 将每个学生信息存储到一个字典中
            stu_dict = {
                "id": row[0],
                "name": row[1],
                "gender": row[2],
                "age": row[3],
                "c_grade": row[4],
                "m_grade": row[5],
                "e_grade": row[6]
            }
            stu_list.append(stu_dict)  # 将学生信息的字典添加到列表中
        # 将学生信息的字典添加到列表中
        stu_all_dict = {}  # 创建一个字典用于保存所有学生的信息， 其中键值是每个学生的id
        for stu in stu_list:
            id = stu['id']
            stu_all_dict[id] = stu
        print('[DB] 学生成绩的所有字典:', stu_all_dict)
        return stu_all_dict
    except Exception as e:
        print('[DB] 查询学生成绩时发生错误。错误消息:', e)
        # 数据库操作时发生错误，将错误信息发送给客户端
        connection.sendall(dict2str({"error": str(e)}).encode())
    db.close()
    return stu_list  # 返回学生信息的列表


def sql_del_stu(sid):  # 管理员修改学生信息
    db = pymysql.connect(host=DB_HOST, user="root", passwd="", db="student")
    cursor = db.cursor()  # 使用cursor()方法获取操作游标
    print('[DB] 打印学生id:', sid)
    sql = "DELETE FROM student_k WHERE id = '%s'" % sid  # SQL 插入语句
    try:
        cursor.execute(sql)
        db.commit()  # 提交到数据库执行
        # messagebox.showinfo('提示！', '删除成功！')
        return 1
    except:
        db.rollback()  # 发生错误时回滚
        # messagebox.showinfo('警告！', '删除失败，数据库连接失败！')
    db.close()


def sql_add_stu(stu_dict):  # 管理员增加学生信息
    # if str(self.var_id.get()) in self.id:
    #     messagebox.showinfo('警告！', '该学生已存在！')
    # else:
    print('[DB] 增加学生的字典', stu_dict)
    if stu_dict['ID'] != '' and stu_dict['NAME'] != '' and stu_dict['GEND'] != '' and stu_dict['AGE'] != '' \
            and stu_dict['MARK_C'] != '' and stu_dict['MARK_M'] != '' and stu_dict['MARK_E'] != '':
        db = pymysql.connect(host='127.0.0.1', user="root",
                             passwd="", db="student")
        cursor = db.cursor()  # 使用cursor()方法获取操作游标
        total = float(stu_dict['MARK_C']) + \
            float(stu_dict['MARK_M']) + float(stu_dict['MARK_E'])
        ave = (float(stu_dict['MARK_C']) +
               float(stu_dict['MARK_M']) + float(stu_dict['MARK_E'])) / 3
        sql = "INSERT INTO student_k(id, name, gender, age ,c_grade, m_grade, e_grade, total ,ave ) \
				       VALUES ('%s', '%s', '%s', '%s','%s','%s','%s','%s','%s')" % \
              (stu_dict['ID'], stu_dict['NAME'], stu_dict['GEND'], stu_dict['AGE'],
               stu_dict['MARK_C'], stu_dict['MARK_M'], stu_dict['MARK_E'], total, ave)  # SQL 插入语句
        try:
            cursor.execute(sql)  # 执行sql语句
            db.commit()  # 提交到数据库执行
        except:
            db.rollback()  # 发生错误时回滚
            # messagebox.showinfo('警告！', '数据库连接失败！')
        db.close()


def sql_update_stu(stu_dict):  # 管理员更新学生信息
    # res = messagebox.askyesnocancel('警告！', '是否更新所填数据？')
    # if res == True:
    #     if self.var_id.get() == self.row_info[0]:  # 如果所填学号 与 所选学号一致
    db = pymysql.connect(host=DB_HOST, user="root", passwd="", db="student")
    cursor = db.cursor()  # 使用cursor()方法获取操作游标
    print("[DB] 更新的学生的信息为:", stu_dict)
    sql = "UPDATE student_k SET name = '%s', gender = '%s', age = '%s',c_grade = '%s', m_grade = '%s', e_grade = '%s' , total = '%s', ave = '%s'  \
				 WHERE id = '%s'" % (
        stu_dict['NAME'], stu_dict['GEND'], stu_dict['AGE'],
        stu_dict['MARK_C'], stu_dict['MARK_M'], stu_dict['MARK_E'],
        float(stu_dict['MARK_C']) + float(stu_dict['MARK_M']) +
        float(stu_dict['MARK_E']),
        (float(stu_dict['MARK_C']) + float(stu_dict['MARK_M'])
         + float(stu_dict['MARK_E'])) / 3, stu_dict['ID'])  # SQL 插入语句

    try:
        cursor.execute(sql)  # 执行sql语句
        db.commit()  # 提交到数据库执行
        # messagebox.showinfo('提示！', '更新成功！')
    except:
        db.rollback()  # 发生错误时回滚
        # messagebox.showinfo('警告！', '更新失败，数据库连接失败！')
    db.close()


def handle_client(conn, caddr):
    try:
        print('Connection from', caddr)
        data = conn.recv(MAX_SIZE)  # 接收数据
        print("Received:", repr(data), type(data))
        msg = str2dict(data.decode())  # 解析数据
        print(msg)
        if "username" in msg and "password" in msg:
            if msg["INTYPE"] == IND_ADM:  # 管理员
                usr = msg["username"]
                pwd = msg["password"]
                print(f'Received message 1: username={usr}, password={pwd}')
                admin_pass = sql_login_adm(usr)  # 数据库操作 查询管理员表

                if msg["password"] == admin_pass:
                    print(admin_pass)
                    conn.sendall('01'.encode())
                else:
                    pass
            elif msg["INTYPE"] == IND_STU:  # 学生
                usr = msg["username"]
                pwd = msg["password"]
                print(f'Received message 1: username={usr}, password={pwd}')
                stu_pass = sql_login_stu(usr)
                if msg["password"] == stu_pass:
                    print(stu_pass)
                    conn.sendall('01'.encode())  # 进入学生信息查看界面
                    data = conn.recv(MAX_SIZE)
                    # 解析数据
                    msg = str2dict(data.decode())
                else:
                    pass
        elif "student_id" in msg and len(msg) == 1:
            student_id = msg["student_id"]
            sql_search_stu(student_id)  # 数据库操作 查询学生成绩
            print('1')

        # conn.close()  # 当前请求处理完毕后可以关闭连接
        print(f'Closed connection: {caddr}')
    except Exception as e:
        print(f'Error occurred on thread for {caddr}: {e}')
        # conn.close()


if __name__ == '__main__':
    server_socket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    server_socket.bind(('', SERVER_PORT))
    server_socket.listen(MAX_LISTEN)
    print(f'Server listening on {SERVER_HOST}:{SERVER_PORT}...')
    while True:
        connection, client_address = server_socket.accept()
        t = th.Thread(target=handle_client,
                      args=(connection, client_address))
        t.start()
