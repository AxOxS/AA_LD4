import unittest
import sys
import os

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.algorithms.shortest_path import dijkstra_shortest_path


class TestShortestPath(unittest.TestCase):
    """Test cases for Dijkstra's Shortest Path algorithm."""

    def test_simple_graph(self):
        """Test with a simple graph."""
        graph = {
            0: [(1, 4), (2, 1)],
            1: [(3, 1)],
            2: [(1, 2), (3, 5)],
            3: []
        }
        result = dijkstra_shortest_path(graph, 0)
        expected = {0: 0, 1: 3, 2: 1, 3: 4}
        self.assertEqual(result, expected)

    def test_disconnected_graph(self):
        """Test with a disconnected graph."""
        graph = {
            0: [(1, 1)],
            1: [(0, 1)],
            2: [(3, 1)],
            3: [(2, 1)]
        }
        result = dijkstra_shortest_path(graph, 0)
        expected = {0: 0, 1: 1, 2: float('infinity'), 3: float('infinity')}
        self.assertEqual(result, expected)

    def test_cycle_graph(self):
        """Test with a graph containing cycles."""
        graph = {
            0: [(1, 1), (2, 4)],
            1: [(2, 2), (3, 6)],
            2: [(3, 3)],
            3: [(0, 7)]
        }
        result = dijkstra_shortest_path(graph, 0)
        expected = {0: 0, 1: 1, 2: 3, 3: 6}
        self.assertEqual(result, expected)

    def test_negative_weights(self):
        """Test with negative weights (not handled by Dijkstra's algorithm)."""
        # Dijkstra's algorithm doesn't handle negative weights correctly
        # This test is to verify this behavior
        graph = {
            0: [(1, 4), (2, 1)],
            1: [(3, -5)],  # Negative weight
            2: [(1, 2), (3, 5)],
            3: []
        }
        result = dijkstra_shortest_path(graph, 0)
        
        # Since Dijkstra doesn't handle negative weights, 
        # the result will be incorrect (but deterministic)
        expected = {0: 0, 1: 3, 2: 1, 3: -2}
        
        self.assertEqual(result, expected, 
            "Dijkstra's algorithm doesn't handle negative weights correctly, " +
            "but should produce a deterministic (if incorrect) result")

    def test_large_graph(self):
        """Test with a larger graph."""
        # Create a simple grid graph
        size = 10
        graph = {}
        
        # Create a grid with connections to adjacent cells
        for i in range(size * size):
            graph[i] = []
            row, col = i // size, i % size
            
            # Connect to right neighbor
            if col < size - 1:
                graph[i].append((i + 1, 1))
                
            # Connect to bottom neighbor
            if row < size - 1:
                graph[i].append((i + size, 1))
        
        result = dijkstra_shortest_path(graph, 0)
        
        # Check a few key distances
        self.assertEqual(result[0], 0)  # Distance to start
        self.assertEqual(result[size-1], size-1)  # Distance to top-right
        self.assertEqual(result[size*(size-1)], size-1)  # Distance to bottom-left
        self.assertEqual(result[size*size-1], 2*(size-1))  # Distance to bottom-right


if __name__ == '__main__':
    unittest.main() 