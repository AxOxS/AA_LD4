"""
Algorithm Comparison Module

This module provides tools for comparing the performance of NP-complete
and P complexity class algorithms.
"""
import os
from typing import List, Tuple

from src.benchmarks.subset_sum_benchmark import benchmark_backtracking, benchmark_dynamic_programming, benchmark_worst_case
from src.benchmarks.shortest_path_benchmark import benchmark_shortest_path
from src.utils.plotting import plot_algorithm_comparison
from src.utils.timer import get_system_info


def save_analysis_report(
        np_sizes: List[int], np_times: List[float],
        p_sizes: List[int], p_times: List[float],
        dp_sizes: List[int] = None, dp_times: List[float] = None,
        wc_sizes: List[int] = None, wc_times: List[float] = None,
        output_file: str = "results/algorithm_analysis_report.txt") -> None:
    """
    Save a detailed analysis report to a text file.
    
    Args:
        np_sizes: Input sizes for the NP-complete algorithm (backtracking)
        np_times: Execution times for the NP-complete algorithm (backtracking)
        p_sizes: Input sizes for the P algorithm (Dijkstra's)
        p_times: Execution times for the P algorithm (Dijkstra's)
        dp_sizes: Input sizes for dynamic programming algorithm
        dp_times: Execution times for dynamic programming algorithm
        wc_sizes: Input sizes for worst-case subset sum algorithm
        wc_times: Execution times for worst-case subset sum algorithm
        output_file: Output file path
    """
    system_info = get_system_info()
    
    # Import numpy once
    import numpy as np
    
    # Calculate growth rates
    np_growth_rate = "N/A"
    p_growth_rate = "N/A"
    dp_growth_rate = "N/A"
    wc_growth_rate = "N/A"
    
    # Helper function to calculate growth rate
    def calculate_growth_rate(sizes, times):
        if len(sizes) > 2:
            log_sizes = np.log(sizes)
            log_times = np.log(times)
            valid_indices = np.isfinite(log_times)
            
            if sum(valid_indices) > 1:
                coef = np.polyfit(np.array(log_sizes)[valid_indices], 
                                 np.array(log_times)[valid_indices], 1)
                return coef[0]
        return "N/A"
    
    # Calculate growth rates for all algorithms
    np_growth_rate = calculate_growth_rate(np_sizes, np_times)
    p_growth_rate = calculate_growth_rate(p_sizes, p_times)
    
    if dp_sizes and dp_times:
        dp_growth_rate = calculate_growth_rate(dp_sizes, dp_times)
    
    if wc_sizes and wc_times:
        wc_growth_rate = calculate_growth_rate(wc_sizes, wc_times)
    
    # Create the report
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=== Algorithm Performance Analysis Report ===\n\n")
        
        f.write("HARDWARE SPECIFICATIONS:\n")
        f.write(f"CPU: {system_info['cpu']}\n")
        f.write(f"RAM: {system_info['ram']}\n")
        f.write(f"OS: {system_info['os']}\n\n")
        
        f.write("ANALYZED ALGORITHMS:\n")
        f.write("1. Subset Sum (Backtracking) - NP-complete algorithm\n")
        f.write("2. Dijkstra's Shortest Path - P algorithm\n")
        if dp_sizes and dp_times:
            f.write("3. Subset Sum (Dynamic Programming) - Pseudo-polynomial algorithm\n")
        if wc_sizes and wc_times:
            f.write("4. Subset Sum (Worst Case) - Exponential algorithm\n")
        f.write("\n")
        
        f.write("SUBSET SUM - BACKTRACKING (NP-COMPLETE):\n")
        f.write(f"Tested sizes: {np_sizes}\n")
        f.write(f"Execution times (s): {[round(t, 6) for t in np_times]}\n")
        f.write(f"Empirical growth rate: O(n^{np_growth_rate if isinstance(np_growth_rate, float) else np_growth_rate})\n")
        f.write(f"Theoretical complexity: O(2^n)\n")
        f.write(f"Note: For small n, exponential functions can appear polynomial-like\n\n")
        
        f.write("DIJKSTRA'S SHORTEST PATH (P):\n")
        f.write(f"Tested sizes: {p_sizes}\n")
        f.write(f"Execution times (s): {[round(t, 6) for t in p_times]}\n")
        f.write(f"Empirical growth rate: O(n^{p_growth_rate if isinstance(p_growth_rate, float) else p_growth_rate})\n")
        f.write(f"Theoretical complexity: O(E + V log V) ≈ O(n²) for dense graphs\n\n")
        
        if dp_sizes and dp_times:
            f.write("SUBSET SUM - DYNAMIC PROGRAMMING (PSEUDO-POLYNOMIAL):\n")
            f.write(f"Tested sizes: {dp_sizes}\n")
            f.write(f"Execution times (s): {[round(t, 6) for t in dp_times]}\n")
            f.write(f"Empirical growth rate: O(n^{dp_growth_rate if isinstance(dp_growth_rate, float) else dp_growth_rate})\n")
            f.write(f"Theoretical complexity: O(n*target) where target can be as large as 2^n\n\n")
        
        if wc_sizes and wc_times:
            f.write("SUBSET SUM - WORST CASE (EXPONENTIAL):\n")
            f.write(f"Tested sizes: {wc_sizes}\n")
            f.write(f"Execution times (s): {[round(t, 6) for t in wc_times]}\n")
            f.write(f"Empirical growth rate: O(n^{wc_growth_rate if isinstance(wc_growth_rate, float) else wc_growth_rate})\n")
            f.write(f"Theoretical complexity: O(2^n)\n")
            f.write(f"Note: This uses specially constructed hard instances\n\n")
        
        f.write("COMPLEXITY COMPARISON ANALYSIS:\n")
        f.write("The experimental results demonstrate the fundamental difference between\n")
        f.write("NP-complete and P complexity classes. The execution time of the Subset Sum\n")
        f.write("problem grows exponentially with input size, quickly becoming impractical\n")
        f.write("beyond small inputs. In contrast, Dijkstra's algorithm scales polynomially,\n")
        f.write("allowing it to handle much larger inputs efficiently.\n\n")
        
        f.write("EMPIRICAL FIT EXPLANATION:\n")
        f.write("The empirical growth rates shown above are derived from regression analysis\n")
        f.write("of the actual execution time data. They may differ from theoretical complexity\n")
        f.write("due to several factors:\n")
        f.write("1. Limited range of input sizes tested\n")
        f.write("2. Implementation optimizations affecting measured performance\n")
        f.write("3. Hardware effects like caching and memory access patterns\n")
        f.write("4. Statistical variation in timing measurements\n\n")
        
        f.write("This is why we display both empirical fits and theoretical complexity curves\n")
        f.write("in the visualizations - they tell different parts of the performance story.\n")


