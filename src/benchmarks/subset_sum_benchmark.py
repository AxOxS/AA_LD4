"""
Subset Sum Benchmark Module

This module provides benchmarking tools for measuring the performance
of different Subset Sum algorithm implementations.
"""
import random
from typing import List, Tuple
import os

from src.algorithms.subset_sum import (
    subset_sum_backtracking,
    subset_sum_dynamic,
    subset_sum_exhaustive
)
from src.utils.timer import time_function, format_time, get_system_info
from src.utils.plotting import plot_execution_times
from src.utils.graph_utils import create_hard_subset_sum_instance


def verify_subset_sum_algorithms():
    """Verify that all subset sum algorithm implementations work correctly."""
    test_cases = [
        ([1, 2, 3, 4], 7, True),
        ([1, 2, 3, 4], 11, False),
        ([3, 34, 4, 12, 5, 2], 9, True),
        ([3, 34, 4, 12, 5, 2], 35, False),
        # Additional test cases
        ([i for i in range(1, 11)], 30, True),  # 1+2+3+4+5+6+9=30
        ([i for i in range(1, 11)], 60, False)  # Sum of all elements is 55 < 60
    ]
    
    algorithms = [
        ("Backtracking", subset_sum_backtracking),
        ("Dynamic Programming", subset_sum_dynamic),
        ("Exhaustive Search", subset_sum_exhaustive)
    ]
    
    print("=== Verifying Subset Sum Algorithm Implementations ===")
    
    for nums, target, expected in test_cases:
        print(f"\nInput: {nums}, Target: {target}")
        
        for name, algorithm in algorithms:
            result = algorithm(nums, target)
            status = "✓" if result == expected else "✗"
            print(f"{name}: {result} (Expected: {expected}) {status}")


def benchmark_backtracking(sizes: List[int] = None, num_trials: int = 10) -> Tuple[List[int], List[float]]:
    """
    Benchmark the backtracking Subset Sum algorithm.
    
    Args:
        sizes: List of input sizes to test (defaults to [10, 15, 20, 25, 30])
        num_trials: Number of trials to run for each size for better accuracy (default: 10)
        
    Returns:
        Tuple of (sizes, average execution times)
    """
    if sizes is None:
        sizes = [10, 15, 20, 22, 24, 26, 28, 30]
    
    times = []
    
    print("\n=== Benchmarking Subset Sum (Backtracking) ===")
    print("This will demonstrate the exponential growth in execution time.")
    print(f"Running {num_trials} trials for each input size for better consistency...")
    
    # Fixed random seed for reproducibility
    random.seed(42)
    
    for size in sizes:
        print(f"\nTesting size {size}...")
        total_time = 0
        
        # Generate a hard problem instance for this size
        nums = []
        for i in range(size):
            # Generate numbers that are close to each other to make the subset sum harder
            nums.append(1000 + random.randint(-5, 5))
        
        # Set target to half the sum to maximize search space
        total_sum = sum(nums)
        target = total_sum // 2
        
        print(f"  Using fixed input: {nums}")
        print(f"  Target: {target}")
        
        for trial in range(num_trials):
            print(f"  Trial {trial+1}/{num_trials}: ", end="", flush=True)
            result, execution_time = time_function(subset_sum_backtracking, nums, target)
            total_time += execution_time
            print(f"Time: {format_time(execution_time)} (Result: {result})")
        
        avg_time = total_time / num_trials
        times.append(avg_time)
        print(f"  Size {size} → Average: {format_time(avg_time)}")
    
    return sizes, times


def benchmark_dynamic_programming(sizes: List[int] = None, num_trials: int = 10) -> Tuple[List[int], List[float]]:
    """
    Benchmark the dynamic programming Subset Sum algorithm.
    
    Args:
        sizes: List of input sizes to test (defaults to [5, 10, 20, ..., 1000])
        num_trials: Number of trials to run for each size for better accuracy (default: 10)
        
    Returns:
        Tuple of (sizes, average execution times)
    """
    if sizes is None:
        sizes = [5, 10, 20, 50, 100, 200, 500, 1000]
    
    times = []
    
    print("\n=== Benchmarking Subset Sum (Dynamic Programming) ===")
    print("This will demonstrate the pseudo-polynomial growth in execution time.")
    print(f"Running {num_trials} trials for each input size for better consistency...")
    
    # Fixed random seed for reproducibility
    random.seed(42)
    
    for size in sizes:
        print(f"\nTesting size {size}...")
        total_time = 0
        
        # Generate a consistent test case for this size
        nums = []
        for i in range(size):
            # Generate numbers that cover a good range
            nums.append(random.randint(1, 1000))
        
        # Set target to a value that will require full DP table computation
        target = sum(nums) // 3
        
        print(f"  Using fixed input of size {size}")
        print(f"  Target: {target}")
        
        for trial in range(num_trials):
            print(f"  Trial {trial+1}/{num_trials}: ", end="", flush=True)
            result, execution_time = time_function(subset_sum_dynamic, nums, target)
            total_time += execution_time
            print(f"Time: {format_time(execution_time)} (Result: {result})")
        
        avg_time = total_time / num_trials
        times.append(avg_time)
        print(f"  Size {size} → Average: {format_time(avg_time)}")
    
    return sizes, times


