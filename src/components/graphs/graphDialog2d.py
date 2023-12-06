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
        self.selected_column = None
        self.class_cbx = None
        self.class_var = None

        self.mount()

    def mount(self):
        columns = self.df.columns.tolist()

        type_label = tk.Label(self, text="Rodzaj wykresu")
        type_label.grid(row=0, column=0, sticky='nw', columnspan=3)
        self.scatter_or_plot_var = tk.StringVar()
        self.scatter_or_plot = ttk.Combobox(self, textvariable=self.scatter_or_plot_var,
                                            values=['punkty', 'linia'])
        self.scatter_or_plot.set('punkty')
        self.scatter_or_plot.grid(row=1, column=0, sticky='nw')

        scale_label = tk.Label(self, text="Wybierz zmienną niezależną (X)")
        scale_label.grid(row=2, column=0, sticky='nw', columnspan=3)
        self.type_var = tk.StringVar()
        self.scale = ttk.Combobox(self, textvariable=self.type_var,
                                  values=columns)
        self.scale.grid(row=3, column=0, sticky='nw')
        # self.scale.set(columns[0])

        series_label = tk.Label(self, text="Wybierz serię danych (Y)")
        series_label.grid(row=4, column=0, sticky='nw', columnspan=3)
        self.series_var = tk.StringVar()
        self.series = ttk.Combobox(self, textvariable=self.series_var,
                                   values=columns)
        self.series.grid(row=5, column=0, sticky='nw')

        class_label = tk.Label(self, text="Wybierz klasę")
        class_label.grid(row=6, column=0, sticky='nw', columnspan=3)
        self.class_var = tk.StringVar()
        self.class_cbx = ttk.Combobox(self, textvariable=self.class_var,
                                      values=columns)
        self.class_cbx.grid(row=7, column=0, sticky='nw')

        self.button = tk.Button(self, text="Dalej")
        self.button.config(command=self.manage_state)
        self.button.grid(row=8, column=0, sticky="ne")

    def mount_2(self):
        self.button.destroy()
        self.button.update()
        column_data = self.df[self.class_var.get()].unique()
        column_data_len = len(column_data)

        for i, data in enumerate(column_data):
            series_label = tk.Label(self, text=data)
            series_label.grid(row=i + 8, column=0, sticky='nw', columnspan=3)

            color_var = tk.StringVar()
            color_combobox = ttk.Combobox(self, textvariable=color_var,
                                          values=self.color_names)
            color_combobox.grid(row=i + 8, column=1, sticky='nw')
            color_combobox.set(self.color_names[i % column_data_len])

            self.color_names_selected.append(color_var)

            marker_var = tk.StringVar()
            marker_combobox = ttk.Combobox(self, textvariable=marker_var,
                                           values=self.markers)
            marker_combobox.grid(row=i + 8, column=2, sticky='nw')
            marker_combobox.set(self.markers[i % column_data_len])

            self.markers_selected.append(marker_var)

        self.button = tk.Button(self, text="Dalej")
        self.button.config(command=self.manage_state)
        self.button.grid(row=len(column_data) + 9, column=0, sticky="ne")

    def manage_state(self):
        if not self.column_data_loaded and self.class_var.get() != '':
            self.mount_2()
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

        # selected_series = self.get_selected_series()
        # self.data_setter((self.type_var.get(), selected_series), self.scatter_or_plot_var.get(), colors, markers)

        self.data_setter((self.type_var.get(), self.series_var.get()), self.scatter_or_plot_var.get(), colors, markers, self.class_var.get())

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
