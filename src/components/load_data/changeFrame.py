import tkinter as tk
from tkinter import filedialog


class ChangeFrame(tk.Frame):
    def __init__(self, master, df):
        super().__init__(master)

        self.label = None
        self.df = df
        self.columns = None
        self.columns_entries = []

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.mount()

    def mount(self):
        self.label = tk.Label(self, text="Kolumny w pliku")
        self.label.grid(row=0, column=0, padx=10, pady=10)

        self.columns = self.df.columns.tolist()
        print(self.columns)

        for column in self.columns:
            entry = tk.Entry(master=self)
            entry.insert(0, column)  # Wypełnij pole obecną nazwą kolumny
            self.columns_entries.append(entry)

        for i, entry in enumerate(self.columns_entries):
            entry.grid(row=1+i, column=0, sticky='nw')

    def get_df(self):
        return self.df

    def get_columns_entries(self):
        return self.columns_entries
