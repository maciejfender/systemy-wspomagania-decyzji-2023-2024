import pandas as pd
from pandastable import Table

from src.components.abstract.customAbstractFrame import CustomAbstractFrame
from src.components.main_window.footerFrameMeta import FooterFrameMeta


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
