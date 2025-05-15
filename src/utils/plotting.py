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
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, times, 'o-', label=label, linewidth=2)
    
    # Add trend line
    if len(sizes) > 2:
        log_sizes = np.log(sizes)
        log_times = np.log(times)
        valid_indices = np.isfinite(log_times)
        
        if sum(valid_indices) > 1:
            coef = np.polyfit(np.array(log_sizes)[valid_indices], 
                             np.array(log_times)[valid_indices], 1)
            fit_times = np.exp(coef[1]) * np.array(sizes) ** coef[0]
            
            fit_label = f'Growth Rate: O(n^{coef[0]:.2f})'
            if expected_complexity:
                fit_label += f' (Expected: {expected_complexity})'
                
            plt.plot(sizes, fit_times, '--', label=fit_label)
    
    plt.xlabel('Input Size (n)')
    plt.ylabel('Execution Time (seconds)')
    plt.title(title)
    plt.grid(True)
    plt.legend()
    
    if log_scale:
        plt.yscale('log')
    
    # Add hardware info
    system_info = get_system_info()
    plt.figtext(0.02, 0.02, 
               f"Hardware: {system_info['cpu']} | RAM: {system_info['ram']} | OS: {system_info['os']}", 
               fontsize=8)
    
    plt.savefig(output_file, dpi=300)
    plt.close()


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
    plt.figure(figsize=(12, 8))
    
    # Plot NP-complete algorithm
    plt.plot(np_sizes, np_times, 'ro-', 
            label='Subset Sum (NP-complete)', linewidth=2)
    
    # Plot P algorithm
    plt.plot(p_sizes, p_times, 'bo-', 
            label='Shortest Path (P)', linewidth=2)
    
    # Add trend lines
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
                    label=f'NP Fit: O(2^n) ≈ O(n^{np_coef[0]:.2f})')
    
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
                   label=f'P Fit: O(n^{p_coef[0]:.2f})')
    
    plt.xlabel('Input Size (n)')
    plt.ylabel('Execution Time (seconds)')
    plt.title('Performance Comparison: NP-complete vs P Algorithms')
    plt.legend()
    plt.grid(True)
    
    # Use logarithmic scale for y-axis to better visualize the difference
    plt.yscale('log')
    
    # Add hardware info
    system_info = get_system_info()
    plt.figtext(0.02, 0.02, 
               f"Hardware: {system_info['cpu']} | RAM: {system_info['ram']} | OS: {system_info['os']}", 
               fontsize=8)
    
    plt.savefig(output_file, dpi=300)
    plt.close() 