import tkinter as tk
from tkinter import ttk
from typing import Union

import pandas as pd
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from components.partitioning.engine import *

COLOR_BLACK = "#000000"


class PartitionPlot2DFrame(tk.Frame):
    @property
    def dataset(self):
        return self.master.dataset

    def __init__(self, master, column_x: str, column_y: str, column_c: str) -> None:
        super().__init__(master)

        self.column_x = column_x
        self.column_y = column_y
        self.column_c = column_c

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
        c = list(self.dataset[self.column_c])
        unique = list(set(c))

        zipped = list(zip(x, y, c))

        zipped_collections_of_series = [
            list(zip(*filter(lambda z: z[2] == unique[ch], zipped)))
            for ch in range(0, len(unique))
        ]
        for xs, ys, _ in zipped_collections_of_series:
            self.subplot.scatter(xs, ys)

        self.x_lims = (min(x), max(x))
        self.y_lims = (min(y), max(y))

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

        # self._dataset = engineUtils.read_to_df("INCOME_2.TXT", header_checked=True, separator_checked=True,
        #                                        separator="\t")
        self._dataset = pd.DataFrame({"a": [0, 1, 2, 3, 4], "b": [0, 1, 0, 1, 0], "c": ["F", "T", "T", "T", "S"]})
        # self._dataset = pd.DataFrame({"a": [0, 0, 1, 2, 2], "b": [0, 1, 1, 0, 1], "c": ["F", "T", "T", "T", "S"]})

        self.removed_count = 0
        self.lines_count = 0

        self.var_1()
        self.var_2()
        self.var_c()
        self.p = None
        self.btn_plot = tk.Button(self, text="plot", command=self.show_plot)
        self.btn_plot.pack()

        self.var_statistics = tk.StringVar(self, value="")
        self.label_statistics = tk.Label(self, textvariable=self.var_statistics)
        self.label_statistics.pack()

        self.partition_engine: Union[PartitionEngine, None] = None

        tk.Button(self, text="New Line", command=self.draw_new_line).pack()
        tk.Button(self, text="Generate All", command=self.draw_all_new_lines).pack()

    def show_plot(self):
        if self.p is not None:
            self.p.pack_forget()
        self.p = PartitionPlot2DFrame(self, self.var_column_1.get(), self.var_column_2.get(), self.var_column_c.get())
        self.p.pack()

    def draw_new_line(self):
        if self.partition_engine is None:
            self.partition_engine = PartitionEngine(self, [self.var_column_1.get(), self.var_column_2.get()],
                                                    self.var_column_c.get())

        new_line = self.partition_engine.new_line()

        if new_line is None:
            return False

        if new_line[TYPE] == VERTICAL:
            a = (None, new_line[VALUE])
        else:
            a = (new_line[VALUE], None)

        if self.p is not None:
            self.p.new_line(*a)

            if new_line[DELETED] is not None:
                deleted_c = len(new_line[DELETED])
                self.removed_count += deleted_c

            self.lines_count += 1

            self.update_statistics_label()
            return True
        return False

    def draw_all_new_lines(self):
        while self.draw_new_line():
            pass

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

    def update_statistics_label(self):
        self.var_statistics.set(
            f"Statystyki:\n\n Ilość krawędzi: {self.lines_count}\nIlość usuniętych wierzchołków: {self.removed_count}")
