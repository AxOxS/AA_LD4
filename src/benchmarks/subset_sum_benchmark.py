"""
Subset Sum Benchmark Module

This module provides benchmarking tools for measuring the performance
of different Subset Sum algorithm implementations.
"""
import random
from typing import List, Tuple
import os
import math

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
        
        # Adaptively reduce trials for extremely large inputs
        actual_trials = num_trials
        if size >= 32:
            actual_trials = min(2, num_trials)
            print(f"  ⚠️ Reducing to {actual_trials} trials for size {size} to avoid excessive runtime")
        elif size >= 30:
            actual_trials = min(3, num_trials) 
            print(f"  ⚠️ Reducing to {actual_trials} trials for size {size} to avoid excessive runtime")
            
        for trial in range(actual_trials):
            print(f"  Trial {trial+1}/{actual_trials}: ", end="", flush=True)
            result, execution_time = time_function(subset_sum_backtracking, nums, target)
            total_time += execution_time
            print(f"Time: {format_time(execution_time)} (Result: {result})")
            
            # Safety cutoff for extremely long-running trials
            if execution_time > 300:  # 5 minutes
                print(f"  ⚠️ Stopping trials for size {size} as execution time exceeded 5 minutes")
                break
        
        avg_time = total_time / (trial + 1)  # Average over completed trials
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
            # For very large sizes, use smaller numbers to prevent excessive memory use
            if size > 800:
                nums.append(random.randint(1, 100))
            else:
                nums.append(random.randint(1, 1000))
        
        # Set target to a value that will require full DP table computation
        # For very large sizes, use a more reasonable target to prevent memory exhaustion
        if size > 800:
            target = sum(nums) // 6
        else:
            target = sum(nums) // 3
        
        print(f"  Using fixed input of size {size}")
        print(f"  Target: {target}")
        
        # Adaptively reduce trials for extremely large inputs
        actual_trials = num_trials
        if size >= 1000:
            actual_trials = 1
            print(f"  ⚠️ Using only 1 trial for size {size} due to expected long runtime and memory usage")
        elif size >= 500:
            actual_trials = min(2, num_trials)
            print(f"  ⚠️ Reducing to {actual_trials} trials for size {size}")
        
        for trial in range(actual_trials):
            print(f"  Trial {trial+1}/{actual_trials}: ", end="", flush=True)
            
            try:
                result, execution_time = time_function(subset_sum_dynamic, nums, target)
                total_time += execution_time
                print(f"Time: {format_time(execution_time)} (Result: {result})")
                
                # Stop early if a single trial takes more than 5 minutes
                if execution_time > 300:
                    print(f"  ⚠️ Stopping trials for size {size} as execution time exceeded 5 minutes")
                    break
            except MemoryError:
                print(f"❌ Memory error for size {size}. Consider reducing size or target.")
                if trial == 0:
                    # Skip this size if we can't even complete one trial
                    total_time = float('nan')
                break
        
        if not math.isnan(total_time):
            avg_time = total_time / (trial + 1)  # Average over completed trials
            times.append(avg_time)
            print(f"  Size {size} → Average: {format_time(avg_time)}")
        else:
            # Skip this size in results
            print(f"  Size {size} → Skipped due to memory constraints")
    
    # Filter out any sizes that were skipped
    completed_sizes = sizes[:len(times)]
    return completed_sizes, times


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
        
        # Adaptively reduce trials for extremely large inputs
        actual_trials = num_trials
        if size >= 24:
            actual_trials = 1
            print(f"  ⚠️ Using only 1 trial for size {size} due to expected long runtime")
        
        total_time = 0
        
        for trial in range(actual_trials):
            print(f"  Trial {trial+1}/{actual_trials}: ", end="", flush=True)
            result, execution_time = time_function(subset_sum_exhaustive, nums, target)
            total_time += execution_time
            print(f"Time: {format_time(execution_time)} (Result: {result})")
            
            # Stop early if a single trial takes more than 10 minutes
            if execution_time > 600:
                print(f"  ⚠️ Stopping trials for size {size} as execution time exceeded 10 minutes")
                break
        
        avg_time = total_time / (trial + 1)  # Average over completed trials
        print(f"  Size {size} → Average: {format_time(avg_time)}")
        
        results.append((size, avg_time))
        
        # Stop if the average execution time exceeds 15 minutes
        if avg_time > 900:
            print(f"  ⚠️ Stopping benchmark as average execution time exceeded 15 minutes")
            break
    
    actual_sizes, times = zip(*results)
    return actual_sizes, times


def run_all_benchmarks():
    """Run all Subset Sum algorithm benchmarks and create plots."""
    # Create results directory if it doesn't exist
    os.makedirs("results", exist_ok=True)
    
    print("\n🔥 EXTREME BENCHMARK MODE - CORE ULTRA 9 🔥")
    
    # First verify all algorithms work correctly
    verify_subset_sum_algorithms()
    
    # Benchmark the backtracking algorithm with extended range
    print("\nRunning backtracking with extreme input sizes...")
    bt_sizes = [5, 10, 15, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42]
    bt_sizes, bt_times = benchmark_backtracking(bt_sizes, num_trials=2)
    plot_execution_times(
        bt_sizes, bt_times,
        "Subset Sum (Backtracking) - Execution Time vs Input Size",
        "Backtracking", "results/subset_sum_backtracking.png",
        expected_complexity="O(2^n)",
        log_scale=True  # Always use log scale for exponential algorithms
    )
    
    # Benchmark the dynamic programming algorithm with extended range
    print("\nRunning dynamic programming with extreme input sizes...")
    dp_sizes = [5, 10, 20, 50, 100, 200, 500, 1000, 1500, 2000]
    dp_sizes, dp_times = benchmark_dynamic_programming(dp_sizes, num_trials=1)
    plot_execution_times(
        dp_sizes, dp_times,
        "Subset Sum (Dynamic Programming) - Execution Time vs Input Size",
        "Dynamic Programming", "results/subset_sum_dp.png",
        expected_complexity="O(n*target)"
    )
    
    # Benchmark worst-case scenario with extended range
    print("\nRunning worst case with extreme input sizes...")
    wc_sizes = [10, 15, 18, 20, 22, 23, 24, 25, 26, 27]
    wc_sizes, wc_times = benchmark_worst_case(wc_sizes, num_trials=1)
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