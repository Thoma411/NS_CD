from C_ui import StartPage
from C_ui import TextFileReader
import tkinter as tk

if __name__ == '__main__':
    window = tk.Tk()
    StartPage(window)
    window1=tk.Tk()
    TextFileReader(window1)
    window.mainloop()