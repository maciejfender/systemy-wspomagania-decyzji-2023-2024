import tkinter as tk

from src.components.engine.engine import Engine
from src.components.main_window.centerAndLowerCompoundPanel import CenterAndLowerCompoundPanel
from src.components.main_window.headerFrame import HeaderFrame


class MainWindow(tk.Tk):

    def __init__(self, ) -> None:
        super().__init__()
        self.right_frame = None
        self.center_and_lower_compound_panel = None
        self.header_frame = None
        self.title("SWD 2023-24")
        self.engine = None

    def mount(self):
        self.header_frame = HeaderFrame(self)
        self.center_and_lower_compound_panel = CenterAndLowerCompoundPanel(self)

        self.header_frame.pack(fill=tk.X, expand=False)
        self.center_and_lower_compound_panel.pack(fill=tk.BOTH, expand=True)

        self.engine = Engine(self)

    @property
    def footer(self):
        return self.center_and_lower_compound_panel.footer

    @property
    def center(self):
        return self.center_and_lower_compound_panel.center_panel.center

    @property
    def right(self):
        return self.center_and_lower_compound_panel.center_panel.right

    @property
    def header(self):
        return self.header_frame
