import tkinter as tk


class CustomAbstractFrame(tk.Frame):
    def __init__(self, master) -> None:
        super().__init__(master, background="pink")


class HeaderAbstractFrame(CustomAbstractFrame):

    def __init__(self, master) -> None:
        super().__init__(master)
        self.label = tk.Label(self, text="123")
        self.label.grid(row=0, column=0, sticky="ne")


class CenterPanel(CustomAbstractFrame):

    def __init__(self, master) -> None:
        super().__init__(master)
        paned_window = tk.PanedWindow(self, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True)

        self.frame1 = tk.Frame(paned_window, background="red")
        self.frame2 = tk.Frame(paned_window, background="blue")

        paned_window.add(self.frame1)
        paned_window.add(self.frame2)


class CenterAndLowerCompoundPanel(CustomAbstractFrame):

    def __init__(self, master) -> None:
        super().__init__(master)

        paned_window = tk.PanedWindow(self, orient=tk.VERTICAL)
        paned_window.pack(fill=tk.BOTH, expand=True)

        self.frame1 = CenterPanel(paned_window)
        self.frame2 = tk.Frame(paned_window, height=100, background="black")

        paned_window.add(self.frame1)
        paned_window.add(self.frame2)


class FooterAbstractFrame(CustomAbstractFrame):

    def __init__(self, master) -> None:
        super().__init__(master)


class RightAbstractFrame(CustomAbstractFrame):

    def __init__(self, master) -> None:
        super().__init__(master)


class MainWindow(tk.Tk):

    def __init__(self, ) -> None:
        super().__init__()
        self.right_frame = None
        self.footer_frame = None
        self.center_and_lower_compound_panel = None
        self.header_frame = None
        self.title("Tytul")

    def mount(self):
        self.header_frame = HeaderAbstractFrame(self)
        self.center_and_lower_compound_panel = CenterAndLowerCompoundPanel(self)

        self.header_frame.pack(fill=tk.X, expand=False)
        self.center_and_lower_compound_panel.pack(fill=tk.BOTH, expand=True)

def main():
    w = MainWindow()
    w.mount()
    w.mainloop()


if __name__ == '__main__':
    main()
    # test2()
