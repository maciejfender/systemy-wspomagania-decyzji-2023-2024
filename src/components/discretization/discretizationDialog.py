import tkinter as tk
from tkinter import ttk


class DiscretizationDialog(tk.Toplevel):

    def __init__(self, master, df, data_setter) -> None:
        super().__init__(master)
        self.geometry("600x370")
        self.df = df
        self.data_setter = data_setter
        self.var = None
        self.bins = None
        self.labels = None
        self.button = None
        self.bins_label = None
        self.labels_label = None
        self.bins_entry = None
        self.labels_entry = None
        self.mount()

    def mount(self):
        numeric_columns = self.df.select_dtypes(include=['int64', 'float64']).columns.tolist()

        self.var = tk.StringVar()
        combobox = ttk.Combobox(self, textvariable=self.var,
                                values=numeric_columns)
        combobox.grid(row=0, column=0, sticky='nw')
        combobox.set(numeric_columns[0])

        self.bins_label = tk.Label(self, text="Przedziały kubełków oddzielone przecinkami")
        self.bins_label.grid(row=1, column=0)

        self.bins = tk.Entry(master=self)
        self.bins.grid(row=2, column=0)

        self.labels_label = tk.Label(self, text="Kubełki oddzielone przecinkami")
        self.labels_label.grid(row=3, column=0)

        self.labels = tk.Entry(master=self)
        self.labels.grid(row=4, column=0)

        self.button = tk.Button(self, text="Dalej")
        self.button.config(command=self.get_graph_params_and_destroy)
        self.button.grid(row=5, column=0, sticky="ne")

    def get_graph_params_and_destroy(self):
        self.data_setter(self.var.get(), self.bins.get(), self.labels.get())
        self.master.footer.update_view()
        self.destroy()
        self.update()
