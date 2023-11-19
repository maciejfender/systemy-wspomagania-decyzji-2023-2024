import tkinter as tk
from tkinter import filedialog
from src.components.engine.engineUtils import normal, deactivate, activate


class ReadFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.path = None
        self.label = None
        self.button_ask_for_path = None
        self.header_checkbox_var = None
        self.header_checkbox = None
        self.separator_checkbox_var = None
        self.separator_checkbox = None
        self.separator_label = None
        self.separator_entry = None

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.mount()

    def mount(self):
        self.focus_set()
        self.label = tk.Label(self, text="Wczytywanie danych")
        self.label.grid(row=0, column=0, padx=10, pady=10)

        self.button_ask_for_path = tk.Button(self, text="Wczytaj dane", command=self.ask_for_path)
        self.button_ask_for_path.grid(row=1, column=0, padx=10, pady=10)

        self.header_checkbox_var = tk.BooleanVar()
        self.header_checkbox = tk.Checkbutton(self, text="Czy posiada nagłówek?", variable=self.header_checkbox_var)
        self.header_checkbox.grid(row=2, column=0, padx=10, pady=10)

        self.separator_checkbox_var = tk.BooleanVar()
        self.separator_checkbox = tk.Checkbutton(self, text="Czy separator?", variable=self.separator_checkbox_var,
                                                 command=self.change_separator_entry_state)
        self.separator_checkbox.grid(row=3, column=0, padx=10, pady=10)

        self.separator_label = tk.Label(self, text="Separator")
        self.separator_label.grid(row=4, column=0, padx=10, pady=10)

        self.separator_entry = tk.Entry(master=self)
        deactivate(self.separator_entry)
        self.separator_entry.grid(row=5, column=0, padx=10, pady=10)

    def show_message_loaded_data(self):
        label = tk.Label(self, text="Wczytano dane")
        self.label.destroy()
        self.label = label
        self.label.grid(row=0, column=0, padx=10, pady=10)
        self.update()

    def ask_for_path(self):
        path = filedialog.askopenfile()
        self.focus_set()
        if path is None:
            return
        self.path = path.name

        self.show_message_loaded_data()
        activate(self.master.button_next)

    def get_path(self):
        return self.path

    def is_header_checked(self):
        return self.header_checkbox_var.get()

    def is_separator_checked(self):
        return self.separator_checkbox_var.get()

    def get_separator(self):
        return self.separator_entry.get()

    def change_separator_entry_state(self):
        if not self.is_separator_checked():
            deactivate(self.separator_entry)
        else:
            normal(self.separator_entry)
