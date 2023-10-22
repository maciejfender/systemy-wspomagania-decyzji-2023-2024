from src.components.abstract.CustomAbstractFrame import CustomAbstractFrame
from FooterFrameMeta import FooterFrameMeta
import tkinter as tk

from pandastable import Table
import pandas as pd
import matplotlib.pyplot as plt


class FooterFrame(CustomAbstractFrame, metaclass=FooterFrameMeta):
    def __init__(self, master=None):
        super().__init__(master)

        self.df = None
        self.pt = None
        self.master = master

    def load_data_excel(self, path):
        self.df = pd.read_excel(path)
        print(self.df)
        self.pt = Table(self, dataframe=self.df)
        self.pt.show()
        self.update()
