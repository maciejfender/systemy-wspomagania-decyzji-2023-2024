from src.components.abstract.CustomAbstractFrame import CustomAbstractFrame, tk


class CenterPanel(CustomAbstractFrame):

    def __init__(self, master) -> None:
        super().__init__(master)
        paned_window = tk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True)

        self.frame1 = tk.Frame(paned_window, background="red")
        self.frame2 = tk.Frame(paned_window, background="blue")

        paned_window.add(self.frame1)
        paned_window.add(self.frame2)
