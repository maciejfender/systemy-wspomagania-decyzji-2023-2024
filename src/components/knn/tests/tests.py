import math
import unittest

import numpy as np
import pandas as pd

from components.knn.distance_strategies.distances import DistanceStrategy, EuclideanDistanceStrategy, \
    MahalanobisDistanceStrategy


class TestDistanceStrategy(unittest.TestCase):

    def test_filter_and_join_data(self):
        a = {'x': 1, 'y': 2, 'z': 3}
        b = {'x': 4, 'y': 5, 'z': 6}
        columns = ['x', 'y']

        result = DistanceStrategy._filter_and_join_data(a, b, columns)

        expected = [(1, 4), (2, 5)]
        self.assertEqual(result, expected)

    def test_filter_dict(self):
        d = {'x': 1, 'y': 2, 'z': 3}
        columns = ['x', 'y']

        result = DistanceStrategy._filter_dict(d, columns)

        expected = {'x': 1, 'y': 2}
        self.assertEqual(result, expected)

    def test_euclidean_distance(self):
        a = {'x': 1, 'y': 2, 'z': 3}
        b = {'x': 4, 'y': 5, 'z': 6}
        columns = ['x', 'y']

        strategy = EuclideanDistanceStrategy(None, columns)
        result = strategy.distance(a, b)

        expected = math.pow(1 - 4, 2) + math.pow(2 - 5, 2)
        self.assertEqual(result, expected)


class TestMahalanobisDistanceStrategy(unittest.TestCase):

    def setUp(self):
        # Sample data
        data = {
            'A': [1, 2, 3],
            'B': [4, 5, 7],
            'C': [6, 8, 9]
        }
        self.df = pd.DataFrame(data)
        self.columns = ['A', 'B']

        # Create an instance of MahalanobisDistanceStrategy
        self.strategy = MahalanobisDistanceStrategy(self.df, self.columns)

    def test_distance_calculation(self):
        # Test data for distance calculation
        a = {'A': 1, 'B': 4}
        b = {'A': 2, 'B': 5}

        # Calculate Mahalanobis distance
        distance = self.strategy.distance(a, b)

        # Define the expected distance
        # Note: This needs to be computed based on the specific logic and test data
        diff_vector = np.array([abs(a_val - b_val) for a_val, b_val in zip(a.values(), b.values())])
        expected_distance = math.sqrt(np.dot(np.dot(diff_vector, self.strategy.inv_covariance_matrix), diff_vector))

        # Assert if the calculated distance matches the expected value
        self.assertAlmostEqual(distance, expected_distance, places=6)