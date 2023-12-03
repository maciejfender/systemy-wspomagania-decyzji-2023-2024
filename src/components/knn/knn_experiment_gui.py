import time
import tkinter as tk
from concurrent.futures import ThreadPoolExecutor
from tkinter import ttk

from components.ScrollableCustomFrame import ScrollableCustomFrame
from components.knn.KnnOneToEveryDecisionStrategy import KnnOneToEveryDecisionStrategy
from components.knn.KnnOneToEveryDecisionStrategyWithOptimization import KnnOneToEveryDecisionStrategyWithOptimization
from components.knn.distance_strategies.distances import *

MAHALANOBIS_STRATEGY = "Mahalanobisa"
MANHATTAN_STRATEGY = "Manhattan"
CZEBYSZEW_STRATEGY = "Czebyszewa"
NORMAL_STRATEGY = 'Normalna'

STRATEGY_MAPPING = {
    MANHATTAN_STRATEGY: MahalanobisDistanceStrategy,
    CZEBYSZEW_STRATEGY: CzebyszewDistanceStrategy,
    MAHALANOBIS_STRATEGY: MahalanobisDistanceStrategy,
    NORMAL_STRATEGY: CartesianDistanceStrategy,
}


class KnnExperimentVariableEntry(tk.Frame):

    def __init__(self, master, name, t, enabled=True) -> None:
        super().__init__(master)
        self.name = name
        self.var_value = tk.StringVar(self, value="")
        self.var_enabled = tk.BooleanVar(self, value=enabled)
        self.t = t

        self.checkbox_enabled = tk.Checkbutton(self, text=f"{name} ({t})", variable=self.var_enabled)
        self.checkbox_enabled.grid(row=0, column=1)

    def __bool__(self):
        return self.var_enabled.get()


class KnnExperimentStartTopLevel(tk.Toplevel):
    @property
    def dataset(self):
        return self.master.dataset

    def __init__(self, master) -> None:
        super().__init__(master)

        STRATEGIES_KEY_LIST = list(STRATEGY_MAPPING.keys())
        self.var_strategy = tk.StringVar(self, value=NORMAL_STRATEGY)
        self.combobox_strategy = ttk.Combobox(self, values=STRATEGIES_KEY_LIST, textvariable=self.var_strategy)
        self.combobox_strategy.pack()

        last_col = self.dataset.columns[-1]
        self.var_column = tk.StringVar(self, value=last_col)
        self.combobox_class_column = ttk.Combobox(self, values=list(self.dataset.columns), textvariable=self.var_column)
        self.combobox_class_column.pack()

        self.var_k = tk.StringVar(self, value=str(1))
        self.entry_k = tk.Entry(self, textvariable=self.var_k)
        self.entry_k.pack()

        self.frame_entries = tk.Frame(self)
        self.frame_entries.pack()
        self.entries = {}
        self.scrollable = ScrollableCustomFrame(self)
        self.scrollable.pack()

        for name, t in list(self.dataset.dtypes.items()):
            temp = KnnExperimentVariableEntry(self.scrollable.get_frame_for_content(), name, str(t),
                                              True if name != last_col else False)
            temp.pack()
            self.entries[name] = temp

        self.scrollable.update_view_after_adding_elements()

        self.btn_submit = tk.Button(self, text="Start", command=self.start)
        self.btn_submit.pack()

    def start(self):
        strategy = STRATEGY_MAPPING[self.var_strategy.get()]
        dataset = self.dataset
        column = self.var_column.get()
        k = self.get_k()
        assert 1 <= k <= len(dataset.index) - 1
        columns = self.get_variables_list()
        records_to_LOO = list(dataset.index)
        print(KnnBetterExperiment(k, column, records_to_LOO, dataset, strategy, columns, ).do())

    def get_k(self):
        return int(self.var_k.get())

    def get_variables_list(self):
        return [k for k, v in self.entries.items() if v]


class KnnExperiment:
    def __init__(self, k, column, records_to_LOO, dataset, strategy, columns):
        self.k = k
        self.class_column = column
        self.records_ids = records_to_LOO
        self.dataset = dataset
        self.strategy = strategy(dataset, columns)

    def do(self):
        results = []
        start = time.time()

        for r in self.records_ids:
            result_expected_class = self.process_one_case(r)

            results.append(result_expected_class)
        end = time.time()
        print(end - start)
        res = results.count(True)
        print(res)

        return res

    def process_one_case(self, r):
        df = self.dataset.copy()
        row = df.loc[r].to_dict()
        df = df.drop(r)
        expected_class = row.pop(self.class_column)
        result = KnnOneToEveryDecisionStrategy(self.strategy,
                                               df,
                                               self.class_column) \
            .make_decision(row, self.k)
        result_expected_class = result == expected_class
        return result_expected_class

    def do_parallel(self):

        results = []
        start = time.time()

        # Użycie ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=3) as executor:
            # Pusta lista do przechowywania wyników
            # Uruchamianie zadań i zbieranie wyników
            futures = [executor.submit(self.process_one_case, r) for r in self.records_ids]

            for future in futures:
                result = future.result()  # Oczekiwanie na wynik
                results.append(result)

        # for r in self.records_ids:
        #     result_expected_class = self.process_one_case(class_column, dataset, k, r, strategy)
        #
        #     results.append(result_expected_class)
        end = time.time()
        print(end - start)
        res = results.count(True)
        print(res)


class KnnBetterExperiment:
    def __init__(self, k, column, records_to_LOO, dataset, strategy, columns):
        self.k = k
        self.class_column = column
        self.records_ids = records_to_LOO

        # columns_to_drop = [col for col in dataset.columns if col not in columns]
        # self.dataset = dataset.drop(columns=columns_to_drop, axis=1)
        self.dataset = dataset

        self.strategy = strategy(dataset, columns)
        self.columns = columns

        self.decision = KnnOneToEveryDecisionStrategyWithOptimization(self.strategy,
                                                                      self.dataset.copy(),
                                                                      self.class_column,
                                                                      self.columns
                                                                      )

    def do(self):
        results = []
        start = time.time()
        no_of_all = len(self.records_ids)
        for i,r in enumerate(self.records_ids):
            result_expected_class = self.process_one_case(r)
            print(f"{i:4}/{no_of_all:4}, {i/no_of_all*100:.2}")

            results.append(result_expected_class)
        end = time.time()
        print(end - start)
        res = results.count(True)
        print(res)

        return res

    def process_one_case(self, r):
        row = self.dataset.loc[r].to_dict()
        result = self.decision \
            .make_decision(r, self.k)
        expected_class = row[self.class_column]
        result_expected_class = result == expected_class
        return result_expected_class
