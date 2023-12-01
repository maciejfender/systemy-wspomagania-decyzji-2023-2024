import tkinter as tk
from tkinter import ttk


class RangePercentageDialog(tk.Toplevel):

    def __init__(self, master, df, min_max_percentage) -> None:
        super().__init__(master)
        self.geometry("600x370")
        self.df = df
        self.min_max_percentage = min_max_percentage
        self.var = None
        self.button = None
        self.lower_bound_label = None
        self.upper_bound_label = None
        self.lower_bound_entry = None
        self.upper_bound_entry = None
        self.mount()

    def mount(self):
        numeric_columns = self.df.select_dtypes(include=['int64', 'float64']).columns.tolist()

        self.var = tk.StringVar()
        combobox = ttk.Combobox(self, textvariable=self.var,
                                values=numeric_columns)
        combobox.grid(row=0, column=0, sticky='nw')
        combobox.set(numeric_columns[0])

        self.lower_bound_label = tk.Label(self, text="Mniejsze od X %")
        self.lower_bound_label.grid(row=1, column=0)

        self.lower_bound_entry = tk.Entry(master=self)
        self.lower_bound_entry.grid(row=2, column=0)

        self.upper_bound_label = tk.Label(self, text="Większe od X %")
        self.upper_bound_label.grid(row=3, column=0)

        self.upper_bound_entry = tk.Entry(master=self)
        self.upper_bound_entry.grid(row=4, column=0)

        self.button = tk.Button(self, text="Dalej")
        self.button.config(command=self.get_graph_params_and_destroy)
        self.button.grid(row=5, column=0, sticky="ne")

    def get_graph_params_and_destroy(self):
        self.min_max_percentage(self.var.get(), self.lower_bound_entry.get(), self.upper_bound_entry.get())
        self.master.footer.update_view()
        self.destroy()
        self.update()
