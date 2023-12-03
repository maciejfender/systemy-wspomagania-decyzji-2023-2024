import tkinter as tk
from tkinter import ttk

import pandas as pd

from components.knn.knn_experiment_gui import KnnExperimentStartTopLevel
from components.knn.knn_test_one_gui import KnnOneClassifierTopLevel


class KnnLabelFrame(ttk.LabelFrame):

    @property
    def dataset(self):
        return self.master.dataset

    @property
    def len_of_data(self):
        return 100
        # return len(self.dataset.index) fixme

    @property
    def main_window(self):
        self.master.master


class KnnExperimentFrame(KnnLabelFrame):

    def __init__(self, master) -> None:
        super().__init__(master, text="Eksperyment i obliczenie statystyk")
        self.launch = tk.Button(self, text ="pokaż", command=self.experiment_start)
        self.launch.pack()

    def experiment_start(self):
        KnnExperimentStartTopLevel(self)


class KnnTestOneFrame(KnnLabelFrame):

    def __init__(self, master) -> None:
        super().__init__(master, text="Klasyfikacja 1 obiektu")

        self.scale_text_var = tk.StringVar(self, value="1")

        self.scale_text_var.trace("w", lambda *args: self.update_values_in_label_and_entry())
        self.scale_label = tk.Label(self, text="K: ")
        self.scale_label.pack()

        self.scale_label = tk.Entry(self, textvariable=self.scale_text_var, )
        self.scale_label.pack()

        self.scale = tk.Scale(self,
                              from_=1,
                              to=self.len_of_data - 1,
                              resolution=1,
                              tickinterval=self.len_of_data // 10,
                              orient=tk.HORIZONTAL,
                              length=300,
                              command=self.update_values_in_label_and_entry)

        self.scale.pack()

        self.button_launch = tk.Button(self, text="start",
                                       command=lambda *args, **kwargs: KnnOneClassifierTopLevel(self,
                                                                                                self.get_value()))
        self.button_launch.pack()

    def get_value(self):
        return int(self.scale_text_var.get())

    def update_values_in_label_and_entry(self, value=None):
        if not value:
            value = self.scale_text_var.get()
        value = int(value)
        assert 1 <= value <= (self.len_of_data - 1)
        self.scale_text_var.set(str(value))
        self.scale.set(value=value)


class KnnModuleTopLevel(tk.Toplevel):

    def __init__(self, master, df: pd.DataFrame) -> None:
        super().__init__(master)
        self.dataset = df
        self._prepare_view()

    def _prepare_experiment_view(self):
        KnnExperimentFrame(self).pack()

    def _prepare_test_one_view(self):
        KnnTestOneFrame(self).pack()

    def _prepare_view(self):
        self._prepare_test_one_view()
        self._prepare_experiment_view()
