import tkinter as tk
#666

class LoginUI:
    def __init__(self, on_login):
        self.on_login = on_login  # 登录回调函数
        self.root = tk.Tk()
        self.root.title("登录")

        # 创建用户名Label和Entry
        tk.Label(self.root, text="用户名").grid(row=0)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.grid(row=0, column=1)

        # 创建密码Label和Entry
        tk.Label(self.root, text="密码").grid(row=1)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.grid(row=1, column=1)

        # 创建登录按钮
        login_btn = tk.Button(self.root, text="登录", command=self.login)
        login_btn.grid(row=2, column=0, columnspan=2, pady=10)

    def run(self):
        self.root.mainloop()

    def login(self):
        # 获取用户名和密码
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        self.on_login(username, password)
