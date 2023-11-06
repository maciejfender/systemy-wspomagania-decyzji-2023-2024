import tkinter as tk
from tkinter import filedialog

from src.components.abstract.headerAbstractFrame import HeaderAbstractFrame
from src.components.main_window.footerFrame import FooterFrame


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
