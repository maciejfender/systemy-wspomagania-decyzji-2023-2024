import abc
import math
from typing import List, Any, Dict, Union

import numpy as np
import pandas as pd

ALL_COLUMNS_C = "__ALL__"


class DistanceStrategy(abc.ABC):

    def __init__(self, df: "pd.DataFrame" = None, columns: Union[List[str], str] = ALL_COLUMNS_C) -> None:
        super().__init__()
        self.dataset = df
        if columns == ALL_COLUMNS_C:
            self.columns = self.dataset.columns
        else:
            self.columns = columns

    @abc.abstractmethod
    def distance(self, a, b) -> float:
        ...

    @classmethod
    def _filter_and_join_data(cls, a: Dict[str, Any], b: Dict[str, Any], columns: List[str]):
        """
        Filters and joins (zips) dictionaries. Columns mentioned only in columns are taken into account.

        :param a: Dict 1
        :param b: Dict 2
        :param columns: List of keys
        :return: Collection with merged values
        """

        filtered_a = cls._filter_dict(a, columns)
        filtered_b = cls._filter_dict(b, columns)

        assert set(filtered_a.keys()) == set(filtered_b.keys()), "Missing Keys!"

        returned_zipped_collection = list()

        for k in filtered_a.keys():
            returned_zipped_collection.append((filtered_a[k], filtered_b[k]))

        return returned_zipped_collection

    @staticmethod
    def _filter_dict(d, columns):
        """
        Removes keys not present in columns list
        :param d: Dictionary to remove keys from
        :param columns: List containing names that can be only in dict
        :return: New dict with constrained keys
        """
        return {key: d[key] for key in d.keys() if key in columns}
        #FIXME
        # return d


    @staticmethod
    def _filter_df_with_col_names(df, columns):
        return df[columns].copy()

    @classmethod
    def _filter_and_calc_cov_matrix(cls, df: "pd.DataFrame", columns: List[str]):
        filtered = cls._filter_df_with_col_names(df, columns)

        for col in filtered.columns:
            try:
                pd.to_numeric(filtered[col])
            except ValueError:
                assert False, f"Column '{col}' contains non-numeric data."

        return np.cov(filtered.values,rowvar=False)


class CartesianDistanceStrategy(DistanceStrategy):
    def distance(self, a: Dict[str, Any], b: Dict[str, Any]) -> float:
        filtered_and_zipped = self._filter_and_join_data(a, b, self.columns)
        return sum(
            map(
                lambda x: math.pow(x[0] - x[1], 2),
                filtered_and_zipped,
            )
        )


class ManhattanDistanceStrategy(DistanceStrategy):
    def distance(self, a, b) -> float:
        filtered_and_zipped = self._filter_and_join_data(a, b, self.columns)
        return sum(
            map(
                lambda x: abs(x[0] - x[1]),
                filtered_and_zipped,
            )
        )


class MahalanobisDistanceStrategy(DistanceStrategy):

    def __init__(self, df, columns) -> None:
        super().__init__(df, columns)
        self.covariance_matrix = self._filter_and_calc_cov_matrix(df, columns)
        self.inv_covariance_matrix = np.linalg.inv(self.covariance_matrix)

    def distance(self, a, b) -> float:
        filtered_and_zipped = self._filter_and_join_data(a, b, self.columns)
        diff_vector = np.array(list(map(lambda v: abs(v[0] - v[1]), filtered_and_zipped)))
        return math.sqrt(np.dot(np.dot(diff_vector, self.inv_covariance_matrix), diff_vector).item())


class CzebyszewDistanceStrategy(DistanceStrategy):
    def distance(self, a, b) -> float:
        filtered_and_zipped = self._filter_and_join_data(a, b, self.columns)
        return max(
            map(
                lambda x: abs(x[0] - x[1]),
                filtered_and_zipped,
            )
        )
