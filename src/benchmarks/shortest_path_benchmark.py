"""
Shortest Path Benchmark Module

This module provides benchmarking tools for measuring the performance
of Dijkstra's Shortest Path algorithm.
"""
import os
from typing import List, Tuple

from src.algorithms.shortest_path import dijkstra_shortest_path
from src.utils.timer import time_function, format_time, get_system_info
from src.utils.plotting import plot_execution_times
from src.utils.graph_utils import generate_random_graph


def verify_shortest_path_algorithm():
    """Verify that the shortest path algorithm works correctly."""
    # Simple test graph
    test_graph = {
        0: [(1, 4), (2, 1)],
        1: [(3, 1)],
        2: [(1, 2), (3, 5)],
        3: []
    }
    
    result = dijkstra_shortest_path(test_graph, 0)
    expected = {0: 0, 1: 3, 2: 1, 3: 4}
    
    print("=== Verifying Dijkstra's Algorithm ===")
    print(f"Test graph: {test_graph}")
    print(f"Shortest paths from vertex 0: {result}")
    print(f"Expected result: {expected}")
    
    if result == expected:
        print("Verification successful: ✓")
    else:
        print("Verification failed: ✗")
        print("Differences:")
        for vertex in expected:
            if vertex not in result or result[vertex] != expected[vertex]:
                print(f"  Vertex {vertex}: Expected {expected[vertex]}, Got {result.get(vertex, 'missing')}")


def benchmark_shortest_path(sizes: List[int] = None, num_trials: int = 3) -> Tuple[List[int], List[float]]:
    """
    Benchmark Dijkstra's Shortest Path algorithm.
    
    Args:
        sizes: List of graph sizes (vertices) to test (defaults to [10, 50, 100, ..., 2000])
        num_trials: Number of trials to run for each size for better accuracy
        
    Returns:
        Tuple of (sizes, average execution times)
    """
    if sizes is None:
        sizes = [10, 50, 100, 200, 500, 1000, 1500, 2000]
    
    times = []
    
    print("\n=== Benchmarking Dijkstra's Shortest Path Algorithm ===")
    print("This will demonstrate the polynomial growth in execution time.")
    
    for size in sizes:
        print(f"\nTesting size {size}...")
        total_time = 0
        
        for trial in range(num_trials):
            # Generate a random graph of the current size
            graph = generate_random_graph(size)
            
            print(f"  Trial {trial+1}/{num_trials}: ", end="", flush=True)
            result, execution_time = time_function(dijkstra_shortest_path, graph, 0)
            total_time += execution_time
            
            # Print just a few distances for brevity
            sample_results = {k: result[k] for k in sorted(result.keys())[:3]}
            print(f"Time: {format_time(execution_time)} (Sample results: {sample_results}...)")
        
        avg_time = total_time / num_trials
        times.append(avg_time)
        print(f"  Size {size} → Average: {format_time(avg_time)}")
    
    return sizes, times


def run_benchmark():
    """Run the Shortest Path algorithm benchmark and create plots."""
    # Create results directory if it doesn't exist
    os.makedirs("results", exist_ok=True)
    
    # First verify algorithm works correctly
    verify_shortest_path_algorithm()
    
    # Benchmark the algorithm
    sizes, times = benchmark_shortest_path()
    
    # Plot results
    plot_execution_times(
        sizes, times,
        "Dijkstra's Shortest Path - Execution Time vs Input Size",
        "Shortest Path", "results/shortest_path.png",
        expected_complexity="O(n²)"
    )
    
    print("\n=== Benchmark Summary ===")
    system_info = get_system_info()
    print(f"Hardware: {system_info['cpu']}")
    print(f"RAM: {system_info['ram']}")
    print(f"OS: {system_info['os']}")
    
    print(f"\nLargest problem size solved: n = {max(sizes)} in {format_time(times[-1])}")
    print(f"Theoretical complexity: O(E + V log V) ≈ O(n²) for dense graphs")


if __name__ == "__main__":
    run_benchmark() 