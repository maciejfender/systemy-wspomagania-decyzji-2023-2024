import tkinter as tk
from tkinter import ttk


class GraphDialog(tk.Toplevel):

    def __init__(self, master, df, data_setter) -> None:
        super().__init__(master)
        self.geometry("600x370")
        self.df = df
        self.data_setter = data_setter
        self.series = None
        self.scale = None
        self.scale_candidates_labels = []
        self.button = None

        self.mount()

    def mount(self):
        self.scale = self.df.columns.tolist()
        print(self.scale)

        for column in self.scale:
            label = tk.Label(master=self, text=column)
            self.scale_candidates_labels.append(label)

        for i, label in enumerate(self.scale_candidates_labels):
            label.grid(row=i, column=0, sticky='nw')

        self.button = tk.Button(self, text="Dalej")
        self.button.config(command=self.get_graph_params_and_destroy)
        self.button.grid(row=len(self.scale) + 1, column=0, sticky="ne")

    def get_graph_params_and_destroy(self):
        self.data_setter(('Imie', ['Wiek']))
        self.master.center_panel.mount_graph_2d()
        self.destroy()
        self.update()

