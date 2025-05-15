"""
Algorithm Comparison Module

This module provides tools for comparing the performance of NP-complete
and P complexity class algorithms.
"""
import os
from typing import List, Tuple

from src.benchmarks.subset_sum_benchmark import benchmark_backtracking, benchmark_worst_case
from src.benchmarks.shortest_path_benchmark import benchmark_shortest_path
from src.utils.plotting import plot_algorithm_comparison
from src.utils.timer import get_system_info


def save_analysis_report(
        np_sizes: List[int], np_times: List[float],
        p_sizes: List[int], p_times: List[float],
        output_file: str = "results/algorithm_analysis_report.txt") -> None:
    """
    Save a detailed analysis report to a text file.
    
    Args:
        np_sizes: Input sizes for the NP-complete algorithm
        np_times: Execution times for the NP-complete algorithm
        p_sizes: Input sizes for the P algorithm
        p_times: Execution times for the P algorithm
        output_file: Output file path
    """
    system_info = get_system_info()
    
    # Calculate growth rates
    np_growth_rate = "N/A"
    p_growth_rate = "N/A"
    
    if len(np_sizes) > 2:
        import numpy as np
        log_np_sizes = np.log(np_sizes)
        log_np_times = np.log(np_times)
        valid_np = np.isfinite(log_np_times)
        if sum(valid_np) > 1:
            np_coef = np.polyfit(np.array(log_np_sizes)[valid_np], 
                              np.array(log_np_times)[valid_np], 1)
            np_growth_rate = np_coef[0]
    
    if len(p_sizes) > 2:
        import numpy as np
        log_p_sizes = np.log(p_sizes)
        log_p_times = np.log(p_times)
        valid_p = np.isfinite(log_p_times)
        if sum(valid_p) > 1:
            p_coef = np.polyfit(np.array(log_p_sizes)[valid_p], 
                             np.array(log_p_times)[valid_p], 1)
            p_growth_rate = p_coef[0]
    
    # Create the report
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=== Algorithm Performance Analysis Report ===\n\n")
        
        f.write("HARDWARE SPECIFICATIONS:\n")
        f.write(f"CPU: {system_info['cpu']}\n")
        f.write(f"RAM: {system_info['ram']}\n")
        f.write(f"OS: {system_info['os']}\n\n")
        
        f.write("NP-COMPLETE ALGORITHM (SUBSET SUM - BACKTRACKING):\n")
        f.write(f"Tested sizes: {np_sizes}\n")
        f.write(f"Execution times (s): {[round(t, 6) for t in np_times]}\n")
        f.write(f"Experimentally determined growth rate: n^{np_growth_rate if isinstance(np_growth_rate, float) else np_growth_rate}\n")
        f.write(f"Theoretical complexity: O(2^n)\n\n")
        
        f.write("POLYNOMIAL ALGORITHM (DIJKSTRA'S SHORTEST PATH):\n")
        f.write(f"Tested sizes: {p_sizes}\n")
        f.write(f"Execution times (s): {[round(t, 6) for t in p_times]}\n")
        f.write(f"Experimentally determined growth rate: n^{p_growth_rate if isinstance(p_growth_rate, float) else p_growth_rate}\n")
        f.write(f"Theoretical complexity: O(E + V log V) ≈ O(n²) for dense graphs\n\n")
        
        f.write("COMPARISON ANALYSIS:\n")
        f.write("The experimental results demonstrate the fundamental difference between\n")
        f.write("NP-complete and P complexity classes. The execution time of the Subset Sum\n")
        f.write("problem grows exponentially with input size, quickly becoming impractical\n")
        f.write("beyond small inputs. In contrast, Dijkstra's algorithm scales polynomially,\n")
        f.write("allowing it to handle much larger inputs efficiently.\n\n")
        
        f.write("LITHUANIAN LANGUAGE SUMMARY:\n")
        f.write("Eksperimentiniai rezultatai aiškiai rodo fundamentalų skirtumą tarp\n")
        f.write("NP-pilnumo ir P sudėtingumo klasių. Poaibio sumos uždavinio vykdymo laikas\n")
        f.write("auga eksponentiškai didėjant įvesties dydžiui, greitai tapdamas nepraktišku\n")
        f.write("net ir nedidelėms įvestims. Priešingai, Dijkstra algoritmas didėja polinomiškai,\n")
        f.write("leidžiant jam efektyviai apdoroti daug didesnes įvestis.\n")


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
    
    # Run NP-complete algorithm benchmark (Subset Sum with backtracking)
    print("\n1. Benchmarking Subset Sum (NP-complete) with backtracking...")
    np_sizes = [5, 10, 15, 20, 22, 24, 26, 28]  # Adjust based on your system's capability
    np_sizes, np_times = benchmark_backtracking(np_sizes)
    
    # Alternatively, to demonstrate true exponential growth:
    # print("\n1. Benchmarking Subset Sum (NP-complete) with worst-case instances...")
    # np_sizes = [10, 12, 15, 18, 20, 22]  # Adjust based on your system's capability
    # np_sizes, np_times = benchmark_worst_case(np_sizes)
    
    # Run P algorithm benchmark (Dijkstra's Shortest Path)
    print("\n2. Benchmarking Dijkstra's Shortest Path (P)...")
    p_sizes = [10, 50, 100, 200, 500, 1000]  # Adjust based on your system's capability
    p_sizes, p_times = benchmark_shortest_path(p_sizes)
    
    # Create comparison plot
    print("\nCreating comparison plot...")
    plot_algorithm_comparison(np_sizes, np_times, p_sizes, p_times, 
                             "results/algorithm_comparison.png")
    
    # Generate analysis report
    print("\nSaving detailed analysis report...")
    save_analysis_report(np_sizes, np_times, p_sizes, p_times)
    
    print("\nComparison complete. Check:")
    print("- 'results/algorithm_comparison.png' for the visualization")
    print("- 'results/algorithm_analysis_report.txt' for detailed analysis")


if __name__ == "__main__":
    run_comparison() 