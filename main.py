#!/usr/bin/env python3
"""
Algorithm Analysis Project - Main Entry Point

This script serves as the main entry point for the algorithm analysis project.
It provides a simple command-line interface to run different benchmarks
and comparisons between P and NP-complete algorithms.
"""
import argparse
import os
import sys
import importlib.util

from src.benchmarks.subset_sum_benchmark import run_all_benchmarks as run_subset_sum_benchmarks
from src.benchmarks.shortest_path_benchmark import run_benchmark as run_shortest_path_benchmark
from src.benchmarks.compare_algorithms import run_comparison
from src.utils.timer import get_system_info


def print_header():
    """Print a header with system information."""
    system_info = get_system_info()
    print("\n" + "=" * 80)
    print("ALGORITHM ANALYSIS PROJECT: P vs NP-COMPLETE ALGORITHMS")
    print("=" * 80)
    print(f"CPU: {system_info['cpu']}")
    print(f"RAM: {system_info['ram']}")
    print(f"OS: {system_info['os']}")
    print("=" * 80 + "\n")


def setup_directories():
    """Create necessary directories if they don't exist."""
    os.makedirs("results", exist_ok=True)
    os.makedirs("tests", exist_ok=True)


def run_tests():
    """Run all unit tests."""
    test_module_path = os.path.join(os.path.dirname(__file__), "tests", "run_all_tests.py")
    
    if not os.path.exists(test_module_path):
        print(f"Error: Test runner not found at {test_module_path}")
        return False
    
    # Import and run the test module
    spec = importlib.util.spec_from_file_location("run_all_tests", test_module_path)
    test_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(test_module)
    
    return test_module.run_tests()


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Algorithm Analysis Project - P vs NP-complete algorithms",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument(
        "command", nargs="?", default="all",
        choices=["all", "subset_sum", "shortest_path", "compare", "test"],
        help="The command to run:\n"
             "  all: Run all benchmarks\n"
             "  subset_sum: Run Subset Sum (NP-complete) benchmarks\n"
             "  shortest_path: Run Shortest Path (P) benchmarks\n"
             "  compare: Run comparison between both algorithms\n"
             "  test: Run unit tests"
    )
    
    parser.add_argument(
        "--worst-case", action="store_true",
        help="Use worst-case scenarios for Subset Sum (much slower but demonstrates true exponential growth)"
    )
    
    return parser.parse_args()


def main():
    """Main entry point."""
    setup_directories()
    
    args = parse_arguments()
    
    if args.command == "test":
        print("Running unit tests...")
        success = run_tests()
        if not success:
            sys.exit(1)
        return
    
    print_header()
    
    if args.command == "all":
        print("Running all benchmarks...")
        run_subset_sum_benchmarks()
        run_shortest_path_benchmark()
        run_comparison()
    
    elif args.command == "subset_sum":
        print("Running Subset Sum (NP-complete) benchmarks...")
        run_subset_sum_benchmarks()
    
    elif args.command == "shortest_path":
        print("Running Shortest Path (P) benchmarks...")
        run_shortest_path_benchmark()
    
    elif args.command == "compare":
        print("Running comparison between P and NP-complete algorithms...")
        run_comparison()
    
    print("\nAll benchmarks completed successfully.")
    print("Results saved in the 'results' directory.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBenchmark interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1) 