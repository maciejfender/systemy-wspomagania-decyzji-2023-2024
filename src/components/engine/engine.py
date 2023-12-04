import functools

import pandas as pd

from components.graphs.graphDialog2d import GraphDialog2d
from components.graphs.graphDialog3d import GraphDialog3d
from components.graphs.histogramDialog import HistogramDialog
from components.header_utils.discretizationDialog import DiscretizationDialog
from components.header_utils.normalizationDialog import NormalizationDialog
from components.header_utils.numericDialog import NumericDialog
from components.header_utils.rangeDialog import RangeDialog
from components.header_utils.rangePercentageDialog import RangePercentageDialog
from components.knn.knn_experiment_gui_all import KnnExperimentAllStartTopLevel
from components.knn.knn_experiment_gui_one import KnnExperimentOneStartTopLevel
from components.knn.knn_test_one_gui import KnnOneClassifierTopLevel
from components.load_data.readData import ReadData


class PrintDecoratorMeta(type):
    def __new__(mcs, name, bases, attrs):
        for attr_name, attr_value in attrs.items():
            if callable(attr_value) and attr_name[0] != '_':
                @functools.wraps(attr_value)
                def callback_decorator(self, *args, func=attr_value, func_name=attr_name, **kwargs):
                    if func_name in self._callbacks_before.keys():  # attr_name[0] != '_' and
                        for i in self._callbacks_before[func_name]:
                            i(self, *args, **kwargs)
                    # print(f"Calling {func_name} with args: {args}, kwargs: {kwargs}")
                    ret = func(self, *args, **kwargs)
                    if func_name in self._callbacks_after.keys():  # attr_name[0] != '_' and
                        for i in self._callbacks_after[func_name]:
                            i(self, *args, result=ret, **kwargs)
                    return ret

                attrs[attr_name] = callback_decorator
        return super(PrintDecoratorMeta, mcs).__new__(mcs, name, bases, attrs)


class Triggerable(metaclass=PrintDecoratorMeta):
    def __init__(self):
        self._callbacks_before = {}
        self._callbacks_after = {}

    def register_callback_before(self, name, callback):
        name = name.__name__
        if name not in self._callbacks_before.keys():
            self._callbacks_before[name] = []
        self._callbacks_before[name].append(callback)

    def unregister_callback_before(self, name, callback):
        name = name.__name__
        if name not in self._callbacks_before.keys():
            return
        self._callbacks_before[name].remove(callback)

    def register_callback_after(self, name, callback):
        name = name.__name__
        if name not in self._callbacks_after.keys():
            self._callbacks_after[name] = []
        self._callbacks_after[name].append(callback)

    def unregister_callback_after(self, name, callback):
        name = name.__name__
        if name not in self._callbacks_after.keys():
            return
        self._callbacks_after[name].remove(callback)


class Engine(Triggerable):

    def __init__(self, main_window) -> None:
        super().__init__()
        self.main_window = main_window
        self.dataset = None
        self.dataset_original = None

        # self.register_callback_after(self.set_dataset, self.main_window.footer.update_view)

    def set_dataset(self, x):
        if self.dataset_original is None:
            self.dataset_original = pd.DataFrame(x)

        self.dataset = x

    def get_dataset(self):
        return self.dataset

    def add_discretization(self, column: str, bins: str, labels: str):
        df = self.dataset

        bins_list = bins.replace(" ", "").split(",")
        bins_list = [float(element) for element in bins_list]
        labels_list = labels.replace(" ", "").split(",")

        df[column + ' - Dyskr'] = pd.cut(df[column], bins=bins_list, labels=labels_list)

        self.dataset = df

    def read_data(self):
        ReadData(self.main_window, self.set_dataset)

    def graph_2d_dialog(self):
        GraphDialog2d(self.main_window, self.dataset, self.main_window.center_panel.temp.set_data)

    def graph_3d_dialog(self):
        GraphDialog3d(self.main_window, self.dataset, self.main_window.center_panel.temp.set_data)

    def discretization_dialog(self):
        DiscretizationDialog(self.main_window, self.dataset, self.add_discretization)

    def df_to_original(self):
        self.dataset = pd.DataFrame(self.dataset_original)

    def min_max(self, column: str, lower_bound: str, upper_bound: str):
        lower = float(lower_bound)
        upper = float(upper_bound)
        self.dataset = self.dataset[(self.dataset[column] >= lower) & (self.dataset[column] <= upper)]

    def min_max_dialog(self):
        RangeDialog(self.main_window, self.dataset, self.min_max)

    def min_max_percentage(self, column: str, lower_bound_percentage: str, upper_bound_percentage: str):
        lower_bound = None
        upper_bound = None

        if lower_bound_percentage != '':
            lower_bound = self.dataset[column].quantile(int(lower_bound_percentage) / 100)

        if upper_bound_percentage != '':
            upper_bound = self.dataset[column].quantile(int(upper_bound_percentage) / 100)

        if lower_bound_percentage != '' and upper_bound_percentage != '':
            self.dataset = self.dataset[(self.dataset[column] <= lower_bound) & (self.dataset[column] >= upper_bound)]
        elif lower_bound_percentage != '':
            self.dataset = self.dataset[(self.dataset[column] <= lower_bound)]
        elif upper_bound_percentage != '':
            self.dataset = self.dataset[(self.dataset[column] >= upper_bound)]

    def min_max_percentage_dialog(self):
        RangePercentageDialog(self.main_window, self.dataset, self.min_max_percentage)

    def normalization(self, column):
        df = self.dataset
        df[column + ' - Norm'] = (df[column] - df[column].mean()) / df[column].std()

        self.dataset = df

    def normalization_dialog(self):
        NormalizationDialog(self.main_window, self.dataset, self.normalization)

    def numeric(self, column):
        data = self.dataset[column]
        data = set(data)
        data = sorted(list(data))

        dictionary = {}

        for idx, item in enumerate(data):
            dictionary[item] = idx + 1

        new_column = []

        for item in self.dataset[column]:
            new_column.append(dictionary[item])

        self.dataset[column + ' - Num'] = new_column

    def numeric_dialog(self):
        NumericDialog(self.main_window, self.dataset, self.numeric)

    def histogram_dialog(self):
        HistogramDialog(self.main_window, self.dataset, self.main_window.center_panel.temp.set_data)

    def open_knn_one_module(self):
        KnnOneClassifierTopLevel(self.main_window, 1)

    def open_knn_experiment_module(self):
        KnnExperimentOneStartTopLevel(self.main_window)

    def open_knn_experiment_all_module(self):
        KnnExperimentAllStartTopLevel(self.main_window)

    def remove_empty_cols(self):
        # Count unique values in each column
        unique_counts = self.dataset.nunique()

        # Get columns with only one unique value
        single_value_cols = unique_counts[unique_counts == 1].index

        # Drop columns with only one unique value
        self.dataset = self.dataset.drop(single_value_cols, axis=1)

