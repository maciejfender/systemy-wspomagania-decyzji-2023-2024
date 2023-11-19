import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np


class Graph2D(tk.Frame):
    def __init__(self, master, width=0, height=0):
        super().__init__(master, width=width, height=height)
        self.data = None
        # self.mount()

    def mount(self):
        df = self.main_window.engine.get_dataset()

        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        # x = [1, 2, 3, 4, 5]
        # y = [2, 3, 5, 7, 11]
        x = None
        if self.data[0] == '':
            x = np.linspace(1, df.shape[0], df.shape[0], endpoint=True)
        else:
            x = df[self.data[0]].values

        for column in self.data[1]:
            y = df[column].values
            ax.plot(x, y)

        # Dodaj wykres do ramki Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def set_data(self, data):
        self.data = data

    @property
    def main_window(self):
        return self.master.master.master.master.master