def benchmark_worst_case(sizes: List[int] = None, num_trials: int = 5) -> Tuple[List[int], List[float]]:
    """
    Benchmark the exhaustive search Subset Sum algorithm on worst-case instances.
    
    Args:
        sizes: List of input sizes to test (defaults to [10, 12, 15, 18, 20, 21, 22, 23])
        num_trials: Number of trials to run for each size for better accuracy
        
    Returns:
        Tuple of (sizes, execution times)
    """
    if sizes is None:
        sizes = [10, 12, 15, 18, 20, 21, 22, 23]
    
    results = []
    
    print("\n=== Benchmarking Subset Sum (Worst Case) ===")
    print("This will demonstrate the true exponential nature of the problem.")
    print(f"Running {num_trials} trials for each input size for better consistency...")
    print("NOTE: This may take several minutes for larger inputs.\n")
    
    # Use fixed seed for reproducibility
    random.seed(42)
    
    for size in sizes:
        print(f"Testing size {size}...")
        
        # Create a hard instance for this size
        nums, target = create_hard_subset_sum_instance(size)
        
        print(f"  Input array: {nums}")
        print(f"  Target (impossible): {target}")
        
        total_time = 0
        
        for trial in range(num_trials):
            print(f"  Trial {trial+1}/{num_trials}: ", end="", flush=True)
            result, execution_time = time_function(subset_sum_exhaustive, nums, target)
            total_time += execution_time
            print(f"Time: {format_time(execution_time)} (Result: {result})")
            
            # Stop early if a single trial takes more than 2 minutes
            if execution_time > 120:
                print(f"  Stopping trials for size {size} as execution time exceeded 2 minutes")
                break
        
        avg_time = total_time / (trial + 1)  # Average over completed trials
        print(f"  Size {size} → Average: {format_time(avg_time)}")
        
        results.append((size, avg_time))
        
        # Stop if the average execution time exceeds 5 minutes
        if avg_time > 300:
            print("  Stopping as average execution time exceeded 5 minutes")
            break
    
    actual_sizes, times = zip(*results)
    return actual_sizes, times


def run_all_benchmarks():
    """Run all Subset Sum algorithm benchmarks and create plots."""
    # Create results directory if it doesn't exist
    os.makedirs("results", exist_ok=True)
    
    # First verify all algorithms work correctly
    verify_subset_sum_algorithms()
    
    # Benchmark the backtracking algorithm
    bt_sizes, bt_times = benchmark_backtracking()
    plot_execution_times(
        bt_sizes, bt_times,
        "Subset Sum (Backtracking) - Execution Time vs Input Size",
        "Backtracking", "results/subset_sum_backtracking.png",
        expected_complexity="O(2^n)"
    )
    
    # Benchmark the dynamic programming algorithm
    dp_sizes, dp_times = benchmark_dynamic_programming()
    plot_execution_times(
        dp_sizes, dp_times,
        "Subset Sum (Dynamic Programming) - Execution Time vs Input Size",
        "Dynamic Programming", "results/subset_sum_dp.png",
        expected_complexity="O(n*target)"
    )
    
    # Benchmark worst-case scenario
    wc_sizes, wc_times = benchmark_worst_case()
    plot_execution_times(
        wc_sizes, wc_times,
        "Subset Sum (Worst Case) - Execution Time vs Input Size",
        "Exhaustive Search", "results/subset_sum_worst_case.png", 
        expected_complexity="O(2^n)",
        log_scale=True
    )
    
    print("\n=== Benchmark Summary ===")
    system_info = get_system_info()
    print(f"Hardware: {system_info['cpu']}")
    print(f"RAM: {system_info['ram']}")
    print(f"OS: {system_info['os']}")
    
    print("\nLargest problem sizes solved:")
    print(f"- Backtracking: n = {max(bt_sizes)} in {format_time(bt_times[-1])}")
    print(f"- Dynamic Programming: n = {max(dp_sizes)} in {format_time(dp_times[-1])}")
    print(f"- Worst Case (Exhaustive): n = {max(wc_sizes)} in {format_time(wc_times[-1])}")


if __name__ == "__main__":
    run_all_benchmarks() 