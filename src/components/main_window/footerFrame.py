from pandastable import Table, TableModel

from src.components.abstract.abstractFrames import CustomAbstractFrame


class FooterFrame(CustomAbstractFrame):
    def __init__(self, master: "MainWindow" = None):
        super().__init__(master)

        self.df = None
        self.pandasFrame = None
        self.master = master

        self._init_view()

    @property
    def main_window(self):
        return self.master.master

    @property
    def dataset(self):
        return self.main_window.engine.dataset

    def load_data(self):
        self.main_window.engine.read_data()
        self.update_view()

    def update_view(self):
        self.pandasFrame.updateModel(TableModel(self.dataset))
        self.pandasFrame.redraw()

    def _init_view(self):
        self.pandasFrame = Table(self)
        self.pandasFrame.show()
        self.update()
