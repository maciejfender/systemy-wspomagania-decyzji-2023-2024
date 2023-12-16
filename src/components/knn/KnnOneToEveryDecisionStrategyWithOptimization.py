import time
from typing import List

import pandas as pd

from components.knn.distance_strategies.distances import DistanceStrategy


class KnnOneToEveryDecisionStrategyWithOptimization:
    def __init__(self, strategy: DistanceStrategy, dataset: pd.DataFrame, class_column_name: str,
                 columns: List[str]) -> None:
        self.strategy = strategy
        self.class_column_name = class_column_name
        self.whole_dataset = dataset.copy()
        columns_to_drop = [col for col in self.whole_dataset.columns if col not in columns]

        self.dataset = self.whole_dataset.drop(columns=columns_to_drop, axis=1)
        self.columns = columns

        self.scores = {}
        start = time.time()
        print("Starting preprocessing")

        self.calculate_distances_every_to_every()

        print("Ended preprocessing")
        print(f"Time: {time.time() - start}")

    def calculate_distances_every_to_every(self):

        def add_to_scores(a1, a2, score):
            if a1 not in self.scores.keys():
                self.scores[a1] = {}

            if a2 not in self.scores.keys():
                self.scores[a2] = {}

            self.scores[a1][a2] = score
            self.scores[a2][a1] = score

        rows = self.dataset.to_dict(orient='index')

        for i1, r1 in rows.items():
            print(i1)
            for i2, r2 in rows.items():
                # if iprint(i2, end=' ')
                if i1 == i2:
                    continue
                score = self.strategy.distance(r2, r1)

                add_to_scores(i1, i2, score)

    def make_decision(self, other_index, k: int):
        """
        W skrócie, bierze sortuje je po scorze, wybiera K z najmniejszymi odl, potem zlicza ile jest czego, jak jest wiele maxów wybiera alfabetycznie najmniejszego

        :param other:
        :param k:
        :return:
        """
        scored = [(score, row_index) for row_index, score in self.scores[other_index].items()]

        counted = {}
        for _, row_id in sorted(scored, key=lambda x: x[0])[:k]:
            c = self.whole_dataset.iloc[row_id].to_dict()[self.class_column_name]
            if c not in counted.keys():
                counted[c] = 0
            counted[c] += 1

        max_occurred = max(counted.values())

        # print(f"{max_occurred=}")
        selected = list({k: v for k, v in counted.items() if v == max_occurred}.keys())
        # print(f"{selected=}\n\n")
        return sorted(selected)[0]
