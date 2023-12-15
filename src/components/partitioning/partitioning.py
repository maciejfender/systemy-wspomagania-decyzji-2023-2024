import tkinter as tk
from tkinter import ttk

import numpy as np
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from components.engine import engineUtils

COLOR_BLACK = "#000000"


class PartitionPlot2DFrame(tk.Frame):
    @property
    def dataset(self):
        return self.master.dataset

    def __init__(self, master, column_x: str, column_y: str) -> None:
        super().__init__(master)

        self.column_x = column_x
        self.column_y = column_y

        fig = Figure(figsize=(5, 4), dpi=100)
        self.fig = fig
        self.subplot = fig.add_subplot(111)
        self.counter = 1

        self.plot_main_plot()

        self.canvas = FigureCanvasTkAgg(fig, master=self)  # A tk.DrawingArea.
        self.update_plot()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(self.canvas, self)
        toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def plot_main_plot(self):
        x = list(map(float, self.dataset[self.column_x]))
        y = list(map(float, self.dataset[self.column_y]))

        self.subplot.scatter(x, y)
        self.x_lims = (np.min(x), np.max(x),)
        self.y_lims = (np.min(y), np.max(y),)

    def update_plot(self):
        self.canvas.draw()

    def new_line(self, x=None, y=None):
        assert (x is not None and y is None) or (x is None and y is not None)

        self.counter += 1
        if x is None:  # horizontal line
            self.subplot.plot(self.x_lims, [y] * 2, color=COLOR_BLACK)
        else:
            self.subplot.plot([x] * 2, self.y_lims, color=COLOR_BLACK)
        self.update_plot()


class Partition2DTopLevel(tk.Toplevel):
    @property
    def dataset(self):
        # todo proper dataset
        return self._dataset
    def __init__(self, master) -> None:
        super().__init__(master)

        self._dataset = engineUtils.read_to_df("INCOME.TXT", header_checked=True, separator_checked=True, separator="\t")

        self.var_1()
        self.var_2()
        self.var_c()
        self.p = None
        self.btn_plot = tk.Button(self, text="plot", command=self.show_plot)
        self.btn_plot.pack()

        self.var_line_y = tk.StringVar(self, value="1 2")
        self.entry = tk.Entry(self, textvariable=self.var_line_y)
        self.entry.pack()

        tk.Button(self, text="press", command=self.draw_vertical_line).pack()

    def show_plot(self):
        if self.p is not None:
            self.p.pack_forget()
        self.p = PartitionPlot2DFrame(self, self.var_column_1.get(), self.var_column_2.get())
        self.p.pack()

    def draw_vertical_line(self):
        x, y = list(map(float, self.var_line_y.get().split(' ')))
        if x == 0:
            self.p.new_line(None, y)
        else:
            self.p.new_line(y, None)

    def var_c(self):
        tk.Label(self, text="Klasa").pack()
        last_col = self.dataset.columns[-1]
        self.var_column_c = tk.StringVar(self, value=last_col)
        self.combobox_class_column = ttk.Combobox(self, values=list(self.dataset.columns),
                                                  textvariable=self.var_column_c)
        self.combobox_class_column.pack()

    def var_2(self):
        second = self.dataset.columns[1]
        tk.Label(self, text="Zmienna B").pack()
        self.var_column_2 = tk.StringVar(self, value=second)
        self.combobox_class_column_2 = ttk.Combobox(self, values=list(self.dataset.columns),
                                                    textvariable=self.var_column_2)
        self.combobox_class_column_2.pack()

    def var_1(self):
        tk.Label(self, text="Zmienna A").pack()
        first = self.dataset.columns[0]
        self.var_column_1 = tk.StringVar(self, value=first)
        self.combobox_class_column_1 = ttk.Combobox(self, values=list(self.dataset.columns),
                                                    textvariable=self.var_column_1)
        self.combobox_class_column_1.pack()
