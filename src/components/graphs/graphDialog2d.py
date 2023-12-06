import tkinter as tk
from tkinter import ttk


class GraphDialog2d(tk.Toplevel):

    def __init__(self, master, df, data_setter) -> None:
        super().__init__(master)
        self.geometry("600x370")
        self.df = df
        self.data_setter = data_setter
        self.checkboxes = []
        self.series_vars = {}
        self.scale: tk.Checkbutton | None = None
        self.scale_candidates_labels = []
        self.button = None
        self.type_var = None
        self.scatter_or_plot = None
        self.scatter_or_plot_var = None
        self.color_names = ['Jasnopoziomkowy', 'Ciemnoniebieski', 'Ciemnofioletowy', 'Zielony limonkowy',
                            'Pomarańczowy', 'Jadeitowy']
        self.color_names_selected = []
        self.markers = ['o', 'x', '+', '1', 'D', '^']
        self.markers_selected = []
        self.series_var = None
        self.series = None
        self.column_data_loaded = False

        self.mount()

    def mount(self):
        columns = self.df.columns.tolist()

        self.scatter_or_plot_var = tk.StringVar()
        self.scatter_or_plot = ttk.Combobox(self, textvariable=self.scatter_or_plot_var,
                                            values=['punkty', 'linia'])
        self.scatter_or_plot.set('punkty')
        self.scatter_or_plot.grid(row=0, column=0, sticky='nw')

        self.type_var = tk.StringVar()
        self.scale = ttk.Combobox(self, textvariable=self.type_var,
                                  values=columns)
        self.scale.grid(row=1, column=0, sticky='nw')
        # self.scale.set(columns[0])

        self.series_var = tk.StringVar()
        self.series = ttk.Combobox(self, textvariable=self.series_var,
                                   values=columns)
        self.series.grid(row=2, column=0, sticky='nw')

        numeric_columns = self.df.select_dtypes(include=['int64', 'float64'])



        self.button = tk.Button(self, text="Dalej")
        self.button.config(command=self.manage_state)
        self.button.grid(row=len(numeric_columns) + 2, column=0, sticky="ne")


    def manage_state(self):
        if not self.column_data_loaded:
            column_data = self.df[self.series_var.get()].unique()

            for i, column in enumerate(column_data):
                self.series_vars[column] = tk.BooleanVar()
                checkbox = tk.Checkbutton(self, text=column, variable=self.series_vars[column])
                checkbox.grid(row=i + 2, column=0, sticky='nw')
                self.checkboxes.append(checkbox)

                color_var = tk.StringVar()
                color_combobox = ttk.Combobox(self, textvariable=color_var,
                                              values=self.color_names)
                color_combobox.grid(row=i + 2, column=1, sticky='nw')

                self.color_names_selected.append(color_var)

                marker_var = tk.StringVar()
                marker_combobox = ttk.Combobox(self, textvariable=marker_var,
                                               values=self.markers)
                marker_combobox.grid(row=i + 2, column=2, sticky='nw')

                self.markers_selected.append(marker_var)

            self.column_data_loaded = True
        else:
            self.get_graph_params_and_destroy()

    def get_graph_params_and_destroy(self):
        colors = []

        for color in self.color_names_selected:
            if color.get() != '':
                colors.append(color.get())

        markers = []

        for marker in self.markers_selected:
            if marker.get() != '':
                markers.append(marker.get())

        selected_series = self.get_selected_series()
        self.data_setter((self.type_var.get(), selected_series), self.scatter_or_plot_var.get(), colors, markers)
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
