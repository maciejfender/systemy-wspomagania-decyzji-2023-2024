from typing import Dict

import pandas as pd

from components.knn.distance_strategies.distances import DistanceStrategy


class KnnOneToEveryDecisionStrategy:
    def __init__(self, strategy: DistanceStrategy, dataset: pd.DataFrame, class_column_name: str) -> None:
        self.strategy = strategy
        self.class_column_name = class_column_name
        self.dataset = dataset

    def _score_every_row(self, other: Dict[str, float]):
        rows = self.dataset.to_dict(orient='records')
        scored = []
        for r in rows:
            c = r[self.class_column_name]
            distance = self.strategy.distance(other, r)
            scored.append([distance, c])
        return scored

    def make_decision(self, other: Dict[str, float], k: int):
        """
        W skrócie, bierze sortuje je po scorze, wybiera K z najmniejszymi odl, potem zlicza ile jest czego, jak jest wiele maxów wybiera alfabetycznie najmniejszego

        :param other:
        :param k:
        :return:
        """
        scored = self._score_every_row(other)
        print(f"{scored=}")
        print(f"{sorted(scored, key=lambda x:x[0])=}")
        print(f"{sorted(scored, key=lambda x:x[1])=}")
        counted = {}
        for _, c in sorted(scored, key=lambda x: x[0])[:k]:
            if c not in counted.keys():
                counted[c] = 0
            counted[c] += 1

        max_occurred = max(counted.values())

        print(f"{max_occurred=}")
        selected = list({k: v for k, v in counted.items() if v == max_occurred}.keys())
        print(f"{selected=}\n\n")
        return sorted(selected)[0]
