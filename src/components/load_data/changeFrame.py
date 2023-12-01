import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import pandas as pd
from src.components.engine.engineUtils import suggest_type


class ChangeFrame(tk.Frame):
    def __init__(self, master, df):
        super().__init__(master)

        self.label = None
        self.df = df
        self.columns = None
        self.columns_entries = []
        self.columns_types = []
        self.types_var = {}
        self.canvas = None
        self.frame_for_content = None
        # self.grid_rowconfigure(0, weight=1)
        # self.grid_columnconfigure(1, weight=1)

        self.mount()

    def on_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def mount(self):

        self.canvas = tk.Canvas(self)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add a scrollbar
        scrollbar = tk.Scrollbar(self, command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Bind the canvas to the scrollbar
        self.canvas.bind('<Configure>', self.on_configure)

        # Create a frame inside the canvas
        self.frame_for_content = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame_for_content, anchor='nw')

        self.label = tk.Label(self.frame_for_content, text="Kolumny w pliku: wybór typów")
        self.label.grid(row=0, column=0, padx=10, pady=10, sticky='n', columnspan=2)

        self.columns = self.df.columns.tolist()
        print(self.columns)

        for column in list(self.columns):
            entry = tk.Entry(master=self.frame_for_content)
            entry.insert(0, column)
            self.columns_entries.append(entry)

            # self.types_var[column] = tk.StringVar()
            suggested_type = suggest_type(column, self.df)
            self.types_var[column] = suggested_type[1]
            column_type = ttk.Combobox(self.frame_for_content, textvariable=self.types_var[column],
                                       values=["int64", "float64", "object", "string"])
            column_type.set(suggested_type[0])
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
