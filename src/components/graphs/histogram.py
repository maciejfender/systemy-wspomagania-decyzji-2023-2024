import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np


class Histogram(tk.Frame):
    def __init__(self, master, width=0, height=0):
        super().__init__(master, width=width, height=height)
        self.column_name = None
        self.discrate_or_continuous = None
        self.bins_count = None

        # self.mount()

    def mount(self):
        df = self.main_window.engine.get_dataset().copy()

        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)

        if self.discrate_or_continuous == 'Zmienna Dyskretna':
            df[self.column_name].value_counts().sort_index()
            ax.plot(df[self.column_name], kind='bar', color='lightcoral')
        else:
            ax.hist(df[self.column_name], bins=self.bins_count, color='lightcoral', edgecolor='black')

        ax.set_xlabel(self.column_name)
        ax.set_ylabel('Liczbność')

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def set_data(self, column_name, discrate_or_continuous, bins_count):
        self.column_name = column_name
        self.discrate_or_continuous = discrate_or_continuous
        self.bins_count = bins_count

    @property
    def main_window(self):
        return self.master.master.master.master.master
