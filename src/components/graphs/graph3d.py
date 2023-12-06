import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np


class Graph3D(tk.Frame):
    def __init__(self, master, width=0, height=0):
        super().__init__(master, width=width, height=height)
        self.data = []
        self.scatter_or_plot = None
        self.colors = ['#ff007f', '#001f3f', '#800080', '#01ff70', '#ff6300', '#00A86B']
        self.color_dict = {
            'Ciemnoniebieski': '#001f3f',
            'Jasnopoziomkowy': '#ff007f',
            'Zielony limonkowy': '#01ff70',
            'Ciemnofioletowy': '#800080',
            'Pomarańczowy': '#ff6300',
            'Jadeitowy': '#00A86B'
        }
        self.markers = ['o', 'x', '+', '1', 'D', '^']
        self.column = None
        # self.mount()

    def mount_normal(self):
        df = self.main_window.engine.get_dataset()
        x = df[self.data[0]]
        y = df[self.data[1]]
        z = df[self.data[2]]

        fig = Figure(figsize=(5, 4), dpi=100)
        plot = fig.add_subplot(111, projection='3d')

        if self.scatter_or_plot == 'punkty':
            plot.scatter(x, y, z, label='Liniowy wykres 3D', linewidth=2, color=self.color_dict[self.color], marker=self.marker)
        else:
            plot.plot(x, y, z, label='Liniowy wykres 3D', linewidth=2, color=self.color_dict[self.color])

        plot.set_xlabel(self.data[0])
        plot.set_ylabel(self.data[1])
        plot.set_zlabel(self.data[2])

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def mount_with_class(self):
        df = self.main_window.engine.get_dataset()
        x = df[self.data[0]]
        y = df[self.data[1]]
        z = df[self.data[2]]

        column_data = df[self.column].unique()

        x_dict = {}
        y_dict = {}
        z_dict = {}

        for class_data in column_data:
            x_dict[class_data] = []
            y_dict[class_data] = []
            z_dict[class_data] = []

        fig = Figure(figsize=(5, 4), dpi=100)
        plot = fig.add_subplot(111, projection='3d')

        for (x, y, z, class_data) in zip(df[self.data[0]].values, df[self.data[1]].values, df[self.data[2]].values, df[self.column].values):
            x_dict[class_data].append(x)
            y_dict[class_data].append(y)
            z_dict[class_data].append(z)

        if self.scatter_or_plot == 'punkty':
            for idx, class_data in enumerate(column_data):
                plot.scatter(x_dict[class_data], y_dict[class_data], z_dict[class_data], linewidth=2, color=self.colors[idx], marker=self.markers[idx], label=class_data)
        else:
            for idx, class_data in enumerate(column_data):
                plot.plot(x_dict[class_data], y_dict[class_data], z_dict[class_data], linewidth=2, color=self.colors[idx], label=class_data)

        plot.set_xlabel(self.data[0])
        plot.set_ylabel(self.data[1])
        plot.set_zlabel(self.data[2])
        plot.legend()

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def set_data(self, x, y, z, scatter_or_plot, color_names, markers, column):
        colors = []

        for color_name in color_names:
            colors.append(self.color_dict[color_name])

        if colors:
            self.colors = colors
        if markers:
            self.markers = markers

        self.column = column
        self.scatter_or_plot = scatter_or_plot
        self.data = [x, y, z]

    def mount(self):
        if self.column == '':
            self.mount_normal()
        else:
            self.mount_with_class()

    @property
    def main_window(self):
        return self.master.master.master.master.master
