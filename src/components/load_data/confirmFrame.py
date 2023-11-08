import tkinter as tk
from tkinter import filedialog


class ConfirmFrame(tk.Frame):
    def __init__(self, master, df):
        super().__init__(master)

        self.label = None
        self.df = df
        self.columns = None
        self.columns_labels = []

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.mount()

    def mount(self):
        self.label = tk.Label(self, text="Kolumny w pliku")
        self.label.grid(row=0, column=0, padx=10, pady=10)

        self.columns = self.df.columns.tolist()
        print(self.columns)

        for column in self.columns:
            label = tk.Label(master=self, text=column)
            self.columns_labels.append(label)

        for i, entry in enumerate(self.columns_labels):
            entry.grid(row=1 + i, column=0, sticky='nw')
