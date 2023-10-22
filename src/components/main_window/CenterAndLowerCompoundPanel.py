from src.components.abstract.CustomAbstractFrame import CustomAbstractFrame
from CenterPanel import CenterPanel, tk


class CenterAndLowerCompoundPanel(CustomAbstractFrame):

    def __init__(self, master) -> None:
        super().__init__(master)

        paned_window = tk.PanedWindow(self, orient=tk.VERTICAL)
        paned_window.pack(fill=tk.BOTH, expand=True)

        self.frame1 = CenterPanel(paned_window)
        self.frame2 = tk.Frame(paned_window, height=100, background="black")

        paned_window.add(self.frame1)
        paned_window.add(self.frame2)
