import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class Graph2D(tk.Frame):
    def __init__(self, master, width=0, height=0):
        super().__init__(master, width=width, height=height)
        self.data = None
        self.mount()

    def mount(self):
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        x = [1, 2, 3, 4, 5]
        y = [2, 3, 5, 7, 11]
        ax.plot(x, y)

        # Dodaj wykres do ramki Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def set_data(self, data):
        self.data = data
