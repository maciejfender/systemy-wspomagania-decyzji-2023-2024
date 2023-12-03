import tkinter as tk
from tkinter import filedialog

from src.components.engine.engineUtils import normal, deactivate, activate

SEPARATORS = [',', ';', '\t']

DEFAULT_SEPARATOR = ','


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

        self.header_checkbox_var = tk.BooleanVar(value=True)
        self.header_checkbox = tk.Checkbutton(self, text="Czy posiada nagłówek?", variable=self.header_checkbox_var)
        self.header_checkbox.grid(row=2, column=0, padx=10, pady=10)

        self.separator_checkbox_var = tk.BooleanVar(value=True)
        self.separator_checkbox = tk.Checkbutton(self, text="Czy separator?", variable=self.separator_checkbox_var,
                                                 command=self.change_separator_entry_state)
        self.separator_checkbox.grid(row=3, column=0, padx=10, pady=10)

        self.separator_label = tk.Label(self, text="Separator")
        self.separator_label.grid(row=4, column=0, padx=10, pady=10)

        self.separator_entry = tk.Entry(master=self)
        # deactivate(self.separator_entry)
        self.activate_separator_entry()

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

        separator = self.detect_separator()
        if separator is not None:
            self.separator_entry.delete(0, 'end')
            self.separator_entry.insert(0, separator.encode())

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
            self.activate_separator_entry()

    def activate_separator_entry(self):

        normal(self.separator_entry)
        if not self.separator_entry.get():
            self.separator_entry.insert(0, DEFAULT_SEPARATOR)

    def detect_separator(self):
        try:
            with open(self.path, "r") as file:
                content = file.read()

            content = content.split('\n')

            def lambda_filter(s):
                row = s.strip()

                if len(row) == 0:
                    return False

                if row[0] == '#':
                    return False
                return True

            content = list(filter(lambda_filter, content))

            for sep in SEPARATORS:
                all_rows = 0
                correctly_split = 0
                expected_split = None
                for row in content:

                    all_rows += 1
                    count = row.count(sep)

                    if count > 0:
                        if expected_split is None:
                            expected_split = count
                        correctly_split += 1
                if all_rows == correctly_split:
                    return sep
        except Exception as e:
            raise e
