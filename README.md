# Algorithm Analysis Project: P vs NP-Complete

This project demonstrates the difference between polynomial-time (P) and NP-complete algorithms through implementation and empirical analysis.

## Project Overview

The project compares two algorithms:
1. **Subset Sum (NP-complete)**: Given a set of integers, find if there's a subset whose sum equals a target value.
2. **Shortest Path (P)**: Find the shortest path from a source vertex to all other vertices in a weighted graph.

## Project Structure

```
algorithm-analysis/
├── main.py                  # Main entry point script
├── README.md                # Project documentation
├── requirements.txt         # Python dependencies
├── results/                 # Generated benchmark results
│   ├── algorithm_comparison.png
│   ├── algorithm_analysis_report.txt
│   └── ...
├── src/                     # Source code
│   ├── __init__.py
│   ├── algorithms/          # Algorithm implementations
│   │   ├── __init__.py
│   │   ├── subset_sum.py    # Subset Sum implementations
│   │   └── shortest_path.py # Shortest Path implementation
│   ├── benchmarks/          # Benchmarking scripts
│   │   ├── __init__.py
│   │   ├── subset_sum_benchmark.py
│   │   ├── shortest_path_benchmark.py
│   │   └── compare_algorithms.py
│   └── utils/               # Utility functions
│       ├── __init__.py
│       ├── graph_utils.py   # Graph generation utilities
│       ├── plotting.py      # Result visualization
│       └── timer.py         # Time measurement utilities
└── tests/                   # Test scripts
    ├── __init__.py          # Test package initialization
    ├── run_all_tests.py     # Test runner script
    ├── test_subset_sum.py   # Tests for Subset Sum algorithms
    ├── test_shortest_path.py # Tests for Shortest Path algorithm
    └── test_utils.py        # Tests for utility functions
```

## Theoretical Complexity

- **Subset Sum (backtracking)**: O(2^n) - exponential time
- **Subset Sum (dynamic programming)**: O(n * target) - pseudo-polynomial time
- **Dijkstra's Shortest Path**: O(E + V log V) - polynomial time, approximately O(n²) in dense graphs

## Installation

### Prerequisites
- Python 3.6+
- Required Python packages: matplotlib, numpy, typing_extensions, psutil

Install required packages:
```bash
pip install -r requirements.txt
```

## Running the Project

### Main Script

```bash
# Run all benchmarks
python main.py

# Run only Subset Sum benchmarks
python main.py subset_sum

# Run only Shortest Path benchmarks
python main.py shortest_path

# Run comparison between both algorithms
python main.py compare

# Run all unit tests
python main.py test
```

### Individual Module Scripts

You can also run individual benchmark modules directly:

```bash
# Subset Sum benchmarks
python -m src.benchmarks.subset_sum_benchmark

# Shortest Path benchmarks
python -m src.benchmarks.shortest_path_benchmark

# Algorithm comparison
python -m src.benchmarks.compare_algorithms
```

### Running Tests

You can run all tests at once:

```bash
# Run all tests via main script
python main.py test

# Or directly using the test runner
python -m tests.run_all_tests
```

You can also run individual test modules:

```bash
# Run Subset Sum algorithm tests
python -m tests.test_subset_sum

# Run Shortest Path algorithm tests
python -m tests.test_shortest_path

# Run utility function tests
python -m tests.test_utils
```

## Output Files

The scripts will generate the following output files in the `results` directory:

- `subset_sum_backtracking.png`: Performance of the backtracking Subset Sum algorithm
- `subset_sum_dp.png`: Performance of the dynamic programming Subset Sum algorithm
- `subset_sum_worst_case.png`: Worst-case performance of the Subset Sum algorithm
- `shortest_path.png`: Performance of Dijkstra's shortest path algorithm
- `algorithm_comparison.png`: Comparison between both algorithms
- `algorithm_analysis_report.txt`: Detailed analysis report

## Interpreting Results

The comparison graph uses a logarithmic scale for the y-axis to better visualize the difference in growth rates between polynomial and exponential functions. 

The NP-complete algorithm's execution time grows exponentially with input size, while the polynomial-time algorithm's execution time grows at a much slower rate.

## Eksperimentinė analizė

Paleidus palyginimo skriptą, matysite algoritmų vykdymo laikus skirtingiems įvesties dydžiams. Duomenys parodo, kaip greitai NP-pilnumo klasės algoritmas tampa nepraktišku didėjant įvesties dydžiui, kai tuo tarpu polinominio laiko algoritmas išlieka efektyvus daug didesniems įvesties dydžiams.

Iš grafiko galima aiškiai matyti, kaip sparčiai auga NP-pilnumo klasės uždavinio eksponentinė laiko funkcija, lyginant su polinominio algoritmo laiko funkcija. Naudojant logaritminę skalę y ašiai, geriau matomas skirtumas tarp šių augimo greičių.

## Hardware Specifications

When documenting your results, include:
- CPU model and speed
- RAM capacity
- Operating system 

These hardware specifications are automatically included in the benchmark results and report.