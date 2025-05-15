"""
Graph Utilities Module

This module provides utility functions for graph generation and manipulation.
"""
import random
from typing import Dict, List, Tuple, TypeVar

# Type definitions
Vertex = TypeVar('Vertex', bound=int)
Weight = TypeVar('Weight', bound=float)
Graph = Dict[Vertex, List[Tuple[Vertex, Weight]]]


def generate_random_graph(n: int, edge_probability: float = 0.5, 
                         min_weight: int = 1, max_weight: int = 100) -> Graph:
    """
    Generate a random graph with n vertices and random edge weights.
    
    Args:
        n: Number of vertices
        edge_probability: Probability of an edge between any two vertices
        min_weight: Minimum weight for edges
        max_weight: Maximum weight for edges
        
    Returns:
        Dictionary representing an adjacency list of the graph
        
    This generates a directed graph with edges having weights between min_weight and max_weight.
    Each possible edge (i,j) for i≠j is included with probability 'edge_probability'.
    """
    graph = {i: [] for i in range(n)}
    
    for i in range(n):
        for j in range(n):
            if i != j and random.random() < edge_probability:
                weight = random.randint(min_weight, max_weight)
                graph[i].append((j, weight))
    
    return graph


def create_hard_subset_sum_instance(size: int) -> Tuple[List[int], int]:
    """
    Create a particularly difficult Subset Sum instance.
    Uses prime numbers and sets an impossible target to force worst-case behavior.
    
    Args:
        size: Number of elements in the set
        
    Returns:
        Tuple of (list of integers, target sum)
    """
    # Use prime numbers to make it harder to find combinations
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 
              59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 
              127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 
              191, 193, 197, 199, 211, 223]
    nums = [p for p in primes if p <= size * 5][:size]
    
    # Set target to an impossible value
    sum_of_all = sum(nums)
    target = sum_of_all + 1  # Impossible target
    
    return nums, target 