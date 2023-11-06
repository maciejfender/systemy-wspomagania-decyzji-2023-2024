import tkinter as tk

from components.abstract.abstractFrames import CustomAbstractFrame
from src.components.main_window.centerPanel import CenterPanel
from src.components.main_window.footerFrame import FooterFrame


class CenterAndLowerCompoundPanel(CustomAbstractFrame):

    def __init__(self, master) -> None:
        super().__init__(master)

        paned_window = tk.PanedWindow(self, orient=tk.VERTICAL)
        paned_window.pack(fill=tk.BOTH, expand=True)

        self.center_panel = CenterPanel(paned_window)
        self.footer = FooterFrame(self)

        paned_window.add(self.center_panel)
        paned_window.add(self.footer)


