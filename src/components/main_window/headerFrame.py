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


    def load_data(self):
        self.master.footer.load_data()

    def graph_2d(self):
        self.master.center_panel.set_and_mount_graph_2d()

    def graph_3d(self):
        self.master.center_panel.set_and_mount_graph_3d()

    def discretization(self):
        self.master.engine.discretization_dialog()
