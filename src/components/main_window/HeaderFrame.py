from src.components.abstract.HeaderAbstractFrame import HeaderAbstractFrame, tk


class HeaderFrame(HeaderAbstractFrame):
    def __init__(self, master):
        super().__init__(master)

        self.button = tk.Button(self, text="Przycisk")
        self.button.grid(row=0, column=1, sticky="ne")

        self.button.config(command=self.load_data_excel)

    def load_data_excel(self):
        print([2,3])
        pass