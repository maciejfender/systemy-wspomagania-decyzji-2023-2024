import json
import random
import time
import tkinter as tk
from concurrent.futures import ProcessPoolExecutor, as_completed
from tkinter import ttk
from tkinter.constants import BOTTOM

from components.ScrollableCustomFrame import ScrollableCustomFrame
from components.knn.KnnOneToEveryDecisionStrategyWithOptimization import KnnOneToEveryDecisionStrategyWithOptimization
from components.knn.distance_strategies.distances import *

MAHALANOBIS_STRATEGY = "Mahalanobis"
MANHATTAN_STRATEGY = "Manhattan"
CZEBYSZEW_STRATEGY = "Czebyszew"
NORMAL_STRATEGY = 'Euclidean'

STRATEGY_MAPPING = {
    MANHATTAN_STRATEGY: ManhattanDistanceStrategy,
    CZEBYSZEW_STRATEGY: CzebyszewDistanceStrategy,
    MAHALANOBIS_STRATEGY: MahalanobisDistanceStrategy,
    NORMAL_STRATEGY: EuclideanDistanceStrategy,
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


class KnnExperimentAllStartTopLevel(tk.Toplevel):

    @property
    def dataset(self):
        return self.master.engine.dataset

    def __init__(self, master) -> None:
        super().__init__(master)

        STRATEGIES_KEY_LIST = list(STRATEGY_MAPPING.keys())

        tk.Label(self, text="Wybór metryki odległości:").pack()
        self.var_strategy = tk.StringVar(self, value=NORMAL_STRATEGY)
        self.combobox_strategy = ttk.Combobox(self, values=STRATEGIES_KEY_LIST, textvariable=self.var_strategy)
        self.combobox_strategy.pack()

        tk.Label(self, text="Wybór klasy:").pack()
        last_col = self.dataset.columns[-1]
        self.var_column = tk.StringVar(self, value=last_col)
        self.combobox_class_column = ttk.Combobox(self, values=list(self.dataset.columns), textvariable=self.var_column)
        self.combobox_class_column.pack()

        tk.Label(self, text="Wybór kolumn działających jako wejścia:").pack()
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
        self.btn_submit.pack(side=BOTTOM)

    def start(self):
        strategy_name = self.var_strategy.get()
        strategy = STRATEGY_MAPPING[strategy_name]
        dataset = self.dataset
        column = self.var_column.get()
        results = {}
        max_k = len(self.dataset.index) - 1
        start = time.time()

        columns = self.get_variables_list()
        records_to_LOO = list(dataset.index)
        experiment = KnnBetterExperiment(column, records_to_LOO, dataset, strategy, columns, )
        for k in range(1, max_k + 1):
            self.k = k
            elapsed = time.time() - start
            time_for_one = (elapsed) / (k + 1)

            print(f"K: {k} / {max_k}\tO: {time_for_one:.4}\tT: {elapsed:.4}\tRemaining: {(max_k - k) * time_for_one}")

            result = experiment.do(k)
            results[k] = result

        self.dump_results_to_file(results, strategy_name)

        print(time.time() - start)
        print(results)

        self.plot_results(results, strategy_name)

    def dump_results_to_file(self, results, strategy_name):
        filename = self.get_file_name(strategy_name)
        with open(filename, 'w+') as file:
            json.dump(results, file)

    def get_k(self):
        return int(self.var_k.get())

    def get_variables_list(self):
        return [k for k, v in self.entries.items() if v]

    def get_file_name(self, strategy):
        from datetime import datetime
        now = datetime.now().strftime("%m %d %Y %H %M %S")
        return now + " " + strategy + str(random.randint(100000, 900000)) + ".json"

    def plot_results(self, results, strategy_name):
        import matplotlib.pyplot as plt
        dataset = list(zip(*[(k, v) for k, v in results.items()]))
        plt.plot(*dataset)
        plt.title(strategy_name)
        plt.savefig(strategy_name+'.png', dpi=300)
        plt.show()


class KnnBetterExperiment:
    def __init__(self, column, records_to_LOO, dataset, strategy, columns):
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

    def do(self, k):
        self.k = k
        results = []
        start = time.time()
        no_of_all = len(self.records_ids)
        for i, r in enumerate(self.records_ids):
            result_expected_class = self.process_one_case(r)
            # print(f"{i:4}/{no_of_all:4}, {i / no_of_all * 100:.5}")

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

    def do_parallel(self):
        results = []
        start = time.time()
        with ProcessPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(self.process_one_case, r) for r in self.records_ids]
            for future in as_completed(futures):
                results.append(future.result())
        # for r in self.records_ids:
        #     result_expected_class = self.process_one_case(r)

        # results.append(result_expected_class)
        end = time.time()
        print(end - start)
        res = results.count(True)
        print(res)

        return res
