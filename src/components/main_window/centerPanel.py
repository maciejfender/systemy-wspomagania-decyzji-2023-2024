import tkinter as tk

from components.abstract.abstractFrames import CustomAbstractFrame
from components.graphs.graph2d import Graph2D
from components.graphs.graph3d import Graph3D
from components.graphs.graphSettings import GraphSettings
from components.graphs.histogram import Histogram


class CenterPanel(CustomAbstractFrame):

    def __init__(self, master) -> None:
        super().__init__(master)
        self.paned_window = tk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        self.left = GraphSettings(self.paned_window, background="gray", width=0)
        self.center = tk.Frame(self.paned_window, background="#3d3d3d", height=200)
        self.temp = None

        self.paned_window.add(self.left)
        self.paned_window.add(self.center)

    def set_and_mount_graph_2d(self):
        self.temp = Graph2D(self.paned_window, height=200)
        self.main_window.engine.graph_2d_dialog()

    def set_and_mount_graph_3d(self):
        self.temp = Graph3D(self.paned_window, height=200)
        self.main_window.engine.graph_3d_dialog()

    def set_and_mount_histogram(self):
        self.temp = Histogram(self.paned_window, height=300)
        self.main_window.engine.histogram_dialog()

    def mount_graph_2d(self):
        self.center.destroy()
        self.center = self.temp
        self.center.mount()
        self.paned_window.add(self.center)
        self.paned_window.update()

    def mount_graph_3d(self):
        self.center.destroy()
        self.center = self.temp
        self.center.mount()
        self.paned_window.add(self.center)
        self.paned_window.update()

    def mount_histogram(self):
        self.center.destroy()
        self.center = self.temp
        self.center.mount()
        self.paned_window.add(self.center)
        self.paned_window.update()

    @property
    def main_window(self):
        return self.master.master.master
