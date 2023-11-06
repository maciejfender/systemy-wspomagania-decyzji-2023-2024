import tkinter as tk

from components.abstract.abstractFrames import CustomAbstractFrame


class CenterPanel(CustomAbstractFrame):

    def __init__(self, master) -> None:
        super().__init__(master)
        paned_window = tk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True)

        self.center = tk.Frame(paned_window, background="red")
        self.right = tk.Frame(paned_window, background="blue")

        paned_window.add(self.center)
        paned_window.add(self.right)
