from CustomAbstractFrame import CustomAbstractFrame, tk


class HeaderAbstractFrame(CustomAbstractFrame):

    def __init__(self, master) -> None:
        super().__init__(master)
        self.label = tk.Label(self, text="123")
        self.label.grid(row=0, column=0, sticky="ne")
