import tkinter as tk
from tkinter import ttk

from components.ScrollableCustomFrame import ScrollableCustomFrame
from components.knn.KnnOneToEveryDecisionStrategy import KnnOneToEveryDecisionStrategy
from components.knn.distance_strategies.distances import *

RESULT_PREFIX = "Rezultat: "

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


class KnnOneClassifierEntry(tk.Frame):

    def __init__(self, master, name) -> None:
        super().__init__(master)
        self.name = name
        self.var_value = tk.StringVar(self, value="")
        self.var_enabled = tk.BooleanVar(self, value=False)

        self.checkbox_enabled = tk.Checkbutton(self, text=name, command=self.toggle_state, variable=self.var_enabled)
        self.checkbox_enabled.grid(row=0, column=1)

        self.entry_value = tk.Entry(self, textvariable=self.var_value)
        self.entry_value.grid(row=0, column=2)
        self.disable()

    def __bool__(self):
        return self.var_enabled.get()

    def disable(self):
        self.entry_value.config(state='disabled')

    def enable(self):
        self.entry_value.config(state='normal')

    def toggle_state(self, *args, **kwargs):
        if self.var_enabled.get():
            self.enable()
        else:
            self.disable()
        pass

    def get_value(self):
        return float(self.var_value.get())

    def set_state_active(self):
        self.enable()
        self.var_enabled.set(True)
    def set_state_inactive(self):
        self.disable()
        self.var_enabled.set(False)


class KnnOneClassifierTopLevel(tk.Toplevel):

    @property
    def dataset(self):
        return self.master.engine.dataset

    @property
    def k(self):
        return int(self.var_k.get())

    def __init__(self, master, k: int) -> None:
        super().__init__(master, )
        self._k = k
        self.entries = {}
        self.label_note = tk.Label(self, )

        self.var_k = tk.StringVar(self, value=str(k))
        self.entry_k = tk.Entry(self, textvariable=self.var_k)
        self.entry_k.pack()

        self.frame_entries = tk.Frame(self)
        self.frame_entries.pack()
        self.entries = {}
        self.scrollable = ScrollableCustomFrame(self)

        for name in self.dataset.columns:
            temp = KnnOneClassifierEntry(self.scrollable.get_frame_for_content(), str(name))
            temp.pack()
            self.entries[name] = temp

        self.scrollable.pack()
        self.scrollable.update_view_after_adding_elements()

        self.btn_enable_all = tk.Button(self, text="Enable all", command = self.enable_all)
        self.btn_enable_all.pack()

        self.btn_disable_all = tk.Button(self, text="Disable all", command = self.disable_all)
        self.btn_disable_all.pack()

        self.label_distance = tk.Label(self, text="Wybierz typ odległości:")
        self.label_distance.pack()
        self.var_distance = tk.StringVar(self, value=NORMAL_STRATEGY )
        self.distance_combobox = ttk.Combobox(self,
                                              textvariable=self.var_distance,
                                              values=[NORMAL_STRATEGY, CZEBYSZEW_STRATEGY, MANHATTAN_STRATEGY,
                                                      MAHALANOBIS_STRATEGY])
        self.distance_combobox.pack()

        list_of_columns = list(self.dataset.columns)
        self.var_class_column = tk.StringVar(self, value=list_of_columns[-1])
        self.combobox_class_column = ttk.Combobox(self,
                                                  textvariable=self.var_class_column,
                                                  values=list_of_columns)
        self.combobox_class_column.pack()

        self.submit = tk.Button(self, text="Sprawdź", command=self.submit_action)
        self.submit.pack()

        self.var_result = tk.StringVar(self, value=RESULT_PREFIX)
        self.label_result = tk.Label(self, textvariable=self.var_result)
        self.label_result.pack()

    def enable_all(self):
        for entry in self.entries.values():
            entry.set_state_active()

    def disable_all(self):
        for entry in self.entries.values():
            entry.set_state_inactive()

    def _get_vector(self):
        ret = {}
        for name, value in self.entries.items():
            if value:
                ret[name] = value.get_value()

        return ret

    def _get_column_names(self):
        ret = []
        for name, value in self.entries.items():
            if value:
                ret.append(name)
        return ret

    def _get_strategy(self, strategy_name):
        return STRATEGY_MAPPING[strategy_name](self.dataset, self._get_column_names())

    def submit_action(self):
        distance_strategy_name = self.var_distance.get()
        distance_strategy = self._get_strategy(distance_strategy_name)
        class_column_name = self.var_class_column.get()
        vec = self._get_vector()

        result = KnnOneToEveryDecisionStrategy(distance_strategy, self.dataset, class_column_name).make_decision(vec, self.k)
        self.var_result.set(RESULT_PREFIX+str(result))

