import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np


class Graph3D(tk.Frame):
    def __init__(self, master, width=0, height=0):
        super().__init__(master, width=width, height=height)
        self.data = []
        # self.mount()

    def mount(self):
        df = self.main_window.engine.get_dataset()
        x = df[self.data[0]]
        y = df[self.data[1]]
        z = df[self.data[2]]

        fig = Figure(figsize=(5, 4), dpi=100)
        plot = fig.add_subplot(111, projection='3d')
        plot.plot(x, y, z, label='Liniowy wykres 3D', linewidth=2)

        plot.set_xlabel(self.data[0])
        plot.set_ylabel(self.data[1])
        plot.set_zlabel(self.data[2])

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def set_data(self, x, y, z):
        self.data = [x, y, z]

    @property
    def main_window(self):
        return self.master.master.master.master.master