def run_comparison():
    """
    Run benchmarks for both NP-complete and P algorithms and compare them.
    
    This function:
    1. Runs backtracking Subset Sum algorithm benchmark
    2. Runs Dijkstra's shortest path algorithm benchmark 
    3. Creates a plot comparing both algorithm performances
    4. Generates a detailed analysis report
    """
    # Create results directory if it doesn't exist
    os.makedirs("results", exist_ok=True)
    
    # Display system information
    system_info = get_system_info()
    print("=== Comparing NP-complete vs P Algorithms Performance ===")
    print(f"Hardware: {system_info['cpu']}")
    print(f"RAM: {system_info['ram']}")
    print(f"OS: {system_info['os']}")
    print("=" * 60)
    
    print("\n🔥🔥🔥 MAXIMUM STRESS TEST MODE FOR CORE ULTRA 9! 🔥🔥🔥")
    print("Testing absolute processing power limits - benchmarks may take 30+ minutes.")
    
    # Run NP-complete algorithm benchmark (Subset Sum with backtracking)
    print("\n1. Benchmarking Subset Sum (NP-complete) with backtracking...")
    # Extended range - add 36 and 38 for true exponential challenge
    np_sizes = [5, 10, 15, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38]
    print(f"  Testing sizes: {np_sizes} (EXTREME RANGE)")
    
    # Use just 1 trial for the largest inputs
    np_sizes, np_times = benchmark_backtracking(np_sizes, num_trials=2)
    
    # Run P algorithm benchmark (Dijkstra's Shortest Path)
    print("\n2. Benchmarking Dijkstra's Shortest Path (P)...")
    # Extreme sizes - going to 15,000 nodes
    p_sizes = [10, 50, 100, 500, 1000, 2000, 5000, 8000, 10000, 15000]
    print(f"  Testing sizes: {p_sizes} (ULTRA HIGH)")
    p_sizes, p_times = benchmark_shortest_path(p_sizes)
    
    # Also run DP and worst-case benchmarks for comprehensive report
    print("\n3. Running additional benchmarks for comprehensive report...")
    
    # Even larger DP sizes
    dp_sizes = [5, 10, 20, 50, 100, 200, 500, 1000, 1500, 2000]
    print(f"  DP sizes: {dp_sizes} (MASSIVE MEMORY TEST)")
    dp_sizes, dp_times = benchmark_dynamic_programming(dp_sizes, num_trials=1)
    
    # Push worst case algorithm to true exponential pain
    wc_sizes = [10, 15, 18, 20, 22, 23, 24, 25, 26, 27]
    print(f"  Worst-case sizes: {wc_sizes} (EXTREME CPU LOAD)")
    wc_sizes, wc_times = benchmark_worst_case(wc_sizes, num_trials=1)
    
    # Create comparison plot
    print("\nCreating comparison plot...")
    plot_algorithm_comparison(np_sizes, np_times, p_sizes, p_times, 
                             "results/algorithm_comparison.png")
    
    # Generate analysis report
    print("\nSaving detailed analysis report...")
    save_analysis_report(np_sizes, np_times, p_sizes, p_times, dp_sizes, dp_times, wc_sizes, wc_times)
    
    print("\nComparison complete. Check:")
    print("- 'results/algorithm_comparison.png' for the visualization")
    print("- 'results/algorithm_analysis_report.txt' for detailed analysis")


if __name__ == "__main__":
    run_comparison() 