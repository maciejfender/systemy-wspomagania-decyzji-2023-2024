import tkinter as tk
from tkinter import filedialog
from src.components.load_data.readFrame import ReadFrame
import pandas as pd


class ReadData(tk.Toplevel):

    def __init__(self, master, data_setter) -> None:
        super().__init__(master)
        self.geometry("600x600")
        self.data_setter = data_setter
        self.path = ""
        self.frames = []
        self.current_frame = None
        self.button_ask_for_path = None
        self.button_next = None
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        # self.button_ask_for_path.pack()

        self.mount()
        # self.button_read_from_path = tk.Button(self, text="read", command=self.button_read_from_path)
        # self.button_read_from_path.pack()

    def mount(self):
        self.button_ask_for_path = tk.Button(self, text="Wczytaj dane", command=self.ask_for_path)
        self.button_ask_for_path.grid(row=0, column=0, padx=10, pady=10)

        read_frame = ReadFrame(self)
        self.frames.append(read_frame)
        self.current_frame = read_frame
        self.current_frame.grid(row=1, column=0, sticky="nsew")


        self.button_next = tk.Button(self, text="Dalej")
        self.button_next.grid(row=2, column=0,sticky='se')

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
