import tkinter as tk
from tkinter import filedialog

import pandas as pd


class CheckData(tk.Toplevel):

    def __init__(self, master, data_setter) -> None:
        super().__init__(master,width=100,height=100)
        self.data_setter = data_setter
        self.path = ""
        self.button_ask_for_path = tk.Button(self, text="path", command=self.ask_for_path)
        self.button_ask_for_path.pack()

        self.button_read_from_path = tk.Button(self, text="read", command=self.button_read_from_path)
        self.button_read_from_path.pack()

    def ask_for_path(self):
        path = filedialog.askopenfile()
        self.focus_set()
        if path is None:
            return
        self.path = path.name

    def button_read_from_path(self):
        if not self.path: return

        self.data_setter(pd.read_excel(self.path))
        self.master.footer.update_view()
        self.destroy()
        self.update()


