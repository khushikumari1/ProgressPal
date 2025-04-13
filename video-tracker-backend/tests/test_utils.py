import unittest
from app.utils import merge_intervals, calculate_total_watched, calculate_percentage

class TestUtils(unittest.TestCase):

    def test_merge_intervals(self):
        self.assertEqual(merge_intervals([[0, 10], [5, 15], [20, 25]]), [[0, 15], [20, 25]])
        self.assertEqual(merge_intervals([[1, 2], [3, 4]]), [[1, 2], [3, 4]])
        self.assertEqual(merge_intervals([]), [])
        self.assertEqual(merge_intervals([[0, 5], [5, 10]]), [[0, 10]])

    def test_total_watched(self):
        self.assertEqual(calculate_total_watched([[0, 10], [5, 15], [20, 25]]), 20)
        self.assertEqual(calculate_total_watched([[1, 2], [3, 4]]), 2)

    def test_percentage(self):
        self.assertAlmostEqual(calculate_percentage([[0, 10], [5, 15], [20, 25]], 50), 40.0)
        self.assertEqual(calculate_percentage([], 60), 0.0)
        self.assertAlmostEqual(calculate_percentage([[0, 30]], 60), 50.0)

