import unittest
import sys
import os

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.algorithms.subset_sum import (
    subset_sum_backtracking,
    subset_sum_dynamic,
    subset_sum_exhaustive
)


class TestSubsetSum(unittest.TestCase):
    """Test cases for Subset Sum algorithms."""

    def setUp(self):
        """Set up test cases."""
        self.test_cases = [
            # (nums, target, expected_result)
            ([1, 2, 3, 4], 7, True),
            ([1, 2, 3, 4], 11, False),
            ([3, 34, 4, 12, 5, 2], 9, True),
            ([3, 34, 4, 12, 5, 2], 35, False),
            ([i for i in range(1, 11)], 30, True),  # 1+2+3+4+5+6+9=30
            ([i for i in range(1, 11)], 60, False),  # Sum of all elements is 55 < 60
            ([], 0, True),  # Empty set sums to 0
            ([], 1, False),  # Empty set doesn't sum to non-zero
            ([5], 5, True),  # Single element equal to target
            ([5], 6, False),  # Single element not equal to target
        ]

    def test_backtracking(self):
        """Test the backtracking implementation."""
        for nums, target, expected in self.test_cases:
            with self.subTest(nums=nums, target=target):
                result = subset_sum_backtracking(nums, target)
                self.assertEqual(result, expected, 
                    f"Backtracking failed for nums={nums}, target={target}")

    def test_dynamic_programming(self):
        """Test the dynamic programming implementation."""
        for nums, target, expected in self.test_cases:
            with self.subTest(nums=nums, target=target):
                result = subset_sum_dynamic(nums, target)
                self.assertEqual(result, expected,
                    f"Dynamic Programming failed for nums={nums}, target={target}")

    def test_exhaustive(self):
        """Test the exhaustive implementation."""
        for nums, target, expected in self.test_cases:
            with self.subTest(nums=nums, target=target):
                result = subset_sum_exhaustive(nums, target)
                self.assertEqual(result, expected,
                    f"Exhaustive Search failed for nums={nums}, target={target}")

    def test_large_input_dp(self):
        """Test dynamic programming with larger inputs."""
        # Create a test case where the answer is known
        nums = list(range(1, 101))  # 1 to 100
        target = 5050  # Sum of 1 to 100
        self.assertTrue(subset_sum_dynamic(nums, target))
        
        # Test with a slightly different target (impossible)
        self.assertFalse(subset_sum_dynamic(nums, target + 1))


if __name__ == '__main__':
    unittest.main() 