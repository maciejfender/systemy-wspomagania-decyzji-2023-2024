import tkinter as tk

from src.components.abstract.abstractFrames import HeaderAbstractFrame


class HeaderFrame(HeaderAbstractFrame):
    def __init__(self, master: "MainWindow"):
        super().__init__(master)

        self.read_btn = tk.Button(self, text="Wczytaj dataset")
        self.read_btn.config(command=self.load_data)
        self.read_btn.grid(row=0, column=1, sticky="ne")

        self.read_btn = tk.Button(self, text="Wykres 2D")
        self.read_btn.config(command=self.graph_2d)
        self.read_btn.grid(row=0, column=2, sticky="ne")

        self.read_btn = tk.Button(self, text="Wykres 3D")
        self.read_btn.config(command=self.graph_3d)
        self.read_btn.grid(row=0, column=3, sticky="ne")

        self.read_btn = tk.Button(self, text="Dyskryminacja zmiennej")
        self.read_btn.config(command=self.discretization)
        self.read_btn.grid(row=0, column=4, sticky="ne")

        self.read_btn = tk.Button(self, text="Histogram")
        self.read_btn.config(command=self.orignal_data)
        self.read_btn.grid(row=0, column=5, sticky="ne")

        self.read_btn = tk.Button(self, text="Normalizacja")
        self.read_btn.config(command=self.normalization)
        self.read_btn.grid(row=0, column=6, sticky="ne")

        self.read_btn = tk.Button(self, text="Zmień rozkład danych - zakres wartości")
        self.read_btn.config(command=self.min_max)
        self.read_btn.grid(row=0, column=7, sticky="ne")

        self.read_btn = tk.Button(self, text="Zmień rozkład danych - zakres procentowy")
        self.read_btn.config(command=self.min_max_percentage)
        self.read_btn.grid(row=0, column=8, sticky="ne")

        self.read_btn = tk.Button(self, text="Zmień dane na numeryczne")
        self.read_btn.config(command=self.numeric)
        self.read_btn.grid(row=0, column=9, sticky="ne")

        self.read_btn = tk.Button(self, text="Przywróć dane")
        self.read_btn.config(command=self.orignal_data)
        self.read_btn.grid(row=0, column=10, sticky="ne")

    def load_data(self):
        self.master.footer.load_data()

    def graph_2d(self):
        self.master.center_panel.set_and_mount_graph_2d()

    def graph_3d(self):
        self.master.center_panel.set_and_mount_graph_3d()

    def discretization(self):
        self.master.engine.discretization_dialog()

    def normalization(self):
        self.master.engine.normalization_dialog()

    def min_max(self):
        self.master.engine.min_max_dialog()

    def min_max_percentage(self):
        self.master.engine.min_max_percentage_dialog()

    def numeric(self):
        self.master.engine.numeric_dialog()

    def orignal_data(self):
        self.master.engine.df_to_original()
        self.master.footer.update_view()
