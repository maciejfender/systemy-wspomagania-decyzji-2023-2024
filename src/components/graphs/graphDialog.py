import tkinter as tk
from tkinter import ttk


class GraphDialog(tk.Toplevel):

    def __init__(self, master, df, data_setter) -> None:
        super().__init__(master)
        self.geometry("600x370")
        self.df = df
        self.data_setter = data_setter
        self.checkboxes = []
        self.series_vars = {}
        self.scale: tk.Checkbutton|None = None
        self.scale_candidates_labels = []
        self.button = None
        self.type_var = None

        self.mount()

    def mount(self):
        columns = self.df.columns.tolist()
        self.type_var = tk.StringVar()
        self.scale = ttk.Combobox(self, textvariable=self.type_var,
                                  values=columns)
        self.scale.grid(row=0, column=0, sticky='nw')
        # self.scale.set(columns[0])

        numeric_columns = self.df.select_dtypes(include=['int64', 'float64'])

        for i, column in enumerate(numeric_columns):
            self.series_vars[column] = tk.BooleanVar()
            checkbox = tk.Checkbutton(self, text=column, variable=self.series_vars[column])
            checkbox.grid(row=i + 1, column=0, sticky='nw')
            self.checkboxes.append(checkbox)

        self.button = tk.Button(self, text="Dalej")
        self.button.config(command=self.get_graph_params_and_destroy)
        self.button.grid(row=len(numeric_columns) + 1, column=0, sticky="ne")

    def get_graph_params_and_destroy(self):
        selected_series = self.get_selected_series()
        self.data_setter((self.type_var.get(), selected_series))
        self.master.center_panel.mount_graph_2d()
        self.destroy()
        self.update()

    def get_selected_series(self):
        numeric_columns = self.df.select_dtypes(include=['int64', 'float64'])
        series = []

        for nc in numeric_columns:
            if self.series_vars[nc].get() is True:
                series.append(nc)

        return series
