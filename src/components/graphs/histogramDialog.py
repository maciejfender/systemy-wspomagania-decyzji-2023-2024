import tkinter as tk
from tkinter import ttk


class HistogramDialog(tk.Toplevel):

    def __init__(self, master, df, data_setter) -> None:
        super().__init__(master)
        self.geometry("600x370")
        self.df = df
        self.data_setter = data_setter
        self.button = None
        self.column_name_var = None
        self.variable_var = None
        self.variable = None
        self.column_name = None
        self.entry = None
        self.entry_label = None
        self.column_label = None

        self.mount()

    def mount(self):
        columns = self.df.columns.tolist()

        self.entry_label = tk.Label(self, text="Ilośc kubełków")
        self.entry_label.grid(row=1, column=0)

        self.entry = tk.Entry(master=self)
        self.entry.grid(row=2, column=0)

        self.variable_var = tk.StringVar()
        self.variable = ttk.Combobox(self, textvariable=self.variable_var,
                                     values=['Zmienna Dyskretna', 'Zmienna Ciągła'])
        self.variable.set('zmienna dyskretna')
        self.variable.grid(row=3, column=0, sticky='nw')

        self.column_label = tk.Label(self, text="Kolumna")
        self.column_label.grid(row=4, column=0)

        self.column_name_var = tk.StringVar()
        self.column_name = ttk.Combobox(self, textvariable=self.column_name_var,
                                        values=columns)
        self.column_name.grid(row=5, column=0, sticky='nw')
        self.column_name.set(columns[0])

        self.button = tk.Button(self, text="Dalej")
        self.button.config(command=self.get_graph_params_and_destroy)
        self.button.grid(row=6, column=0, sticky="ne")

    def get_graph_params_and_destroy(self):
        self.data_setter(self.column_name_var.get(), self.variable_var.get(), int(self.entry.get()))
        self.master.center_panel.mount_histogram()
        self.destroy()
        self.update()
