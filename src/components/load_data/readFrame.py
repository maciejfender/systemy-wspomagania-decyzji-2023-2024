import tkinter as tk
from tkinter import filedialog


class ReadFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.path = None
        self.label = None
        self.button_ask_for_path = None

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.mount()

    def mount(self):
        self.button_ask_for_path = tk.Button(self, text="Wczytaj dane", command=self.ask_for_path)
        self.button_ask_for_path.grid(row=0, column=0, padx=10, pady=10)

        self.label = tk.Label(self, text="Cześć")
        self.label.grid(row=1, column=0, padx=10, pady=10)

    def show_message_loaded_data(self):
        label = tk.Label(self, text="Wczytano dane")
        label.grid(row=1, column=0, padx=10, pady=10)

    def ask_for_path(self):
        path = filedialog.askopenfile()
        self.focus_set()
        if path is None:
            return
        self.path = path.name

        self.show_message_loaded_data()
        self.master.focus_set()
        self.master.go_to_change_frame()

    def get_path(self):
        return self.path
