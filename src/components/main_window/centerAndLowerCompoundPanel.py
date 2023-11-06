import tkinter as tk

from src.components.main_window.centerPanel import CenterPanel
from src.components.main_window.customFrame import CustomFrame
from src.components.main_window.footerFrame import FooterFrame


class CenterAndLowerCompoundPanel(CustomFrame):

    def __init__(self, master) -> None:
        super().__init__(master)

        paned_window = tk.PanedWindow(self, orient=tk.VERTICAL)
        paned_window.pack(fill=tk.BOTH, expand=True)

        self.frame1 = CenterPanel(paned_window)
        #self.frame2 = tk.Frame(paned_window, height=100, background="black")
        self.frame2 = FooterFrame(self)

        paned_window.add(self.frame1)
        paned_window.add(self.frame2)


