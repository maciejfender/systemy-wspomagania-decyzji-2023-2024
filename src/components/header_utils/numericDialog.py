import tkinter as tk
from tkinter import ttk


class NumericDialog(tk.Toplevel):

    def __init__(self, master, df, numeric) -> None:
        super().__init__(master)
        self.geometry("300x100")
        self.df = df
        self.numeric = numeric
        self.var = None
        self.button = None
        self.mount()

    def mount(self):
        columns = self.df.columns.tolist()

        self.var = tk.StringVar()
        combobox = ttk.Combobox(self, textvariable=self.var,
                                values=columns)
        combobox.grid(row=0, column=0, sticky='nw')
        combobox.set(columns[0])

        self.button = tk.Button(self, text="Dalej")
        self.button.config(command=self.get_graph_params_and_destroy)
        self.button.grid(row=1, column=0, sticky="ne")

    def get_graph_params_and_destroy(self):
        self.numeric(self.var.get())
        self.master.footer.update_view()
        self.destroy()
        self.update()
