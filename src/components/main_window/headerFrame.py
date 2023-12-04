import tkinter as tk

from src.components.abstract.abstractFrames import HeaderAbstractFrame


class HeaderFrame(HeaderAbstractFrame):
    def __init__(self, master: "MainWindow"):
        super().__init__(master)

        self._mount_elements()

    def _mount_elements(self):
        self.read_btn = tk.Button(self, text="Wczytaj dataset", command=self.load_data)
        self.read_btn.grid(row=self._row(), column=self._new_col(), sticky="nsew")

        self.read_btn = tk.Button(self, text="Wykres 2D", command=self.graph_2d)
        self.read_btn.grid(row=self._row(), column=self._new_col(), sticky="nsew")

        self.read_btn = tk.Button(self, text="Wykres 3D", command=self.graph_3d)
        self.read_btn.grid(row=self._row(), column=self._new_col(), sticky="nsew")

        self.read_btn = tk.Button(self, text="Dyskryminacja zmiennej", command=self.discretization)
        self.read_btn.grid(row=self._row(), column=self._new_col(), sticky="nsew")

        self.read_btn = tk.Button(self, text="Histogram", command=self.histogram)
        self.read_btn.grid(row=self._row(), column=self._new_col(), sticky="nsew")

        self._reset_col()

        self.read_btn = tk.Button(self, text="Normalizacja", command=self.normalization)
        self.read_btn.grid(row=self._new_row(), column=self._new_col(), sticky="nsew")

        self.read_btn = tk.Button(self, text="Normalizacja całego zbioru", command=self.normalization_whole)
        self.read_btn.grid(row=self._row(), column=self._new_col(), sticky="nsew")

        self.read_btn = tk.Button(self, text="Zmień rozkład danych - zakres wartości", command=self.min_max)
        self.read_btn.grid(row=self._row(), column=self._new_col(), sticky="nsew")

        self.read_btn = tk.Button(self, text="Zmień rozkład danych - zakres procentowy",command=self.min_max_percentage)
        self.read_btn.grid(row=self._row(), column=self._new_col(), sticky="nsew")

        self.read_btn = tk.Button(self, text="Zmień dane na numeryczne", command=self.numeric)
        self.read_btn.grid(row=self._row(), column=self._new_col(), sticky="nsew")

        self._reset_col()

        self.read_btn = tk.Button(self, text="knn", command=self.knn)
        self.read_btn.grid(row=self._new_row(), column=self._new_col(), sticky="nsew")

        self.read_btn = tk.Button(self, text="Przywróć dane", command=self.original_data)
        self.read_btn.grid(row=self._row(), column=self._new_col(), sticky="nsew")

    def load_data(self):
        self.master.footer.load_data()

    def graph_2d(self):
        self.master.center_panel.set_and_mount_graph_2d()

    def graph_3d(self):
        self.master.center_panel.set_and_mount_graph_3d()

    def discretization(self):
        self.master.engine.discretization_dialog()

    def normalization(self):
        self.master.engine.normalization_dialog()

    def normalization_whole(self):
        self.master.engine.normalize_whole_dataset()
        self.master.footer.update_view()

    def min_max(self):
        self.master.engine.min_max_dialog()

    def min_max_percentage(self):
        self.master.engine.min_max_percentage_dialog()

    def numeric(self):
        self.master.engine.numeric_dialog()

    def original_data(self):
        self.master.engine.df_to_original()
        self.master.footer.update_view()

    def histogram(self):
        self.master.center_panel.set_and_mount_histogram()

    def knn(self):
        self.master.engine.open_knn_module()
