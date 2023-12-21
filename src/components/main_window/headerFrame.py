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

        self.read_btn = tk.Button(self, text="Zmień zakres danych", command=self.min_max)
        self.read_btn.grid(row=self._row(), column=self._new_col(), sticky="nsew")

        self.read_btn = tk.Button(self, text="Zmień zakres danych",
                                  command=self.min_max_percentage)
        self.read_btn.grid(row=self._row(), column=self._new_col(), sticky="nsew")

        self.read_btn = tk.Button(self, text="Zmień dane na numeryczne", command=self.numeric)
        self.read_btn.grid(row=self._row(), column=self._new_col(), sticky="nsew")

        self._reset_col()

        self.read_btn = tk.Button(self, text="Usuń kolumny z jedną wartością", command=self.delete_columns_with_one_value)
        self.read_btn.grid(row=self._new_row(), column=self._new_col(), sticky="nsew")

        self.btn_knn_one = tk.Button(self, text="knn One", command=self.knn_one)
        self.btn_knn_one.grid(row=self._row(), column=self._new_col(), sticky="nsew")

        self.btn_knn_exp = tk.Button(self, text="knn Experiment", command=self.knn_experiment)
        self.btn_knn_exp.grid(row=self._row(), column=self._new_col(), sticky="nsew")

        self.btn_knn_exp_all = tk.Button(self, text="knn Experiment ALL", command=self.knn_experiment_all)
        self.btn_knn_exp_all.grid(row=self._row(), column=self._new_col(), sticky="nsew")

        self.read_btn = tk.Button(self, text="Zmień rozkład danych - zakres wartości", command=self.min_max_normalize)
        self.read_btn.grid(row=self._row(), column=self._new_col(), sticky="nsew")

        self._reset_col()

        self.btn_partition_frame = tk.Button(self, text="Partitioning", command=self.partition_2D_frame)
        self.btn_partition_frame.grid(row=self._new_row(), column=self._new_col(), sticky="nsew")

        self.btn_partition_frame = tk.Button(self, text="Partitioning MultiDim", command=self.partition_multi_dim_frame)
        self.btn_partition_frame.grid(row=self._row(), column=self._new_col(), sticky="nsew")

        self.btn_save_df = tk.Button(self, text="Save data", command=self.save_data)
        self.btn_save_df.grid(row=self._row(), column=self._new_col(), sticky="nsew")

        self.read_btn = tk.Button(self, text="Przywróć dane", command=self.original_data)
        self.read_btn.grid(row=self._row(), column=self._new_col(), sticky="nsew")

    def load_data(self):
        self.master.footer.load_data()

    def save_data(self):
        self.master.engine.save_data_dialog()

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

    def min_max_normalize(self):
        self.master.engine.min_max_normalize_dialog()

    def min_max_percentage(self):
        self.master.engine.min_max_percentage_dialog()

    def numeric(self):
        self.master.engine.numeric_dialog()

    def original_data(self):
        self.master.engine.df_to_original()
        self.master.footer.update_view()

    def histogram(self):
        self.master.center_panel.set_and_mount_histogram()

    def knn_one(self):
        self.master.engine.open_knn_one_module()

    def knn_experiment(self):
        self.master.engine.open_knn_experiment_module()

    def knn_experiment_all(self):
        self.master.engine.open_knn_experiment_all_module()

    def partition_multi_dim_frame(self):
        self.master.engine.open_partition_multi_dim_module()
    def partition_2D_frame(self):
        self.master.engine.open_partition_2D_module()

    def remove_empty_cols(self):
        self.master.engine.remove_empty_cols()
        self.master.footer.update_view()

    def delete_columns_with_one_value(self):
        self.master.engine.delete_columns_with_one_value()
        self.master.footer.update_view()
