import tkinter as tk
from tkinter import filedialog


class ConfirmFrame(tk.Frame):
    def __init__(self, master, df):
        super().__init__(master)

        self.label = None
        self.df = df
        self.columns = None
        self.columns_labels = []
        self.canvas = None
        self.frame_for_content = None

        # self.grid_rowconfigure(1, weight=1)
        # self.grid_columnconfigure(0, weight=1)

        self.mount()

    def on_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def mount(self):
        self.canvas = tk.Canvas(self)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(self, command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind('<Configure>', self.on_configure)

        self.frame_for_content = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame_for_content, anchor='nw')

        self.label = tk.Label(self.frame_for_content, text="Kolumny w pliku")
        self.label.grid(row=0, column=0, padx=10, pady=10)

        self.columns = self.df.columns.tolist()
        print(self.columns)

        for column in self.columns:
            label = tk.Label(master=self.frame_for_content, text=column)
            self.columns_labels.append(label)

        for i, entry in enumerate(self.columns_labels):
            entry.grid(row=1 + i, column=0, sticky='nw')
