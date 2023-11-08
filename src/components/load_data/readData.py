import tkinter as tk
from tkinter import filedialog
from src.components.load_data.readFrame import ReadFrame
from src.components.load_data.changeFrame import ChangeFrame
from src.components.load_data.confirmFrame import ConfirmFrame
import pandas as pd


def deactivate(obj):
    obj.configure(state="disabled")


def activate(obj):
    obj.configure(state="active")


class ReadData(tk.Toplevel):

    def __init__(self, master, data_setter) -> None:
        super().__init__(master)
        self.geometry("600x600")
        self.data_setter = data_setter
        self.path = ""
        self.df = ""
        self.frames = []
        self.current_frame = None
        self.button_next = None
        self.button_back = None

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.mount()

    def mount(self):
        self.append_frame(ReadFrame(self))
        self.current_frame.grid(row=0, column=0, sticky="nsew")

        self.button_back = tk.Button(self, text="Wstecz", command=self.go_back)
        self.button_back.grid(row=1, column=0, sticky='se')
        deactivate(self.button_back)

        self.button_next = tk.Button(self, text="Dalej", command=self.go_next)
        self.button_next.grid(row=1, column=1, sticky='se')
        deactivate(self.button_next)

    def go_to_read_frame(self):
        self.frames = []
        self.append_frame(ReadFrame(self))

    def go_to_change_frame(self):
        activate(self.button_back)
        activate(self.button_next)

        self.path = self.current_frame.get_path()
        self.df = pd.read_excel(self.path)
        print(self.df)

        self.append_frame(ChangeFrame(self, self.df))
        self.current_frame.grid(row=0, column=0, sticky="nsew")

    def go_to_confirm_frame(self):
        activate(self.button_back)
        activate(self.button_next)

        entries = self.current_frame.get_columns_entries()
        self.update_column_names(entries)
        print(self.df)

        self.append_frame(ConfirmFrame(self, self.df))
        self.current_frame.grid(row=0, column=0, sticky="nsew")

    def append_frame(self, frame):
        self.frames.append(frame)
        self.current_frame = self.frames[-1]
        self.current_frame.focus_set()

    def go_back(self):
        frame_to_delete = self.frames.pop()
        frame_to_delete.destroy()
        self.current_frame = self.frames[-1]

        self.current_frame.grid(row=0, column=0, sticky="nsew")

    def go_next(self):
        self.current_frame = self.frames[-1]
        if isinstance(self.current_frame, ChangeFrame):
            self.go_to_confirm_frame()
        elif isinstance(self.current_frame, ConfirmFrame):
            self.button_read_from_path()

    def update_column_names(self, entries):
        new_names = [entry.get() for entry in entries]
        self.df.columns = new_names

    def button_read_from_path(self):
        if not self.path: return

        self.data_setter(self.df)
        self.master.footer.update_view()
        self.destroy()
        self.update()
