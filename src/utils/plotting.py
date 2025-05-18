"""
Plotting Utilities Module

This module provides functions for visualizing algorithm performance.
"""
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Optional, Tuple

from .timer import get_system_info


def plot_execution_times(sizes: List[int], times: List[float], 
                       title: str, label: str, output_file: str,
                       expected_complexity: str = None,
                       log_scale: bool = False) -> None:
    """
    Plot algorithm execution times.
    
    Args:
        sizes: List of input sizes
        times: List of execution times
        title: Plot title
        label: Label for the data series
        output_file: Output file path
        expected_complexity: Expected complexity (e.g., "O(n²)")
        log_scale: Whether to use logarithmic scale for the y-axis
    """
    plt.figure(figsize=(12, 8))  # Larger figure for better visibility
    
    # Create main plot with actual times
    plt.plot(sizes, times, 'o-', label=f"Actual {label} Time", linewidth=2, markersize=8)
    
    # Add data point annotations for clarity
    for i, (size, time) in enumerate(zip(sizes, times)):
        plt.annotate(f"{size}: {format_numeric(time)}s", 
                    (size, time),
                    textcoords="offset points", 
                    xytext=(0, 10), 
                    ha='center',
                    fontsize=8)
    
    # Add empirical trend line
    if len(sizes) > 2:
        log_sizes = np.log(sizes)
        log_times = np.log(times)
        valid_indices = np.isfinite(log_times)
        
        if sum(valid_indices) > 1:
            coef = np.polyfit(np.array(log_sizes)[valid_indices], 
                             np.array(log_times)[valid_indices], 1)
            fit_times = np.exp(coef[1]) * np.array(sizes) ** coef[0]
            
            fit_label = f'Empirical Fit: O(n^{coef[0]:.2f})'
            plt.plot(sizes, fit_times, '--', label=fit_label, color='orange', linewidth=2)
    
    # Add theoretical complexity curve
    if expected_complexity:
        max_time = max(times)
        min_time = min(times)
        min_size = min(sizes)
        
        # Generate theoretical curve based on the expected complexity
        x_dense = np.linspace(min(sizes), max(sizes), 200)  # More points for smoother curve
        
        if expected_complexity == "O(n²)":
            # Scale the curve to match approximate magnitude of actual data
            scale_factor = min_time / (min_size ** 2)
            theo_times = [scale_factor * (x ** 2) for x in x_dense]
            plt.plot(x_dense, theo_times, ':', label=f"Theoretical: {expected_complexity}", color='green', linewidth=2.5)
            
        elif expected_complexity == "O(n*target)" or expected_complexity == "O(n*T)":
            # For DP, we estimate target as proportional to n for display purposes
            scale_factor = min_time / (min_size ** 2)  # n*target where target ~ n
            theo_times = [scale_factor * (x ** 2) for x in x_dense]
            plt.plot(x_dense, theo_times, ':', label=f"Theoretical: {expected_complexity}", color='green', linewidth=2.5)
            
        elif expected_complexity == "O(2^n)":
            # For exponential algorithms, using log scale is critical
            # Adjust scale to match around the middle of the data range
            mid_idx = len(sizes) // 2
            mid_size = sizes[mid_idx]
            mid_time = times[mid_idx]
            scale_factor = mid_time / (2 ** mid_size)
            
            # Limit the max theoretical time to avoid overflow
            theo_times = []
            for x in x_dense:
                if x <= 40:  # Prevent overflow for large values
                    theo_times.append(scale_factor * (2 ** x))
                else:
                    # Extrapolate from last valid point
                    theo_times.append(theo_times[-1] * 2)
            
            plt.plot(x_dense[:len(theo_times)], theo_times, ':', label=f"Theoretical: {expected_complexity}", color='green', linewidth=2.5)
            
            # Force log scale for exponential algorithms
            log_scale = True
            
        else:
            # Generic case for other complexities
            scale_factor = min_time
            theo_times = [scale_factor for x in x_dense]  # Default to constant
            plt.plot(x_dense, theo_times, ':', label=f"Theoretical: {expected_complexity}", color='green', linewidth=2.5)
    
    plt.xlabel('Input Size (n)', fontsize=12)
    plt.ylabel('Execution Time (seconds)', fontsize=12)
    plt.title(title, fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    
    # Use tight layout for better use of space
    plt.tight_layout()
    
    # Improve legend
    plt.legend(fontsize=11, loc='best', framealpha=0.7)
    
    if log_scale:
        plt.yscale('log')
        plt.title(f"{title} (Log Scale)", fontsize=14, fontweight='bold')
    
    # Add hardware info
    system_info = get_system_info()
    plt.figtext(0.02, 0.02, 
               f"Hardware: {system_info['cpu']} | RAM: {system_info['ram']} | OS: {system_info['os']}", 
               fontsize=9)
    
    # Add timestamp
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    plt.figtext(0.78, 0.02, f"Generated: {timestamp}", fontsize=8)
    
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()


def format_numeric(value):
    """Format a numeric value for display, handling very small and large numbers appropriately."""
    if value < 0.001:
        return f"{value:.2e}"
    elif value < 0.01:
        return f"{value:.5f}"
    elif value < 1:
        return f"{value:.4f}"
    elif value < 10:
        return f"{value:.3f}"
    else:
        return f"{value:.2f}"


def plot_algorithm_comparison(
        np_sizes: List[int], np_times: List[float],
        p_sizes: List[int], p_times: List[float],
        output_file: str = "results/algorithm_comparison.png") -> None:
    """
    Plot comparison between NP-complete and P algorithm performance.
    
    Args:
        np_sizes: Input sizes for the NP-complete algorithm
        np_times: Execution times for the NP-complete algorithm
        p_sizes: Input sizes for the P algorithm
        p_times: Execution times for the P algorithm
        output_file: Output file path
    """
    plt.figure(figsize=(14, 10))
    
    # Plot NP-complete algorithm
    plt.plot(np_sizes, np_times, 'ro-', 
            label='Subset Sum (NP-complete)', linewidth=3, markersize=8)
    
    # Plot P algorithm
    plt.plot(p_sizes, p_times, 'bo-', 
            label='Shortest Path (P)', linewidth=3, markersize=8)
    
    # Add annotations for largest size tested
    last_np_size = np_sizes[-1]
    last_np_time = np_times[-1]
    plt.annotate(f"n={last_np_size}: {format_numeric(last_np_time)}s", 
                (last_np_size, last_np_time),
                textcoords="offset points", 
                xytext=(5, 10), 
                ha='left',
                fontsize=10)
    
    last_p_size = p_sizes[-1]
    last_p_time = p_times[-1]
    plt.annotate(f"n={last_p_size}: {format_numeric(last_p_time)}s", 
                (last_p_size, last_p_time),
                textcoords="offset points", 
                xytext=(5, 10), 
                ha='left',
                fontsize=10)
                
    # Add trend lines and theoretical curves
    if len(np_sizes) > 2:
        # For NP algorithm (exponential fit)
        log_np_sizes = np.log(np_sizes)
        log_np_times = np.log(np_times)
        valid_np = np.isfinite(log_np_times)
        
        if sum(valid_np) > 1:
            np_coef = np.polyfit(np.array(log_np_sizes)[valid_np], 
                               np.array(log_np_times)[valid_np], 1)
            np_fit = np.exp(np_coef[1]) * np.array(np_sizes) ** np_coef[0]
            plt.plot(np_sizes, np_fit, 'r--', 
                    label=f'NP Empirical Fit: O(n^{np_coef[0]:.2f})', linewidth=2)
            
            # Add theoretical exponential curve
            x_dense = np.linspace(min(np_sizes), max(np_sizes), 200)
            mid_idx = len(np_sizes) // 2
            mid_size = np_sizes[mid_idx] 
            mid_time = np_times[mid_idx]
            scale_factor = mid_time / (2 ** mid_size)
            
            theo_times = []
            for x in x_dense:
                if x <= 40:  # Prevent overflow
                    theo_times.append(scale_factor * (2 ** x))
                else:
                    # Extrapolate from last valid point
                    theo_times.append(theo_times[-1] * 2)
            
            plt.plot(x_dense[:len(theo_times)], theo_times, ':r', 
                   label='Theoretical: O(2^n)', linewidth=2.5)
    
    if len(p_sizes) > 2:
        # For P algorithm (polynomial fit)
        log_p_sizes = np.log(p_sizes)
        log_p_times = np.log(p_times)
        valid_p = np.isfinite(log_p_times)
        
        if sum(valid_p) > 1:
            p_coef = np.polyfit(np.array(log_p_sizes)[valid_p], 
                              np.array(log_p_times)[valid_p], 1)
            p_fit = np.exp(p_coef[1]) * np.array(p_sizes) ** p_coef[0]
            plt.plot(p_sizes, p_fit, 'b--', 
                   label=f'P Empirical Fit: O(n^{p_coef[0]:.2f})', linewidth=2)
            
            # Add theoretical polynomial curve
            x_dense = np.linspace(min(p_sizes), max(p_sizes), 200)
            min_size = min(p_sizes)
            min_time = min(p_times)
            scale_factor = min_time / (min_size ** 2)
            
            theo_times = [scale_factor * (x ** 2) for x in x_dense]
            plt.plot(x_dense, theo_times, ':b', 
                   label='Theoretical: O(n²)', linewidth=2.5)
    
    plt.xlabel('Input Size (n)', fontsize=14)
    plt.ylabel('Execution Time (seconds)', fontsize=14)
    plt.title('Performance Comparison: NP-complete vs P Algorithms (Log Scale)', fontsize=16, fontweight='bold')
    plt.legend(fontsize=12, loc='best')
    plt.grid(True, alpha=0.3)
    
    # Use logarithmic scale for y-axis to better visualize the difference
    plt.yscale('log')
    
    # Add hardware info
    system_info = get_system_info()
    plt.figtext(0.02, 0.02, 
               f"Hardware: {system_info['cpu']} | RAM: {system_info['ram']} | OS: {system_info['os']}", 
               fontsize=9)
    
    # Add timestamp
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    plt.figtext(0.78, 0.02, f"Generated: {timestamp}", fontsize=8)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close() 