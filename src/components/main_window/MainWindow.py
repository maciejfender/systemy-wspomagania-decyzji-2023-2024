from HeaderFrame import HeaderFrame
from FooterFrame import FooterFrame
from CenterAndLowerCompoundPanel import CenterAndLowerCompoundPanel, tk


class MainWindow(tk.Tk):

    def __init__(self, ) -> None:
        super().__init__()
        self.right_frame = None
        self.footer_frame = None
        self.center_and_lower_compound_panel = None
        self.header_frame = None
        self.title("Kuwa najlepsza apka ever")

    def mount(self):
        self.header_frame = HeaderFrame(self)
        self.center_and_lower_compound_panel = CenterAndLowerCompoundPanel(self)
        # self.footer_frame = FooterFrame(self)

        self.header_frame.pack(fill=tk.X, expand=False)
        self.center_and_lower_compound_panel.pack(fill=tk.BOTH, expand=True)
        # self.footer_frame.pack(fill=tk.X, expand=True)
