from HeaderAbstractFrame import HeaderAbstractFrame, tk
from CenterAndLowerCompoundPanel import CenterAndLowerCompoundPanel


class MainWindow(tk.Tk):

    def __init__(self, ) -> None:
        super().__init__()
        self.right_frame = None
        self.footer_frame = None
        self.center_and_lower_compound_panel = None
        self.header_frame = None
        self.title("Kuwa najlepsza apka ever")

    def mount(self):
        self.header_frame = HeaderAbstractFrame(self)
        self.center_and_lower_compound_panel = CenterAndLowerCompoundPanel(self)

        self.header_frame.pack(fill=tk.X, expand=False)
        self.center_and_lower_compound_panel.pack(fill=tk.BOTH, expand=True)
