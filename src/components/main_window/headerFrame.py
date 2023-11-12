import tkinter as tk

from src.components.abstract.abstractFrames import HeaderAbstractFrame


class HeaderFrame(HeaderAbstractFrame):
    def __init__(self, master: "MainWindow"):
        super().__init__(master)

        self.read_btn = tk.Button(self, text="Wczytaj dataset")
        self.read_btn.config(command=self.load_data)
        self.read_btn.grid(row=0, column=1, sticky="ne")

        self.read_btn = tk.Button(self, text="Wykres byczq liniowy")
        self.read_btn.config(command=self.graph_2d)
        self.read_btn.grid(row=0, column=2, sticky="ne")

    def load_data(self):
        self.master.footer.load_data()

    def graph_2d(self):
        self.master.center_panel.set_and_mount_graph_2d()
