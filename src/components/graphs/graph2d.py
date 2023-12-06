import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np


class Graph2D(tk.Frame):
    def __init__(self, master, width=0, height=0):
        super().__init__(master, width=width, height=height)
        self.data = None
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
        self.series = None
        # self.mount()

    def mount_normal(self):
        df = self.main_window.engine.get_dataset()

        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)

        x = None
        if self.data[0] == '':
            x = np.linspace(1, df.shape[0], df.shape[0], endpoint=True)
        else:
            x = df[self.data[0]].values

        y = df[self.data[1]].values
        if self.scatter_or_plot == 'punkty':
            ax.scatter(x, y, color=self.colors[0], marker=self.markers[0])
        else:
            ax.plot(x, y, color=self.colors[0])
        ax.set_xlabel(self.data[0])
        ax.set_ylabel('Series')

        # Dodaj wykres do ramki Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def mount_with_class(self):
        df = self.main_window.engine.get_dataset()
        column_data = df[self.column].unique()

        x_dict = {}
        y_dict = {}

        for class_data in column_data:
            x_dict[class_data] = []
            y_dict[class_data] = []

        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)

        x = None
        if self.data[0] == '':
            for idx, (data, class_data) in enumerate(zip(df[self.data[1]].values, df[self.column].values)):
                x_dict[class_data].append(idx)
                y_dict[class_data].append(data)
        else:
            for (x, data, class_data) in zip(df[self.data[0]].values, df[self.data[1]].values, df[self.column].values):
                x_dict[class_data].append(x)
                y_dict[class_data].append(data)

        if self.scatter_or_plot == 'punkty':
            for idx, class_data in enumerate(column_data):
                ax.scatter(x_dict[class_data], y_dict[class_data], color=self.colors[idx], marker=self.markers[idx], label=class_data)
        else:
            for idx, class_data in enumerate(column_data):
                ax.plot(x_dict[class_data], y_dict[class_data], color=self.colors[idx], label=class_data)
        ax.set_xlabel(self.data[0])
        ax.set_ylabel('Series')
        ax.legend()

        # Dodaj wykres do ramki Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def mount(self):
        if self.column == '':
            self.mount_normal()
        else:
            self.mount_with_class()

    def set_data(self, data, scatter_or_plot, color_names, markers, column):
        colors = []

        for color_name in color_names:
            colors.append(self.color_dict[color_name])

        if colors:
            self.colors = colors
        if markers:
            self.markers = markers
        self.scatter_or_plot = scatter_or_plot
        self.column = column
        self.data = data

    @property
    def main_window(self):
        return self.master.master.master.master.master
