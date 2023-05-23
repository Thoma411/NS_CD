import tkinter as tk
from tkinter import filedialog
import os
import time

class TextFileReader(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        self.title('实时文本阅读器')
        
        self.text1 = tk.Text(self, wrap=tk.WORD)
        self.text1.pack(expand=True, fill=tk.BOTH)
        
        self.text2 = tk.Text(self, wrap=tk.WORD)
        self.text2.pack(expand=True, fill=tk.BOTH)
        
        button = tk.Button(self, text='打开文件1', command=self.open_file_1)
        button.pack(fill=tk.X)
        
        button2 = tk.Button(self, text='打开文件2', command=self.open_file_2)
        button2.pack(fill=tk.X)
        
        self.file_path_1 = None
        self.file_path_2 = None
        
        self.text_last_update_time_1 = None
        self.text_last_update_time_2 = None

        self.poll_file_changes()

    def load_text(self, file_path, text_widget):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, content)

    def open_file_1(self):
        self.file_path_1 = filedialog.askopenfilename()
        self.text_last_update_time_1 = time.time()
        self.load_text(self.file_path_1, self.text1)

    def open_file_2(self):
        self.file_path_2 = filedialog.askopenfilename()
        self.text_last_update_time_2 = time.time()
        self.load_text(self.file_path_2, self.text2)

    def poll_file_changes(self):
        if self.file_path_1:
            if os.path.getmtime(self.file_path_1) >= self.text_last_update_time_1:
                self.load_text(self.file_path_1, self.text1)
            
        if self.file_path_2:
            if os.path.getmtime(self.file_path_2) >= self.text_last_update_time_2:
                self.load_text(self.file_path_2, self.text2)

        self.after(2000, self.poll_file_changes)

if __name__ == '__main__':
    app = TextFileReader()
    app.mainloop()

