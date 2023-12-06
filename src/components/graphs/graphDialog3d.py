import tkinter as tk
from tkinter import ttk


class GraphDialog3d(tk.Toplevel):

    def __init__(self, master, df, data_setter) -> None:
        super().__init__(master)
        self.geometry("600x370")
        self.df = df
        self.data_setter = data_setter
        self.comboboxes = []
        self.vars = {}
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
        self.scatter_or_plot_var = tk.StringVar()
        self.scatter_or_plot = ttk.Combobox(self, textvariable=self.scatter_or_plot_var,
                                            values=['punkty', 'linia'])
        self.scatter_or_plot.set('punkty')
        self.scatter_or_plot.grid(row=0, column=0, sticky='nw')

        numeric_columns = self.df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        columns = self.df.columns.tolist()

        for i, name in enumerate(['X', 'Y', 'Z']):
            series_label = tk.Label(self, text=name)
            series_label.grid(row=i + 1, column=0, sticky='nw', columnspan=2)

            self.vars[i] = tk.StringVar()
            combobox = ttk.Combobox(self, textvariable=self.vars[i],
                                    values=numeric_columns)
            combobox.grid(row=i + 1, column=1, sticky='nw')
            combobox.set(numeric_columns[i])
            self.comboboxes.append(combobox)

        class_label = tk.Label(self, text="Wybierz klasę")
        class_label.grid(row=5, column=0, sticky='nw', columnspan=3)
        self.class_var = tk.StringVar()
        self.class_cbx = ttk.Combobox(self, textvariable=self.class_var,
                                      values=columns)
        self.class_cbx.grid(row=6, column=0, sticky='nw')

        self.button = tk.Button(self, text="Dalej")
        self.button.config(command=self.manage_state)
        self.button.grid(row=7, column=0, sticky="ne")

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

        self.data_setter(self.vars[0].get(), self.vars[1].get(), self.vars[2].get(), self.scatter_or_plot_var.get(),
                         colors, markers, self.class_var.get())
        self.master.center_panel.mount_graph_3d()
        self.destroy()
        self.update()
