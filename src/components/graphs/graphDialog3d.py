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

        self.mount()

    def mount(self):
        self.scatter_or_plot_var = tk.StringVar()
        self.scatter_or_plot = ttk.Combobox(self, textvariable=self.scatter_or_plot_var,
                                            values=['punkty', 'linia'])
        self.scatter_or_plot.set('punkty')
        self.scatter_or_plot.grid(row=0, column=0, sticky='nw')

        numeric_columns = self.df.select_dtypes(include=['int64', 'float64']).columns.tolist()

        for i in range(3):
            self.vars[i] = tk.StringVar()
            combobox = ttk.Combobox(self, textvariable=self.vars[i],
                                    values=numeric_columns)
            combobox.grid(row=i + 1, column=0, sticky='nw')
            combobox.set(numeric_columns[i])
            self.comboboxes.append(combobox)

        color_var = tk.StringVar()
        color_combobox = ttk.Combobox(self, textvariable=color_var,
                                      values=self.color_names)
        color_combobox.grid(row=4, column=0, sticky='nw')

        self.color_names_selected.append(color_var)

        marker_var = tk.StringVar()
        marker_combobox = ttk.Combobox(self, textvariable=marker_var,
                                       values=self.markers)
        marker_combobox.grid(row=5, column=0, sticky='nw')

        self.markers_selected.append(marker_var)

        self.button = tk.Button(self, text="Dalej")
        self.button.config(command=self.get_graph_params_and_destroy)
        self.button.grid(row=len(numeric_columns) + 2, column=0, sticky="ne")

    def get_graph_params_and_destroy(self):
        self.data_setter(self.vars[0].get(), self.vars[1].get(), self.vars[2].get(), self.scatter_or_plot_var.get(),
                         self.color_names_selected[0].get(), self.markers_selected[0].get())
        self.master.center_panel.mount_graph_3d()
        self.destroy()
        self.update()
