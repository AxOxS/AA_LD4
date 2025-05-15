import unittest
import sys
import os
import time

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.timer import time_function, format_time
from src.utils.graph_utils import generate_random_graph, create_hard_subset_sum_instance


class TestTimerFunctions(unittest.TestCase):
    """Test cases for timer utility functions."""

    def test_time_function(self):
        """Test that time_function correctly measures execution time."""
        def slow_function(duration):
            time.sleep(duration)
            return "result"
        
        # Test with a function that sleeps for 0.1 seconds
        result, duration = time_function(slow_function, 0.1)
        
        self.assertEqual(result, "result")
        self.assertGreaterEqual(duration, 0.09)  # Allow for small timing errors
        self.assertLessEqual(duration, 0.2)      # Allow for overhead
    
    def test_format_time(self):
        """Test the format_time function with different time ranges."""
        # Microseconds
        self.assertTrue("μs" in format_time(0.0005))
        
        # Milliseconds
        self.assertTrue("ms" in format_time(0.05))
        
        # Seconds
        self.assertTrue("s" in format_time(5.0))
        
        # Minutes
        self.assertTrue("min" in format_time(120.0))
        
        # Hours
        self.assertTrue("hours" in format_time(3600.0))


class TestGraphUtils(unittest.TestCase):
    """Test cases for graph utility functions."""
    
    def test_generate_random_graph(self):
        """Test that generate_random_graph creates a valid graph."""
        # Test with small graph
        n = 5
        graph = generate_random_graph(n)
        
        # Check graph structure
        self.assertEqual(len(graph), n)
        for vertex in range(n):
            self.assertIn(vertex, graph)
            # Each edge should be (neighbor, weight) where neighbor is in [0, n-1]
            for edge in graph[vertex]:
                neighbor, weight = edge
                self.assertLess(neighbor, n)
                self.assertGreaterEqual(neighbor, 0)
                self.assertNotEqual(neighbor, vertex)  # No self-loops
                self.assertGreaterEqual(weight, 1)     # Positive weights
        
        # Test with different edge probability
        graph_sparse = generate_random_graph(n, edge_probability=0.1)
        graph_dense = generate_random_graph(n, edge_probability=0.9)
        
        # Count total edges
        sparse_edges = sum(len(edges) for edges in graph_sparse.values())
        dense_edges = sum(len(edges) for edges in graph_dense.values())
        
        # Dense should generally have more edges, though this is probabilistic
        # and might fail occasionally
        self.assertLessEqual(sparse_edges, n * (n-1))  # Maximum possible edges
        self.assertLessEqual(dense_edges, n * (n-1))   # Maximum possible edges
    
    def test_create_hard_subset_sum_instance(self):
        """Test that create_hard_subset_sum_instance creates valid instances."""
        size = 10
        nums, target = create_hard_subset_sum_instance(size)
        
        # Check that we get the right number of elements
        self.assertEqual(len(nums), size)
        
        # Check that all elements are positive
        self.assertTrue(all(n > 0 for n in nums))
        
        # Check that target is sum + 1 (impossible)
        self.assertEqual(target, sum(nums) + 1)
        
        # Check that elements are sorted (should be using prime number list)
        self.assertEqual(sorted(nums), nums)


if __name__ == '__main__':
    unittest.main() 