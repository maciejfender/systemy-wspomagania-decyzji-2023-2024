import tkinter as tk
from tkinter import filedialog
from tkinter import ttk


class ChangeFrame(tk.Frame):
    def __init__(self, master, df):
        super().__init__(master)

        self.label = None
        self.df = df
        self.columns = None
        self.columns_entries = []
        self.columns_types = []
        self.types_var = {}
        self.scrollbar = None  # TODO scrollbar
        self.scrollable_frame = None  # TODO scrollbar
        self.canvas = None  # TODO scrollbar

        # self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.mount()

    def mount(self):

        self.label = tk.Label(self, text="Kolumny w pliku")
        self.label.grid(row=0, column=0, padx=10, pady=10, sticky='n', columnspan=2)

        self.columns = self.df.columns.tolist()
        print(self.columns)

        for column in self.columns:
            entry = tk.Entry(master=self)
            entry.insert(0, column)  # Wypełnij pole obecną nazwą kolumny
            self.columns_entries.append(entry)

            self.types_var[column] = tk.StringVar()
            column_type = ttk.Combobox(self, textvariable=self.types_var[column],
                                       values=["int64", "float64", "object", "string"])
            column_type.set("string")
            self.columns_types.append(column_type)

        for i, entry in enumerate(self.columns_entries):
            entry.grid(row=1 + i, column=0, sticky='w', padx=10, pady=0)
            self.columns_types[i].grid(row=1 + i, column=1, sticky='w', padx=10, pady=0)

    def get_df(self):
        return self.df

    def get_columns_entries(self):
        return self.columns_entries

    def get_column_types(self):
        return self.columns_types

    def get_types_var(self):
        return self.types_var
