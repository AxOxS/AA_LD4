"""
Timer Utilities Module

This module provides timing utilities for algorithm benchmarking.
"""
import time
from typing import Any, Callable, List, Tuple
import platform
import psutil


def time_function(func: Callable, *args, **kwargs) -> Tuple[Any, float]:
    """
    Measure the execution time of a function.
    
    Args:
        func: The function to time
        *args: Arguments to pass to the function
        **kwargs: Keyword arguments to pass to the function
        
    Returns:
        Tuple of (function result, execution time in seconds)
    """
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    
    return result, end_time - start_time


def get_system_info() -> dict:
    """
    Get system hardware information for benchmarking context.
    
    Returns:
        Dictionary with CPU, RAM, and OS information
    """
    try:
        cpu_info = platform.processor() or "Unknown CPU"
        ram_gb = round(psutil.virtual_memory().total / (1024**3), 2)
        os_info = f"{platform.system()} {platform.release()}"
        
        return {
            "cpu": cpu_info,
            "ram": f"{ram_gb}GB",
            "os": os_info
        }
    except Exception:
        return {
            "cpu": "Error getting CPU info",
            "ram": "Error getting RAM info",
            "os": f"{platform.system()} {platform.release()}"
        }


def format_time(seconds: float) -> str:
    """
    Format a time duration in a human-readable format.
    
    Args:
        seconds: Time in seconds
        
    Returns:
        Formatted time string
    """
    if seconds < 0.001:
        return f"{seconds * 1_000_000:.2f} μs"
    elif seconds < 1:
        return f"{seconds * 1_000:.2f} ms"
    elif seconds < 60:
        return f"{seconds:.4f} s"
    elif seconds < 3600:
        return f"{seconds / 60:.2f} min"
    else:
        return f"{seconds / 3600:.2f} hours" 