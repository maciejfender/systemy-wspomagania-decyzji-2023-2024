from src.components.abstract.HeaderAbstractFrame import HeaderAbstractFrame, tk
from FooterFrame import FooterFrame
from tkinter import filedialog

class HeaderFrame(HeaderAbstractFrame):
    def __init__(self, master):
        super().__init__(master)

        self.read_excel_btn = tk.Button(self, text="Wczytaj dataset")
        self.read_excel_btn.grid(row=0, column=1, sticky="ne")

        self.read_excel_btn.config(command=self.load_data_excel)

    def load_data_excel(self):
        file = filedialog.askopenfile()
        print(file.name)
        ff = FooterFrame()
        ff.load_data_excel(file.name)

