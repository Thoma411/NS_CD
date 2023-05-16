import time
import json
import struct
from loginui import LoginUI
from network import send_message
from loginui import StartPage
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from tkinter import *  # 图形界面库

if __name__ == '__main__':
    # login_ui = LoginUI(on_login)
    window = tk.Tk()
    StartPage(window)
    # login_ui.run()
