import tkinter as tk
from src.components.load_data.readFrame import ReadFrame
from src.components.load_data.changeFrame import ChangeFrame
from src.components.load_data.confirmFrame import ConfirmFrame
from src.components.engine.engineUtils import activate, deactivate, read_to_df


class ReadData(tk.Toplevel):

    def __init__(self, master, data_setter) -> None:
        super().__init__(master)
        self.geometry("600x370")
        self.data_setter = data_setter
        self.path = ""
        self.df = ""
        self.frames = []
        self.current_frame = None
        self.button_next = None
        self.button_back = None

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.mount()

    def mount(self):
        self.button_back = tk.Button(self, text="Wstecz", command=self.go_back)
        self.button_back.grid(row=1, column=0, sticky='se')

        self.button_next = tk.Button(self, text="Dalej", command=self.go_next)
        self.button_next.grid(row=1, column=1, sticky='se')

        self.append_frame(ReadFrame(self))

    def go_to_read_frame(self):
        self.frames = []
        self.append_frame(ReadFrame(self))

    def go_to_change_frame(self):
        path = self.current_frame.get_path()
        header_checked = self.current_frame.is_header_checked()
        separator_checked = self.current_frame.is_separator_checked()
        separator = self.current_frame.get_separator()

        self.df = read_to_df(path, header_checked=header_checked, separator_checked=separator_checked, separator=separator)
        print(self.df)

        self.append_frame(ChangeFrame(self, self.df))

    def go_to_confirm_frame(self):
        entries = self.current_frame.get_columns_entries()
        self.update_column_names(entries)

        ct = self.current_frame.get_column_types()
        self.update_data_types(ct)
        print(self.df)

        self.append_frame(ConfirmFrame(self, self.df))

    def append_frame(self, frame):
        self.frames.append(frame)
        self.current_frame = self.frames[-1]
        self.manage_button_states()
        self.current_frame.grid(row=0, column=0, sticky="nsew", columnspan=2)
        self.current_frame.focus_set()

    def go_back(self):
        if len(self.frames) != 0:
            frame_to_delete = self.frames.pop()
            frame_to_delete.destroy()
            self.current_frame = self.frames[-1]
            self.manage_button_states()
            self.current_frame.grid(row=0, column=0, sticky="nsew", columnspan=2)
            self.current_frame.focus_set()

            if isinstance(self.current_frame, ChangeFrame):
                print("ChangeFrame")
            elif isinstance(self.current_frame, ConfirmFrame):
                print("ConfirmFrame")
            elif isinstance(self.current_frame, ReadFrame):
                print("ReadFrame")

    def go_next(self):
        if isinstance(self.current_frame, ChangeFrame):
            self.go_to_confirm_frame()
        elif isinstance(self.current_frame, ConfirmFrame):
            self.button_read_from_path()

    def update_column_names(self, entries):
        new_names = [entry.get() for entry in entries]
        self.df.columns = new_names

    def update_data_types(self, data_types):
        new_types = {}
        for i, column in enumerate(self.df.columns.tolist()):
            new_types[column] = data_types[i].get()
        self.df = self.df.astype(new_types)

    def button_read_from_path(self):
        self.data_setter(self.df)
        self.master.footer.update_view()
        self.destroy()
        self.update()

    @property
    def engine(self):
        return self.master

    def manage_button_states(self):
        if isinstance(self.current_frame, ChangeFrame):
            activate(self.button_back)
            activate(self.button_next)
        elif isinstance(self.current_frame, ConfirmFrame):
            activate(self.button_back)
            activate(self.button_next)
        elif isinstance(self.current_frame, ReadFrame):
            deactivate(self.button_back)
            deactivate(self.button_next)
